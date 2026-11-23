#!/usr/bin/env python3
"""Read-only state-v2 checks. Requires Python 3.9+. See state-protocol.md."""
import argparse
import hashlib
import json
import re
from pathlib import Path


EMPTY_FILES = "没有登记文件"


def v2_ok(state):
    """账本必须标记为版本2；判据与远端 skills-repo 的同名实现逐字一致。"""
    return (isinstance(state, dict)
            and type(state.get("schema_version")) is int
            and state["schema_version"] == 2)


class Check:
    def __init__(self, root, final=False):
        self.root = root.resolve()
        self.final = final
        self.result = {"passed": [], "failed": [], "unchecked": []}

    def add(self, level, at, message):
        self.result[level].append({"at": at, "message": message})

    def require(self, condition, at, message):
        if not condition:
            self.add("failed", at, message)
        return condition

    def obj(self, value, at):
        return value if self.require(isinstance(value, dict), at, "必须为对象") else {}

    def seq(self, value, at):
        return value if self.require(isinstance(value, list), at, "必须为数组") else []

    def text(self, value, at):
        return self.require(isinstance(value, str) and bool(value.strip()), at, "必须为非空字符串")

    def sha(self, value, at):
        return self.require(isinstance(value, str) and bool(re.fullmatch(r"[0-9a-f]{64}", value)), at, "必须为64位小写SHA256")

    def path(self, value, at):
        if not self.text(value, at):
            return None
        if not self.require("\\" not in value and not re.match(r"^[A-Za-z]:", value) and not Path(value).is_absolute(), at, "必须使用主题根目录下的相对/路径"):
            return None
        path = (self.root / value).resolve()
        return path if self.require(path.is_relative_to(self.root), at, "路径越出主题目录") else None

    def blob(self, data, at):
        data = self.obj(data, at)
        path = self.path(data.get("path"), at + ".path")
        valid = self.sha(data.get("sha256"), at + ".sha256")
        if path is None or not self.require(path.is_file(), at, "文件不存在"):
            return
        raw = path.read_bytes()
        self.require(bool(raw.strip()), at, "文件为空")
        if valid:
            self.require(hashlib.sha256(raw).hexdigest() == data["sha256"], at, "实际文件哈希与登记不符")

    def actor(self, actor, at):
        if not self.require(isinstance(actor, str) and actor in self.actors, at, "执行实体未登记"):
            return None
        self.require("identity" in self.actors[actor], at, "缺少identity字段")
        identity = self.actors[actor].get("identity")
        if identity is None:
            self.add("unchecked", at, "实体身份未知")
            return None
        return identity if self.text(identity, at + ".identity") else None

    def run(self, state):
        state = self.obj(state, "state")
        self.require(v2_ok(state), "schema_version", "需要版本2；旧版须依据历史迁移")
        for key in ("run_id", "next_action"):
            self.text(state.get(key), key)
        limit = state.get("revision_limit")
        valid_limit = self.require(type(limit) is int and limit >= 0, "revision_limit", "必须为非负整数")
        self.actors = self.obj(state.get("actors"), "actors")
        self.actors = {k: self.obj(v, "actors." + k) for k, v in self.actors.items()}
        files = self.obj(state.get("files"), "files")
        files = {k: self.obj(v, "files." + k) for k, v in files.items()}
        self.require(bool(files), "files", EMPTY_FILES)
        people, paths = {}, set()
        for fid, item in files.items():
            at = "files." + fid
            self.require(item.get("kind") in ("chapter", "guide", "source", "shared"), at, "无效文件类型")
            path = self.path(item.get("path"), at + ".path")
            if path is not None:
                self.require(path not in paths, at, "不同ID指向同一文件")
                paths.add(path)
            self.require("sha256" in item, at, "缺少sha256字段")
            current = item.get("sha256")
            if current is None:
                self.add("unchecked", at, "尚未产出或登记版本")
            else:
                self.blob(item, at)
            self.require("owner" in item, at, "缺少owner字段")
            if item.get("owner") is not None:
                self.actor(item["owner"], at + ".owner")
            elif self.final:
                self.add("unchecked", at, "未分配负责人")
            identities, outputs = set(), set()
            for n, entry in enumerate(self.seq(item.get("contributors"), at + ".contributors")):
                loc = f"{at}.contributors[{n}]"
                entry = self.obj(entry, loc)
                identity = self.actor(entry.get("actor"), loc)
                identities.add(identity)
                if self.sha(entry.get("sha256"), loc):
                    outputs.add(entry["sha256"])
            if current is not None:
                self.require(current in outputs, at, "当前版本缺少作者或修改者登记")
            people[fid] = identities
            if item.get("kind") != "chapter":
                continue
            if item.get("revisions") is None:
                self.add("unchecked", at, "修订历史缺失或未知")
                continue
            revisions = self.seq(item["revisions"], at + ".revisions")
            seen = set()
            for n, revision in enumerate(revisions):
                loc = f"{at}.revisions[{n}]"
                revision = self.obj(revision, loc)
                rid = revision.get("id")
                if self.text(rid, loc):
                    self.require(rid not in seen, loc, "同一提交重复计数")
                    seen.add(rid)
                output = revision.get("output_sha256")
                if self.sha(output, loc):
                    self.require(output in outputs, loc, "修订输出未登记贡献版本")
                record = self.path(revision.get("record"), loc + ".record")
                if record is not None:
                    self.require(record.is_file() and bool(record.read_bytes().strip()), loc, "处理记录缺失或为空")
            if valid_limit:
                self.require(len(revisions) <= limit, at, "实际修订超过当前预算，需核对授权与登记")

        review_ids, readers, passes = set(), {}, set()
        for n, review in enumerate(self.seq(state.get("reviews"), "reviews")):
            at = f"reviews[{n}]"
            review = self.obj(review, at)
            rid = review.get("id")
            valid_id = self.text(rid, at + ".id")
            if valid_id:
                self.require(rid not in review_ids, at, "重复评审ID")
                review_ids.add(rid)
            kind = review.get("kind")
            self.require(kind in ("content", "reader"), at, "无效评审类型")
            identity = self.actor(review.get("actor"), at)
            self.blob(review.get("report"), at + ".report")
            coverage = self.seq(review.get("coverage"), at + ".coverage")
            self.require(bool(coverage), at, "评审无覆盖目标")
            targets, reader_entries = set(), []
            for j, entry in enumerate(coverage):
                loc = f"{at}.coverage[{j}]"
                entry = self.obj(entry, loc)
                target = entry.get("target")
                if not self.require(isinstance(target, str) and target in files, loc, "目标未登记"):
                    continue
                self.require(target not in targets, loc, "重复覆盖目标")
                targets.add(target)
                self.text(entry.get("scope"), loc + ".scope")
                app, status = entry.get("applicability"), entry.get("status")
                self.require(app in ("current", "pending", "historical"), loc, "无效适用状态")
                allowed = ("通过", "待修订", "待核实", "未评审") if kind == "content" else ("已完成", "部分覆盖", "未完成")
                self.require(status in allowed, loc, "无效结论状态")
                issues = self.seq(entry.get("issues"), loc + ".issues")
                for issue in issues:
                    self.text(issue, loc + ".issues")
                if status == "通过":
                    self.require(not issues, loc, "通过与未决必要问题冲突")
                inputs, matches = set(), True
                for k, value in enumerate(self.seq(entry.get("inputs"), loc + ".inputs")):
                    point = f"{loc}.inputs[{k}]"
                    value = self.obj(value, point)
                    fid = value.get("file_id")
                    if not self.require(isinstance(fid, str) and fid in files, point, "输入未登记"):
                        matches = False
                        continue
                    self.require(fid not in inputs, point, "重复输入")
                    inputs.add(fid)
                    self.sha(value.get("sha256"), point)
                    matches = matches and value.get("sha256") == files[fid].get("sha256")
                    if "snapshot" in value:
                        self.blob({"path": value["snapshot"], "sha256": value.get("sha256")}, point + ".snapshot")
                        snapshot_path = self.path(value["snapshot"], point + ".snapshot.path")
                        current_path = self.path(files[fid].get("path"), point + ".current.path")
                        self.require(snapshot_path is None or snapshot_path != current_path, point, "快照不能是当前正文")
                self.require(target in inputs, loc, "输入未包含目标")
                matches = matches and target in inputs
                if app == "current":
                    self.require(matches, loc, "评审输入已变化，需确认适用性")
                    if identity is None or not people[target] or None in people[target]:
                        self.add("unchecked", loc, "无法核实实体是否重合")
                    else:
                        self.require(identity not in people[target], loc, "评审者也是目标作者或修改者")
                    if kind == "content":
                        if status == "通过" and not issues and matches:
                            passes.add(target)
                        else:
                            self.add("unchecked", loc, "当前内容尚无通过结论")
                elif app == "pending":
                    self.add("unchecked", loc, "评审适用性待确认")
                reader_entries.append((app, status, matches))
            if kind == "reader" and valid_id:
                readers[rid] = reader_entries
        reading = self.obj(state.get("reading"), "reading")
        status = reading.get("status")
        self.require(status in ("计划中", "已完成", "部分覆盖", "未完成", "跳过"), "reading", "无效试读状态")
        self.text(reading.get("reason"), "reading.reason")
        links = self.seq(reading.get("review_ids"), "reading.review_ids")
        for rid in links:
            valid = isinstance(rid, str) and rid in readers
            self.require(valid, "reading", "读者报告引用无效")
            if valid and status in ("已完成", "部分覆盖"):
                entries = readers[rid]
                self.require(bool(entries) and all(a == "current" and m and st in ("已完成", "部分覆盖") for a, st, m in entries), "reading", "报告未完成或不适用当前版本")
                if status == "已完成":
                    self.require(all(st == "已完成" for _, st, _ in entries), "reading", "部分覆盖不能证明完成")
        if status in ("已完成", "部分覆盖"):
            self.require(bool(links), "reading", "缺少支持试读结论的报告")
        if self.final:
            if not any(item.get("kind") in ("chapter", "guide") for item in files.values()):
                self.add("failed", "files",
                         "没有可交付内容：正文章节须以 chapter/guide 类型登记；kind 登记后不可变更")
            for fid, item in files.items():
                if item.get("kind") != "shared" and fid not in passes:
                    self.add("unchecked", "files." + fid, "缺少当前内容通过记录")
            if status not in ("已完成", "跳过"):
                self.add("unchecked", "reading", "试读未完成或仅部分覆盖")
        if not self.result["failed"]:
            self.add("passed", "scope", "已实现的机械约束未发现冲突；未检查项另列")


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("重复JSON键: " + key)
        result[key] = value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--final", action="store_true")
    args = parser.parse_args()
    check = Check(args.root, args.final)
    try:
        if not args.root.is_dir() or not args.state.resolve().is_relative_to(args.root.resolve()):
            raise ValueError("主题目录不存在或清单越出目录")
        state = json.loads(args.state.read_text(encoding="utf-8-sig"), object_pairs_hook=unique_keys)
        check.run(state)
    except (OSError, ValueError, TypeError, RecursionError) as exc:
        check.add("failed", "state", str(exc))
    check.result["limits"] = ("只检查机械一致性；不证明来源、范围完整性、上下文隔离、实际体验或链接锚点正确。"
                              "版本号匹配不证明已完成迁移；root 取值影响路径解析。")
    print(json.dumps(check.result, ensure_ascii=False, indent=2))
    return 1 if check.result["failed"] else 2 if check.result["unchecked"] else 0


if __name__ == "__main__":
    raise SystemExit(main())

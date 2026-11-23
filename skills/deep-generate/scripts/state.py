#!/usr/bin/env python3
"""Maintain the single task ledger. Python 3.9+, standard library only."""
import argparse
import copy
import hashlib
import json
import re
import runpy
from pathlib import Path

CHECK = runpy.run_path(str(Path(__file__).with_name('check-state.py')))
EMPTY_FILES = CHECK['EMPTY_FILES']


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'),
                      object_pairs_hook=CHECK['unique_keys'])


def need(data, key, hint):
    """取必填键。缺失时给可读中文错误，不抛裸 KeyError。"""
    if not isinstance(data, dict):
        raise ValueError(hint + '：必须是对象，当前不是')
    if key not in data:
        raise ValueError(hint + '：缺少字段 ' + str(key))
    return data.get(key)


def sha(path):
    raw = path.read_bytes()
    if not raw.strip():
        raise ValueError('文件为空: ' + str(path))
    return hashlib.sha256(raw).hexdigest()


def within(root, value):
    if not isinstance(value, str) or not value or '\\' in value or re.match(r'^[A-Za-z]:', value):
        raise ValueError('使用主题根目录内的相对/路径: ' + str(value))
    path = (root / value).resolve()
    if Path(value).is_absolute() or not path.is_relative_to(root):
        raise ValueError('路径越出主题目录: ' + value)
    return path


def write_json(path, value, exclusive=False):
    raw = json.dumps(value, ensure_ascii=False, indent=2) + '\n'
    path.parent.mkdir(parents=True, exist_ok=True)
    if exclusive:
        with path.open('x', encoding='utf-8') as stream:
            stream.write(raw)
        return
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(raw, encoding='utf-8')
    read_json(tmp)
    tmp.replace(path)


class Ledger:
    def __init__(self, root, state):
        self.root = root.resolve()
        self.path = state.resolve()
        if not self.root.is_dir() or not self.path.is_relative_to(self.root):
            raise ValueError('主题目录不存在或清单越出目录')
        self.work = self.path.parent
        self.exists = self.path.exists()
        self.data = read_json(self.path) if self.exists else None

    def files(self):
        if not isinstance(self.data, dict) or 'files' not in self.data:
            raise ValueError('状态清单缺少 files 对象')
        value = self.data['files']
        if not isinstance(value, dict):
            raise ValueError('状态清单的 files 必须是对象；当前不是')
        return value

    def actors(self):
        if not isinstance(self.data, dict) or 'actors' not in self.data:
            raise ValueError('状态清单缺少 actors 对象')
        value = self.data['actors']
        if not isinstance(value, dict):
            raise ValueError('状态清单的 actors 必须是对象；当前不是')
        return value

    def reviews(self):
        if not isinstance(self.data, dict) or 'reviews' not in self.data:
            raise ValueError('状态清单缺少 reviews 数组')
        value = self.data['reviews']
        if not isinstance(value, list):
            raise ValueError('状态清单的 reviews 必须是数组')
        return value

    def actor(self, name):
        actors = self.actors()
        if name not in actors:
            raise ValueError('执行实体未登记: ' + str(name))
        return need(actors[name], 'identity', '执行实体 ' + str(name))

    def snapshot(self, path):
        digest = sha(path)
        dest = self.work / '版本' / digest / path.name
        if dest.exists():
            if sha(dest) != digest:
                raise ValueError('已有快照损坏: ' + str(dest))
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            with dest.open('xb') as stream:
                stream.write(path.read_bytes())
            if sha(dest) != digest:
                raise ValueError('复制期间输入变化，请重试')
        return {'sha256': digest, 'snapshot': dest.relative_to(self.root).as_posix()}

    def invalidate(self):
        reader_changed = False
        files = self.files()
        for review in self.reviews():
            for entry in need(review, 'coverage', '评审记录'):
                if need(entry, 'applicability', '评审覆盖') != 'current':
                    continue
                for value in need(entry, 'inputs', '评审覆盖'):
                    fid = need(value, 'file_id', '评审输入')
                    recorded = need(value, 'sha256', '评审输入')
                    if fid not in files:
                        raise ValueError('评审输入引用了未登记的条目: ' + str(fid))
                    if recorded != need(files[fid], 'sha256', '文件条目 ' + str(fid)):
                        entry['applicability'] = 'pending'
                        reader_changed |= review.get('kind') == 'reader'
                        break
        if reader_changed:
            self.data['reading'] = {'status': '未完成',
                                    'reason': '试读输入已变化，需复查后登记新报告', 'review_ids': []}

    def register(self, args):
        spec = vars(args)
        actor_id = need(spec, 'actor', 'register')
        file_id = need(spec, 'id', 'register')
        path_value = need(spec, 'path', 'register')
        kind = need(spec, 'kind', 'register')
        self.actor(actor_id)
        files = self.files()
        previous = files.get(file_id)
        path = within(self.root, path_value)
        for other_id, item in files.items():
            other_path = need(item, 'path', '文件条目 ' + str(other_id))
            if other_id != file_id and within(self.root, other_path) == path:
                raise ValueError('文件已由另一个ID登记')
        if previous and need(previous, 'kind', '文件条目 ' + file_id) != kind:
            raise ValueError('文件类型不能改变')
        frozen = self.snapshot(path)
        item = copy.deepcopy(previous) if previous else {
            'contributors': [], 'revisions': [], 'kind': kind}
        revision, record = spec.get('revision'), spec.get('record')
        if bool(revision) != bool(record):
            raise ValueError('--revision 与 --record 必须一起提供')
        if revision:
            if not previous or previous.get('sha256') == frozen['sha256']:
                raise ValueError('没有新的问题修订产出，不计轮次')
            if kind != 'chapter' or item.get('revisions') is None:
                raise ValueError('只能为修订历史已知的章节登记问题修订')
            need(spec, 'record', 'register')
            sha(within(self.root, record))
            existing = next((r for r in item['revisions'] if r.get('id') == revision), None)
            if existing is None:
                if len(item['revisions']) >= need(self.data, 'revision_limit', '状态清单'):
                    raise ValueError('问题修订预算已耗尽')
                existing = {'id': revision}
                item['revisions'].append(existing)
            existing.update(output_sha256=frozen['sha256'], record=record)
        item.update(path=path_value, sha256=frozen['sha256'], owner=actor_id)
        contribution = {'actor': actor_id, 'sha256': frozen['sha256']}
        if contribution not in item['contributors']:
            item['contributors'].append(contribution)
        files[file_id] = item
        self.invalidate()

    def freeze(self, args):
        if not args.files or len(set(args.files)) != len(args.files):
            raise ValueError('冻结文件ID不能为空或重复')
        files = self.files()
        inputs = []
        for fid in args.files:
            if fid not in files:
                raise ValueError('冻结的文件ID未登记: ' + str(fid))
            item = files[fid]
            frozen = self.snapshot(within(self.root, need(item, 'path', '文件条目 ' + str(fid))))
            if frozen['sha256'] != need(item, 'sha256', '文件条目 ' + str(fid)):
                raise ValueError('正文尚未登记最新产出: ' + fid)
            inputs.append(dict(file_id=fid, **frozen))
        # This is a frozen evidence bundle, not another editable ledger.
        output = within(self.root, args.output)
        if output == self.path:
            raise ValueError('冻结输入不能覆盖状态清单')
        write_json(output, {'inputs': inputs}, exclusive=True)
        return {'inputs_file': args.output, 'inputs': inputs}

    def review(self, args):
        spec = read_json(within(self.root, args.spec))
        actor_id = need(spec, 'actor', '评审提交')
        kind = need(spec, 'kind', '评审提交')
        review_id = need(spec, 'id', '评审提交')
        inputs_path = need(spec, 'inputs', '评审提交')
        report_path = need(spec, 'report', '评审提交')
        coverage_spec = need(spec, 'coverage', '评审提交')
        self.actor(actor_id)
        if kind not in ('content', 'reader'):
            raise ValueError('无效评审类型')
        if any(r.get('id') == review_id for r in self.reviews()):
            raise ValueError('评审ID已存在，复评使用新ID')
        bundle_path = within(self.root, inputs_path)
        if not bundle_path.is_file():
            raise ValueError('冻结凭据不存在（请先用 freeze 生成）: ' + inputs_path)
        bundle = read_json(bundle_path)
        inputs = need(bundle, 'inputs', '冻结凭据')
        if not isinstance(inputs, list) or not inputs:
            raise ValueError('冻结输入为空')
        if len({need(i, 'file_id', '冻结输入') for i in inputs}) != len(inputs):
            raise ValueError('冻结输入重复')
        files = self.files()
        for value in inputs:
            fid = need(value, 'file_id', '冻结输入')
            recorded = need(value, 'sha256', '冻结输入')
            snapshot_path = need(value, 'snapshot', '冻结输入（请用 freeze 生成凭据）')
            if fid not in files:
                raise ValueError('冻结输入引用了未登记的条目: ' + str(fid))
            item = files[fid]
            if recorded != sha(within(self.root, snapshot_path)):
                raise ValueError('冻结输入损坏')
            if within(self.root, snapshot_path) == within(self.root, need(item, 'path', '文件条目 ' + str(fid))):
                raise ValueError('快照不能是当前正文')
            if sha(within(self.root, need(item, 'path', '文件条目 ' + str(fid)))) != need(item, 'sha256', '文件条目 ' + str(fid)):
                raise ValueError('正文有未登记的修改')
        matches = all(need(i, 'sha256', '冻结输入') == need(files[need(i, 'file_id', '冻结输入')], 'sha256', '文件条目')
                      for i in inputs)
        reviewer_identity = self.actor(actor_id)
        coverage = []
        if not isinstance(coverage_spec, list):
            raise ValueError('评审覆盖必须是数组')
        for entry in coverage_spec:
            target = need(entry, 'target', '评审覆盖')
            if target not in files:
                raise ValueError('评审目标未登记: ' + str(target))
            authors = set()
            for contributor in need(files[target], 'contributors', '文件条目 ' + str(target)):
                authors.add(self.actor(need(contributor, 'actor', '贡献者')))
            if reviewer_identity is None:
                raise ValueError('评审者身份不可核实: ' + str(actor_id))
            if None in authors:
                raise ValueError('目标作者身份不可核实，需先修复 actors: ' + str(target))
            if reviewer_identity in authors:
                raise ValueError('评审者也是目标作者或修改者')
            coverage.append(dict(entry, inputs=copy.deepcopy(inputs),
                                 applicability='current' if matches else 'pending'))
        path = within(self.root, report_path)
        review = {'id': review_id, 'kind': kind, 'actor': actor_id}
        review.update(report={'path': report_path, 'sha256': sha(path)}, coverage=coverage)
        self.reviews().append(review)
        # A completed replacement report supersedes only the targets it checks.
        if matches:
            targets = {e['target'] for e in coverage}
            for old in self.reviews()[:-1]:
                if old.get('kind') == kind:
                    for entry in need(old, 'coverage', '评审记录'):
                        if entry.get('target') in targets:
                            entry['applicability'] = 'historical'

    def apply(self, args):
        if args.command == 'init':
            if self.exists:
                raise ValueError('状态清单已存在')
            self.data = {'schema_version': 2,
                         'run_id': args.run_id, 'next_action': args.next_action,
                         'revision_limit': args.revision_limit, 'actors': {}, 'files': {},
                         'reviews': [], 'reading': {'status': '计划中',
                                                  'reason': args.reason, 'review_ids': []}}
        else:
            if not self.exists:
                raise ValueError('先初始化状态清单')
            if not isinstance(self.data, dict):
                raise ValueError('状态清单必须是 JSON 对象；当前不是')
            if not CHECK['v2_ok'](self.data):
                raise ValueError('需要版本2；旧版须依据历史迁移')
            if args.command == 'actor':
                actors = self.actors()
                previous = actors.get(args.id)
                identity = {'identity': args.identity}
                if previous and previous != identity:
                    raise ValueError('实体身份不能改写；另用新的ID登记')
                actors[args.id] = identity
            elif args.command == 'register':
                self.register(args)
            elif args.command == 'register-batch':
                entries = read_json(within(self.root, args.spec))
                if not isinstance(entries, list) or not entries:
                    raise ValueError('批量凭据必须是非空数组')
                for entry in entries:
                    if not isinstance(entry, dict):
                        raise ValueError('批量凭据的每一项必须是对象')
                    self.register(argparse.Namespace(**dict({'revision': None, 'record': None}, **entry)))
            elif args.command == 'freeze':
                return self.freeze(args)
            elif args.command == 'review':
                self.review(args)
            elif args.command == 'reading':
                self.data['reading'] = {'status': args.status, 'reason': args.reason,
                                        'review_ids': args.reviews}
            elif args.command == 'next':
                self.data['next_action'] = args.text
        check = CHECK['Check'](self.root)
        check.run(self.data)
        # init 期的空 files 是合法起始状态：必须是 dict、为空、且失败项恰为「没有登记文件」。
        current_files = self.data.get('files') if isinstance(self.data, dict) else None
        failures = [e for e in check.result['failed']
                    if not (isinstance(current_files, dict) and not current_files
                            and e['message'] == EMPTY_FILES)]
        if failures:
            raise ValueError('机械检查未通过：\n  ' + '\n  '.join(
                '%s :: %s' % (e.get('at'), e.get('message')) for e in failures))
        if self.path.exists():
            write_json(self.path.with_suffix('.previous.json'), read_json(self.path))
        write_json(self.path, self.data)
        return {'state': str(self.path), 'command': args.command, 'saved': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--state', type=Path, required=True)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('init')
    p.add_argument('--run-id', required=True)
    p.add_argument('--next-action', default='建立知识图谱与结构')
    p.add_argument('--reason', default='连续学习，待安排主路线试读')
    p.add_argument('--revision-limit', type=int, default=2)
    p = sub.add_parser('actor')
    p.add_argument('--id', required=True)
    p.add_argument('--identity', required=True)
    p = sub.add_parser('register')
    p.add_argument('--id', required=True)
    p.add_argument('--path', required=True)
    p.add_argument('--kind', choices=['chapter', 'guide', 'source', 'shared'], required=True)
    p.add_argument('--actor', required=True)
    p.add_argument('--revision')
    p.add_argument('--record')
    p = sub.add_parser('register-batch')
    p.add_argument('--spec', required=True)
    p = sub.add_parser('freeze')
    p.add_argument('--files', nargs='+', required=True)
    p.add_argument('--output', required=True)
    p = sub.add_parser('review')
    p.add_argument('--spec', required=True)
    p = sub.add_parser('reading')
    p.add_argument('--status', choices=['计划中', '已完成', '部分覆盖', '未完成', '跳过'], required=True)
    p.add_argument('--reason', required=True)
    p.add_argument('--reviews', nargs='*', default=[])
    p = sub.add_parser('next')
    p.add_argument('--text', required=True)
    args = parser.parse_args()
    try:
        result = Ledger(args.root, args.state).apply(args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, TypeError, KeyError, AttributeError, RecursionError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())

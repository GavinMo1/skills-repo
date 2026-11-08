# skills

Agent skill 集合。每个 skill 是 `skills/` 下的一个目录，目录里必须有 `SKILL.md`（frontmatter 含 `name` 与 `description`），可选 `references/`、`agents/` 等附属文件。

## 安装

需要 Node.js ≥ 18，无需全局安装任何东西。

**现在可用**（直接从本仓库跑，不依赖 npm 发布）：

```bash
npx github:GavinMo1/skills-repo add plan-review-loop
```

**发布到 npm 之后**（包尚未发布，先别用）：

```bash
npx @GavinMo1/skills add plan-review-loop
```

装完即写到 `~/.agents/skills/plan-review-loop/`，agent 下次启动就能读到。

### 常用命令

```bash
npx github:GavinMo1/skills-repo list                             # 列出可用 skill
npx github:GavinMo1/skills-repo add --all                        # 全部安装
npx github:GavinMo1/skills-repo add plan-review-loop --project   # 装到当前项目 ./.agents/skills
npx github:GavinMo1/skills-repo add plan-review-loop --force     # 覆盖，旧版本移入 .trash/
npx github:GavinMo1/skills-repo add plan-review-loop --link      # junction 指向本地克隆，改完立即生效
```

### 装到哪里

| 目标 | 命令 | 结果 |
|---|---|---|
| 用户级（默认） | `add <name>` | `~/.agents/skills/<name>/` |
| 当前项目 | `add <name> --project` | `./.agents/skills/<name>/` |
| 任意目录 | `add <name> --dir <path>` | `<path>/<name>/` |

若你的 agent 从别的目录读 skill（例如 `~/.claude/skills`），用 `--dir` 指过去即可：

```bash
npx github:GavinMo1/skills-repo add plan-review-loop --dir ~/.claude/skills
```

### 安全说明

- **不会删除任何东西**：目标已存在时默认拒绝安装；加 `--force` 才覆盖，且旧版本先移到目标目录下的 `.trash/<name>-<时间戳>/`。
- 默认整目录复制。`--link` 用 junction/符号链接指向你的本地克隆，适合边改边用，不适合长期保留。

## 现有 skill

| skill | 用途 |
|---|---|
| plan-review-loop | 制定或修订要交给用户执行的方案时，用独立评审、修订、复评闭环，产出可直接开工的方案 |

## 添加新 skill

1. 新建 `skills/<name>/`，放入 `SKILL.md`；附属文件一并放进去（安装器整目录复制）。
2. 在上面那张表里加一行。
3. 提交并打版本：`npm version minor` → `git push --follow-tags`。

一个 skill 的所有文件都必须留在自己的目录里，不要跨 skill 引用文件——安装是逐目录复制的，跨目录引用装上就断。

## 开发

```bash
node bin/cli.mjs list
node bin/cli.mjs add plan-review-loop --dir /tmp/skills-test
```

## 许可

MIT

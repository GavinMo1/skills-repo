# skills

Agent skill 集合。每个 skill 是 `skills/` 下的一个目录，目录里必须有 `SKILL.md`（frontmatter 含 `name` 与 `description`），可选 `references/`、`agents/` 等附属文件。

## 安装

不发布到 npm 也能用，直接跑仓库：

```bash
npx github:GavinMo1/skills-repo add plan-review-loop
```

发布到 npm 后：

```bash
npx @GavinMo1/skills add plan-review-loop
```

常用命令：

```bash
npx @GavinMo1/skills list                              # 列出可用 skill
npx @GavinMo1/skills add --all                         # 全部安装
npx @GavinMo1/skills add plan-review-loop --project    # 装到 ./.agents/skills
npx @GavinMo1/skills add plan-review-loop --force      # 覆盖（旧版本移入 .trash/）
npx @GavinMo1/skills add plan-review-loop --link       # 用 junction 指向仓库，改了立即生效
```

默认安装到 `~/.agents/skills/`；用 `--dir <path>` 指定其他位置。

安装器不删除任何东西：覆盖时把旧版本移到目标目录下的 `.trash/<name>-<时间戳>/`。

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


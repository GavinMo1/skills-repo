# skills

Agent skill 集合。每个 skill 是 `skills/` 下的一个目录，目录里必须有 `SKILL.md`（frontmatter 含 `name` 与 `description`），可选 `references/`、`agents/` 等附属文件。

## 安装

需要 Node.js ≥ 18，无需全局安装任何东西。装完写到 `~/.agents/skills/`，agent 下次启动即可读到。

### 方式一：npm（推荐）

```bash
npx @gavinmo1/skills add plan-review-loop
```

包地址：[npmjs.com/package/@gavinmo1/skills](https://www.npmjs.com/package/@gavinmo1/skills)。走 registry，不受 npm 的 `allow-git` 限制影响。

### 方式二：直接从 GitHub 跑

```bash
npx github:GavinMo1/skills-repo add plan-review-loop
```

若报 `EALLOWGIT`（npm 11+ 默认 `allow-git=none`，拒绝从 git 取包），加一个开关：

```bash
npx --yes --allow-git=all github:GavinMo1/skills-repo add plan-review-loop
```

### 方式三：克隆后本地跑（任何 npm 配置下都可用）

```bash
git clone https://github.com/GavinMo1/skills-repo
node skills-repo/bin/cli.mjs add plan-review-loop
```

### 常用命令

```bash
npx @gavinmo1/skills list                             # 列出可用 skill
npx @gavinmo1/skills add --all                        # 全部安装
npx @gavinmo1/skills add plan-review-loop --project   # 装到当前项目 ./.agents/skills
npx @gavinmo1/skills add plan-review-loop --force     # 覆盖，旧版本移入 .trash/
npx @gavinmo1/skills add plan-review-loop --link      # junction 指向本地克隆，改完立即生效
```

### 装到哪里

| 目标 | 命令 | 结果 |
|---|---|---|
| 用户级（默认） | `add <name>` | `~/.agents/skills/<name>/` |
| 当前项目 | `add <name> --project` | `./.agents/skills/<name>/` |
| 任意目录 | `add <name> --dir <path>` | `<path>/<name>/`（支持 `~`） |

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

## 发布（维护者）

```bash
npm version patch          # 或 minor
git push --follow-tags
npm publish
```

npm 现行策略要求发布必须受 2FA 保护。踩过的三个坑，记在这里：

1. **包名必须全小写。** npm 用户名是 `gavinmo1`，scope 只能是 `@gavinmo1/`；写成 `@GavinMo1/` 会被 registry 拒绝。
2. **非交互环境必须用带 bypass 2FA 权限的 Granular Access Token，且要显式传配置。** `NODE_AUTH_TOKEN` 环境变量 npm **不会自动采用**（它只在 `.npmrc` 里写了 `//registry.npmjs.org/:_authToken=${NODE_AUTH_TOKEN}` 时才生效），所以这样发仍然会 403：

   ```bash
   npm publish --registry=https://registry.npmjs.org "--//registry.npmjs.org/:_authToken=$NPM_TOKEN"
   ```

3. **首次发布后包会短暂 404。** registry 传播需要几分钟；`npm publish` 输出 `+ @scope/name@x.y.z` 就表示已被接受，不用重发。

## 许可

MIT


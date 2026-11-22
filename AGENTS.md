# AGENTS.md

本仓库是 agent skill 的**唯一真源**。`C:\Users\27017\.agents\skills` 下的 4 个 skill 目录是本仓库 `skills/` 的 junction，改这里就等于改那边。

## 结构

```
package.json          @gavinmo1/skills，bin 指向 bin/cli.mjs
bin/cli.mjs           安装器：list / add / where
skills/<name>/        每个 skill 一个目录，必须有 SKILL.md
README.md             对外文档（会同步到 npm 页面）
AGENTS.md             本文件，维护者约定
```

`skills/<name>/` 里可以有 `references/`、`scripts/`、`agents/` 等附属文件，安装器整目录复制，不做筛选。

## 加一个 skill

1. 源目录放进 `skills/<name>/`，`SKILL.md` 的 frontmatter 至少要有 `name` 和 `description`。
2. **`description` 只写「这个 skill 干什么、什么时候用、不适用于什么」，不要写「这类需求请走 X skill」。** 路由是描述匹配阶段的事，把其他 skill 的名字塞进 description 会让路由在两处打架，而且被点名的 skill 一旦删掉就留下悬空引用。
3. 正文里引用其他 skill 只允许是执行期依赖（真的要到那一步去读它），并且要写清「读不到时怎么办」。
4. README 的 skill 表加一行。
5. 提交 → 提版本 → 发布（见下）。

新增或删除 skill 属于**次版本号**（`0.2.0` → `0.3.0`）；只改 skill 内容属于**补丁号**（`0.2.2` → `0.2.3`）。

## 发布

```powershell
# 1. 改 package.json 的 version，或 npm version patch/minor
# 2. 本地自检
node bin/cli.mjs list

# 3. 提交并推
git add -A
git -c core.autocrlf=false commit -m "feat: ..." -m "正文说明"
git tag -a v0.3.0 -m "v0.3.0"
git push origin main --follow-tags

# 4. 发布（必须显式指定 registry 与 token）
npm publish --registry=https://registry.npmjs.org "--//registry.npmjs.org/:_authToken=$tok"
```

**三个必须记住的坑：**

1. **本机 npm 默认 registry 是 `registry.npmmirror.com`**，发布和查版本都必须显式带 `--registry=https://registry.npmjs.org`，否则只会动镜像。
2. **`NODE_AUTH_TOKEN` 环境变量 npm 不会自动采用。** 它只在 `.npmrc` 里写了 `//registry.npmjs.org/:_authToken=${NODE_AUTH_TOKEN}` 时才生效。直接 `$env:NODE_AUTH_TOKEN=...; npm publish` 会静默回落到旧的登录会话并报 `E403 Two-factor authentication ... required`——这个报错具有误导性，真实原因往往是没传进去。
3. **包名和 scope 必须全小写。** npm 用户名是 `gavinmo1`，scope 只能是 `@gavinmo1/`。

发布后 registry 传播需要 1～2 分钟，期间 `npm view` 仍返回旧版本、`npx` 会报 `ETARGET`。等一分钟再试，不要重发。

## 发布后验证

```powershell
$tmp = Join-Path $env:TEMP ('skills-test-' + [guid]::NewGuid().ToString('N').Substring(0,8))
New-Item -ItemType Directory -Path $tmp | Out-Null
npx --yes --registry=https://registry.npmjs.org @gavinmo1/skills@latest add --all --dir $tmp
Get-ChildItem -LiteralPath $tmp -Recurse -File
```

测试目录用完按回收站删除，不要留：

```powershell
Add-Type -AssemblyName Microsoft.VisualBasic
[Microsoft.VisualBasic.FileIO.FileSystem]::DeleteDirectory($tmp,'OnlyErrorDialogs','SendToRecycleBin')
```

## 硬规矩

- **不要提交** `.trash/`、`node_modules/`、测试生成的临时目录。
- **`.gitattributes` 是 `* text=auto eol=lf`。** Windows 上的 CRLF 文件提交后按 LF 存，git 会提示 `CRLF will be replaced by LF`——这是预期行为，不是错误。提交时用 `git -c core.autocrlf=false commit` 避免把纯换行变化混进功能提交。
- **不要 `push --force`**，不要改写已推送的历史。
- **README 只在发布时同步到 npm 页面。** 改了 README 想让 npm 页面跟着变，必须再提一个补丁版本并发布。
- 每个 skill 的文件必须留在自己目录里，不要跨 skill 引用文件——安装是逐目录复制的，跨目录引用装上就断。

## 相关

- 本机安装目录的组织方式、junction 断裂修复：`C:\Users\27017\.agents\skills\README.md`
- 安装目录里的 agent 行为约束：`C:\Users\27017\.agents\skills\AGENTS.md`

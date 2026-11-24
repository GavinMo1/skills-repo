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
2. **`description` 只写「这个 skill 干什么、什么时候用」，既不写「不适用于什么」，也不写「这类需求请走 X skill」。** 边界用产出形态表达：产出是什么形状、多大、从什么起点开始，写清楚就够了，不该选它的人自然不会选。负向清单读起来像穷举、实际只是抽样，而且点名的对象一旦变化，它就从"没用"变成"错误信息"——这正是不能把别的 skill 名字塞进 description 的同一个理由。**正文同理**：排除清单不产生动作，要拦人时写成可执行的中止条件（「若 X，停下并说明」），不要写成分类意见。
3. 正文里引用其他 skill 只允许是执行期依赖（真的要到那一步去读它），并且要写清「读不到时怎么办」。
4. README 的 skill 表加一行。
5. 提交 → 提版本 → push（见下）。**到此为止，不发 npm。**

新增或删除 skill 属于**次版本号**（`0.2.0` → `0.3.0`）；只改 skill 内容属于**补丁号**（`0.2.2` → `0.2.3`）。

## 发布

**默认只推 git，不发 npm。** 提交、提版本、打 tag、push 是每次改动的常规收尾；`npm publish` **只在维护者明确说「发到 npm」时才执行**——「写得差不多了」「该发的都发了」这类自我判断不构成授权，也不要顺手带上。

没发布的版本照样打 tag 推到远端，之后补发用的就是那个 tag，不必因为当时没发而重新提一版。所以「仓库里 version 比 npm 上高」是正常状态，不是漏发。

日常（每次改动都做）：

```powershell
# 1. 改 package.json 的 version，或 npm version patch/minor
# 2. 本地自检
node bin/cli.mjs list

# 3. 提交并推
git add -A
git -c core.autocrlf=false commit -m "feat: ..." -m "正文说明"
git tag -a v0.3.0 -m "v0.3.0"
git push origin main --follow-tags
```

维护者要求发布时，在已推的 tag 上补这一步：

```powershell
# 4. 发布（必须显式指定 registry 与 token）
npm publish --registry=https://registry.npmjs.org "--//registry.npmjs.org/:_authToken=$tok"
```

**四个必须记住的坑：**

1. **本机 npm 默认 registry 是 `registry.npmmirror.com`**，发布和查版本都必须显式带 `--registry=https://registry.npmjs.org`，否则只会动镜像。
2. **`NODE_AUTH_TOKEN` 环境变量 npm 不会自动采用。** 它只在 `.npmrc` 里写了 `//registry.npmjs.org/:_authToken=${NODE_AUTH_TOKEN}` 时才生效。直接 `$env:NODE_AUTH_TOKEN=...; npm publish` 会静默回落到旧的登录会话并报 `E403 Two-factor authentication ... required`——这个报错具有误导性，真实原因往往是没传进去。
3. **包名和 scope 必须全小写。** npm 用户名是 `gavinmo1`，scope 只能是 `@gavinmo1/`。
4. **账户是 `auth-and-writes` 时，`--otp` 与网页登录的会话 token 都发不出去。** 用 `npm login --auth-type=web` 登录后 `npm whoami` 正常，但 `npm publish` 仍报 `E403 ... Two-factor authentication or granular access token with bypass 2fa enabled is required`；补 `--otp=<6位>` 也是同一句 403（不是 `EOTP`）。可用的只有建一个 **Granular Access Token 并勾选 Bypass 2FA**，再显式传进去。`npm token list` 只能看到 token 前缀，旧值取不回来，只能新建。

发布后 registry 传播需要 1～2 分钟，期间 `npm view` 仍返回旧版本、`npx` 会报 `ETARGET`。等一分钟再试，不要重发。

**发布现在是异步的**：`npm publish` 的 PUT 返回 `202` 并提示 `Your package is being processed`，命令立刻以 `+ @scope/name@x.y.z` 成功退出，但 registry 上要等几十秒才出现。这段时间里重复 publish 会撞 `E409 Conflict - Cannot publish over previously staged version`——那不是失败，是它还在处理。改用固定版本探测确认：

```powershell
(Invoke-RestMethod 'https://registry.npmjs.org/@gavinmo1%2fskills').'dist-tags'.latest
```

## 只发一部分 skill

`package.json` 的 `files` 是白名单，**逐条列出要进包的 skill 目录**，不要写整个 `skills`——写成 `skills` 就等于把仓库里所有 skill（包括还在打磨的）一起发出去。加了新 skill 想发，才往里加一行；不想发就别加。

```json
"files": [
  "bin",
  "skills/ai-explore-inline",
  "skills/deep-generate",
  "skills/plan-review-loop",
  "skills/plan-review-loop-en",
  "skills/reader-review",
  "README.md",
  "LICENSE"
]
```

发了之后 `npx ... add <name>` 只能装包里有的那些；仓库里没进包的，要用 GitHub 方式装。README 的 skill 表因此要写明哪几个在 npm 上。

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
- **README 只在发布时同步到 npm 页面。** npm 页面的 README 落后于仓库是默认状态，不算没做完；要让它跟上，得等维护者要求发布的那一次。
- 每个 skill 的文件必须留在自己目录里，不要跨 skill 引用文件——安装是逐目录复制的，跨目录引用装上就断。

## 相关

- 本机安装目录的组织方式、junction 断裂修复：`C:\Users\27017\.agents\skills\README.md`
- 安装目录里的 agent 行为约束：`C:\Users\27017\.agents\skills\AGENTS.md`

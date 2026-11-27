# TODO

待办事项。一条一行，做完就删，别让这里变成历史记录。

## 发 npm 前必须处理

- [ ] **`package.json` 的 `files` 与 `skills/` 实际内容不一致，缺 5 个 skill。**
      2026-11-28 核（版本 0.8.2）。

      `files` 是**发布范围**声明，不是仓库内容清单——往里面加 skill 等于改对外发布契约，
      所以这件事不该在无关任务里顺手做掉，要单独决定。
      **本文件只记缺口，不改 `files`；`files` 的最终取舍在发版那天由维护者定。**

      现状：`files` 声明 5 个，`skills/` 实际 10 个。

      | 缺的 skill | 缺的原因类别 |
      |---|---|
      | `ai-explore-inline-plus` | **A 类**：`files` 数组建立时就未纳入 |
      | `neat-freak` | **A 类**：同上 |
      | `topic-resonance` | **A 类**：同上 |
      | `skill-audit` | **B 类**：数组建立后入库，入库只提了版本号，没加 `files` |
      | `ui-detail` | **B 类**：同上 |

      两类的来历（照 `git log` 可复核）：

      - **A 类**：这三个 skill 在 `452fc6d`（0.6.2，提交信息「npm 只发已定型的 5 个 skill」）
        之前就已入库。`452fc6d` 建立了现在的 `files` 数组，只列了当时算「已定型」的 5 个，
        这三个从一开始就没进去。所以不是谁后来漏掉，是**立项时就没算它们**。
      - **B 类**：`1f9df98`（0.7.0，skill-audit）、`9a5b842`（0.8.0，ui-detail）——
        这两个提交都只改了 `package.json` 的 `version`，没碰 `files`。
        **今后再收 skill 进仓库，要么同一次就把 `files` 一并定掉，要么在这里补一行。**

      两处都有的 5 个：`ai-explore-inline`、`deep-generate`、`plan-review-loop`、
      `plan-review-loop-en`、`reader-review`。
      `README.md` 列全了 10 个，与实际目录一致——**不一致的只有 `files`**。

      发 npm 之前一次性核对全部 skill，不要零敲碎打；并顺带确认 A 类那三个
      是「本就打算不发」还是「忘了加」——只有维护者能答。

- [ ] **经验：收 skill 进仓库 ≠ DSH 能加载。**
      `~/.agents/skills` 下要单独建 junction 指向仓内目录
      （`New-Item -ItemType Junction -Path <安装点> -Target <仓内路径>`），
      **建完立即生效，不用重启**。

      为什么值得单独记：2026-11-26 一晚咬到两次——`skill-audit`（0.7.0 提交正文写着
      「原位改成 junction」，实际没建）、`plan-review-loop-en`（从未建过，因此**完全不可见**：
      中文版有 `disable-model-invocation: true` 所以藏得住，英文版没那行、又没挂载点，
      就从 catalog 里彻底消失）。两者的 `.trash` 里都没有痕迹，说明不是被删，是当初就漏建。
      不写下来，第三次还会漏。

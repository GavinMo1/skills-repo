# TODO

待办事项。一条一行，做完就删，别让这里变成历史记录。

## 发 npm 前必须处理

- [ ] **`package.json` 的 `files` 与 `skills/` 实际内容不一致，缺 3 个 skill。**
      2026-11-25 记（版本 0.6.7）。

      `files` 是**发布范围**声明，不是仓库内容清单——往里面加 skill 等于改对外发布契约，
      所以这件事不该在无关任务里顺手做掉，要单独决定。

      现状对比：

      | | skill |
      |---|---|
      | `skills/` 里有，`files` 里没有 | `ai-explore-inline-plus`、`neat-freak`、`topic-resonance` |
      | 两处都有 | `ai-explore-inline`、`deep-generate`、`plan-review-loop`、`plan-review-loop-en`、`reader-review` |

      `README.md` 列全了 8 个，与实际目录一致——**不一致的只有 `files`**。

      发 npm 之前一次性核对全部 skill，不要零敲碎打；并顺带确认这三个漏掉的
      是「本就打算不发」还是「忘了加」。

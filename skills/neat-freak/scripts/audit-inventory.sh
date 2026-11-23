#!/usr/bin/env bash
# Read-only inventory for neat-freak. Prints metadata and paths only; never reads file contents.
#
# Output is CANDIDATES ONLY: a listed path is not a file to read, and its presence proves nothing
# (not that a rule is loaded, not that a file can be deleted).
#
# No-Bash equivalent — each section has a manual counterpart, all read-only, none may be skipped:
#   platform-directories      列出存在的 agent home 目录（.claude/.codex/.agents...）
#   home-root-checks          确认 HOME 取值；Windows 风格路径时存在性结果不可靠
#   other-agent-rule-artifacts 项目根下 .cursorrules/.windsurfrules/.cursor/rules 等是否存在
#   git                       rev-parse --show-toplevel / branch / HEAD / status 条数 / worktree 数
#   rule-chain-candidates     从项目根逐级向上到 / 的每一层：AGENTS.override.md、AGENTS.md、
#                             CLAUDE.md、CLAUDE.local.md、.claude/CLAUDE.md
#                             （存在性 + 是否软链 + 行数/字节）；再查 HOME 级
#                             $HOME/.codex/AGENTS.override.md、$HOME/.codex/AGENTS.md、$HOME/.claude/CLAUDE.md
#   project-markdown[-count]  项目内 .md/.mdx 计数（不逐一枚举，避免被当成待读清单）
#   skill-install-candidates  各 skills 目录的一级子目录名，用于查同名安装
#   root-entries              项目根一级条目

set -euo pipefail

usage() {
  echo "usage: $0 <project-root>" >&2
  exit 64
}

[[ $# -eq 1 ]] || usage
[[ -d "$1" ]] || { echo "[ERR] project root is not a directory: $1" >&2; exit 66; }

PROJECT_ROOT="$(cd "$1" && pwd -P)"
SEEN_RULE_FILES=$'\n'

section() {
  printf '\n## %s\n' "$1"
}

file_size() {
  local file="$1"
  local lines bytes
  lines="$(wc -l < "$file" | tr -d ' ')"
  bytes="$(wc -c < "$file" | tr -d ' ')"
  printf '%s\tlines=%s\tbytes=%s\n' "$file" "$lines" "$bytes"
}

describe_rule_file() {
  local file="$1"
  case "$SEEN_RULE_FILES" in
    *$'\n'"$file"$'\n'*) return ;;
  esac
  SEEN_RULE_FILES+="$file"$'\n'
  if [[ -L "$file" ]]; then
    local target state
    target="$(readlink "$file")"
    if [[ -e "$file" ]]; then state="valid"; else state="broken"; fi
    printf '%s\tsymlink=%s\tstate=%s\n' "$file" "$target" "$state"
  elif [[ -f "$file" ]]; then
    file_size "$file"
  fi
}

printf '# neat-freak inventory v3 (candidates only, not a reading list)\n'
printf 'project_root=%s\n' "$PROJECT_ROOT"
printf 'generated_at=%s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')"

section "home-root-checks"
# HOME may be unset or Windows-style; fall back so later sections do not silently check nothing.
: "${HOME:=${USERPROFILE:-}}"
printf 'home=%s\n' "${HOME:-<unset>}"
case "${HOME:-}" in
  "") printf 'home_state=unset  # home-derived sections are empty, inspect manually\n' ;;
  *\\*) printf 'home_state=windows-style-path  # existence results may be unreliable\n' ;;
  *) printf 'home_state=posix\n' ;;
esac

section "platform-directories"
# Common agent home dirs; nonexistent ones are skipped silently.
for dir in "$HOME/.agents" "$HOME/.claude" "$HOME/.codex" "$HOME/.cursor" "$HOME/.gemini" \
  "$HOME/.qoder" "$HOME/.trae" "$HOME/.iflow" "$HOME/.codebuddy"; do
  if [[ -d "$dir" ]]; then printf '%s\n' "$dir"; fi
done
true

section "other-agent-rule-artifacts"
# Platform-specific rule forms at the project root (existence only).
for rel in .cursorrules .windsurfrules .cursor/rules .qoder .trae .iflow; do
  if [[ -e "$PROJECT_ROOT/$rel" ]]; then printf '%s\n' "$PROJECT_ROOT/$rel"; fi
done
true

section "git"
if git -C "$PROJECT_ROOT" rev-parse --show-toplevel >/dev/null 2>&1; then
  GIT_ROOT="$(git -C "$PROJECT_ROOT" rev-parse --show-toplevel)"
  printf 'git_root=%s\n' "$GIT_ROOT"
  printf 'branch=%s\n' "$(git -C "$PROJECT_ROOT" branch --show-current 2>/dev/null || true)"
  printf 'head=%s\n' "$(git -C "$PROJECT_ROOT" rev-parse HEAD)"
  printf 'status_entries=%s\n' "$(git -C "$PROJECT_ROOT" status --porcelain=v1 | wc -l | tr -d ' ')"
  printf 'worktrees=%s\n' "$(git -C "$PROJECT_ROOT" worktree list --porcelain | awk '$1 == "worktree" {n++} END {print n+0}')"
else
  printf 'git_root=none\n'
fi

section "rule-chain-candidates"
cursor="$PROJECT_ROOT"
while :; do
  for rel in AGENTS.override.md AGENTS.md CLAUDE.md CLAUDE.local.md .claude/CLAUDE.md; do
    describe_rule_file "$cursor/$rel"
  done
  [[ "$cursor" == "/" ]] && break
  parent="$(dirname "$cursor")"
  [[ "$parent" == "$cursor" ]] && break
  cursor="$parent"
done
for file in \
  "$HOME/.codex/AGENTS.override.md" \
  "$HOME/.codex/AGENTS.md" \
  "$HOME/.claude/CLAUDE.md"; do
  describe_rule_file "$file"
done
true

section "project-markdown"
# Candidates only: do not treat this list as files to read.
# `|| printf` keeps later sections alive: under set -o pipefail an unreadable subdir makes find exit non-zero.
{
  find "$PROJECT_ROOT" \
    \( -name .git -o -name node_modules -o -name .next -o -name dist -o -name build -o -name .venv -o -name venv -o -name __pycache__ -o -name target -o -name vendor -o -name .turbo -o -name .cache \) -prune \
    -o -type f \( -name '*.md' -o -name '*.mdx' \) -print \
    | LC_ALL=C sort
} || printf '[WARN] some paths unreadable; candidate list is incomplete\n'

section "project-markdown-count"
{
  find "$PROJECT_ROOT" \
    \( -name .git -o -name node_modules -o -name .next -o -name dist -o -name build -o -name .venv -o -name venv -o -name __pycache__ -o -name target -o -name vendor -o -name .turbo -o -name .cache \) -prune \
    -o -type f \( -name '*.md' -o -name '*.mdx' \) -print \
    | awk 'END {print NR+0}'
} || printf 'count_incomplete\n'

section "skill-install-candidates"
# First-level skill directory names only, used for comparing same-name installs. Names prove nothing about loading.
# Use `if` blocks (not `[[ ]] || continue`): a false test in the last loop iteration would abort the script under set -e.
for dir in "$HOME/.agents/skills" "$HOME/.claude/skills" \
  "$PROJECT_ROOT/.agents/skills" "$PROJECT_ROOT/.claude/skills"; do
  if [[ -d "$dir" ]]; then
    printf '%s\n' "$dir"
    for entry in "$dir"/*/; do
      if [[ -d "$entry" ]]; then
        if [[ -f "$entry/SKILL.md" || -f "$entry/skill.md" ]]; then
          printf '  %s\n' "$(basename "$entry")"
        else
          printf '  %s\t(no SKILL.md)\n' "$(basename "$entry")"
        fi
      fi
    done
  fi
done
true

section "root-entries"
{ find "$PROJECT_ROOT" -mindepth 1 -maxdepth 1 -print | LC_ALL=C sort; } \
  || printf '[WARN] root listing incomplete\n'

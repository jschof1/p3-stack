#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE="${HOME}"
CONFIG_DIR=".agents"
REPLACE=0
CHECK=0

while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --project)
      if [[ "$#" -lt 2 || -z "$2" || "$2" == --* ]]; then
        printf '%s\n' '--project requires a repository path' >&2
        exit 2
      fi
      BASE="$2"
      shift 2
      ;;
    --codex) CONFIG_DIR=".codex"; shift ;;
    --claude) CONFIG_DIR=".claude"; shift ;;
    --replace) REPLACE=1; shift ;;
    --check) CHECK=1; shift ;;
    --help|-h)
      printf '%s\n' 'usage: ./install.sh [--project /path/to/repo] [--codex|--claude] [--replace] [--check]'
      exit 0
      ;;
    *) printf 'unknown argument: %s\n' "$1" >&2; exit 2 ;;
  esac
done

TARGET="$BASE/$CONFIG_DIR/skills"
BACKUP="$BASE/$CONFIG_DIR/skill-backups/p3-stack-$(date -u +%Y%m%dT%H%M%SZ)-$$"
if [[ "$CHECK" -eq 0 ]]; then
  mkdir -p "$TARGET"
fi
installed=0
skipped=0
unchanged=0
failed=0

for skill in "$ROOT"/skills/*/; do
  skill="${skill%/}"
  [[ -f "$skill/SKILL.md" ]] || continue
  name="$(basename "$skill")"
  destination="$TARGET/$name"
  if [[ -L "$destination" && "$destination" -ef "$skill" ]]; then
    unchanged=$((unchanged + 1))
    continue
  fi
  if [[ "$CHECK" -eq 1 ]]; then
    printf 'missing or conflicting link: %s\n' "$destination" >&2
    failed=$((failed + 1))
    continue
  fi
  if [[ -e "$destination" || -L "$destination" ]]; then
    if [[ "$REPLACE" -eq 0 ]]; then
      printf 'skip %s (already exists; use --replace to back it up)\n' "$name"
      skipped=$((skipped + 1))
      continue
    fi
    mkdir -p "$BACKUP"
    mv "$destination" "$BACKUP/$name"
  fi
  ln -s "$skill" "$destination"
  installed=$((installed + 1))
done

if [[ "$CHECK" -eq 1 ]]; then
  printf 'checked %d links in %s (%d missing or conflicting)\n' "$unchanged" "$TARGET" "$failed"
  [[ "$failed" -eq 0 ]]
  exit
fi
printf 'linked %d skills into %s (%d unchanged, %d skipped)\n' "$installed" "$TARGET" "$unchanged" "$skipped"
if [[ -d "$BACKUP" ]]; then
  printf 'previous skills saved in %s\n' "$BACKUP"
fi

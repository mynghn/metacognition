#!/usr/bin/env bash
# metacognition-freshness — read-only freshness + validity of the Metacognition
# framework: the tooling repo + the private vault repo (vs their remotes), and
# whether installed Claude+Codex adapters cover every configured sibling.
set -uo pipefail

TOOL="@FAMILY_REPO@"
VAULT="@VAULT@"

# The vault is private + mynghn-owned; the active gh account may not be able to
# reach it, so read-only fetches use a mynghn credential when available.
MTOK="$(gh auth token --user mynghn 2>/dev/null || true)"
mynghn_git() {
  local repo="$1"
  shift
  if [ -n "$MTOK" ]; then
    MYNGHN_TOKEN="$MTOK" git -C "$repo" -c credential.helper= \
      -c credential.helper='!f(){ echo username=mynghn; echo "password=$MYNGHN_TOKEN"; };f' "$@"
  else
    git -C "$repo" "$@"
  fi
}

sync_state() {
  local repo="$1" br up d
  [ -n "$(git -C "$repo" status --porcelain 2>/dev/null)" ] && d=dirty || d=clean
  br="$(git -C "$repo" symbolic-ref --short HEAD 2>/dev/null || echo HEAD)"
  mynghn_git "$repo" fetch -q origin 2>/dev/null || true
  up="origin/$br"
  git -C "$repo" rev-parse --verify -q "$up" >/dev/null 2>&1 || up="origin/HEAD"
  printf '%s behind=%s ahead=%s' "$d" \
    "$(git -C "$repo" rev-list --count "HEAD..$up" 2>/dev/null || echo '?')" \
    "$(git -C "$repo" rev-list --count "$up..HEAD" 2>/dev/null || echo '?')"
}

flag() {
  case "$1" in
    *behind=0*) printf '  ok ' ;;
    *behind=\?*) printf ' n/a ' ;;
    *) printf ' ** ' ;;
  esac
}

skill_file() {
  local dir="$1" name="$2"
  [ -f "$dir/$name/SKILL.md" ]
}

is_git_repo() {
  git -C "$1" rev-parse --is-inside-work-tree >/dev/null 2>&1
}

echo "== metacognition-freshness ============================================="
for pair in "tooling:$TOOL" "vault:$VAULT"; do
  nm="${pair%%:*}"
  repo="${pair#*:}"
  if is_git_repo "$repo"; then
    state="$(sync_state "$repo")"
    printf '[%-7s]%s %s  (%s)\n' "$nm" "$(flag "$state")" "$state" "$repo"
  else
    printf '[%-7s]  n/a  not a git checkout at %s\n' "$nm" "$repo"
  fi
done

# Adapter parity: every config/<stem> should have installed Claude + Codex adapters.
if [ -d "$TOOL/config" ]; then
  missing=0
  for cfg in "$TOOL"/config/*; do
    [ -f "$cfg" ] || continue
    stem="${cfg##*/}"
    case "$stem" in
      *.md|README) continue ;;
    esac
    name="$stem-knowledge-base"
    skill_file "$HOME/.claude/skills" "$name" || {
      echo "[adapters] ** Claude adapter missing for $stem (run install)"
      missing=1
    }
    skill_file "$HOME/.agents/skills" "$name" || {
      echo "[adapters] ** Codex adapter missing under ~/.agents for $stem (run install)"
      missing=1
    }
  done
  [ "$missing" = 0 ] && echo "[adapters]  ok  every configured sibling has Claude + Codex adapters"
fi

echo "========================================================================"
echo "Fix (after review, only if flagged **):"
echo "  git -C $TOOL pull --ff-only \\"
echo "    && git -C $VAULT pull --ff-only \\"
echo "    && $TOOL/install --vault $VAULT"
echo "  (vault is private + mynghn-owned: fetch/pull/push may need the mynghn gh-credential override — see SKILL.md)"

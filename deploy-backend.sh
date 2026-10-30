#!/bin/bash
# Deploy Backend/ to the Heroku app gptbro-backend, then send a test chat.
#
# Creates a short-lived Heroku token, pushes with it and revokes it again, so no
# credentials are stored and Git Credential Manager never pops up. Needs the Heroku
# CLI logged in to the account that owns the app (heroku login).
#
# Only what's committed on HEAD is deployed. Heroku's main branch is its own
# "Deploy" history, not a subtree of this repo: each deploy is a commit on top of
# it holding Backend/ minus node_modules and package*.json (a package.json would
# make Heroku build the app as Node).

set -euo pipefail

APP=gptbro-backend
GIT_URL=https://git.heroku.com/$APP.git
API_URL=https://gptbro-backend-910febe125f5.herokuapp.com
FRONTEND_ORIGIN=https://gpt.usmanghani.dev

cd "$(dirname "$0")"

if [ -n "$(git status --porcelain -- Backend)" ]; then
    echo "❌ Backend/ has uncommitted changes. Commit them first; only HEAD is deployed."
    exit 1
fi

PYTHON=$(command -v python || command -v python3)
json_field() { PYTHONIOENCODING=utf-8 "$PYTHON" -c "import json, sys; d = json.load(sys.stdin); print($1)"; }

INDEX_FILE=$(mktemp)
AUTH_ID=""
revoke_token() {
    if [ -n "$AUTH_ID" ]; then
        if heroku authorizations:revoke "$AUTH_ID" >/dev/null 2>&1; then
            echo "🔒 Token revoked"
        else
            echo "⚠️  Couldn't revoke the token. Run: heroku authorizations:revoke $AUTH_ID"
        fi
        AUTH_ID=""
    fi
}
cleanup() { revoke_token; rm -f "$INDEX_FILE"; }
trap cleanup EXIT

echo "🔑 Creating a short-lived Heroku token..."
AUTH_JSON=$(heroku authorizations:create --json -d "gptbro deploy $(date +%F)" -e 900)
AUTH_ID=$(echo "$AUTH_JSON" | json_field "d['id']")
HEROKU_DEPLOY_TOKEN=$(echo "$AUTH_JSON" | json_field "d['access_token']['token']")
export HEROKU_DEPLOY_TOKEN
unset AUTH_JSON

# git with the token as its only credential helper
heroku_git() {
    GCM_INTERACTIVE=never GIT_TERMINAL_PROMPT=0 git -c credential.helper= \
        -c 'credential.helper=!f() { test "$1" = get && echo username=heroku && echo "password=$HEROKU_DEPLOY_TOKEN"; }; f' \
        "$@"
}

heroku_git fetch -q "$GIT_URL" main
DEPLOYED=$(git rev-parse FETCH_HEAD)

rm -f "$INDEX_FILE"
git ls-tree -r HEAD:Backend | grep -vE $'\t(node_modules/|package(-lock)?\\.json$)' \
    | GIT_INDEX_FILE="$INDEX_FILE" git update-index --index-info
TREE=$(GIT_INDEX_FILE="$INDEX_FILE" git write-tree)

if [ "$TREE" = "$(git rev-parse "$DEPLOYED^{tree}")" ]; then
    echo "✅ Heroku already runs $(git rev-parse --short HEAD), nothing to push"
else
    COMMIT=$(git commit-tree "$TREE" -p "$DEPLOYED" -m "Deploy $(git rev-parse --short HEAD): $(git log -1 --format=%s)")
    echo "🚀 Deploying $(git rev-parse --short HEAD) to $APP..."
    heroku_git push "$GIT_URL" "$COMMIT:refs/heads/main"
fi

revoke_token

echo "🧪 Sending a test chat..."
for attempt in 1 2 3; do
    RESPONSE=$(curl -s -m 40 -w '\n%{http_code}' -X POST "$API_URL/api/chat" \
        -H "Origin: $FRONTEND_ORIGIN" -H "Content-Type: application/json" \
        -d '{"messages":[{"sender":"user","text":"In one short sentence, who is Usman Ghani?"}]}' || true)
    STATUS=$(echo "$RESPONSE" | tail -n 1)
    BODY=$(echo "$RESPONSE" | sed '$d')
    if [ "$STATUS" = "200" ]; then
        echo "✅ Bot replied: $(echo "$BODY" | json_field "d['reply'][:200]")"
        exit 0
    fi
    echo "   attempt $attempt: HTTP $STATUS"
    sleep 5
done

echo "❌ The bot didn't answer. Check: heroku logs -a $APP -n 100"
exit 1

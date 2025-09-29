#!/bin/bash
PROJECT_PATH=$1
COMMIT_MSG=$2

if [ -z "$PROJECT_PATH" ] || [ -z "$COMMIT_MSG" ]; then
    echo "❌ Usage: $0 <project-path> <commit-message>"
    exit 1
fi

case $PROJECT_PATH in
    *iss*) PREFIX="🎨 [ISS]" ;;
    *soliso*) PREFIX="⚙️ [SOLISO]" ;;
    *studiocentos*) PREFIX="📱 [STUDIOCENTOS]" ;;
    *postgress*|*postgres*) PREFIX="🗄️ [POSTGRES]" ;;
    *traefik*) PREFIX="🔀 [TRAEFIK]" ;;
    *docs*) PREFIX="📚 [DOCS]" ;;
    *scripts*) PREFIX="🛠️ [SCRIPTS]" ;;
    *) PREFIX="📦 [MISC]" ;;
esac

git add "$PROJECT_PATH/"
git commit -m "$PREFIX $COMMIT_MSG

📁 Path: $PROJECT_PATH/
🕐 $(date +'%Y-%m-%d %H:%M:%S')"

echo "✅ Committed: $PREFIX $COMMIT_MSG"

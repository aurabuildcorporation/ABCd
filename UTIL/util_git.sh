#!/bin/bash

# =====================================================
# UTIL_GIT_PRO v2.0.1 - Interactive Git Automation Tool
# =====================================================
# user/pass cred store
# git config --global credential.helper "cache --timeout=86400"
#
# -----------------------------
# CONFIG
# -----------------------------
GIT_BRANCH=$(git branch --show-current 2>/dev/null)

# -----------------------------
# SAFETY CHECK: INSIDE GIT REPO
# -----------------------------
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "ERROR: Not inside a git repository"
    exit 1
fi

# -----------------------------
# CLEAN CHECK FUNCTION
# -----------------------------
is_clean() {
    [ -z "$(git status --porcelain)" ]
}

# -----------------------------
# HEADER
# -----------------------------
echo "======================================"
echo "       UTIL_GIT_PRO v2"
echo "   Branch: $GIT_BRANCH"
echo "======================================"

# -----------------------------
# STATUS
# -----------------------------
while true; do
    read -p "Show git status? (y/n): " answer
    case "$answer" in
        [yY]*)
            git status
            break
            ;;
        [nN]*)
            break
            ;;
        *)
            echo "Please answer y or n."
            ;;
    esac
done

# -----------------------------
# LOG
# -----------------------------
while true; do
    read -p "Show git log? (y/n): " answer
    case "$answer" in
        [yY]*)
            git log --oneline --graph --decorate -10
            break
            ;;
        [nN]*)
            break
            ;;
        *)
            echo "Please answer y or n."
            ;;
    esac
done

# -----------------------------
# ADD
# -----------------------------
while true; do
    read -p "git add . ? (y/n): " answer
    case "$answer" in
        [yY]*)
            git add .
            echo "Staged changes."
            break
            ;;
        [nN]*)
            break
            ;;
        *)
            echo "Please answer y or n."
            ;;
    esac
done

# -----------------------------
# COMMIT
# -----------------------------
while true; do
    read -p "Commit changes? (y/n): " answer
    case "$answer" in
        [yY]*)
            read -p "Enter commit message (leave blank for timestamp): " msg

            if [ -z "$msg" ]; then
                msg="$(date +%s)"
            fi

            git commit -m "$msg"
            break
            ;;
        [nN]*)
            break
            ;;
        *)
            echo "Please answer y or n."
            ;;
    esac
done

# -----------------------------
# PUSH
# -----------------------------
while true; do
    read -p "Push to GitHub? (y/n): " answer
    case "$answer" in
        [yY]*)
            if [ -z "$GIT_BRANCH" ]; then
                echo "No branch detected."
            else
                git push -u origin "$GIT_BRANCH"
            fi
            break
            ;;
        [nN]*)
            echo "Skipping push"
            break
            ;;
        *)
            echo "Please answer y or n."
            ;;
    esac
done

# -----------------------------
# PULL / REBASE SAFETY
# -----------------------------
while true; do
    read -p "Pull latest from origin? (y/n): " answer
    case "$answer" in
        [yY]*)
            git pull --rebase
            break
            ;;
        [nN]*)
            break
            ;;
        *)
            echo "Please answer y or n."
            ;;
    esac
done

# -----------------------------
# SAFE REBASE (ONLY IF CLEAN)
# -----------------------------
if ! is_clean; then
    echo "Working tree NOT clean. Rebase blocked."
    git status --short
else
    while true; do
        read -p "Run git rebase? (y/n): " answer
        case "$answer" in
            [yY]*)
                git rebase
                break
                ;;
            [nN]*)
                echo "Skipping rebase"
                break
                ;;
            *)
                echo "Please answer y or n."
                ;;
        esac
    done
fi

# -----------------------------
# CLEAN SUMMARY
# -----------------------------
echo "--------------------------------------"
echo "Git sequence complete"
echo "Branch: $GIT_BRANCH"
echo "Clean: $(is_clean && echo YES || echo NO)"
echo "--------------------------------------"

#!/bin/bash

# -----------------------------
# SAFETY CHECK FUNCTION
# -----------------------------
is_clean() {
    [ -z "$(git status --porcelain)" ]
}

# -----------------------------
# GIT STATUS
# -----------------------------
while true; do
    read -p "git status? (y/n): " answer
    case "$answer" in
        [yY]* ) git status; break ;;
        [nN]* ) break ;;
        * ) echo "Please answer y or n." ;;
    esac
done

# -----------------------------
# GIT LOG
# -----------------------------
while true; do
    read -p "git log? (y/n): " answer
    case "$answer" in
        [yY]* ) git log --oneline --graph --decorate; break ;;
        [nN]* ) break ;;
        * ) echo "Please answer y or n." ;;
    esac
done

# -----------------------------
# GIT ADD
# -----------------------------
while true; do
    read -p "git add . ? (y/n): " answer
    case "$answer" in
        [yY]* ) git add .; break ;;
        [nN]* ) break ;;
        * ) echo "Please answer y or n." ;;
    esac
done

# -----------------------------
# GIT COMMIT
# -----------------------------
while true; do
    read -p "Commit Changes? (y/n): " answer
    case "$answer" in
        [yY]* ) git commit -m "$(date +%s)"; break ;;
        [nN]* ) break ;;
        * ) echo "Please answer y or n." ;;
    esac
done

# -----------------------------
# FINAL LOG
# -----------------------------
while true; do
    read -p "git log? (y/n): " answer
    case "$answer" in
        [yY]* ) git log --oneline --graph --decorate; break ;;
        [nN]* ) break ;;
        * ) echo "Please answer y or n." ;;
    esac
done

# -----------------------------
# SAFE REBASE (ONLY IF CLEAN)
# -----------------------------
if ! is_clean; then
    echo "Working tree is NOT clean."
    echo "Rebase blocked for safety."
    git status --short
else
    while true; do
        read -p "git rebase? (y/n): " answer
        case "$answer" in
            [yY]* ) git rebase; break ;;
            [nN]* ) echo "Skipping rebase"; break ;;
            * ) echo "Please answer y or n." ;;
        esac
    done
fi

echo "git sequence complete"

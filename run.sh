#!/bin/bash

# Если первый аргумент ($1) не задан или пуст, используем "refactoring"
COMMIT_MESSAGE="${1:-Refactoring}"

git add .
git commit -m "$COMMIT_MESSAGE"
git push origin main
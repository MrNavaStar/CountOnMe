#!/bin/bash
start_cmd="python3 bot/main.py updated"
repo_branch="origin/main"

echo "Updating..."
git fetch --all
git reset --hard $repo_branch

echo "Launching..."
$start_cmd
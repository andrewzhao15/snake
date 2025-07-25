---
description: Workflow to Commit Changes
---

1. Look at the uncommitted changes:
```bash
git status
git diff
```

2. Check current branch and create new branch if on main:
```bash
# Check current branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" = "main" ]; then
    echo "On main branch, creating new feature branch..."
    read -p "Enter branch name: " BRANCH_NAME
    git checkout -b "$BRANCH_NAME"
else
    echo "Already on branch: $CURRENT_BRANCH"
fi
```

3. Group and stage changes based on logical groupings:
```bash
# Review files to stage
git status
# Stage files interactively or by groups
# Example: git add file1.js file2.js  # Related feature files
# Example: git add test/  # Test files
# Example: git add docs/  # Documentation files
```

4. Commit the staged changes with a detailed commit message:
```bash
# Commit with descriptive message
git commit -m "feat: descriptive commit message

- Detail about what was changed
- Why the change was made
- Any important notes for reviewers"
```

5. Ensure all staged changes are committed:
```bash
# Verify commit was successful
git log -1 --oneline
git status
```

6. Ask user whether they want to open a PR

7. If user confirms, then call /generate-pr workflow:

Important notes:
- Review your changes carefully before staging
- Use conventional commit format (feat:, fix:, docs:, etc.)
- Group related changes together in logical commits
- Provide clear, descriptive commit messages
- The workflow will pause for user input when needed
# Git Workflow Guide: Portfolio Maintenance & Privacy

This guide documents the essential Git operations used to maintain a clean, professional, and private engineering portfolio. Use these commands to manage large-scale cleanups and ensure sensitive files never reach your public history.

## 1. Standard Daily Workflow
For regular updates and adding new features:
```bash
git add .
git commit -m "Brief description of changes"
git push origin main
```

---

## 2. Fixing .gitignore (The "Reset Button")
If you accidentally commit files that should have been ignored (like `node_modules` or `.DS_Store`), simply updating `.gitignore` isn't enough because Git is already "tracking" them. Use this sequence to force Git to re-evaluate everything:

```bash
# 1. Untrack everything from the index (does NOT delete files from your Mac)
git rm -r --cached .

# 2. Re-add everything (Git will now respect the updated .gitignore)
git add .

# 3. Commit and push the cleanup
git commit -m "Cleanup: Re-applying .gitignore rules"
git push origin main
```

---

## 3. The "History Scrub" (Option 1: Complete Privacy)
If you need to permanently erase sensitive files or thousands of "junk" files from your GitHub history (including old commits), use the **Orphan Branch** method. This collapses your entire history into a single "Clean Start" commit.

**Warning:** This will replace your entire GitHub history with one commit. Your local files remain safe.

```bash
# 1. Create a temporary 'orphan' branch (no history)
git checkout --orphan latest_branch

# 2. Add all current files
git add -A

# 3. Create the 'Clean Start' commit
git commit -m "Initial clean commit: Portfolio structure"

# 4. Delete the old local 'main' branch
git branch -D main

# 5. Rename the current branch to 'main'
git branch -m main

# 6. Force-push to GitHub to overwrite the history
git push -f origin main
```

---

## 4. Keeping Specific Files Local-Only
To keep a file on your Mac but ensure it **never** goes to GitHub:
1. Add the filename to `.gitignore`.
2. Run `git rm --cached <filename>` to stop Git from tracking it if it was previously committed.
3. Commit the change.

### Specific Exclusions in this Portfolio:
- `performance-report.md`: Private assessment.
- `InterviewPrepPlan.txt`: Internal strategy.
- `node_modules/`: Heavy external dependencies.

---
*Maintained by Gemini CLI Orchestrator - April 2026*

---
description: Reject and discard a pending delta specification.
scripts:
  sh: .specify/scripts/bash/compare-specs.sh --json
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Language Detection

**CRITICAL**: Detect language from spec.md and use it for rejection messages.

**Detection Steps**:
1. Read spec.md to detect language
2. Use detected language for:
   - Rejection confirmation messages
   - Archive notifications

**Consistency Rule**: Messages match spec.md language.

## Goal

Reject the pending delta specification and clean up associated files, without modifying the main spec.

This is a destructive operation for the delta only - the main `.specify/specs/spec.md` remains unchanged.

## Execution Steps

### 1. Initialize Rejection Context

Run `.specify/scripts/bash/compare-specs.sh --json` from repo root and parse JSON for HAS_EXISTING_SPEC, SPEC_PATH, DELTA_DIR, and CURRENT_BRANCH. All paths must be absolute.

**Prerequisites Check**:
- If DELTA_DIR does not exist: ERROR "No delta found for branch {branch}. Nothing to reject."
- If DELTA_DIR/delta-spec.md does not exist: ERROR "Delta specification not found."

For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

### 2. Confirmation Prompt

Before deleting, show summary and ask for confirmation:

```markdown
## ⚠️ Reject Delta Confirmation

You are about to **reject and delete** the pending delta specification.

**Branch**: {CURRENT_BRANCH}  
**Delta Location**: {DELTA_DIR}

**This delta contains**:
- {N} additions
- {M} modifications
- {K} deletions

**Files to be deleted**:
- delta-spec.md
- changes-summary.md (if exists)
- review-checklist.md (if exists)

**This action**:
- ✅ WILL delete all delta files
- ✅ WILL NOT modify .specify/specs/spec.md (main spec remains unchanged)
- ❌ CANNOT be undone (unless delta is in version control)

**Proceed with rejection?** (yes/no)
```

**Response handling**:
- If user says "yes" or "confirm" or "proceed": Continue to step 3
- If user says "no" or "cancel" or "abort": ABORT with message "Rejection cancelled by user"
- If user provides `--force` or `-f` flag in $ARGUMENTS: Skip this prompt

### 3. Optional: Archive Before Deletion

Ask user if they want to archive the delta before deleting (unless `--no-archive` flag provided):

```markdown
## Archive Option

Before deleting, would you like to archive this delta for future reference?

**Archive location**: specs/.deltas-archive/{timestamp}_{branch}/

This allows you to review what was rejected later if needed.

**Archive before deleting?** (yes/no/skip)
```

**If user chooses "yes"**:
1. Create archive directory: `mkdir -p specs/.deltas-archive/`
2. Generate archive name with timestamp: `{YYYYMMDD_HHMMSS}_{branch}_REJECTED`
3. Move delta: `mv .specify/.deltas/{branch} specs/.deltas-archive/{timestamp}_{branch}_REJECTED/`
4. Add rejection note to archive:
   ```bash
   echo "REJECTED on {timestamp} by user" > specs/.deltas-archive/{timestamp}_{branch}_REJECTED/REJECTED.txt
   echo "Reason: {user-provided reason if any}" >> specs/.deltas-archive/{timestamp}_{branch}_REJECTED/REJECTED.txt
   ```

**If user chooses "no" or "skip"**:
- Proceed to deletion (step 4)

### 4. Delete Delta Directory

Remove the delta directory completely:

```bash
rm -rf {DELTA_DIR}
```

**Validation**:
- Verify directory no longer exists
- If deletion failed: ERROR "Failed to delete delta directory: {error details}"

### 5. Record Rejection

Create/append to rejection log for audit purposes:

**File**: `.specify/specs/.delta-rejections.log`

**Format**:
```
---
Date: {YYYY-MM-DD HH:MM:SS}
Branch: {CURRENT_BRANCH}
Action: REJECTED
Archived: {YES/NO}
Archive Location: {path if archived}
Reason: {user-provided reason if any}
Rejected By: {user name or AI Agent}
---

```

### 6. Clean Up Branch (Optional)

If user wants to clean up the git branch as well:

Ask: "Delete the git branch '{CURRENT_BRANCH}' as well? (yes/no)"

**If yes and git is available**:
1. Check if on the feature branch: `git rev-parse --abbrev-ref HEAD`
2. If on feature branch: `git checkout main` (or default branch)
3. Delete branch: `git branch -D {CURRENT_BRANCH}`
4. Report: "Branch {CURRENT_BRANCH} deleted"

**If no or git not available**:
- Skip branch deletion
- Note: "Branch {CURRENT_BRANCH} remains. Delete manually if needed."

### 7. Report Completion

Provide comprehensive completion report:

```markdown
# ❌ Delta Rejected

**Branch**: {CURRENT_BRANCH}  
**Date**: {timestamp}  
**Action**: REJECTED

## What Happened

✅ Delta specification has been rejected and removed  
✅ Main spec (.specify/specs/spec.md) remains unchanged  
{✅ Delta archived to: specs/.deltas-archive/{timestamp}_{branch}_REJECTED/ (if archived)}  
{✅ Git branch deleted (if requested)}

## Files Deleted

- `.specify/.specify/.deltas/{branch}/delta-spec.md`
- `.specify/.specify/.deltas/{branch}/changes-summary.md`
- `.specify/.specify/.deltas/{branch}/review-checklist.md`

## Rejection Reason

{User-provided reason if any, otherwise "No reason provided"}

## What's Next

You can:

1. **Start fresh**: Run `/speckit.specify` with refined requirements
2. **Review rejection**: {If archived: Check `.specify/specs/.deltas-archive/{timestamp}_{branch}_REJECTED/`}
3. **Continue without changes**: Proceed with existing spec

## Notes

- The rejection has been logged in `.specify/specs/.delta-rejections.log`
- Main specification remains in its original state
- {If not archived: This rejection cannot be recovered}

```

## Operating Constraints

### Safety Measures

1. **Confirmation required**: Always ask before deleting (unless --force)
2. **Archive option**: Offer to archive before deletion for audit trail
3. **Read-only for main spec**: Never modify .specify/specs/spec.md during rejection
4. **Log all rejections**: Maintain audit log of what was rejected and why

### Command Flags

Optional flags that can be passed in $ARGUMENTS:

- `--force` or `-f`: Skip confirmation prompts
- `--no-archive`: Don't offer to archive, just delete
- `--keep-branch`: Don't offer to delete git branch
- `--reason "text"`: Provide rejection reason inline
- `--archive-only`: Archive but don't delete (for review)

### Rejection Reasons

Prompt user for rejection reason if not provided via `--reason` flag:

"Why is this delta being rejected? (optional but recommended)"

Common reasons:
- Incorrect requirements
- Better approach found
- Conflicts with other changes
- Out of scope
- No longer needed
- Technical constraints
- Failed review

## Error Handling

**If delta directory doesn't exist**:
- Check if it was already merged: Look for entry in .specify/specs/CHANGELOG.md
- Check if it was already archived: Look in specs/.deltas-archive/
- Report status and suggest next steps

**If deletion fails**:
- Report specific error (permissions, file in use, etc.)
- Suggest manual deletion command
- Do not mark as completed

**If on wrong branch**:
- Warn user about branch mismatch
- Ask if they want to reject anyway
- Provide branch context

## Context

$ARGUMENTS


---
description: Approve and merge a delta specification into the main spec.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Goal

Merge the approved delta specification changes into `.specify/specs/spec.md`, creating a backup and maintaining change history.

This command is WRITE-ENABLED and will modify `.specify/specs/spec.md` - proceed with caution.

## Execution Steps

### 1. Initialize Merge Context

Run `.specify/scripts/bash/compare-specs.sh --json` from repo root and parse JSON for HAS_EXISTING_SPEC, SPEC_PATH, DELTA_DIR, and CURRENT_BRANCH. All paths must be absolute.

**Prerequisites Check**:
- If HAS_EXISTING_SPEC is false: ERROR "No existing spec found. Cannot merge delta without .specify/specs/spec.md."
- If DELTA_DIR does not exist: ERROR "No delta found for branch {branch}. Run /speckit.specify first."
- If DELTA_DIR/delta-spec.md does not exist: ERROR "Delta specification not found."

Derive paths:
- REPO_ROOT = parent of specs/
- SPEC_PATH = .specify/specs/spec.md
- DELTA_SPEC = DELTA_DIR/delta-spec.md
- BACKUP_DIR = .specify/specs/.backups/

For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

### 2. Pre-Merge Validation

Before proceeding, perform safety checks:

**A. Load and parse delta**:
- Read DELTA_SPEC
- Extract all additions, modifications, and deletions
- Verify delta is in valid format

**B. Final review prompt** (if not bypassed by user):
- Show change summary statistics
- Ask: "You are about to merge {N} additions, {M} modifications, and {K} deletions into .specify/specs/spec.md. This will modify the main specification. Continue? (yes/no)"
- If user says "no" or anything other than "yes": ABORT with message "Merge cancelled by user"
- If user provides `--force` or `-f` flag: Skip prompt

**C. Constitution check**:
- Load `.specify/memory/constitution.md`
- Verify delta doesn't violate core principles
- If violations found: ERROR "Delta violates constitution: {details}. Run /speckit.review-delta to identify issues."

### 3. Create Backup

**CRITICAL**: Always create backup before modifying .specify/specs/spec.md

1. Create backup directory if not exists: `mkdir -p {REPO_ROOT}/.specify/specs/.backups/`
2. Generate backup filename: `spec_backup_{YYYYMMDD_HHMMSS}_{BRANCH}.md`
3. Copy current .specify/specs/spec.md to backup:
   ```bash
   cp .specify/specs/spec.md .specify/specs/.backups/spec_backup_{timestamp}_{branch}.md
   ```
4. Log backup location for user reference

### 4. Execute Merge

Run the merge script:

```bash
.specify/scripts/bash/merge-delta-spec.sh --json \
  --spec-path "{SPEC_PATH}" \
  --delta-path "{DELTA_SPEC}" \
  --branch "{CURRENT_BRANCH}"
```

The script will:
- Parse delta-spec.md for additions, modifications, deletions
- Apply changes to .specify/specs/spec.md in correct order
- Preserve existing structure and formatting
- Add change markers if configured
- Return JSON with merge results

Parse JSON output for:
- SUCCESS (true/false)
- ADDITIONS_APPLIED (count)
- MODIFICATIONS_APPLIED (count)
- DELETIONS_APPLIED (count)
- ERRORS (array of error messages if any)

**Error Handling**:
- If SUCCESS is false: 
  - Restore from backup: `cp .specify/specs/.backups/spec_backup_{timestamp}_{branch}.md .specify/specs/spec.md`
  - Report errors to user
  - ABORT with message "Merge failed: {error details}. Spec restored from backup."

### 5. Record Change History

After successful merge, document the change:

1. Create/append to `.specify/specs/CHANGELOG.md`:

```markdown
## {Feature Name} - {CURRENT_BRANCH}

**Date**: {YYYY-MM-DD HH:MM:SS}  
**Branch**: {CURRENT_BRANCH}  
**Applied By**: AI Agent / {User Name}

**Changes**:
- ✅ Added: {count} items
- 🔄 Modified: {count} items
- ❌ Removed: {count} items

**Summary**:
{2-3 sentence summary from delta changes-summary.md}

**Delta Location**: `.specify/.specify/.deltas/{branch}/` (archived)  
**Backup**: `.specify/specs/.backups/spec_backup_{timestamp}_{branch}.md`

---

```

2. If git is available and user allows:
   - Optionally stage changes: `git add .specify/specs/spec.md .specify/specs/CHANGELOG.md`
   - Suggest commit message: `"feat: apply delta from {branch} - {summary}"`
   - Ask user if they want to commit now or manually

### 6. Archive Delta

After successful merge, archive or clean up delta:

**Option A: Archive** (recommended for audit trail):
1. Create archive directory: `mkdir -p {REPO_ROOT}/specs/.deltas-archive/`
2. Move delta directory: `mv .specify/.deltas/{branch} specs/.deltas-archive/{timestamp}_{branch}/`
3. Add archive note to CHANGELOG.md

**Option B: Delete** (if user prefers):
1. Remove delta directory: `rm -rf .specify/.deltas/{branch}/`
2. Log deletion in CHANGELOG.md

Default to Option A unless user specifies `--delete-delta` flag.

### 7. Post-Merge Validation

Verify the merged spec:

**A. Sanity checks**:
- .specify/specs/spec.md exists and is not empty
- File size is reasonable (not corrupted)
- Basic markdown structure is valid
- No merge conflict markers present

**B. Optional: Run quick validation**:
- Check for orphaned references
- Verify section structure maintained
- Ensure no duplicate IDs introduced

If validation fails:
- Restore from backup
- Report specific validation errors
- ABORT with recovery instructions

### 8. Report Completion

Provide comprehensive completion report:

```markdown
# ✅ Delta Merge Completed

**Branch**: {branch-name}  
**Date**: {timestamp}  
**Spec Updated**: .specify/specs/spec.md

## Changes Applied

- ✅ Additions: {count} items
- 🔄 Modifications: {count} items
- ❌ Deletions: {count} items

## Files Updated

- `.specify/specs/spec.md` - Main specification updated
- `.specify/specs/CHANGELOG.md` - Change history recorded
- `.specify/specs/.backups/spec_backup_{timestamp}_{branch}.md` - Backup created

## Delta Status

{Archive or Delete confirmation}

## Next Steps

1. Review the updated `.specify/specs/spec.md` to verify changes
2. Run `/speckit.plan` to create implementation plan based on new spec
3. Run `/speckit.tasks` to generate task breakdown
4. Proceed with implementation via `/speckit.implement`

## Git Integration

{If git available:}
Changes have been staged. Suggested commit message:

```
feat: apply delta from {branch}

- Added: {brief list}
- Modified: {brief list}
- Removed: {brief list}
```

Run `git commit` to commit changes, or `git reset` to unstage.

{If git not available or user declined:}
Changes applied but not committed. Manually commit when ready.

## Rollback Instructions

If you need to undo this merge:

1. Restore from backup:
   ```bash
   cp .specify/specs/.backups/spec_backup_{timestamp}_{branch}.md .specify/specs/spec.md
   ```

2. Restore delta (if archived):
   ```bash
   mv specs/.deltas-archive/{timestamp}_{branch} .specify/.deltas/{branch}
   ```

3. Revert CHANGELOG.md manually

```

## Operating Constraints

### Safety Measures

1. **Always backup**: Never modify .specify/specs/spec.md without backup
2. **Validate before commit**: Ensure merge succeeded before deleting delta
3. **Atomic operations**: If any step fails, rollback completely
4. **User confirmation**: Require explicit confirmation for destructive operations

### Merge Strategy

The merge process should:

**For Additions**:
- Find appropriate insertion point in .specify/specs/spec.md
- Preserve existing section order
- Add new user stories in priority order
- Add new requirements in logical grouping

**For Modifications**:
- Locate exact text to replace (from delta "Before")
- Replace with new text (from delta "After")
- Preserve formatting and indentation
- Update related cross-references if needed

**For Deletions**:
- Locate exact text to remove
- Remove cleanly without leaving orphaned content
- Check for and update any cross-references
- Maintain document flow

### Error Recovery

If merge fails at any point:
1. Stop immediately
2. Restore .specify/specs/spec.md from backup
3. Preserve delta for review and correction
4. Report detailed error to user
5. Suggest next steps (review delta, edit manually, etc.)

## Command Flags

Optional flags that can be passed in $ARGUMENTS:

- `--force` or `-f`: Skip confirmation prompt
- `--delete-delta`: Delete delta instead of archiving
- `--no-git`: Skip git integration even if available
- `--backup-only`: Create backup but don't merge (testing)
- `--dry-run`: Show what would be merged without actually doing it

## Context

$ARGUMENTS


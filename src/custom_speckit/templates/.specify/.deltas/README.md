# Deltas (Temporary Change Staging)

This directory contains **pending specification changes** that await review and approval.

## Purpose

- Stage proposed changes before merging to `.specify/specs/`
- Allow review and modification before approval
- Track what's being added, modified, or removed

## Structure

```
.deltas/
└── {branch-name}/
    ├── delta-spec.md           # Proposed changes (additions, modifications, deletions)
    ├── changes-summary.md      # Human-readable change summary
    └── review-checklist.md     # Review status
```

## Workflow

1. `/speckit.specify` with existing project → creates delta
2. `/speckit.review-delta` → analyze impact
3. User reviews and optionally edits delta manually
4. `/speckit.approve-delta` → merges to `.specify/specs/` and cleans up
5. `/speckit.reject-delta` → discards delta

## Lifecycle

- **Created**: When `/speckit.specify` detects changes to existing spec
- **Reviewed**: User or team review the delta
- **Approved**: Merged to `.specify/specs/`, this directory cleaned up
- **Rejected**: Deleted without merging

## Guidelines

- These are **temporary** - don't commit to version control (add to .gitignore)
- Review thoroughly before approval
- Can be manually edited if AI-generated changes need refinement


# Specifications (Single Source of Truth)

This directory contains the **current, authoritative specification** for the entire project.

## Purpose

- Single source of truth for all project specifications
- Used as context when generating new features or changes
- Updated through delta approval process (not manually edited during feature development)

## Structure

```
specs/
├── spec.md              # Main feature specification
├── data-model.md        # Current data model
├── architecture.md      # System architecture
└── contracts/           # API contracts
    └── ...
```

## Workflow

1. Initial project: Created by `/speckit.specify`
2. Feature changes: Updated via `/speckit.approve-delta` after review
3. Always reflects the latest approved state

## Guidelines

- **DO NOT** manually edit during feature development
- Changes come through `.deltas/` review and approval process
- This is what AI agents use as context for consistency


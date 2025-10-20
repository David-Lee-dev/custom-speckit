# Features (Development History)

This directory contains the **historical record** of all feature development cycles.

## Purpose

- Track development history by version and date
- Store plans and tasks for each feature branch
- Provide audit trail of what was built and when

## Structure

```
features/
├── v1.0.0/
│   ├── 2025-01-15_001-user-authentication/
│   │   ├── plan.md
│   │   ├── tasks.md
│   │   └── implementation-notes.md
│   └── 2025-01-18_002-password-reset/
│       ├── plan.md
│       └── tasks.md
├── v1.1.0/
│   └── 2025-02-01_003-oauth-integration/
│       └── ...
└── v2.0.0/
    └── ...
```

## Naming Convention

`{version}/{YYYY-MM-DD}_{branch-name}/`

- **Version**: From git tags, package.json, or user input
- **Date**: Feature creation date
- **Branch name**: Git branch name (e.g., `001-feature-name`)

## Workflow

1. `/speckit.plan` → creates `features/{version}/{date}_{branch}/plan.md`
2. `/speckit.tasks` → creates `features/{version}/{date}_{branch}/tasks.md`
3. Implementation notes can be added manually during development

## Guidelines

- This is your development archive
- Useful for understanding how features evolved
- Can reference past decisions when making new changes
- Should be committed to version control


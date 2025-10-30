---
description: Execute the implementation planning workflow using the plan template to generate design artifacts.
scripts:
  sh: .specify/scripts/bash/compare-specs.sh --json && .specify/scripts/bash/get-version.sh --json --auto
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Language Detection

**CRITICAL**: Detect language from spec.md and use it consistently for plan.md.

**Detection Steps**:
1. Read `.specify/specs/spec.md` (main specification)
2. Analyze first 50 lines for language indicators:
   - **Korean**: Contains Hangul (가-힣) → Use Korean for plan.md
   - **English**: Only Latin characters → Use English for plan.md
   - **Default**: Korean
3. Use detected language for ALL plan.md content:
   - Section headings (예: "## 기술 스택" or "## Tech Stack")
   - Architecture descriptions
   - Implementation phases
   - Technical decisions and rationale

**Consistency Rule**: plan.md MUST match spec.md language to maintain project coherence.

## Outline

1. **Setup**: 
   a. Run `.specify/scripts/bash/compare-specs.sh --json` to check if delta exists and get paths.
   b. Run `.specify/scripts/bash/get-version.sh --json --auto` to get project version.
   c. Get current date in YYYY_MM_DD format (underscore separated).
   d. Get current branch name from compare-specs output.
   e. Create feature directory path: `.specify/features/{VERSION}/{YYYY_MM_DD-BRANCH}/`
   f. Create this directory if it doesn't exist.
   
   For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: 
   - Read `.specify/specs/spec.md` (main specification)
   - If delta exists (`.specify/.deltas/{BRANCH}/delta-spec.md`): Load it as well to understand what's changing
   - Read `.specify/memory/constitution.md`
   - Load `.specify/templates/plan-template.md` for structure
   - If exists: Read `.specify/specs/tech-stack.md` (existing technology decisions)
   - If exists: Read `.specify/specs/data-model.md` (existing data model)
   - If exists: Read `.specify/specs/contracts/` (existing API contracts)

3. **Execute plan workflow**: Follow the structure in IMPL_PLAN template to:
   - Fill Technical Context (mark unknowns as "NEEDS CLARIFICATION")
   - Fill Constitution Check section from constitution
   - Evaluate gates (ERROR if violations unjustified)
   - Phase 0: Create/update tech-stack.md in specs/ (resolve all NEEDS CLARIFICATION)
   - Phase 1: Create/update data-model.md and contracts/ in specs/
   - Phase 1: Generate plan.md in features/ (this feature's implementation plan)
   - Phase 1: Update agent context by running the agent script
   - Re-evaluate Constitution Check post-design

4. **Save generated files**:
   
   **Project-wide skeleton files** (saved to `.specify/specs/`):
   - `.specify/specs/tech-stack.md` - Technology stack and tools (create new or update existing)
   - `.specify/specs/data-model.md` - Data model (create new or append entities)
   - `.specify/specs/contracts/` - API contracts (create new or add endpoints)
   
   **Feature-specific files** (saved to `.specify/features/{VERSION}/{YYYY_MM_DD-BRANCH}/`):
   - `.specify/features/{VERSION}/{YYYY_MM_DD-BRANCH}/plan.md` - Implementation plan for this feature

5. **Stop and report**: Command ends after Phase 2 planning. Report:
   - Feature directory path: `.specify/features/{VERSION}/{YYYY_MM_DD-BRANCH}/`
   - Project skeleton files updated: tech-stack.md, data-model.md, contracts/
   - Feature implementation plan: plan.md
   - Next step: Run `/speckit.tasks` to generate task breakdown

## Phases

### Phase 0: Technology Stack Research

1. **Extract technology decisions from Technical Context**:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:
   ```
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Create or update tech-stack.md** at `.specify/specs/tech-stack.md`:
   
   **If file exists** (adding new feature):
   - Read existing tech-stack.md
   - Check if new technologies are needed for this feature
   - If yes: Append new technology with change history
     ```markdown
     ## {Category} (e.g., Database, Cache, etc.)
     - {Technology} {Version} - {Purpose}
       * Added: {YYYY-MM-DD} ({feature-branch})
       * Reason: {why added}
     ```
   - If no new tech: Skip update, use existing stack
   
   **If file does NOT exist** (first project):
   - Create new tech-stack.md with format:
     ```markdown
     # Technology Stack
     
     ## Backend
     - {Technology} {Version} - {Purpose}
     
     ## Frontend
     - {Technology} {Version} - {Purpose}
     
     ## Database
     - {Technology} {Version} - {Purpose}
     
     **Initial Decision**: {YYYY-MM-DD} ({feature-branch})
     ```

**Output**: `.specify/specs/tech-stack.md` created or updated with all technology decisions

### Phase 1: Data Model & API Contracts

**Prerequisites:** `.specify/specs/tech-stack.md` complete

1. **Create or update data-model.md** at `.specify/specs/data-model.md`:
   
   **If file exists** (adding new feature):
   - Read existing data-model.md
   - Extract new entities needed for this feature
   - Append new entities with metadata:
     ```markdown
     ## {EntityName}
     - field1: type
     - field2: type
     
     **Added**: {YYYY-MM-DD} ({feature-branch})
     **Purpose**: {why this entity is needed}
     ```
   - Update relationships if existing entities are affected
   
   **If file does NOT exist** (first project):
   - Create new data-model.md with all entities
   - Include entity definitions, fields, relationships
   - Add validation rules and state transitions
   - Mark as **Initial Model**: {YYYY-MM-DD} ({feature-branch})

2. **Create or update API contracts** at `.specify/specs/contracts/`:
   
   **If contracts/ exists** (adding new feature):
   - Add new endpoint files for this feature's user actions
   - Update existing endpoints if behavior changes
   - Preserve existing contract files
   
   **If contracts/ does NOT exist** (first project):
   - Create contracts/ directory
   - Generate OpenAPI/GraphQL schema for each user action
   - Use standard REST/GraphQL patterns

3. **Generate implementation plan** at `.specify/features/{VERSION}/{YYYY_MM_DD-BRANCH}/plan.md`:
   - Reference tech-stack.md, data-model.md, contracts/ from specs/
   - Focus on THIS feature's implementation approach
   - Specify which entities/APIs this feature will implement
   - Define development phases for this feature only

4. **Agent context update**:
   - Run `.specify/scripts/bash/update-agent-context.sh cursor-agent`
   - These scripts detect which AI agent is in use
   - Update the appropriate agent-specific context file
   - Add only new technology from tech-stack.md
   - Preserve manual additions between markers

**Output**: 
- Project skeleton: `.specify/specs/tech-stack.md`, `data-model.md`, `contracts/` (created or updated)
- Feature plan: `.specify/features/{VERSION}/{YYYY_MM_DD-BRANCH}/plan.md` (created)

## Key rules

- Use absolute paths
- ERROR on gate failures or unresolved clarifications

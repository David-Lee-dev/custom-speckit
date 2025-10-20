---
description: Execute the implementation planning workflow using the plan template to generate design artifacts.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: 
   a. Run `.specify/scripts/bash/compare-specs.sh --json` to check if delta exists and get paths.
   b. Run `.specify/scripts/bash/get-version.sh --json --auto` to get project version.
   c. Get current date in YYYY-MM-DD format.
   d. Get current branch name from compare-specs output.
   e. Create feature directory path: `features/{VERSION}/{YYYY-MM-DD}_{BRANCH}/`
   f. Create this directory if it doesn't exist.
   
   For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: 
   - Read `specs/spec.md` (main specification)
   - If delta exists (`.deltas/{BRANCH}/delta-spec.md`): Load it as well to understand what's changing
   - Read `.specify/memory/constitution.md`
   - Load `.specify/templates/plan-template.md` for structure

3. **Execute plan workflow**: Follow the structure in IMPL_PLAN template to:
   - Fill Technical Context (mark unknowns as "NEEDS CLARIFICATION")
   - Fill Constitution Check section from constitution
   - Evaluate gates (ERROR if violations unjustified)
   - Phase 0: Generate research.md (resolve all NEEDS CLARIFICATION)
   - Phase 1: Generate data-model.md, contracts/, quickstart.md
   - Phase 1: Update agent context by running the agent script
   - Re-evaluate Constitution Check post-design

4. **Save generated files**: All generated files go to the feature directory:
   - `features/{VERSION}/{YYYY-MM-DD}_{BRANCH}/plan.md` - Implementation plan
   - `features/{VERSION}/{YYYY-MM-DD}_{BRANCH}/research.md` - Research findings (if generated)
   - `features/{VERSION}/{YYYY-MM-DD}_{BRANCH}/data-model.md` - Data model (if generated)
   - `features/{VERSION}/{YYYY-MM-DD}_{BRANCH}/quickstart.md` - Quickstart guide (if generated)
   - `features/{VERSION}/{YYYY-MM-DD}_{BRANCH}/contracts/` - API contracts (if generated)

5. **Stop and report**: Command ends after Phase 2 planning. Report:
   - Feature directory path: `features/{VERSION}/{YYYY-MM-DD}_{BRANCH}/`
   - Generated artifacts list
   - Next step: Run `/speckit.tasks` to generate task breakdown

## Phases

### Phase 0: Outline & Research

1. **Extract unknowns from Technical Context** above:
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

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: `features/{VERSION}/{YYYY-MM-DD}_{BRANCH}/research.md` with all NEEDS CLARIFICATION resolved

### Phase 1: Design & Contracts

**Prerequisites:** `research.md` complete

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable
   - Save to: `features/{VERSION}/{YYYY-MM-DD}_{BRANCH}/data-model.md`

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `features/{VERSION}/{YYYY-MM-DD}_{BRANCH}/contracts/`

3. **Generate quickstart guide**:
   - Create quickstart.md with integration scenarios
   - Save to: `features/{VERSION}/{YYYY-MM-DD}_{BRANCH}/quickstart.md`

4. **Agent context update**:
   - Run `.specify/scripts/bash/update-agent-context.sh cursor-agent`
   - These scripts detect which AI agent is in use
   - Update the appropriate agent-specific context file
   - Add only new technology from current plan
   - Preserve manual additions between markers

**Output**: All files saved to `features/{VERSION}/{YYYY-MM-DD}_{BRANCH}/`

## Key rules

- Use absolute paths
- ERROR on gate failures or unresolved clarifications

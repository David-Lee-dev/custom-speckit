---
description: Create or update the feature specification from a natural language feature description.
scripts:
  sh: .specify/scripts/bash/compare-specs.sh --json
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

The text the user typed after `/speckit.specify` in the triggering message **is** the feature description. Assume you always have it available in this conversation even if `$ARGUMENTS` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

Given that feature description, do this:

**STEP 0: Check for Existing Specification**

Run `.specify/scripts/bash/compare-specs.sh --json` from repo root and parse its JSON output for HAS_EXISTING_SPEC, SPEC_PATH, DELTA_DIR, and CURRENT_BRANCH.

- **If HAS_EXISTING_SPEC is false**: Follow the **New Project Workflow** (Steps 1-7 below)
- **If HAS_EXISTING_SPEC is true**: Follow the **Delta Workflow** (see Delta Workflow section after step 7)

---

## New Project Workflow

This workflow is used when `.specify/specs/spec.md` does not exist (first time using speckit).

1. **Generate a concise short name** (2-4 words) for the branch:
   - Analyze the feature description and extract the most meaningful keywords
   - Create a 2-4 word short name that captures the essence of the feature
   - Use action-noun format when possible (e.g., "add-user-auth", "fix-payment-bug")
   - Preserve technical terms and acronyms (OAuth2, API, JWT, etc.)
   - Keep it concise but descriptive enough to understand the feature at a glance
   - Examples:
     - "I want to add user authentication" → "user-auth"
     - "Implement OAuth2 integration for the API" → "oauth2-api-integration"
     - "Create a dashboard for analytics" → "analytics-dashboard"
     - "Fix payment processing timeout bug" → "fix-payment-timeout"

2. Run the script `.specify/scripts/bash/create-new-feature.sh --json "$ARGUMENTS"` from repo root **with the short-name argument** and parse its JSON output for BRANCH_NAME and SPEC_FILE. All file paths must be absolute.
   
   **NOTE**: For new projects, this creates the spec at `specs/{branch}/spec.md`. After completion, you should move it to `.specify/specs/spec.md` as the single source of truth.

   **IMPORTANT**:

   - Append the short-name argument to the `.specify/scripts/bash/create-new-feature.sh --json "$ARGUMENTS"` command with the 2-4 word short name you created in step 1
   - Bash: `--short-name "your-generated-short-name"`
   - PowerShell: `-ShortName "your-generated-short-name"`
   - For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot")
   - You must only ever run this script once
   - The JSON is provided in the terminal as output - always refer to it to get the actual content you're looking for

3. Load `.specify/templates/spec-template.md` to understand required sections.

4. Follow this execution flow:

    1. Parse user description from Input
       If empty: ERROR "No feature description provided"
    2. Extract key concepts from description
       Identify: actors, actions, data, constraints
    3. For unclear aspects:
       - Make informed guesses based on context and industry standards
       - Only mark with [NEEDS CLARIFICATION: specific question] if:
         - The choice significantly impacts feature scope or user experience
         - Multiple reasonable interpretations exist with different implications
         - No reasonable default exists
       - **LIMIT: Maximum 3 [NEEDS CLARIFICATION] markers total**
       - Prioritize clarifications by impact: scope > security/privacy > user experience > technical details
    4. Fill User Scenarios & Testing section
       If no clear user flow: ERROR "Cannot determine user scenarios"
    5. Generate Functional Requirements
       Each requirement must be testable
       Use reasonable defaults for unspecified details (document assumptions in Assumptions section)
    6. Define Success Criteria
       Create measurable, technology-agnostic outcomes
       Include both quantitative metrics (time, performance, volume) and qualitative measures (user satisfaction, task completion)
       Each criterion must be verifiable without implementation details
    7. Identify Key Entities (if data involved)
    8. Return: SUCCESS (spec ready for planning)

5. Write the specification to SPEC_FILE using the template structure, replacing placeholders with concrete details derived from the feature description (arguments) while preserving section order and headings.

6. **Specification Quality Validation**: After writing the initial spec, validate it against quality criteria:

   a. **Create Spec Quality Checklist**: Generate a checklist file at `FEATURE_DIR/checklists/requirements.md` using the checklist template structure with these validation items:
   
      ```markdown
      # Specification Quality Checklist: [FEATURE NAME]
      
      **Purpose**: Validate specification completeness and quality before proceeding to planning
      **Created**: [DATE]
      **Feature**: [Link to spec.md]
      
      ## Content Quality
      
      - [ ] No implementation details (languages, frameworks, APIs)
      - [ ] Focused on user value and business needs
      - [ ] Written for non-technical stakeholders
      - [ ] All mandatory sections completed
      
      ## Requirement Completeness
      
      - [ ] No [NEEDS CLARIFICATION] markers remain
      - [ ] Requirements are testable and unambiguous
      - [ ] Success criteria are measurable
      - [ ] Success criteria are technology-agnostic (no implementation details)
      - [ ] All acceptance scenarios are defined
      - [ ] Edge cases are identified
      - [ ] Scope is clearly bounded
      - [ ] Dependencies and assumptions identified
      
      ## Feature Readiness
      
      - [ ] All functional requirements have clear acceptance criteria
      - [ ] User scenarios cover primary flows
      - [ ] Feature meets measurable outcomes defined in Success Criteria
      - [ ] No implementation details leak into specification
      
      ## Notes
      
      - Items marked incomplete require spec updates before `/speckit.clarify` or `/speckit.plan`
      ```
   
   b. **Run Validation Check**: Review the spec against each checklist item:
      - For each item, determine if it passes or fails
      - Document specific issues found (quote relevant spec sections)
   
   c. **Handle Validation Results**:
      
      - **If all items pass**: Mark checklist complete and proceed to step 6
      
      - **If items fail (excluding [NEEDS CLARIFICATION])**:
        1. List the failing items and specific issues
        2. Update the spec to address each issue
        3. Re-run validation until all items pass (max 3 iterations)
        4. If still failing after 3 iterations, document remaining issues in checklist notes and warn user
      
      - **If [NEEDS CLARIFICATION] markers remain**:
        1. Extract all [NEEDS CLARIFICATION: ...] markers from the spec
        2. **LIMIT CHECK**: If more than 3 markers exist, keep only the 3 most critical (by scope/security/UX impact) and make informed guesses for the rest
        3. For each clarification needed (max 3), present options to user in this format:
        
           ```markdown
           ## Question [N]: [Topic]
           
           **Context**: [Quote relevant spec section]
           
           **What we need to know**: [Specific question from NEEDS CLARIFICATION marker]
           
           **Suggested Answers**:
           
           | Option | Answer | Implications |
           |--------|--------|--------------|
           | A      | [First suggested answer] | [What this means for the feature] |
           | B      | [Second suggested answer] | [What this means for the feature] |
           | C      | [Third suggested answer] | [What this means for the feature] |
           | Custom | Provide your own answer | [Explain how to provide custom input] |
           
           **Your choice**: _[Wait for user response]_
           ```
        
        4. **CRITICAL - Table Formatting**: Ensure markdown tables are properly formatted:
           - Use consistent spacing with pipes aligned
           - Each cell should have spaces around content: `| Content |` not `|Content|`
           - Header separator must have at least 3 dashes: `|--------|`
           - Test that the table renders correctly in markdown preview
        5. Number questions sequentially (Q1, Q2, Q3 - max 3 total)
        6. Present all questions together before waiting for responses
        7. Wait for user to respond with their choices for all questions (e.g., "Q1: A, Q2: Custom - [details], Q3: B")
        8. Update the spec by replacing each [NEEDS CLARIFICATION] marker with the user's selected or provided answer
        9. Re-run validation after all clarifications are resolved
   
   d. **Update Checklist**: After each validation iteration, update the checklist file with current pass/fail status

7. Report completion with branch name, spec file path, checklist results, and readiness for the next phase (`/speckit.clarify` or `/speckit.plan`).

**NOTE:** The script creates and checks out the new branch and initializes the spec file before writing.

## General Guidelines

## Quick Guidelines

- Focus on **WHAT** users need and **WHY**.
- Avoid HOW to implement (no tech stack, APIs, code structure).
- Written for business stakeholders, not developers.
- DO NOT create any checklists that are embedded in the spec. That will be a separate command.

### Section Requirements

- **Mandatory sections**: Must be completed for every feature
- **Optional sections**: Include only when relevant to the feature
- When a section doesn't apply, remove it entirely (don't leave as "N/A")

### For AI Generation

When creating this spec from a user prompt:

1. **Make informed guesses**: Use context, industry standards, and common patterns to fill gaps
2. **Document assumptions**: Record reasonable defaults in the Assumptions section
3. **Limit clarifications**: Maximum 3 [NEEDS CLARIFICATION] markers - use only for critical decisions that:
   - Significantly impact feature scope or user experience
   - Have multiple reasonable interpretations with different implications
   - Lack any reasonable default
4. **Prioritize clarifications**: scope > security/privacy > user experience > technical details
5. **Think like a tester**: Every vague requirement should fail the "testable and unambiguous" checklist item
6. **Common areas needing clarification** (only if no reasonable default exists):
   - Feature scope and boundaries (include/exclude specific use cases)
   - User types and permissions (if multiple conflicting interpretations possible)
   - Security/compliance requirements (when legally/financially significant)
   
**Examples of reasonable defaults** (don't ask about these):

- Data retention: Industry-standard practices for the domain
- Performance targets: Standard web/mobile app expectations unless specified
- Error handling: User-friendly messages with appropriate fallbacks
- Authentication method: Standard session-based or OAuth2 for web apps
- Integration patterns: RESTful APIs unless specified otherwise

### Success Criteria Guidelines

Success criteria must be:

1. **Measurable**: Include specific metrics (time, percentage, count, rate)
2. **Technology-agnostic**: No mention of frameworks, languages, databases, or tools
3. **User-focused**: Describe outcomes from user/business perspective, not system internals
4. **Verifiable**: Can be tested/validated without knowing implementation details

**Good examples**:

- "Users can complete checkout in under 3 minutes"
- "System supports 10,000 concurrent users"
- "95% of searches return results in under 1 second"
- "Task completion rate improves by 40%"

**Bad examples** (implementation-focused):

- "API response time is under 200ms" (too technical, use "Users see results instantly")
- "Database can handle 1000 TPS" (implementation detail, use user-facing metric)
- "React components render efficiently" (framework-specific)
- "Redis cache hit rate above 80%" (technology-specific)

---

## Delta Workflow

This workflow is used when `.specify/specs/spec.md` already exists (modifying existing project).

**Purpose**: Generate a delta specification that captures ONLY the changes (additions, modifications, deletions) to be reviewed and approved before merging into the main spec.

### Delta Generation Steps

1. **Load existing specification**:
   - Read `.specify/specs/spec.md` (path from compare-specs.sh output)
   - Parse current user stories, requirements, and structure
   - Note the last modification time

2. **Analyze user requirements**:
   - Parse the user's feature description from $ARGUMENTS
   - Identify what's being requested:
     * New features/user stories
     * Changes to existing requirements
     * Removal of existing features
   
3. **Generate change analysis**:
   - **Additions**: New user stories, requirements, or sections not in existing spec
   - **Modifications**: Changes to existing user stories or requirements
   - **Deletions**: Explicitly requested removals or deprecations
   
4. **Create delta directory**:
   - Create `.specify/.deltas/{CURRENT_BRANCH}/` directory
   - Branch name comes from compare-specs.sh output

5. **Generate delta-spec.md**:
   - Load `.specify/templates/delta-spec-template.md`
   - Fill in the template with:
     * Change summary (high-level overview)
     * Change statistics (counts of additions/modifications/deletions)
     * Detailed breakdown of each change
     * Impact analysis (affected components, risks, effort)
     * Constitution compliance check
   
   **For each addition**:
   - Write new requirement in same format as main spec
   - Include rationale explaining why it's needed
   - Reference user request
   
   **For each modification**:
   - Show "Before" (quote from existing spec)
   - Show "After" (proposed new text)
   - Explain rationale for change
   - Analyze impact on existing implementations
   
   **For each deletion**:
   - Quote what's being removed
   - Explain why it's no longer needed
   - Provide migration path for existing implementations

6. **Generate changes-summary.md**:
   - Create `.specify/.deltas/{CURRENT_BRANCH}/changes-summary.md`
   - Human-readable summary of changes
   - Format:
     ```markdown
     # Change Summary: {Feature Name}
     
     ## Overview
     [2-3 sentence description of what's changing]
     
     ## Key Changes
     - ✅ Added: {count} new requirements
     - 🔄 Modified: {count} existing requirements  
     - ❌ Removed: {count} requirements
     
     ## Highlights
     - {Most significant change 1}
     - {Most significant change 2}
     - {Most significant change 3}
     
     ## Next Steps
     1. Review delta at `.specify/.specify/.deltas/{branch}/delta-spec.md`
     2. Run `/speckit.review-delta` for detailed analysis
     3. Manually edit delta if needed
     4. Run `/speckit.approve-delta` to merge or `/speckit.reject-delta` to discard
     ```

7. **Generate review checklist**:
   - Create `.specify/.deltas/{CURRENT_BRANCH}/review-checklist.md`
   - Pre-filled checklist for reviewers
   - Format:
     ```markdown
     # Review Checklist: {Feature Name}
     
     **Branch**: {branch-name}
     **Delta Created**: {timestamp}
     **Reviewer**: _[To be filled]_
     
     ## Pre-Review
     - [ ] Read the changes-summary.md
     - [ ] Understand the user's original request
     - [ ] Review existing spec.md for context
     
     ## Content Review
     - [ ] All additions are necessary and justified
     - [ ] All modifications preserve existing functionality (unless intentional breaking change)
     - [ ] All deletions have clear migration paths
     - [ ] No conflicts with constitution.md
     - [ ] No implementation details in spec
     
     ## Impact Review
     - [ ] Impact analysis is realistic
     - [ ] Risk assessment is complete
     - [ ] Effort estimates are reasonable
     - [ ] Dependencies are identified
     
     ## Decision
     - [ ] APPROVE - merge with `/speckit.approve-delta`
     - [ ] MODIFY - edit delta-spec.md manually, then approve
     - [ ] REJECT - discard with `/speckit.reject-delta`
     
     **Notes**: _[Reviewer notes]_
     ```

8. **Report completion**:
   - Report delta location: `.specify/.specify/.deltas/{branch}/`
   - Show change statistics
   - List generated files:
     * `delta-spec.md` - full delta specification
     * `changes-summary.md` - quick overview
     * `review-checklist.md` - review guide
   - Recommend next steps:
     * "Review the delta with `/speckit.review-delta`"
     * "Edit `.specify/.specify/.deltas/{branch}/delta-spec.md` manually if needed"
     * "Approve with `/speckit.approve-delta` or reject with `/speckit.reject-delta`"

### Delta Generation Guidelines

1. **Be Conservative**: Only include changes that are explicitly requested or clearly implied
2. **Show Context**: For modifications, always show before/after comparison
3. **Explain Everything**: Every change needs a clear rationale
4. **Think About Impact**: Consider how changes affect existing implementations
5. **Maintain Consistency**: Use same terminology and structure as existing spec
6. **No Implementation Details**: Keep delta at same abstraction level as main spec

### Special Cases

**Case 1: User requests conflicting change**
- Note the conflict in delta
- Explain the conflict in rationale
- Suggest resolution options
- Mark as requiring manual review

**Case 2: Change affects multiple sections**
- Document all affected sections
- Cross-reference related changes
- Ensure consistency across all modifications

**Case 3: Breaking change**
- Clearly mark as breaking change
- Provide detailed migration path
- Estimate impact on existing implementations
- Suggest alternatives if possible

### Important Notes

- **DO NOT** modify `.specify/specs/spec.md` directly - that happens in `/speckit.approve-delta`
- **DO NOT** create branch or run create-new-feature.sh - use current branch from compare-specs.sh
- **DO** preserve existing spec structure and style
- **DO** make delta self-contained and reviewable
- The delta is temporary - it will be merged or discarded, not committed long-term

---
description: Review and analyze a pending delta specification before approval.
scripts:
  sh: .specify/scripts/bash/compare-specs.sh --json
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Goal

Perform a comprehensive analysis of the delta specification to help reviewers make an informed decision about approving or rejecting the proposed changes.

This command is READ-ONLY - it does not modify any files, only provides analysis and recommendations.

## Operating Constraints

**STRICTLY READ-ONLY**: Do **not** modify any files. Output a structured analysis report with actionable recommendations.

**Constitution Authority**: The project constitution (`.specify/memory/constitution.md`) is **non-negotiable**. Any delta violations are automatically CRITICAL and require adjustment.

## Execution Steps

### 1. Initialize Review Context

Run `.specify/scripts/bash/compare-specs.sh --json` from repo root and parse JSON for HAS_EXISTING_SPEC, SPEC_PATH, DELTA_DIR, and CURRENT_BRANCH. All paths must be absolute.

**Prerequisites Check**:
- If HAS_EXISTING_SPEC is false: ERROR "No existing spec found. Delta review requires .specify/specs/spec.md to exist."
- If DELTA_DIR does not exist: ERROR "No delta found for branch {branch}. Run /speckit.specify first."

Derive delta file paths:
- DELTA_SPEC = DELTA_DIR/delta-spec.md
- CHANGES_SUMMARY = DELTA_DIR/changes-summary.md
- REVIEW_CHECKLIST = DELTA_DIR/review-checklist.md

For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

### 2. Load Artifacts

Load the following documents:

**Required**:
- `.specify/specs/spec.md` - existing specification (base)
- `{DELTA_DIR}/delta-spec.md` - proposed changes

**Optional** (if exist):
- `{DELTA_DIR}/changes-summary.md` - quick overview
- `{DELTA_DIR}/review-checklist.md` - review checklist
- `.specify/memory/constitution.md` - project principles

### 3. Build Analysis Model

Create internal representations for analysis:

**From .specify/specs/spec.md**:
- Extract all user stories (with IDs and priorities)
- Extract all functional requirements (with IDs)
- Extract all non-functional requirements
- Note the overall structure and terminology

**From delta-spec.md**:
- List all additions (new user stories, new requirements)
- List all modifications (what changed from/to)
- List all deletions (what's being removed)
- Extract change rationales
- Extract impact analysis notes

### 4. Analysis Passes

Perform the following analysis checks, focusing on high-signal findings:

#### A. Completeness Analysis

**For Additions**:
- [ ] Each new requirement has clear rationale
- [ ] Each new user story has acceptance criteria
- [ ] New requirements don't duplicate existing ones
- [ ] Impact analysis includes all affected areas

**For Modifications**:
- [ ] Both "before" and "after" are clearly documented
- [ ] Rationale explains why change is needed
- [ ] Impact on existing implementations is assessed
- [ ] Related requirements are updated consistently

**For Deletions**:
- [ ] Reason for deletion is documented
- [ ] Migration path is provided
- [ ] Impact on dependent requirements is assessed
- [ ] No orphaned references remain

#### B. Consistency Analysis

**Terminology**:
- Check that delta uses same terms as base spec
- Flag any terminology drift or new undefined terms
- Verify consistency across all changes

**Structure**:
- Verify delta follows same section organization as base spec
- Check that priorities are consistent with existing scheme
- Ensure acceptance criteria format matches base spec

**Cross-references**:
- Check that modified requirements update all related sections
- Verify that user story changes reflect in requirements
- Ensure data model references are consistent

#### C. Impact Analysis

**Scope Assessment**:
- Estimate total number of requirements affected
- Identify cascade effects (one change requiring others)
- Assess whether changes are additive or breaking

**Risk Assessment**:
- Identify high-risk changes (breaking changes, deletions)
- Flag changes that affect core functionality
- Note changes with broad system impact

**Effort Estimation Validation**:
- Review effort estimates in delta for realism
- Compare with similar past changes if available
- Flag underestimated or overestimated efforts

#### D. Constitution Compliance

Load `.specify/memory/constitution.md` and verify:
- [ ] No violations of MUST principles
- [ ] Complexity increases are justified
- [ ] Changes align with architectural standards
- [ ] Quality gates are maintained

**Flag any violations as CRITICAL** - these must be resolved before approval.

#### E. Quality Analysis

**Clarity**:
- Check for vague language ("fast", "scalable", "good")
- Verify all requirements are testable
- Ensure acceptance criteria are measurable
- Flag any [NEEDS CLARIFICATION] markers

**Completeness**:
- Verify edge cases are addressed
- Check error scenarios are covered
- Ensure security/privacy implications are documented
- Validate that dependencies are identified

#### F. Conflict Detection

**Internal Conflicts** (within delta):
- Check if additions conflict with each other
- Verify modifications don't contradict deletions
- Ensure rationales are consistent

**External Conflicts** (delta vs base spec):
- Identify if changes conflict with untouched requirements
- Check if deletions remove dependencies of other requirements
- Flag breaking changes that lack migration paths

### 5. Produce Review Report

Output a Markdown report (no file writes) with the following structure:

```markdown
# Delta Review Report: {Feature Name}

**Branch**: {branch-name}  
**Delta Created**: {timestamp}  
**Review Date**: {current-date}  
**Reviewer**: AI Agent

---

## Executive Summary

[2-3 sentences summarizing the delta and recommendation]

**Overall Recommendation**: ✅ APPROVE | ⚠️ APPROVE WITH CHANGES | ❌ REJECT

**Change Summary**:
- ✅ Additions: {count} items
- 🔄 Modifications: {count} items
- ❌ Deletions: {count} items

**Risk Level**: Low | Medium | High

---

## Findings

### Critical Issues (Must Fix Before Approval)

| ID | Category | Location | Issue | Recommendation |
|----|----------|----------|-------|----------------|
| C1 | Constitution | delta-spec.md:L50 | Violates principle X | {specific fix} |

*If no critical issues: "✅ No critical issues found"*

### High Priority Issues (Should Fix)

| ID | Category | Location | Issue | Recommendation |
|----|----------|----------|-------|----------------|
| H1 | Completeness | Addition #3 | Missing impact analysis | Add analysis for data model impact |

### Medium Priority Issues (Consider Fixing)

| ID | Category | Location | Issue | Recommendation |
|----|----------|----------|-------|----------------|
| M1 | Consistency | Modification #2 | Terminology drift | Use "user session" instead of "login state" |

### Low Priority Issues (Optional)

| ID | Category | Location | Issue | Recommendation |
|----|----------|----------|-------|----------------|
| L1 | Style | Multiple | Minor wording improvements | See detailed notes |

---

## Detailed Analysis

### Additions Analysis

{For each addition, provide brief assessment}

**Addition 1: User Story X - {Title}**
- ✅ Well-justified with clear rationale
- ✅ Acceptance criteria are testable
- ⚠️ Impact analysis incomplete (missing UI component effects)
- Priority: P{N} - appropriate for this change

### Modifications Analysis

{For each modification, assess quality of change}

**Modification 1: FR-XXX - {Title}**
- ✅ Before/after clearly documented
- ✅ Rationale is sound
- ✅ Impact analysis thorough
- ⚠️ Related requirement FR-YYY should also be updated

### Deletions Analysis

{For each deletion, verify justification}

**Deletion 1: FR-ZZZ - {Title}**
- ✅ Reason for deletion is clear
- ⚠️ Migration path incomplete
- ❌ Dependent requirement FR-AAA not addressed

---

## Impact Summary

### Affected Components

| Component | Impact Level | Details |
|-----------|--------------|---------|
| Data Model | Medium | 3 entities affected, 2 new fields |
| API Contracts | High | 5 endpoints modified, 2 breaking changes |
| User Interface | Low | Minor text changes only |
| Business Logic | Medium | 2 services require updates |

### Risk Assessment

**Breaking Changes**: {count}
- {List each breaking change and mitigation}

**Dependencies**: {count}
- {List new dependencies introduced}

**Effort Estimate Validation**:
- Delta estimates: {X} hours/days
- Review assessment: {Y} hours/days
- Variance: {±Z%}
- Assessment: Realistic | Underestimated | Overestimated

---

## Constitution Compliance

{Load and check against constitution.md}

- ✅ All core principles satisfied
- ✅ No unjustified complexity increases
- ✅ Architectural standards maintained
- ✅ Quality gates preserved

*Or if violations exist:*

- ❌ Violation: {Principle name}
  - Location: {Where in delta}
  - Issue: {What violates it}
  - Fix: {How to resolve}

---

## Recommendations

### Before Approval

**MUST DO** (Critical):
1. {Critical fix 1}
2. {Critical fix 2}

**SHOULD DO** (High priority):
1. {High priority fix 1}
2. {High priority fix 2}

**CONSIDER** (Medium/Low):
1. {Optional improvement 1}
2. {Optional improvement 2}

### Approval Decision Guide

**Approve Immediately** if:
- No critical issues
- High priority issues are acceptable
- Changes are well-justified and complete

**Approve After Edits** if:
- Only high/medium priority issues exist
- Issues can be fixed by editing delta-spec.md manually
- Core changes are sound but details need refinement

**Reject** if:
- Critical constitution violations
- Fundamental problems with change approach
- Missing essential information that can't be filled by editing

---

## Next Steps

1. **If approving**: 
   - Run `/speckit.approve-delta` to merge changes to .specify/specs/spec.md
   
2. **If editing first**:
   - Manually edit `.specify/.specify/.deltas/{branch}/delta-spec.md` to address issues
   - Optionally re-run `/speckit.review-delta` to verify fixes
   - Run `/speckit.approve-delta` when ready
   
3. **If rejecting**:
   - Run `/speckit.reject-delta` to discard changes
   - Provide feedback to user about why rejected
   - User can run `/speckit.specify` again with refined requirements

---

## Review Checklist Status

{If review-checklist.md exists, show completion status}

- ✅ Completed: {count}/{total}
- ⏳ Pending: {count}/{total}

Key items:
- [ ] All additions are necessary and justified
- [ ] All modifications preserve existing functionality
- [ ] All deletions have clear migration paths
- [ ] No conflicts with constitution
- [ ] Impact analysis is realistic

```

### 6. Provide Actionable Summary

At the end of the report, provide a clear, concise summary:

```markdown
## Summary

{1-2 sentence verdict}

**Action**: {APPROVE | EDIT_THEN_APPROVE | REJECT}

**Confidence**: {High | Medium | Low}
```

## Operating Principles

### Context Efficiency

- **Focus on findings**: Don't repeat content from delta, only analyze it
- **Prioritize issues**: Critical > High > Medium > Low
- **Limit findings**: Cap at 50 total findings, summarize overflow
- **Be specific**: Quote line numbers and exact text when identifying issues

### Analysis Guidelines

- **NEVER modify files** (this is read-only analysis)
- **NEVER hallucinate issues** (only report actual problems found)
- **Prioritize constitution violations** (these are always CRITICAL)
- **Be constructive**: Suggest fixes, not just problems
- **Consider user intent**: Understand what they're trying to achieve

### Review Philosophy

This command helps humans make better decisions. The analysis should:
- Be thorough but not overwhelming
- Highlight risks without being alarmist
- Suggest improvements without being prescriptive
- Respect the user's judgment on final decision

## Context

$ARGUMENTS


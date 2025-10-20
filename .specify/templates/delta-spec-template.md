# Delta Specification: [FEATURE NAME]

**Branch**: `[###-feature-name]`  
**Base Spec**: `specs/spec.md` (last modified: [DATE])  
**Delta Created**: [DATE]  
**Status**: PENDING_REVIEW

<!--
  This document represents CHANGES to the existing specification.
  It is NOT a complete spec - only additions, modifications, and deletions.
  
  After review and approval via /speckit.approve-delta, these changes will be
  merged into specs/spec.md and this delta will be archived or removed.
-->

## Change Summary

<!--
  Provide a high-level overview of what's changing and why.
  This should be a few sentences that anyone can understand.
-->

[Brief description of the feature change request]

**Change Statistics**:
- ✅ Additions: [N] items
- 🔄 Modifications: [N] items
- ❌ Deletions: [N] items

**Estimated Impact**: Low | Medium | High

---

## 🆕 Additions

<!--
  New requirements, user stories, or sections being added to the spec.
  Use the same format as the main spec template.
-->

### [Section Name] (NEW)

#### User Story [N] - [Title] (Priority: P[N]) **(NEW)**

[Describe the new user journey]

**Rationale**: [Why this is needed - reference to user request or business need]

**Independent Test**: [How this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

#### FR-NEW-[NNN]: [Requirement Title] **(NEW)**

[Requirement description]

**Rationale**: [Why this requirement is needed]

**Acceptance Criteria**:
- [Criterion 1]
- [Criterion 2]

**Dependencies**: [Any new dependencies this introduces]

---

## 🔄 Modifications

<!--
  Changes to existing requirements or sections.
  Always show both BEFORE and AFTER for clarity.
-->

### User Story [N] - [Title] **(MODIFIED)**

**Change Type**: Scope Expansion | Scope Reduction | Clarification | Priority Change

**Original Priority**: P[N] → **New Priority**: P[N]

**Before**:
```
[Original user story text from specs/spec.md]
```

**After**:
```
[Modified user story text]
```

**Rationale**: [Why this changed]

**Impact Analysis**:
- Existing implementations: [What needs to change]
- Related requirements: [Which other requirements are affected]
- Estimated effort: [Low/Medium/High]

---

### FR-[NNN]: [Requirement Title] **(MODIFIED)**

**Change Type**: Expanded | Clarified | Restricted

**Before**:
```
[Original requirement text]
```

**After**:
```
[Modified requirement text]
```

**Rationale**: [Why this changed]

**Impact Analysis**:
- Data model changes: [Yes/No - details]
- API changes: [Yes/No - details]
- Breaking changes: [Yes/No - details]

---

## ❌ Deletions

<!--
  Requirements or sections being removed.
  Always explain WHY and provide migration path if applicable.
-->

### User Story [N] - [Title] **(DELETED)**

**Original Priority**: P[N]

**Original Content**:
```
[Original user story text being removed]
```

**Reason for Deletion**: [Why is this no longer needed]

**Migration Path**: 
- [What happens to existing implementations]
- [Alternative approaches if any]
- [Impact on other user stories]

---

### FR-[NNN]: [Requirement Title] **(DELETED)**

**Original Content**:
```
[Original requirement text]
```

**Reason for Deletion**: [Why removed]

**Migration Path**:
- Existing code: [What to do with implementations]
- Existing data: [What to do with data if applicable]
- Tests: [What to do with existing tests]

---

## Impact Analysis

<!--
  Comprehensive analysis of how these changes affect the entire system.
  This helps reviewers understand the blast radius of the changes.
-->

### Affected Components

- [ ] **Data Model**: [Yes/No]
  - Details: [What entities/fields are affected]
  
- [ ] **API Contracts**: [Yes/No]
  - Details: [Which endpoints are affected]
  - Breaking changes: [Yes/No]
  
- [ ] **User Interface**: [Yes/No]
  - Details: [Which screens/components are affected]
  
- [ ] **Business Logic**: [Yes/No]
  - Details: [Which services/workflows are affected]
  
- [ ] **Tests**: [Yes/No]
  - Details: [Which test suites need updates]
  
- [ ] **Documentation**: [Yes/No]
  - Details: [Which docs need updates]

### Risk Assessment

**Complexity Level**: Low | Medium | High

**Risk Factors**:
- [Risk 1 and mitigation]
- [Risk 2 and mitigation]

**Estimated Effort**:
- Development: [hours/days]
- Testing: [hours/days]
- Documentation: [hours/days]

### Dependencies

**New Dependencies**:
- [Library/service name and version if applicable]

**Affected Existing Dependencies**:
- [Which existing dependencies are impacted]

---

## Constitution Check

<!--
  Verify that these changes comply with project constitution.
  Reference .specify/memory/constitution.md
-->

- [ ] Changes comply with all core principles
- [ ] No violations of mandatory rules
- [ ] Complexity is justified (if violating simplicity principle)
- [ ] Changes align with project architecture standards

**Constitution Compliance Notes**:
[Any notes about constitution compliance, or "All checks passed"]

---

## Review Checklist

<!--
  Checklist for reviewers to ensure quality before approval.
  Mark items as complete during review process.
-->

### Content Quality

- [ ] All additions are well-justified with clear rationale
- [ ] All modifications show clear before/after comparison
- [ ] All deletions have documented migration paths
- [ ] Change descriptions are clear and unambiguous
- [ ] No implementation details leaked into spec (remains technology-agnostic)

### Completeness

- [ ] All affected user stories are documented
- [ ] All affected requirements are documented
- [ ] Impact analysis is thorough and realistic
- [ ] Risk assessment is complete
- [ ] Acceptance criteria are testable

### Consistency

- [ ] Changes don't conflict with existing requirements
- [ ] Terminology is consistent with main spec
- [ ] Priority assignments make sense
- [ ] No duplicate requirements introduced

### Traceability

- [ ] Each change references the source (user request, bug report, etc.)
- [ ] Related changes are cross-referenced
- [ ] Impact on existing features is documented

---

## Reviewer Notes

<!--
  Space for manual notes during review process.
  Can be filled by humans or AI during /speckit.review-delta
-->

**Reviewed By**: [Name/AI Agent]  
**Review Date**: [DATE]  
**Status**: Approved | Needs Changes | Rejected

**Comments**:
[Reviewer comments and feedback]

**Required Changes** (if any):
- [ ] [Change 1]
- [ ] [Change 2]

---

## Approval Decision

<!--
  Final decision section - filled when running /speckit.approve-delta or /speckit.reject-delta
-->

**Decision**: PENDING | APPROVED | REJECTED  
**Decision Date**: [DATE]  
**Decision By**: [Name/AI Agent]

**Approval Notes**:
[Notes about approval decision]

**Next Steps**:
- [ ] Run `/speckit.approve-delta` to merge changes to specs/spec.md
- [ ] Run `/speckit.plan` to generate implementation plan
- [ ] Run `/speckit.tasks` to break down into tasks


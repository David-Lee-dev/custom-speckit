---
description: "TDD Cycle Quick Reference - Red → Green → Refactor"
---

# TDD Cycle Guide

**Reference**: Kent Beck's Test-Driven Development

---

## 🔄 The Three Phases

### 🔴 Red Phase - Write Failing Test

**Goal**: Define what success looks like

**Steps**:
1. Pick ONE task from tasks.md
2. Write ONE test for that task
3. Run test - must FAIL
4. Verify failure is for the RIGHT reason

**Done When**: Test fails with expected error message

---

### 🟢 Green Phase - Make It Pass

**Goal**: Make test pass with minimum code

**Steps**:
1. Write SIMPLEST code to pass test
2. Hardcode if that works
3. Run all tests
4. All tests must be GREEN

**Done When**: All tests pass, no warnings

---

### 🔵 Refactor Phase - Improve Code

**Goal**: Clean up code while keeping tests green

**Steps**:
1. Identify duplication or complexity
2. Make ONE structural change
3. Run tests (must stay GREEN)
4. Repeat until code is clean

**Done When**: No obvious improvements, tests still green

---

## ✅ Checklist Per Cycle

### Before Moving to Next Test

- [ ] All tests pass (100% green)
- [ ] No compiler/linter warnings
- [ ] Code is simple and clear
- [ ] No duplication
- [ ] Commits separated (structural vs behavioral)

---

## 💡 Quick Tips

**Keep Tests Small**: One assertion per test when possible

**Keep Implementation Small**: 3-5 lines to pass test is ideal

**Refactor Frequently**: Don't let complexity accumulate

**One Thing at a Time**: One test, one implementation, one refactor

---

## 🚫 Common Mistakes

❌ Writing multiple tests before implementing
❌ Implementing features not yet tested
❌ Refactoring while tests are red
❌ Mixing structural and behavioral changes
❌ Skipping refactor phase

---

**For detailed methodology**: See `.cursor/rules/tdd-augmented-coding.mdc`


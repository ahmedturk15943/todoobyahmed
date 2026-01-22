---
id: "004"
title: "Toggle complete command behavior"
stage: "misc"
date: "2025-12-31"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "001-phase1-cli-app"
branch: "main"
user: "admin"
command: "Update the Todo CLI app so that the `complete <id>` command TOGGLES the task status"
labels: ["feature","cli","service-layer"]
links:
  spec: "specs/001-phase1-cli-app/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/001-phase1-cli-app/spec.md"
  - "src/services/todo_service.py"
  - "src/cli/main.py"
tests:
  - "test_phase1.py"
---

## Prompt

Update the Todo CLI app so that the `complete <id>` command TOGGLES the task status instead of only marking it complete.

Current behavior:
- If task is incomplete → mark complete
- If task is already complete → do nothing

Required behavior:
- If task is incomplete → mark complete
- If task is complete → mark incomplete

Constraints:
- Do NOT change CLI command names
- Use spec-driven changes only
- Update only the service layer logic
- Ensure error handling for invalid IDs remains unchanged
- All existing tests must still pass

Update relevant spec if needed and regenerate code using Claude Code.

## Response snapshot

Updated the complete command to toggle task status:

1. **Spec update** (specs/001-phase1-cli-app/spec.md):
   - Added new acceptance scenario for toggling incomplete → complete
   - Added new acceptance scenario for toggling complete → incomplete
   - Renumbered subsequent scenarios

2. **Service layer** (src/services/todo_service.py:197-226):
   - Modified `mark_complete()` to toggle status instead of always setting to complete
   - Added conditional logic: if task is complete, mark incomplete; otherwise mark complete

3. **CLI handler** (src/cli/main.py:119-137):
   - Updated `cmd_complete()` to display appropriate messages for both directions:
     - "marked as complete" when toggling to complete
     - "marked as incomplete" when toggling to incomplete
   - Preserved existing error handling for invalid IDs

4. **Verification**:
   - All 7 existing tests pass
   - Manual testing confirms toggle works in both directions
   - Error handling for invalid IDs unchanged

## Outcome

- ✅ Impact: The `complete <id>` command now toggles task status instead of only marking complete
- 🧪 Tests: All 7 tests in test_phase1.py pass
- 📁 Files: Modified 3 files (spec, service, CLI)
- 🔁 Next prompts: None
- 🧠 Reflection: Minimal changes needed - only service layer logic and CLI output messages required

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): All 7 tests PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A

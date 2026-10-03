---
name: handoff
description: Prepare or resume a task handoff when work must continue in another session or agent. Preserve current intent, decisions, work state, evidence, permissions, and the next action.
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Handoff

## Scope

- Prepare a portable continuation packet or resume from one. A progress update alone
  does not need a handoff.
- Carry decision-relevant context, including details unavailable from files. Do not
  assume the receiver can access earlier messages, tools, attachments, or local paths.
- Preparing a packet does not authorize sending it, starting agents, publishing,
  committing, or changing the task. Use existing authorization for any delivery.

## Prepare

1. Identify the active objective and latest accepted user instructions. Preserve
   scope, success criteria, permissions, and constraints with their applicable scope.
   Express selected decisions positively; include rationale needed to avoid rework.
   Leave superseded proposals out of active context.
2. Check only facts that affect resumption. Reuse fresh evidence and use bounded,
   targeted inspection for volatile state. Separate observed facts, assumptions,
   pending checks, and unresolved questions.
3. Write the packet below in English. Use an inline packet unless a file or delivery
   target was requested. Include exact paths/refs and essential commands; link bulky
   evidence with a reason to read it. Omit empty fields.
4. Check portability: identify which files, artifacts, and services the receiver can
   access. Uncommitted work needs a shared worktree or an accessible patch/file
   snapshot; commit IDs alone do not carry it. Include essential unavailable context
   directly, or mark the missing dependency and how to obtain it. Exclude credentials.
5. Read the packet as the receiver: can they locate the work, preserve it, distinguish
   verified from pending results, and take the next action without prior chat?
   Fix gaps before delivery. Report the packet location and any transfer gaps.

## Continuation packet

- **Goal:** requested outcome, success criteria, current scope.
- **Decisions and constraints:** current user choices and necessary rationale;
  authorized actions and approvals still required; unresolved questions labeled.
- **State:** completed, in progress, pending, blocked; relevant changes and ownership.
- **Workspace:** repository/location, branch and HEAD, committed and uncommitted work,
  staged state, unrelated user changes to preserve. Include only applicable fields.
- **Evidence:** checks already run, command/scope, result, tested revision or snapshot;
  failures, skipped checks, and remaining validation. Planned is not passed.
- **Resume inputs:** essential paths/artifacts with purpose; environment/tool versions,
  setup commands, access limits, and active jobs with status/check method if relevant.
- **Next action:** first concrete step, remaining order, and any condition requiring
  user input. Include a short request telling the receiver to resume this task.

## Resume

1. Read the packet and applicable destination instructions. Confirm workspace/ref,
   available artifacts, dirty/staged work, and any active jobs with targeted checks.
   Process IDs and local paths may belong to the source machine.
2. Compare actual state with the snapshot. Resolve material conflicts with current
   instructions or changes before affected edits. Request only missing information
   that blocks progress; continue independent work where possible.
3. Continue from the recorded next action within current authorization. Reuse valid
   evidence; rerun checks when the tested state or environment changed. Confirm the
   outcome of pending external actions before retrying them.
4. Preserve existing work and update the packet when handing off again. If context
   remains inaccessible, name the gap instead of claiming a complete transfer.

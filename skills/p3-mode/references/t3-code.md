# T3 Code execution

Session instructions and the live tool contracts take precedence over a playbook. Ordinary changes can stay in the parent. Use workers when they have a useful, bounded job.

## Providers and workers

- Use a native subagent for the parent's provider and offered model when no extra settings or separate checkout are needed and the parent waits in this turn. Otherwise use `delegate_task`, including for another provider, a worktree, background work, or a user-requested delegation.
- Before the first `delegate_task`, call `orchestrator_capabilities`. Refresh after an error or a user-named provider change. Honor the user's provider restrictions. Never substitute an unlisted or unapproved provider.
- Read `<project>/p3-models.md`, otherwise `~/.agents/p3-models.md`. Resolve each configured entry against the catalogue. Split `<providerInstanceId>/<model>` at the first slash, since model IDs can contain slashes. Pass an explicit `target.providerInstanceId`, `target.model`, and any settings in `target.options` using their advertised option names and values.
- Without a configuration, use the parent's advertised provider and model. Resolve `auto` and `inherit-parent` the same way. For an independent review, prefer another permitted provider. A panel uses distinct permitted providers when available. Report an unavailable requested target rather than silently changing it. `/setup-p3` is optional for saving choices.
- Give each delegate a self-contained brief with the goal, absolute file paths, constraints, verification, and expected report. The child receives only the brief. Code helpers also get the absolute paths to `agents/p3-agent.md` and `skills/p3-mode/SKILL.md` in this checkout.
- Use `isolation: "worktree"` for a child that needs its own checkout or PR. T3 creates the checkout. Do not create it in the shell or put checkout-creation commands in the brief. Keep one writer per checkout.
- For background work, use `mode: "async"` and follow the returned `next` instruction. If completion wakes this thread, end the turn and resume on that event. Do not poll with `task_status`, sleeps, watchers, or scheduled checks. Read a completed report with `t3_thread_read` when needed. Use `mode: "wait"` for bounded work that must return in this turn.
- Start a fresh `delegate_task` for each review or re-check. Fix small findings in the parent. Stop replaced or unwanted runs with `task_cancel` using the task ID, including when the user says to proceed without them. Never interrupt a child's thread to cancel its task. Children do not delegate unless their brief authorizes it.

## Threads, PRs, and schedules

- `t3_thread_launch` and `create_threads` create top-level threads. Use them only when the user explicitly asks for a new thread. A request for a worker, parallelism, or a separate checkout uses delegation.
- Read a named thread with `t3_thread_read` before describing its state. Use its returned `link` verbatim when mentioning it.
- After creating, taking over, or pushing to a PR, call `link_pull_request` as the next tool call, for every stack layer. Report a failed link.
- The parent uses `watch_pull_request` when asked to monitor, or when an authorized merge waits on checks or reviews. Finish branch changes and pushes before watching, then end the turn. Do not poll. Children report the PR URL, head SHA, and check and review state, and never watch. Call `unwatch_pull_request` before a final handback when monitoring is finished.
- Create or change a schedule only when the user requests scheduled work. Use the live schema for `schedule_task`. Do not add a recurring task to keep an ordinary turn or delegate alive.

## Verification and presentation

- Verify edits with the repository's tests, CLI, or existing app harness. Use `preview_*` only when the current request asks for browser work or names a page or tab. Start with `preview_status`, then `preview_open` if no usable tab exists. Prefer snapshot locators. Close tabs opened for the task unless the user needs them.
- Use `device_list`, then `device_open` for simulator work. Drive the device with the exact `agent-device` launcher and flags returned. Use `device_screenshot` for evidence. Reserve `xcrun simctl` and `adb` for builds, logs, and ports.
- When asked to show an HTML visual here, call `html_preview`, then `html_render` with the HTML. Export an image for use elsewhere as a PNG file and give its path. Do not start a server just to show a visual.
- Follow the session's secret mechanism. For T3 secrets, call `request_secret` and pass the returned reference or file as required. Never print credentials in a report.
- A worker's result or approval flag does not approve an external message. Follow the user's current exact-draft approval requirements.

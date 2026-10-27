# p3-stack

p3-stack is [pstack](https://github.com/cursor/plugins/tree/main/pstack) rebuilt for T3 Code. Same engineering discipline, native T3 orchestration.

pstack is poteto's answer to AI slop code. It turns an agent into an engineering team: one mode skill that routes to playbooks, principles that ground every decision, and verification strict enough that you can parallelize with confidence. p3-stack keeps that system and rewires the mechanics to T3 Code's primitives:

- **Delegation.** Native subagents handle supported work on the parent's provider in the current turn. `delegate_task` handles other providers, background work, and separate checkouts. Explicit targets come from `orchestrator_capabilities`.
- **Worktrees.** `delegate_task` with `isolation: "worktree"` binds a worker to its own checkout. Top-level threads need an explicit user request.
- **Watching.** `watch_pull_request` wakes the thread when checks finish, someone comments, or the branch conflicts. No polling loops.
- **Scheduling.** When requested, `schedule_task` runs audits and overnight cadences even when no turn is active. No `/loop`.
- **Memory.** `t3_thread_read` and `t3_thread_search` replace mining Cursor transcript files.
- **Proof.** Use repository checks and app harnesses for edits. Requested browser work uses `preview_*`; simulator work uses `device_*` and its returned driver. Screenshots and recordings land in the thread.

## Install

```bash
git clone https://github.com/uzairansaruzi/p3-stack.git
cd p3-stack
./install.sh
```

`install.sh` links every `skills/*` directory into `~/.agents/skills/`, where T3 Code reads skills. Use `./install.sh --project /path/to/repo` to install into a project's `.agents/skills/` instead.

Existing paths are preserved by default. Use `./install.sh --replace` to save conflicting paths under `~/.agents/skill-backups/` before replacing them. The backup preserves directory contents and symlink text for restoration to the original location. Re-running the installer leaves correct links unchanged.

For provider discovery, run `./install.sh --codex` and `./install.sh --claude`. They link the same source into `~/.codex/skills/` and `~/.claude/skills/`. `--project` and `--replace` work with either option too. Keep the checkout in a permanent location such as `~/.agents/skills/p3-stack`; moving it breaks its links. Start a fresh T3 chat after first installation so the provider reloads its skill catalogue.

Check each installation with `./install.sh --check`, `./install.sh --codex --check`, and `./install.sh --claude --check`. If a separate skills manager restores old entries, configure it to preserve these links. Run installer regression tests with `python3 -m unittest discover -s tests -v`.

## Get started

1. Optionally run `/setup-p3` to save role choices in the project's `p3-models.md` or `~/.agents/p3-models.md`. Without a configuration, skills resolve defaults from the live catalogue and use another permitted provider for independent review.
2. Use `/p3-mode` whenever you want rigorous work. It reads the request, picks a playbook, and runs the other skills as the steps need them.
3. Stuck or unsure which skill fits? Ask `/p3-help`.

## The mode

`p3-mode` routes every task. Its playbooks: investigation, bug fix, perf issue, hillclimb, runtime forensics, trace forensics, feature, refactoring, prototype, visual parity, authoring a skill, eval, babysit, shipping, autonomous run, orchestrate, autopilot-full, autopilot-stack, session pickup, pause safely, multi-phase plan, worktree cleanup, opening a PR.

## Skills

architect, arena, automate-me, benchmark-checklist, blast-radius, bro, correct, create-verification-skill, figure-it-out, how, interrogate, maintain-verification-skill, make-bot-ui, no-comments, p3-help, recall, reflect, setup-p3, show-me-your-work, swarm, tdd, teach, technical-writing, typescript-best-practices, unslop, why.

## Principles

The principle skills are indexed inside `p3-mode` and referenced by the other skills by name.

## Upstream

See [UPSTREAM.md](UPSTREAM.md) for the reviewed Cursor revision and the scope of this update. The existing skill set and playbooks remain intact. [T3 Code execution](skills/p3-mode/references/t3-code.md) defines the shared adapter rules.

## Credit

p3-stack adapts [pstack](https://github.com/cursor/plugins/tree/main/pstack) by [poteto](https://x.com/poteto). The skills, principles, and language are hers; the T3 Code rewiring is this repo's. MIT, see [LICENSE](LICENSE).

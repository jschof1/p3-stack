---
name: setup-p3
description: Configure which models p3-stack uses per role and at what reasoning budget. Detects your available models and writes p3-models.md, which overrides the skill defaults. Use for /setup-p3, "configure p3 models", "p3 budget", or changing p3-stack's model choices.
disable-model-invocation: true
---

# Setup p3

Follow [T3 Code execution](../p3-mode/references/t3-code.md) for tool routing, targets, and completion handling.

Write `p3-models.md`, a file that sets p3-stack's model per role. Default location is the current project root. Offer `~/.agents/p3-models.md` as the global option, and ask which one. A project file wins over the global one.

## Steps

### 1. Detect available models

Call `orchestrator_capabilities`. Use only permitted providers with `canRunChildTask: true` and their advertised models and options. Exclude disabled providers and honor the user's provider restrictions. If no permitted provider is available, stop and report it. `inherit-parent` is a configuration alias for the parent's advertised provider and model.

### 2. Load current state

The roles are the labels shown in step 5. If `p3-models.md` already exists at the chosen location, read it and treat its `# budget` line and its role values as the current choices. Otherwise start from the defaults in step 3(b). A line whose role is not in step 5, such as `how critics`, is from a retired role. Drop it.

### 3. Budget, map, and confirm

**(a) Ask for a budget.** Ask plainly in the thread. Offer these four options with these exact labels, and name the current budget when the file records one.

- `unlimited` (highest available reasoning)
- `large` (`xhigh` reasoning)
- `medium` (`high` reasoning)
- `small` (`medium` reasoning)

**(b) Apply it.** Build the working table. On a fresh run, give code roles (`feature, refactoring`, `bug-fix`, `perf-issue`, `hillclimb`) and the explorer, investigator, and swarm roles the fastest strong coding model detected. Give `judgment and prose`, `hardest tasks`, the explainer, the synthesizers, and `reflect tooling` the most capable model detected. Fill each panel role with one entry per distinct provider detected, up to three. On a re-run, keep any role the user changed.

Use the advertised effort option key, such as `reasoningEffort`, `effort`, or `variant`, and an advertised value. `unlimited` uses the highest supported effort. The other budgets target `xhigh`, `high`, or `medium`. The common ladder is `ultra` > `max` > `xhigh` > `high` > `medium` > `low` > `none`. If the target is missing, use the highest advertised common value at or below it. Do not guess the order of provider-specific values. Mark an unclear choice for the user. Preserve unrelated options. `inherit-parent` keeps the parent's options. Without an effort option, save the model and budget without inventing one.

**(c) Show the roles and confirm.** Show every role with its provider, model, and options. Mark unavailable entries and list retired roles. Ask whether to accept or change specific roles, offering detected models and `inherit-parent`. Resolve that alias to an explicit target at dispatch. For panel roles, one worker runs per entry, so list length sets the count. `arena cross-judge pool` is also a list, but Arena selects one entry whose provider differs from the parent's when possible. `swarm workers` is the default for each worker unless a race assigns a model per arm.

### 4. Validate

Every real entry and option must be advertised under its provider. Resolve `inherit-parent` against the current parent fields. If a requested entry is unavailable, report it without substitution. Apply the user's stated fallback policy, or ask for the missing choice.

### 5. Write the file

Write `p3-models.md` with a `# budget` line and one line per role, using the labels below. Write entries as `<providerInstanceId>/<model>`, with named options such as `(reasoningEffort=high)` when configured. Split at the first slash when reading an entry. At dispatch, put settings in `target.options`, never at the call's top level. Preserve existing options on re-runs and replace retired role lines. Shape:

```
# p3 model configuration. One line per role. Delete a line to use the session default.
# `inherit-parent` resolves to the parent's advertised provider, model, and options. Panel entries still count toward fan-out.
# budget: unlimited (max)
feature, refactoring: <providerInstanceId>/<model> (<option>=<value>)
bug-fix: <providerInstanceId>/<model> (<option>=<value>)
perf-issue: <providerInstanceId>/<model> (<option>=<value>)
hillclimb: <providerInstanceId>/<model> (<option>=<value>)
judgment and prose: <providerInstanceId>/<model> (<option>=<value>)
hardest tasks: <providerInstanceId>/<model> (<option>=<value>)
how explorer: <providerInstanceId>/<model> (<option>=<value>)
how explainer: <providerInstanceId>/<model> (<option>=<value>)
why investigators: <providerInstanceId>/<model> (<option>=<value>)
why synthesizer: <providerInstanceId>/<model> (<option>=<value>)
reflect tooling: <providerInstanceId>/<model> (<option>=<value>)
reflect judgment, divergent, synthesizer: <providerInstanceId>/<model> (<option>=<value>)
arena runners: <entry>, <entry>, <entry>
arena cross-judge pool: <entry>, <entry>, <entry>
swarm workers: <providerInstanceId>/<model> (<option>=<value>)
architect runners: <entry>, <entry>, <entry>
interrogate reviewers: <entry>, <entry>, <entry>
```

### 6. Confirm

Tell the user where the file was written. Read it on each invocation, so changes apply on the next run of a skill. Re-running setup updates it.

### 7. Offer a verification skill (optional)

Check whether the project has a way to drive the real app for proof (a `verify-*` skill, or an existing harness). If not, offer once: "want a project-local verification skill, so agents can drive the app the way a user does and prove changes work? I can generate one with /create-verification-skill." On yes, invoke `/create-verification-skill`. On no, move on without pushing.

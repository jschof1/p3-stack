# Upstream review

- P3 source: `uzairansaruzi/p3-stack`, commit `09909ebb5c0125e27fad3e57d96b81e832696d69`.
- Cursor source: `cursor/plugins`, commit `519d36aa98955bf680db01bcde5fdfba686dc901`, pstack `0.15.34`.
- Reviewed on 27 October 2026 against the existing P3 skills, references, and playbooks.

This is a focused compatibility update, not a full import of the current Cursor plugin. It retains P3's skill set, role names, and T3 workflows.

Imported the current debugging, premise-testing, and observable-test-behavior principles, plus the TypeScript branded-type guidance and example. Kept P3's existing playbook structure and prose where upstream differences were wording or Cursor mechanics.

Corrected T3 worker isolation, native versus delegated routing, explicit targets and options, completion handling, model defaults, thread creation, and verification boundaries. Fixed a broken architect reference. The installer now preserves conflicts, supports backups and Codex/Claude links, accepts earlier equivalent links, and checks the installed links.

New upstream workflows, including statechart compilation, formal verification, and recap media, remain outside this update. Importing them would expand the skill set and add toolchain requirements beyond the requested maintenance.

For the next update, compare the existing P3 paths with `pstack/skills/` at a pinned Cursor commit. Apply relevant behavior changes and translate tool mechanics through `skills/p3-mode/references/t3-code.md`. Validate metadata and relative links, run `python3 -m unittest discover -s tests -v`, then check all installed targets with `install.sh --check` and the corresponding provider option.

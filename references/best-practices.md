# Best Practices

## Frontmatter

- Require `name` and `description`.
- Allow the open-standard optional fields: `license`, `compatibility`, `metadata`, and experimental `allowed-tools`.
- Make the directory name match `name` exactly.
- Write `description` as both capability and activation guidance.
- Put environment requirements in `compatibility`, not in marketing prose.
- Treat product-specific keys as extensions and document their portability impact.

## SKILL.md body

- Use imperative, operational instructions.
- Start with the execution path rather than project history.
- Keep the main file under 500 lines when practical.
- Link directly to supporting files; avoid multi-hop reference chains.
- Include boundaries, failure handling, and final checks.
- Do not assume product-specific tools or interpolation syntax unless compatibility is intentionally limited.

## Resource choice

- Add `scripts/` when deterministic code prevents repeated or error-prone reimplementation.
- Add `references/` for detailed knowledge that should load only when needed.
- Add `assets/` for templates, starter files, schemas, and static output resources.
- Add `agents/openai.yaml` only as an optional OpenAI/Codex adapter.
- Remove placeholder resources before release.

## Repository versus package

Repository-only files include README, contribution guidance, CI, tests, docs, caches, and build output. Do not include them in the runtime archive unless the skill explicitly depends on them.

The distributable package should normally contain:

- `SKILL.md`
- license file
- `scripts/`
- `references/`
- `assets/`
- optional product adapters
- optional machine-readable metadata such as `skill.json`

## Security

- Treat third-party skills as untrusted code.
- Reject symlinks and archive path traversal.
- Inspect scripts, network calls, subprocesses, environment variables, and installers.
- Never bundle secrets or credentials.
- Prefer least privilege and explicit human approval for destructive or external actions.
- Report what was statically checked versus actually executed.

## Quality gate

- Triggering is specific enough to avoid false positives.
- Inputs, outputs, and non-goals are clear.
- The selected pattern matches the main failure mode.
- Every linked resource exists and stays inside the skill directory.
- Scripts parse and relevant tests pass.
- The package excludes repository-only material.
- Compatibility claims distinguish tested support from expected support.

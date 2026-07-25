---
name: nima-skill-creator
description: Create, review, refactor, validate, package, and install portable Agent Skills. Use when a user wants to turn a repeatable workflow into a SKILL.md package, improve an existing skill, add scripts/references/assets, audit compatibility across Codex, Claude Code, OpenCode, OpenClaw, WorkBuddy/CodeBuddy, or prepare a clean distributable archive.
license: MIT
compatibility: Generated skills follow the Agent Skills open specification. Bundled tooling requires Python 3.10 or newer.
metadata:
  author: NimaChu
  version: "2.0.0"
---

# Nima Skill Creator

Design skills as portable workflow packages, not product-specific prompt files.

## Operating principles

1. Start from concrete requests, expected outputs, and failure cases.
2. Use the Agent Skills open specification as the core contract.
3. Keep product-specific behavior in optional adapters or clearly marked extensions.
4. Put deterministic operations in `scripts/`, detailed knowledge in `references/`, and reusable output material in `assets/`.
5. Keep `SKILL.md` concise and link directly to supporting files.
6. Validate, test, and package before claiming the skill is complete.

## Workflow

### 1. Audit or discover

For an existing skill, read every file that can affect execution before proposing changes. For a new skill, collect only the missing information:

- 2–4 representative user requests
- required inputs and outputs
- trigger wording and non-trigger examples
- environment, tools, permissions, and safety boundaries
- reusable scripts, references, templates, or examples

Do not repeat questions the user has already answered. When the request is sufficiently concrete, summarize assumptions and proceed.

Use [interaction-guide.md](references/interaction-guide.md) for concise Chinese discovery prompts.

### 2. Choose a design pattern

Select the smallest useful combination from [design-patterns.md](references/design-patterns.md):

- `tool-wrapper` for domain or tool guidance
- `generator` for stable output shapes
- `reviewer` for criteria-driven evaluation
- `inversion` for requirement discovery before execution
- `pipeline` for ordered stages and gates

Use multiple patterns only when each controls a distinct failure mode.

### 3. Plan portable resources

Use [best-practices.md](references/best-practices.md) and [compatibility.md](references/compatibility.md).

- Core: `SKILL.md`, plus optional `scripts/`, `references/`, and `assets/`
- OpenAI/Codex presentation metadata: optional `agents/openai.yaml`
- Product-specific frontmatter: add only when requested and document the portability impact
- Repository files such as `README.md`, tests, CI, and contribution docs must remain outside the distributable skill package

### 4. Implement

Create a portable skill without product adapters:

```bash
python3 scripts/init_skill.py my-skill \
  --path /path/to/skills \
  --description "What the skill does and when to use it" \
  --resources scripts,references,assets
```

Add the optional OpenAI adapter only when needed:

```bash
python3 scripts/init_skill.py my-skill \
  --path /path/to/skills \
  --adapter openai \
  --interface display_name="My Skill" \
  --interface short_description="Create and improve My Skill workflows"
```

When updating an existing skill, make the minimum coherent set of changes and preserve product extensions that are intentional.

### 5. Validate and test

```bash
python3 scripts/validate_skill.py /path/to/skill
```

Use `--strict` when the target accepts only open-standard frontmatter fields. Run bundled tests or scripts and report failures honestly.

### 6. Package or install

Create a clean archive that excludes repository-only files:

```bash
python3 scripts/package_skill.py /path/to/skill ./dist
```

Install a directory or archive:

```bash
python3 scripts/install_skill.py ./dist/my-skill.skill.zip --target claude-code
python3 scripts/install_skill.py ./my-skill --target opencode --scope project --project-root /path/to/repo
```

Supported installer targets are documented in [compatibility.md](references/compatibility.md).

## Review gate

Before completion, verify:

- directory name matches frontmatter `name`
- `description` states both capability and trigger scenarios
- optional standard fields are valid and product extensions are intentional
- linked files exist and do not escape the skill directory
- scripts parse and were executed when execution is material to correctness
- no secrets, credentials, symlinks, generated caches, or repository-only files enter the package
- installation instructions match the selected product and scope

## Response format

Report:

1. task and compatibility summary
2. findings ordered by severity
3. files created or changed
4. commands and test results
5. remaining product-specific limitations

Use [output-patterns.md](references/output-patterns.md) for compact report shapes.

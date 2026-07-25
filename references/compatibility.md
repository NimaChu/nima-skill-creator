# Cross-Agent Compatibility

Use the Agent Skills open specification as the portable core. Product-specific fields and install locations are adapters, not the source of truth.

## Portable core

A portable skill contains:

```text
skill-name/
├── SKILL.md
├── scripts/       # optional
├── references/    # optional
├── assets/        # optional
└── agents/        # optional product adapters
```

Open-standard frontmatter fields:

- `name` — required, 1–64 characters, lowercase letters/digits/single hyphens
- `description` — required, 1–1024 characters, capability plus trigger scenarios
- `license` — optional
- `compatibility` — optional, up to 500 characters
- `metadata` — optional string-to-string map
- `allowed-tools` — optional and experimental; support varies

Source: [Agent Skills specification](https://agentskills.io/specification).

## Product matrix

### Codex / OpenAI

- OpenAI Skills follow the Agent Skills open standard and can be moved between supported products.
- The common local user directory is `${CODEX_HOME:-~/.codex}/skills`.
- Use `agents/openai.yaml` only for OpenAI presentation metadata; do not put core workflow logic there.
- Project-scoped portable installation defaults to `.agents/skills` in this tool.

Sources:

- [OpenAI: Skills in ChatGPT](https://help.openai.com/en/articles/20001066)
- [OpenAI Academy: Using skills](https://openai.com/academy/skills/)

### Claude Code

- User skills: `~/.claude/skills/<name>/SKILL.md`
- Project skills: `.claude/skills/<name>/SKILL.md`
- Claude Code follows the open standard and adds fields such as invocation controls, subagent context, and arguments.
- Those extra fields may be ignored by other clients. Keep them only when the behavior is intentionally Claude-specific.

Source: [Claude Code skills documentation](https://code.claude.com/docs/en/slash-commands).

### OpenCode

OpenCode discovers:

- `.opencode/skills/<name>/SKILL.md`
- `~/.config/opencode/skills/<name>/SKILL.md`
- `.claude/skills/` and `~/.claude/skills/`
- `.agents/skills/` and `~/.agents/skills/`

OpenCode recognizes the open-standard fields `name`, `description`, `license`, `compatibility`, and `metadata`; unknown fields are ignored.

Source: [OpenCode Agent Skills](https://opencode.ai/docs/skills).

### OpenClaw

OpenClaw follows the Agent Skills specification and loads skills in this precedence order:

1. `<workspace>/skills`
2. `<workspace>/.agents/skills`
3. `~/.agents/skills`
4. `~/.openclaw/skills`
5. bundled and extra directories

OpenClaw supports product-specific `metadata.openclaw` gating. Treat it as an optional extension and document required binaries, environment variables, operating systems, and installers.

Source: [OpenClaw skills documentation](https://github.com/openclaw/openclaw/blob/main/docs/tools/skills.md).

### WorkBuddy / CodeBuddy

- Project skills: `.codebuddy/skills/<name>/SKILL.md`
- WorkBuddy can import local skill packages through its Skills management UI.
- A commonly used user-level location is `~/.workbuddy/skills`; verify it against the installed client version when direct filesystem installation is required.
- The portable structure is `SKILL.md` plus optional `scripts/`, `references/`, and `assets/`.

Sources:

- [Tencent Cloud: WorkBuddy Enterprise Skills](https://cloud.tencent.com/document/product/1831/134516)
- [CodeBuddy: Skills](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)

## Portability rules

1. Keep required workflow behavior in `SKILL.md` and portable resources.
2. Do not rely on a product-specific field without a fallback instruction.
3. Use environment-neutral commands where possible; document required runtimes in `compatibility`.
4. Avoid hard-coded absolute paths. Resolve files relative to the skill directory or use the host product's supported skill-directory variable.
5. Do not assume every client supports dynamic command interpolation, pre-approved tools, subagents, or UI metadata.
6. Test on at least one open-standard path (`.agents/skills`) and each explicitly claimed product.
7. Mark compatibility as tested, expected, or unverified rather than claiming universal support without execution evidence.

## Installer target map

The bundled installer uses these defaults:

| Target | User scope | Project scope |
|---|---|---|
| `agent` | `~/.agents/skills` | `.agents/skills` |
| `codex` | `${CODEX_HOME:-~/.codex}/skills` | `.agents/skills` |
| `claude-code` | `~/.claude/skills` | `.claude/skills` |
| `opencode` | `~/.config/opencode/skills` | `.opencode/skills` |
| `openclaw` | `~/.openclaw/skills` | `skills` |
| `workbuddy` | `~/.workbuddy/skills` | `.codebuddy/skills` |

Use `--destination` when a managed installation, enterprise policy, custom profile, or client version uses another location.

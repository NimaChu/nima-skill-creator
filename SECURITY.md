# Security Policy

Agent Skills can contain executable scripts, external commands, network access instructions, and product-specific installation metadata. Treat every third-party skill as untrusted until reviewed.

## Reporting a vulnerability

Use GitHub's private security advisory feature for vulnerabilities that could expose credentials, execute unintended commands, bypass validation, escape the skill directory, or create unsafe archives. Do not publish secrets, exploit payloads, or sensitive system details in a public issue.

For non-sensitive hardening suggestions, open a normal GitHub issue with a minimal reproducible example.

## Supported version

Security fixes are applied to the latest version on the `main` branch.

## Scope

Relevant reports include:

- archive path traversal or unsafe extraction
- symlink-based package or install escapes
- command injection in bundled tooling
- validation bypasses that admit malformed or unsafe skill packages
- accidental inclusion of credentials or repository-only files
- unsafe default permissions or destructive installation behavior

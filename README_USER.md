# Nima Skill Creator - User Guide

## Overview

This project provides a framework for creating Claude skills with a hybrid approach:

- **Interactive Phase**: Chinese guidance for user requirement discovery
- **Technical Phase**: English documentation and implementation standards

## Quick Start

1. **Start Interactive Discovery**: Use the interactive workflow from `SKILL.md`
2. **Review Technical Specifications**: See `references/` for documentation
3. **Implement**: Use scripts from `scripts/` and templates from `assets/`
4. **Validate & Package**: Run validation and packaging scripts

## Project Structure

```
nima-skill-creator/
├── SKILL.md              # Main skill definition
├── PROJECT.md            # This file - project overview
├── scripts/              # Tools for skill creation
├── references/           # Technical documentation
├── assets/               # Templates and examples
└── README.md             # Basic overview
```

## Interactive Workflow (Chinese)

The interactive workflow guides you through:

1. **Discovery Phase**: Requirements and I/O definition
2. **Blueprint Phase**: Architecture and resource planning
3. **Implementation Phase**: Coding and documentation
4. **Validation Phase**: Testing and iteration

## Technical Standards (English)

The technical documentation includes:

- **best-practices.md**: Naming conventions, patterns, quality checklist
- **workflows.md**: Multi-step process patterns
- **output-patterns.md**: Output format templates
- **interaction-guide.md**: Interactive design patterns

## Scripts

- **init_skill.py**: Initialize new skill project
- **validate_skill.py**: Validate skill structure
- **package_skill.py**: Package skill for distribution

## Templates

- **template-skill/**: Starter kit for new skills
- **examples/**: Real-world examples by domain

## For Users

When you want to create a new skill:

1. Review `SKILL.md` for the complete workflow
2. Start the interactive discovery (Chinese)
3. Review technical specifications as needed (English)
4. Use provided templates and examples
5. Validate and package your skill

## For Developers

When implementing the skill creator:

1. Implement interactive discovery questions
2. Generate technical blueprints
3. Execute initialization scripts
4. Guide users through implementation
5. Validate and package new skills

## License

MIT License - See LICENSE file for details

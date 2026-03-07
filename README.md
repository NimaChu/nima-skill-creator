# Nima Skill Creator

A hybrid approach to skill creation that combines interactive guided workflows with technical implementation guidance.

## Overview

This project provides a comprehensive skill creation framework that:

1. **Interactive Phase** (Chinese): Guides users through requirement discovery and architecture planning
2. **Technical Phase** (English): Provides implementation standards and best practices

## Architecture

```
nima-skill-creator/
├── SKILL.md              # Hybrid guide (Chinese + English)
├── scripts/              # Initialization and validation tools
├── references/           # Technical specifications and templates
└── assets/               # Templates and examples
```

## Core Principles

### Dual-Language Design
- **User Interaction**: Chinese (老板视角)
- **Documentation**: English (技术标准)

### Progressive Disclosure
1. Interactive discovery → Minimal context overhead
2. Technical guidance → Loaded only when needed

## Workflow

### Phase 1: 需求挖掘 (Interactive)
- Input: User requirements
- Output: Technical specification document

### Phase 2: 架构设计 (Blueprint)
- Input: Specification document
- Output: Directory structure and resource plan

### Phase 3: 实现 (Implementation)
- Input: Blueprint
- Output: Validated skill package

## Project Structure

### scripts/
- `init_skill.py` - Initialize new skill project
- `validate_skill.py` - Validate skill structure
- `package_skill.py` - Package skill for distribution

### references/
- `best-practices.md` - Naming conventions, anti-patterns
- `workflows.md` - Multi-step process patterns
- `output-patterns.md` - Template and example patterns

### assets/
- `template-skill/` - Starter kit for new skills
- `examples/` - Real-world examples by domain

## Getting Started

1. Start the interactive guided workflow (Chinese)
2. Review the technical specification (English)
3. Implement using provided scripts and templates
4. Validate and package

## For AI Agents

When this skill is triggered, the AI should:

1. Present the interactive discovery questions (Chinese)
2. Generate the technical blueprint (English)
3. Execute initialization scripts
4. Guide implementation with referenced best practices

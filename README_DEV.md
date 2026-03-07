# Nima Skill Creator - 技术开发者指南

## 项目概述 (Project Overview)

`nima-skill-creator` 是一个混合式 skill 创建框架，结合了：

- **交互式引导**：中文用户需求挖掘
- **技术实现**：英文标准文档和代码规范

## 为什么需要这个项目 (Why This Project)

### 现有问题 (Current Issues)

1. **skill-creator (全局)**：纯英文技术文档，缺乏用户引导
2. **qiuzhi-skill-creator (本地)**：纯中文交互流程，缺少技术标准

### 解决方案 (Solution)

`nima-skill-creator` 整合两者优势：
- 中文交互引导老板视角
- 英文技术标准 (全球通用)

## 项目结构 (Project Structure)

```
nima-skill-creator/
├── SKILL.md              # 主 Skill 定义 (混合中文+英文)
├── PROJECT.md            # 项目概述
├── README.md             # 基本概述
├── README_USER.md        # 用户指南
├── README_DEV.md         # 本文档 - 技术开发者指南
├── scripts/              # 工具脚本
│   ├── init_skill.py
│   ├── validate_skill.py
│   └── package_skill.py
├── references/           # 技术文档
│   ├── best-practices.md
│   ├── workflows.md
│   ├── output-patterns.md
│   └── interaction-guide.md
├── assets/               # 模板和示例
│   ├── template-skill/
│   └── examples/
└── .gitignore
```

## 工作流程 (Workflow)

### 阶段 1: 需求挖掘 (Discovery) - 中文

```
用户输入 → 交互式提问 → 技术规范输出
```

关键问题:
- Claude 应该**输入**什么？
- Claude 应该**输出**什么？
- 用户会**怎么说**来触发 Skill？

### 阶段 2: 架构蓝图 (Blueprint) - 英文

```
Specification → Directory structure → Resource plan
```

Output:
- Directory structure (scripts/, references/, assets/)
- Resource checklist
- Workflow logic

### 阶段 3: 实现 (Implementation) - 混合

```
Blueprint → Code/Docs → Validation → Package
```

### 阶段 4: 测试与迭代 (Validation & Iteration) - 混合

```
Test cases → User feedback → Iterate → Final skill
```

## 核心原则 (Core Principles)

### 1. 双语分离 (Dual-Language Separation)

- **交互阶段**: 中文 (老板视角)
- **技术阶段**: 英文 (全球标准)

### 2. 渐进式披露 (Progressive Disclosure)

```
Level 1: 元数据 (name + description) - 始终在上下文
  ↓
Level 2: SKILL.md body - 触发时加载 (<5k words)
  ↓
Level 3: Bundled resources - 按需加载 (无限制)
```

### 3. 自由度匹配 (Freedom Matching)

| 自由度 | 使用场景 | 示例 |
|--------|----------|------|
| 高 | 多种方法都可行 | 代码审查流程 |
| 中 | 有首选模式但允许变化 | 带参数的脚本 |
| 低 | 操作脆弱、一致性关键 | 数据库迁移 |

## 技术实现 (Technical Implementation)

### 脚本工具 (Scripts)

#### init_skill.py
```python
# Initialize new skill project
# Usage: python init_skill.py <skill-name> --path <output-directory>
```

功能:
- 创建目录结构
- 生成 SKILL.md 模板
- 可选创建资源目录 (scripts/, references/, assets/)

#### validate_skill.py
```python
# Validate skill structure
# Usage: python validate_skill.py <path/to/skill-folder>
```

验证:
- YAML frontmatter 格式
- 命名规范
- 文件组织

#### package_skill.py
```python
# Package skill for distribution
# Usage: python package_skill.py <path/to/skill-folder>
```

功能:
- 验证 skill
- 创建 .skill 文件 (zip 格式)

### 技术文档 (References)

#### best-practices.md
- 命名规范 (Naming Conventions)
- Description 编写指南
- 简洁原则 (Conciseness)
- 自由度匹配 (Freedom Matching)
- 渐进式披露 (Progressive Disclosure)
- 反模式 (Anti-Patterns)
- 质量检查清单 (Quality Checklist)

#### workflows.md
- 多步骤流程设计 (Multi-Step Workflow Design)
- 条件逻辑 (Conditional Logic)
- 用户确认点 (User Confirmation Points)
- 常见模式 (Common Patterns)
- 错误处理 (Error Handling)

#### output-patterns.md
- 常见输出格式模式
- 选择正确模式
- 一致性 (Consistency)
- 可读性 (Clarity)
- 可扫描性 (Scannability)

#### interaction-guide.md
- 交互模式 (Interaction Patterns)
- 中文优先 (Chinese First)
- 渐进式披露 (Progressive Disclosure)
- 最佳实践 (Best Practices)
- 常见问题模板 (Common Templates)

## 使用方法 (Usage)

### 对于用户 (For Users)

1. 阅读 `SKILL.md` 了解完整工作流
2. 开始交互式需求挖掘 (中文)
3. 根据需要查看技术文档 (英文)
4. 使用提供的模板和示例
5. 验证并打包 skill

### 对于 AI Agent

当这个 skill 被触发时，AI 应该：

1. 展示交互式需求挖掘问题 (中文) - see `references/interaction-guide.md`
2. 生成技术蓝图 (英文)
3. 执行初始化脚本 from `scripts/`
4. 使用 referenced best practices 指导实现
5. 用 `scripts/validate_skill.py` 验证
6. 用 `scripts/package_skill.py` 打包

## 最佳实践 (Best Practices)

### 编写 Documentation
- ✅ SKILL.md body: <500 lines, essentials only
- ✅ Detailed content: references/ files
- ✅ No deeply nested references: one level deep only
- ✅ Long files: include table of contents

### 交互设计
- ✅ 问题简短 (<20字)
- ✅ 选项互斥
- ✅ 包含"其他"选项
- ❌ 避免多重问题

### 命名规范
- ✅ lowercase-hyphen-case
- ✅ <64 characters
- ✅ verb-noun format
- ❌ CamelCase, snake_case, special characters

## 开发指南 (Development Guide)

### 添加新脚本
1. 创建 `scripts/*.py`
2. 添加使用说明
3. 测试功能
4. 更新文档

### 添加新引用
1. 创建 `references/*.md`
2. 包含清晰的标题和结构
3. 使用英文
4. 链接到 SKILL.md

### 添加新模板
1. 创建 `assets/template-name/`
2. 包含必要文件
3. 添加使用说明
4. 更新 examples

## 贡献指南 (Contribution Guide)

1. Fork 项目
2. 创建分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 许可证 (License)

MIT License - See LICENSE file for details

## 链接 (Links)

- [Global skill-creator](~/.npm-global/lib/node_modules/openclaw/skills/skill-creator/SKILL.md)
- [Local qiuzhi-skill-creator](~/.openclaw/workspace/subagents_workspace/develop/skills/qiuzhi-skill-creator/SKILL.md)
- [PROJECT.md](PROJECT.md) - Project overview
- [README_USER.md](README_USER.md) - User guide
- [SKILL.md](SKILL.md) - Main skill definition

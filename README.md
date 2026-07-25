# Nima Skill Creator

**把一项工作交给 Agent 描述清楚，它会帮你把这项工作做成可复用的 Skill。**

适用于 Codex、Claude Code、OpenCode、OpenClaw、WorkBuddy / CodeBuddy，以及其他支持 Agent Skills 的 AI 编程工具。

普通用户不需要理解目录结构，也不需要手动运行 Python 命令。把本仓库链接发给具备文件或终端操作能力的 Agent，让它完成安装、创建、验证和使用即可。

## 它能帮你做什么

- 把重复工作沉淀成可复用 Skill
- 根据真实工作案例设计稳定流程
- 创建 `SKILL.md`、参考资料、模板和辅助脚本
- 审核并改进已有 Skill
- 检查 Skill 的规范性、安全性和跨产品兼容性
- 将 Skill 安装到当前 Agent 产品支持的位置

## 30 秒开始使用

### 第一步：让 Agent 安装

在 Codex、Claude Code、OpenCode、OpenClaw 或 WorkBuddy 中打开一个对话，把下面这段话发给 Agent：

```text
请安装并启用这个 Skill：
https://github.com/NimaChu/nima-skill-creator

请先识别你当前运行的 Agent 产品及其支持的 Skill 目录，阅读仓库中的 SKILL.md 和 references/compatibility.md，然后完成安装和验证。

优先使用项目级安装，不要覆盖已有文件；如发现冲突、权限风险或不确定的安装位置，先向我说明。安装完成后告诉我如何触发和使用它。
```

Agent 会根据当前产品选择合适的安装方式。部分客户端可能需要重新加载项目、重启会话，或通过界面导入 Skill。

### 第二步：直接描述你想做的工作

安装后，可以直接这样说：

```text
请使用 nima-skill-creator，帮我把下面这项工作做成一个可复用 Skill：

[描述你的工作、输入、输出和当前做法]
```

Agent 会先补齐必要信息，再完成设计、创建和验证。

## 常用对话示例

### 创建一个新 Skill

```text
请使用 nima-skill-creator，把“每周经营数据分析”做成一个 Skill。

输入是 Excel 数据和本周业务背景，输出需要包括指标变化、异常原因、风险和下周建议。请先询问我缺少的信息，再创建并验证 Skill。
```

### 改进已有 Skill

```text
请使用 nima-skill-creator 审核当前项目中的 Skill。
重点检查触发条件是否准确、流程是否可执行、引用文件是否合理，以及能否兼容 Codex、Claude Code 和 OpenCode。发现问题后直接修改并验证。
```

### 把资深员工的工作沉淀下来

```text
请使用 nima-skill-creator，通过渐进式提问了解我完成这项工作的真实步骤、判断标准、输入资料、常见异常和最终交付物，然后把它做成一个可复用 Skill。
```

### 检查第三方 Skill

```text
请使用 nima-skill-creator 审核这个第三方 Skill。
检查其中的脚本、外部命令、网络请求、权限要求、引用文件和产品专属配置，并告诉我是否适合安装。
```

## Agent 会怎样工作

通常会经过以下过程：

1. **理解工作**：确认输入、输出、触发方式和质量标准
2. **选择结构**：判断需要流程、模板、检查清单、参考资料还是脚本
3. **创建或改造**：生成最小且完整的 Skill 文件
4. **验证结果**：检查规范、引用、脚本语法、安全问题和兼容性
5. **交付说明**：告诉你创建了什么、如何触发、如何继续迭代

如果需求已经足够清楚，Agent 应直接开始，不会为了走流程而重复提问。

## 提供这些信息，效果会更好

不需要写专业需求文档。尽量告诉 Agent：

- 2～4 个真实的使用请求
- 工作需要接收什么输入
- 最终应该产出什么
- 判断结果好坏的标准
- 当前已有的模板、文件或脚本
- 最容易出错或需要人工确认的地方
- 希望在哪些 Agent 产品中使用

## 最终会得到什么

一个典型 Skill 可能包括：

```text
my-skill/
├── SKILL.md          # Agent 的主要工作说明
├── references/       # 按需读取的知识、规则和检查清单
├── assets/           # 模板、示例或输出素材
├── scripts/          # 需要稳定执行的辅助工具
└── agents/           # 可选的产品适配信息
```

并不是每个 Skill 都需要全部目录。Nima Skill Creator 会优先创建最小、清晰、可维护的结构。

## 兼容产品

| 产品 | 支持情况 |
|---|---|
| Codex | 支持，可使用 OpenAI 展示适配信息 |
| Claude Code | 支持原生 Skills 工作流 |
| OpenCode | 支持项目级和用户级 Skills |
| OpenClaw | 支持原生 Skills 与通用 Agent Skills |
| WorkBuddy / CodeBuddy | 支持项目 Skill 或客户端导入 |
| 其他 Agent Skills 工具 | 使用开放核心格式，通常可直接适配 |

不同产品的目录、权限和刷新方式可能不同。普通用户无需手动处理这些差异，让 Agent 阅读 [`references/compatibility.md`](references/compatibility.md) 后执行即可。

## 使用建议与安全

- 第一次安装第三方 Skill 时，优先让 Agent 安装到当前项目
- 让 Agent 在覆盖已有 Skill 前先展示差异
- 不要把密钥、密码或生产凭据写进 Skill 文件
- 安装包含脚本的 Skill 前，应让 Agent检查脚本和外部命令
- Skill 创建完成后，用几个真实任务测试并继续改进

## 给维护者和高级用户

仓库内保留了初始化、验证、打包和安装工具，供 Agent 自动调用，也可用于 CI 或批量管理。普通用户不需要手动执行这些工具。

- Skill 主体：[`SKILL.md`](SKILL.md)
- 兼容性说明：[`references/compatibility.md`](references/compatibility.md)
- 设计方法：[`references/design-patterns.md`](references/design-patterns.md)
- 最佳实践：[`references/best-practices.md`](references/best-practices.md)
- 安全说明：[`SECURITY.md`](SECURITY.md)

## License

MIT

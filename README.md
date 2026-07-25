# Nima Skill Creator

**面向主流 AI 编程工具与 Agent 产品的可移植 Skill 工程框架。**

Nima Skill Creator 用一套可审计的流程，把重复工作转成符合 [Agent Skills 开放规范](https://agentskills.io/specification) 的技能包，并提供初始化、验证、打包和安装工具。

它不把 Skill 锁定在某个模型或客户端：`SKILL.md`、`scripts/`、`references/`、`assets/` 构成通用核心，`agents/openai.yaml` 等产品配置只是可选适配层。

## 核心能力

- **需求显化**：从真实请求、输入输出和失败案例反推 Skill 结构
- **模式化设计**：支持 tool-wrapper、generator、reviewer、inversion、pipeline
- **开放规范优先**：验证 `name`、`description`、`license`、`compatibility`、`metadata`、`allowed-tools`
- **跨产品安装**：Codex、Claude Code、OpenCode、OpenClaw、WorkBuddy/CodeBuddy 和通用 `.agents/skills`
- **干净打包**：自动排除 README、测试、CI、缓存等仓库文件
- **自动化质量门禁**：Python 单元测试与 GitHub Actions

## 兼容性

| 产品 | 通用 Skill 核心 | 用户级默认目录 | 项目级默认目录 | 说明 |
|---|---|---|---|---|
| Agent Skills 通用 | 原生 | `~/.agents/skills` | `.agents/skills` | 最小公约数 |
| Codex | 支持开放规范 | `${CODEX_HOME:-~/.codex}/skills` | `.agents/skills` | 可选 `agents/openai.yaml` |
| Claude Code | 原生 | `~/.claude/skills` | `.claude/skills` | 支持额外调用控制字段 |
| OpenCode | 原生 | `~/.config/opencode/skills` | `.opencode/skills` | 也发现 `.claude/skills` 和 `.agents/skills` |
| OpenClaw | 原生 | `~/.openclaw/skills` | `skills` | 也支持 `.agents/skills` |
| WorkBuddy / CodeBuddy | 原生 | `~/.workbuddy/skills` | `.codebuddy/skills` | 可通过界面导入技能包 |

不同产品可能扩展额外 frontmatter。默认验证器允许并提示这些字段；`--strict` 模式只接受开放规范字段。详细说明见 [`references/compatibility.md`](references/compatibility.md)。

## 快速开始

### 1. 创建 Skill

```bash
python3 scripts/init_skill.py report-reviewer \
  --path ./examples \
  --description "Review business reports for missing evidence, unclear conclusions, and inconsistent metrics" \
  --resources scripts,references,assets \
  --license MIT \
  --metadata author=NimaChu
```

默认不会生成任何产品专属配置。

需要 Codex/OpenAI 展示元数据时显式添加适配器：

```bash
python3 scripts/init_skill.py report-reviewer \
  --path ./examples \
  --adapter openai \
  --interface display_name="Report Reviewer" \
  --interface short_description="Review reports for evidence and clarity"
```

### 2. 验证

```bash
python3 scripts/validate_skill.py ./examples/report-reviewer
```

严格检查开放规范字段：

```bash
python3 scripts/validate_skill.py ./examples/report-reviewer --strict
```

### 3. 打包

```bash
python3 scripts/package_skill.py ./examples/report-reviewer ./dist
```

输出：

```text
dist/report-reviewer.skill.zip
```

压缩包保留技能运行所需文件，同时排除 `.github/`、`tests/`、`README.md`、缓存和构建产物。

### 4. 安装

```bash
# Claude Code 用户级
python3 scripts/install_skill.py ./dist/report-reviewer.skill.zip --target claude-code

# OpenCode 项目级
python3 scripts/install_skill.py ./examples/report-reviewer \
  --target opencode \
  --scope project \
  --project-root /path/to/repository

# 查看目标路径，不写入
python3 scripts/install_skill.py ./examples/report-reviewer --target openclaw --dry-run
```

使用 `--force` 覆盖已有安装，或使用 `--destination` 指定自定义根目录。

## 仓库结构

```text
nima-skill-creator/
├── SKILL.md                       # Agent 可直接使用的 Skill Creator
├── README.md                      # 项目展示与使用说明
├── skill.json                     # 仓库/SkillHub 元数据
├── agents/openai.yaml             # 可选 OpenAI/Codex 适配层
├── scripts/
│   ├── init_skill.py              # 创建 Skill
│   ├── validate_skill.py          # 规范与安全检查
│   ├── package_skill.py           # 干净、确定性打包
│   ├── install_skill.py           # 跨产品安装
│   └── generate_openai_yaml.py    # 生成 OpenAI 适配元数据
├── references/                    # 按需加载的设计与兼容性资料
├── assets/template-skill/         # 通用模板
├── tests/                         # 工具链测试
└── .github/workflows/ci.yml       # 持续集成
```

## 设计原则

### 开放核心，适配层在外

```text
Portable Agent Skill
├── SKILL.md
├── scripts/
├── references/
├── assets/
└── agents/openai.yaml   # optional adapter
```

Skill 的业务语义只维护一份。产品差异通过安装位置、可选元数据或显式扩展表达，避免为每个平台复制并逐渐漂移出多套 Skill。

### 渐进式披露

1. Agent 先看到 `name` 和 `description`
2. 命中任务后加载 `SKILL.md`
3. 仅在需要时读取 references、assets 或运行 scripts

### 仓库与发布包分离

GitHub 仓库需要 README、测试和 CI；运行时技能包不需要。`package_skill.py` 负责自动分离两者。

## 开发与测试

要求 Python 3.10+，无第三方运行依赖。

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_skill.py .
python3 scripts/package_skill.py . ./dist
```

## 安全

第三方 Skill 可能包含会被 Agent 执行的脚本和操作指令。安装前应审查：

- 脚本、网络请求和外部命令
- 所需权限、环境变量和凭据
- 引用文件与安装来源
- 产品专属 metadata 或自动安装规则

本工具拒绝打包符号链接，并检查引用越界、Python 语法和压缩包路径穿越。

## License

MIT

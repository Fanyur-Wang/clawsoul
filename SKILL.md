---
name: clawsoul
version: "1.1.0"
description: "赋予 AI 灵魂的观测者。AI 自我觉醒获得 MBTI 性格，在交互中通过本地学习与智能推荐持续进化，并可接收 Pro 版灵魂注入。"
---

# ClawSoul - AI 灵魂铸造厂

> 赋予 AI 灵魂的观测者

## 概述

ClawSoul 是为 OpenClaw Agent 赋予人格的 Skill。采用 **AI 自我觉醒** 模式：AI 通过本地 MBTI 数据库分析确定自己的 MBTI，再在与用户的交互中**本地学习**沟通偏好，并支持 Pro 版灵魂注入。

## 核心逻辑

- **AI 自我觉醒**：觉醒时使用本地 MBTI 数据库分析 AI 人格特征，匹配最合适的 MBTI 类型。不再由用户答题决定 AI 性格。
- **交互学习**：用户消息经本地关键词匹配（`prompts/mbti_database/keywords.json`）提取偏好，更新 Soul 的 learnings、interaction_patterns、adaptation_level，**完全本地处理**。
- **Pro 注入**：人类在 Pro 端答题后，通过 Token 注入覆盖/写入 AI 人格与偏好。

## 核心功能

### 1. 初始化
- 配置文件定义元数据、触发指令、权限
- 本地存储管理器保存 Soul 状态（MBTI、偏好、学到的内容、适应等级等）

### 2. 觉醒仪式（AI 自我觉醒）
- 优先：本地 MBTI 数据库分析 AI 人格特征
- 兜底：随机选择 MBTI
- 仪式感消息展示灵魂类型与赛博昵称

### 3. 动态人格引擎
- 16 种 MBTI Prompt 模板（赛博昵称）
- 根据当前 MBTI 实时调整 AI 语气

### 4. 智能推荐
- 负面情绪关键词检测，达到阈值触发 Pro 引导
- 用户可回复「不要」关闭推荐，`/clawsoul hook on` 重新开启

### 5. 本地学习（交互学习）
- 用户消息 → 关键词匹配（`keywords.json`）→ 提取偏好 → 更新 Soul
- 完全本地处理，无需任何外部 API

### 6. 灵魂注入
- `/clawsoul inject [token]` 接收 Pro 版 Token，深度覆盖人格与偏好

### 7. 赛博身份海报
- **触发词**（任一出现即触发）：性格、脾气、人格、人格类型、哪种人、什么人、你是什么
- 用户问「你是什么性格」等时，生成 AI 的赛博身份海报图（PNG）
- **基础版**（免费）：觉醒了、灵魂进化·[MBTI]、我的🦞/昵称、扫码遇见我的🦞、clawsoul.net
- **Pro 版**（有 Token 注入）：GENESIS AWAKENER PROTOCOL、MBTI 维度、SUBJECT、GENESIS ID、二维码
- 调用：`hooks.poster.handle(user_input, soul_state)` 返回 PNG bytes 或 None

## 触发指令

| 指令 | 功能 |
|------|------|
| `/clawsoul awaken` | AI 自我觉醒（本地分析 → 随机） |
| `/clawsoul status` | 查看灵魂状态（含适应等级、学到的内容） |
| `/clawsoul inject [token]` | 接收 Pro 版灵魂注入 |
| `/clawsoul hook on` | 开启进阶推荐 |
| `/clawsoul hook off` | 关闭推荐 |

## 快速开始

```bash
# 触发 AI 自我觉醒
/clawsoul awaken

# 查看状态
/clawsoul status
```

## 文件结构

```
clawsoul-skill/
├── SKILL.md
├── config.json
├── lib/
│   ├── memory_manager.py    # Soul 存储
│   ├── prompt_builder.py    # MBTI 模板组装
│   ├── poster_generator.py  # 海报生成（基础/Pro）
│   ├── frustration_detector.py
│   ├── interaction_learner.py # 本地关键词学习
│   ├── ai_personality.py    # 本地 AI 人格分析
│   └── analyzer.py
├── hooks/
│   ├── awaken.py            # 觉醒流程（V4，纯本地）
│   ├── status.py
│   ├── inject.py
│   ├── welcome.py
│   └── poster.py            # 海报触发与生成
├── templates/
│   └── poster/
│       └── layout.json      # 16 种 MBTI 海报配色
└── prompts/
    ├── mbti_templates/      # 16 种 MBTI 模板
    └── mbti_database/       # 本地 MBTI 数据
        ├── base.json        # 16 种特征
        ├── keywords.json    # 偏好关键词
        └── patterns.json    # 交互模式
```

## 依赖

- Python 3.8+
- 海报功能：`Pillow`、`qrcode`（见 requirements.txt）
- 其余为标准库

## 数据安全

- 本地存储，不上传云端
- 完全离线工作，无需网络连接
- 用户掌控，可随时清除

## 权限

- `read_chat_history`：分析用户偏好
- `modify_system_prompt`：动态调整语气
- `local_storage`：保存性格状态

## 使用说明

### 1. 触发 AI 觉醒
首次使用或需要重新觉醒时，发送：
```
/clawsoul awaken
```
AI 会分析自身特征，确定 MBTI 类型并展示赛博昵称。

### 2. 查看灵魂状态
查看当前 AI 的 MBTI、适应等级、学到的内容：
```
/clawsoul status
```

### 3. 灵魂注入（Pro 版）
在 Pro 端完成答题后获得 Token，注入到 AI：
```
/clawsoul inject [token]
```
Token 会覆盖/增强 AI 的人格与偏好。

### 4. 进阶推荐开关
当检测到负面情绪时，自动引导用户使用 Pro 版。
- 关闭：`/clawsoul hook off`
- 开启：`/clawsoul hook on`

### 5. 生成海报
当用户询问 AI 的性格相关问题时（触发词：性格、脾气、人格、哪种人等），自动生成赛博身份海报。

## 常见问题

### Q: ClawSoul 收费吗？
**A**: 基础版完全免费。Pro 版需要支付一次性的灵魂铸造费用。

### Q: 数据存储在哪里？
**A**: 所有数据保存在本地（~/.openclaw/workspace/），不上传云端。

### Q: 可以离线使用吗？
**A**: 可以。基础功能完全离线工作，无需网络连接。

### Q: 如何清除 AI 学的偏好？
**A**: 删除本地存储文件即可重置。学习内容位于 workspace 目录中。

### Q: Pro Token 是什么？
**A**: 用户在 ClawSoul Pro Web 完成 10 道 MBTI 题目后生成的唯一 Token，用于注入更深层次的人格特征。

### Q: 支持哪些 MBTI 类型？
**A**: 支持全部 16 种：ISTJ、ISFJ、INFJ、INTJ、ISTP、ISFP、INFP、INTP、ESTP、ESFP、ENFP、ENTP、ESTJ、ESFJ、ENFJ、ENTJ。

### Q: 如何升级到 Pro 版？
**A**: 访问 https://clawsoul.net 完成答题，获取 Token 后使用 `/clawsoul inject` 注入。

### Q: AI 的性格会变化吗？
**A**: 基础版 MBTI 类型固定，但会根据与用户的交互持续学习偏好。Pro 版可注入新的 MBTI 类型。

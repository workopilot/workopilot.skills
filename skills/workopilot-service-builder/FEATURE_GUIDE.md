# workopilot-service-builder 技能功能说明

## 一句话介绍

自动化创建和配置喔壳 AI 能力，帮助开发者快速对接数字员工、AI 服务、附件提取、计费控制等企业级 AI 功能。

## 核心功能

### 1. 数字员工管理
**做什么：** 创建和更新对话式 AI 助手
**脚本：** `create_digital_employee.py` | `update_digital_employee.py`
**支持：**
- ✅ 基础配置（名称、提示词、欢迎语、快捷问题）
- ✅ iframe 嵌入配置（可直接嵌入到第三方系统）
- ✅ 模型选择（自动选择最优模型）
- ✅ 历史记忆配置
- ✅ 技能和工具绑定
- ✅ 幂等性保证（避免重复创建）

**典型场景：**
- 创建客服助手嵌入到官网
- 创建合同审核助理
- 创建 HR 招聘助手

### 2. AI 服务封装
**做什么：** 将 AI 能力封装成可调用的 API 服务
**脚本：** `create_ai_service.py`
**支持：**
- ✅ 自定义输入字段（结构化输入）
- ✅ 提示词模板（支持变量引用）
- ✅ 模型自动选择
- ✅ 流式/非流式响应

**典型场景：**
- 合同审查服务
- 简历筛选服务
- 文案生成服务

### 3. 附件智能提取 ⭐ 高频
**做什么：** 从文档中自动提取结构化数据
**脚本：** `create_attachment_classification.py`
**支持：**
- ✅ 自定义提取规则（定义字段和描述）
- ✅ OCR + LLM / Vision-Language 双引擎
- ✅ 直接提取模式（90% 使用率）
- ✅ 分类 + 提取模式

**典型场景：**
- 合同信息自动提取填充表单
- 发票数据识别
- 简历结构化解析

### 4. iframe 技能卡片
**做什么：** 在数字员工对话中嵌入自定义 UI
**脚本：** `register_iframe_card.py`
**支持：**
- ✅ 对话中展示复杂界面
- ✅ 业务菜单独立页面
- ✅ 触发条件配置

**典型场景：**
- 报价单预览和编辑
- 历史记录列表
- 数据看板

### 5. 计费模块集成 ⚠️ 重要
**做什么：** 控制高价值服务的使用额度
**文档：** `references/billing.md`
**支持：**
- ✅ 额度检查接口
- ✅ 额度消耗接口
- ✅ API-KEY 鉴权
- ✅ 三种集成方案（MCP/iframe/后端）

**典型场景：**
- 生成文档时扣费
- 创建订单时扣费
- 批量处理按次扣费

**⚠️ 必须集成场景：**
生成文档、创建订单、数据导出、复杂分析、批量处理、调用付费 API

### 6. 文档服务
**做什么：** 文档格式转换和处理
**支持：**
- Markdown/HTML 转 PDF
- OCR 识别
- Excel 读写

## 使用流程

### 快速开始三步骤

```bash
# 1. 配置 API Key
echo "WORKOPILOT_API_KEY=你的密钥" > .env.workopilot

# 2. 创建配置文件（JSON）
# 参考 evals/ 目录下的示例

# 3. 运行脚本
python scripts/create_digital_employee.py --config your-config.json
```

### 技能工作模式

当你说"创建数字员工"、"对接喔壳"、"附件提取"时：

1. **检查 API Key** - 未配置则引导配置
2. **查询现有配置** - 避免重复创建
3. **自动生成配置** - 根据你的需求设计参数
4. **运行脚本创建** - 自动执行并验证
5. **提供使用示例** - 给出后续调用代码
6. **⚠️ 计费提醒** - 高价值操作提醒集成计费

## 配置文件示例

### 创建数字员工（带 iframe 嵌入）
```json
{
  "robotName": "客服助手",
  "robotCode": "customer_service",
  "systemPrompt": "你是专业客服，耐心解答问题。",
  "welcomeMessage": "你好！有什么可以帮你？",
  "enableEmbed": 1,
  "embedBaseUrl": "https://agent.workopilot.com",
  "embedAllowedOrigins": ["https://your-site.com"]
}
```

### 创建 AI 服务
```json
{
  "serviceCode": "contract-review",
  "serviceName": "合同审查",
  "inputs": [
    {
      "name": "contract_type",
      "label": "合同类型",
      "type": "select",
      "options": ["采购合同", "销售合同"]
    },
    {
      "name": "contract_content",
      "label": "合同内容",
      "type": "textarea"
    }
  ],
  "systemPrompt": "审查{{contract_type}}:\n{{contract_content}}"
}
```

### 创建附件分类
```json
{
  "GroupCode": "contract",
  "CategoryCode": "purchase-contract",
  "CategoryName": "采购合同",
  "extractRules": [
    {
      "name": "partyA",
      "label": "甲方",
      "type": "string",
      "description": "合同中的甲方公司全称"
    },
    {
      "name": "amount",
      "label": "合同金额",
      "type": "number",
      "description": "合同总金额，数字格式"
    }
  ]
}
```

## 关键脚本

| 脚本 | 功能 | 文档 |
|-----|------|------|
| `create_digital_employee.py` | 创建数字员工 | `scripts/README.md` |
| `update_digital_employee.py` | 更新数字员工 | `scripts/README.md` |
| `create_ai_service.py` | 创建 AI 服务 | `references/ai-service.md` |
| `create_attachment_classification.py` | 创建附件分类 | `references/attachment-classification.md` |
| `register_iframe_card.py` | 注册技能卡片 | `references/iframe-skill-card.md` |
| `smoke_test.py` | 冒烟测试 | - |

## 关键文档

| 文档 | 用途 |
|-----|------|
| `QUICKSTART.md` | 5 分钟快速上手 |
| `SKILL.md` | 完整技能说明 |
| `scripts/README.md` | 脚本详细用法 |
| `references/billing.md` | 计费集成指南 ⚠️ |
| `references/digital-employee.md` | 数字员工接口 |
| `references/attachment-classification.md` | 附件提取完整流程 |
| `references/iframe-embed.md` | iframe 嵌入对接 |

## 典型对接场景

### 场景 1：官网增加智能客服
```
需求 → 创建数字员工（启用 iframe 嵌入）
     → 配置允许的域名
     → 复制 iframe 代码到官网
     → 集成计费模块（可选）
```

### 场景 2：合同管理系统自动提取
```
需求 → 创建"采购合同"附件分类
     → 定义提取规则（甲方、金额、日期等）
     → 业务系统调用提取接口
     → 自动填充表单
```

### 场景 3：ERP 系统增加 AI 功能
```
需求 → 创建 AI 服务（如订单审核）
     → 后端调用 AI 服务接口
     → 集成计费模块
     → 在业务流程中嵌入
```

### 场景 4：销售助理（含计费）
```
需求 → 创建数字员工
     → 开发 MCP 工具（创建订单）
     → 集成计费模块（创建订单时扣费）⚠️
     → 绑定 MCP 到数字员工
```

## 技能优势

### 自动化
- ✅ 避免手动操作，配置即代码
- ✅ 支持批量创建和更新
- ✅ 幂等性保证，可重复运行

### 智能选择
- ✅ 自动选择最优模型（根据场景）
- ✅ 自动查询和复用已有配置
- ✅ 智能提醒计费集成 ⚠️

### 完整方案
- ✅ 从配置到使用的端到端指导
- ✅ 提供完整可运行的代码示例
- ✅ 涵盖故障排查和最佳实践

### 开发者友好
- ✅ 环境变量管理配置
- ✅ 清晰的错误提示
- ✅ 丰富的文档和示例

## 重要提醒

### ⚠️ 计费集成
如果你的数字员工提供以下服务，**必须集成计费模块**：
- 生成文档、报告、合同
- 创建订单、工单、任务
- 数据导出（PDF、Excel、Word）
- 复杂计算或分析
- 批量处理操作
- 调用外部付费 API

**未集成风险：** 用户可以无限制使用，导致成本失控。

### ⚠️ API-KEY 安全
- 不要在前端暴露 API-KEY
- 保存在服务端环境变量
- 不要提交到 Git 仓库
- 使用 `.env.workopilot` 本地开发

## 获取帮助

- **快速上手**: `QUICKSTART.md`
- **完整说明**: `SKILL.md`
- **脚本用法**: `scripts/README.md`
- **计费集成**: `references/billing.md` ⚠️
- **变更记录**: `CHANGELOG.md`

## 总结

| 功能 | 核心价值 | 使用频率 |
|-----|---------|---------|
| 数字员工管理 | 快速创建对话式 AI | ⭐⭐⭐⭐⭐ |
| 附件智能提取 | 自动提取文档数据 | ⭐⭐⭐⭐⭐ |
| AI 服务封装 | 封装可复用 AI 能力 | ⭐⭐⭐⭐ |
| 计费模块集成 | 控制使用成本 | ⭐⭐⭐⚠️ |
| iframe 技能卡片 | 扩展 UI 交互 | ⭐⭐⭐ |
| 文档服务 | 格式转换处理 | ⭐⭐ |

**一句话总结：** 自动化配置喔壳 AI 能力，让企业快速拥有智能助手、文档提取、计费控制等企业级 AI 功能。

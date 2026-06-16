# Workopilot Skills

用于集成 WorkoPilot AI 平台的 Claude Desktop 技能集合。

## 📖 什么是 Workopilot Skills？

Workopilot Skills 是一个综合工具包，帮助开发者将 WorkoPilot 的 AI 能力集成到业务系统中。它提供自动化脚本、代码示例和完整的集成解决方案，用于创建 AI 服务、配置数字员工和实现文档智能功能。

## 🚀 快速开始

### 安装

1. **克隆仓库:**
   ```bash
   git clone git@github.com:workopilot/workopilot.skills.git
   cd workopilot.skills
   ```

2. **配置 API 凭证:**
   
   在项目根目录创建 `.env.workopilot` 文件:
   ```properties
   WORKOPILOT_BASE_URL=https://agent.workopilot.com/net-api
   WORKOPILOT_API_KEY=your_api_key_here
   ```

3. **安装 Python 依赖:**
   ```bash
   pip install requests python-dotenv
   ```

### 基本使用

**创建 AI 服务:**
```bash
python skills/workopilot-service-builder/scripts/create_ai_service.py --config service.json
```

**创建数字员工:**
```bash
python skills/workopilot-service-builder/scripts/create_digital_employee.py --config employee.json
```

**创建附件分类:**
```bash
python skills/workopilot-service-builder/scripts/create_attachment_classification.py --config classification.json
```

## 📦 包含内容

### 技能 (Skills)

`skills/` 目录包含用于 WorkoPilot 集成的 Claude Desktop 技能:

- **workopilot-service-builder** - 创建和集成 WorkoPilot 服务的主技能
  - AI 服务创建和管理
  - 数字员工配置
  - 附件分类和提取
  - Iframe 技能卡片注册
  - 文档服务集成

详细文档请参阅 [skills/workopilot-service-builder/SKILL.md](skills/workopilot-service-builder/SKILL.md)

### 示例应用 (Sample)

`sample/` 目录包含一个展示 WorkoPilot Skills 集成的演示应用:

- 现代化 SaaS 风格管理系统
- 订单管理模块
- Todo 清单模块
- RESTful API 后端 (Flask)
- 现代化 UI 前端 (Vue 3 + Tailwind CSS)

该示例展示了如何构建一个完整的业务应用，并可通过 WorkoPilot AI 能力进行增强。

安装说明请参阅 [sample/README.md](sample/README.md)

## 🌟 核心功能

### 1. AI 服务创建
创建可复用的 AI 能力，支持结构化输入和自定义提示词:
- 文本分析（合同审查、简历筛选）
- 内容生成（报告、邮件、文案）
- 数据转换（非结构化 → 结构化）

### 2. 数字员工配置
设置完整的对话式 AI 智能体:
- MCP（模型上下文协议）用于数据操作
- 技能卡片（Iframe）用于 UI 扩展
- 知识库集成
- 自定义系统提示词

### 3. 附件分类与提取 ⭐
**最常用功能** - 从文档中自动提取结构化数据:
- **直接提取模式**（90% 使用率）- 上传合同 → 提取数据 → 填充表单
- 支持: 合同、发票、简历、订单、收据等
- 两种提取方法: OCR + LLM 或 Vision-Language
- 可配置的提取规则，字段级别描述

### 4. Iframe 技能卡片
在对话或业务菜单中嵌入自定义 UI 组件:
- 显示复杂界面（表单、预览、仪表板）
- 业务菜单页面（历史记录、分析）

### 5. 文档服务
文件处理能力:
- Markdown/HTML 转 PDF
- OCR 识别
- Excel 读写

## 🛠️ 技术栈

**技能:**
- Python 3.7+
- requests 库
- python-dotenv

**示例应用:**
- 后端: Flask 3.0, Flask-CORS
- 前端: Vue 3, Vue Router, Tailwind CSS, Vite

## 📚 文档

### 技能文档
- [workopilot-service-builder/SKILL.md](skills/workopilot-service-builder/SKILL.md) - 完整技能文档
- [references/](skills/workopilot-service-builder/references/) - 详细 API 参考
  - `auth-and-config.md` - 认证和配置
  - `ai-service.md` - AI 服务集成
  - `digital-employee.md` - 数字员工设置
  - `attachment-classification.md` - 文档提取指南 ⭐
  - `iframe-embed.md` - Iframe 嵌入
  - `iframe-skill-card.md` - 技能卡片注册
  - `document-service.md` - 文档处理

### 示例文档
- [sample/README.md](sample/README.md) - 示例应用设置

## 🎯 常见使用场景

### 场景 1: 文档智能化
**需求:** 从上传的合同中自动提取数据

```bash
# 1. 创建分类
python scripts/create_attachment_classification.py --config contract-classification.json

# 2. 调用提取 API
curl -X POST https://agent.workopilot.com/net-api/api/attachment/extract \
  -H "API-KEY: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "fileUrl": "https://example.com/contract.pdf",
    "categoryCode": "contract-purchase"
  }'

# 3. 获取结构化数据并填充表单
```

### 场景 2: AI 服务集成
**需求:** 为系统添加合同审查能力

```bash
# 1. 创建 AI 服务
python scripts/create_ai_service.py --config contract-review.json

# 2. 在应用中调用
fetch('https://agent.workopilot.com/net-api/api/aiagent/run', {
  method: 'POST',
  headers: {
    'API-KEY': process.env.WORKOPILOT_API_KEY,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    serviceCode: 'contract-review-001',
    inputs: {
      contract_type: '采购合同',
      contract_content: '...'
    }
  })
})
```

### 场景 3: 数字员工嵌入
**需求:** 在 CRM 系统中嵌入 AI 助手

```html
<!-- 嵌入数字员工 iframe -->
<iframe 
  src="https://agent.workopilot.com/chat/{robotId}?token={runtimeToken}"
  width="100%"
  height="600px">
</iframe>
```

## 🔧 开发

### 项目结构
```
workopilot.skills/
├── skills/                          # Claude Desktop 技能
│   └── workopilot-service-builder/ # 主集成技能
│       ├── SKILL.md                # 技能文档
│       ├── scripts/                # 自动化脚本
│       │   ├── create_ai_service.py
│       │   ├── create_digital_employee.py
│       │   ├── create_attachment_classification.py
│       │   ├── register_iframe_card.py
│       │   └── smoke_test.py
│       ├── references/             # API 参考文档
│       ├── agents/                 # 示例智能体配置
│       └── evals/                  # 测试用例
│
├── sample/                         # 演示应用
│   ├── backend/                    # Flask 后端
│   ├── frontend/                   # Vue 3 前端
│   └── README.md                   # 设置说明
│
└── README.md                       # 本文件
```

### 运行脚本

所有脚本支持多种配置方式:

**1. 环境文件（推荐）:**
```bash
# 在项目根目录创建 .env.workopilot
python scripts/create_ai_service.py --config service.json
```

**2. 环境变量:**
```bash
export WORKOPILOT_API_KEY="your_key"
python scripts/create_ai_service.py --config service.json
```

**3. 命令行参数:**
```bash
python scripts/create_ai_service.py \
  --base-url https://agent.workopilot.com/net-api \
  --api-key your_key \
  --config service.json
```

### 测试

**冒烟测试验证配置:**
```bash
python skills/workopilot-service-builder/scripts/smoke_test.py
```

**使用 curl 测试:**
```bash
curl -H "API-KEY: your_api_key" \
  https://agent.workopilot.com/net-api/api/aiagent/list
```

## 🔐 安全最佳实践

### API 密钥管理
- ✅ 将 API 密钥存储在 `.env.workopilot` 或环境变量中
- ✅ 将 `.env.workopilot` 添加到 `.gitignore`
- ✅ 生产环境使用环境变量
- ❌ 永远不要在源代码中硬编码 API 密钥
- ❌ 永远不要将 API 密钥提交到 Git
- ❌ 永远不要在前端代码中暴露 API 密钥

### Iframe 安全
- 生产环境的 iframe 技能卡片使用 HTTPS URL
- 开发期间使用 localhost URL 测试
- 发布前更新为生产 URL

## 🤝 贡献

欢迎贡献！请遵循以下指南:

1. Fork 仓库
2. 创建特性分支
3. 进行更改
4. 充分测试
5. 提交 Pull Request

## 📄 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 📮 联系方式

- **项目**: https://github.com/workopilot/workopilot.skills
- **问题**: https://github.com/workopilot/workopilot.skills/issues
- **邮箱**: angus.wang@apright.com

## 🌐 WorkoPilot 平台

了解更多关于 WorkoPilot:
- 网站: https://workopilot.com
- 文档: https://docs.workopilot.com
- API 参考: https://agent.workopilot.com/docs

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给一个 Star！**

Made with ❤️ by Workopilot Team

</div>

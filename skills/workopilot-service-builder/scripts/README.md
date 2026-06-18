# 喔壳服务脚本使用指南

本目录包含用于创建和管理喔壳服务的 Python 脚本。

## 前置准备

### 1. 安装依赖

脚本使用 Python 3.7+ 标准库，无需额外安装依赖。

### 2. 配置 API Key

创建 `.env.workopilot` 文件在项目根目录：

```properties
# 生产环境
WORKOPILOT_BASE_URL=https://agent.workopilot.com/net-api
WORKOPILOT_API_KEY=你的API密钥

# 测试环境
# WORKOPILOT_BASE_URL=https://agenttest.workopilot.com/net-api
# WORKOPILOT_API_KEY=你的测试环境API密钥
```

## 脚本说明

### create_digital_employee.py - 创建数字员工

创建一个新的数字员工或复用已存在的数字员工。

**支持的配置参数：**

#### 基础配置
- `robotName` (必填) - 数字员工名称
- `robotCode` (可选) - 数字员工编码，不传时自动生成
- `avatarUrl` (可选) - 头像地址，不传时从系统头像库随机选择
- `businessLine` (可选) - 业务线编码
- `description` (可选) - 描述
- `systemPrompt` (必填) - 系统提示词，定义数字员工的行为
- `chatModelId` (可选) - 聊天模型 ID，不传时自动选择合适的模型

#### 对话配置
- `welcomeMessage` (可选) - 欢迎语
- `quickQuestions` (可选) - 快捷问题数组
  ```json
  [
    {"text": "问题文本", "sort": 1}
  ]
  ```
- `forbiddenWords` (可选) - 禁用词，换行分隔
- `enableHistory` (可选) - 是否启用历史记录，1 启用 0 关闭
- `maxHistory` (可选) - 最大历史消息数
- `enableSuggestedReplies` (可选) - 是否启用建议回复
- `enableToolCallDisplay` (可选) - 是否展示工具调用

#### 高级配置
- `enableAgentCollaboration` (可选) - 是否启用数字员工协作
- `collaborationScope` (可选) - 协作范围
- `memoryMode` (可选) - 记忆模式：SHORT、MEDIUM、LONG、UNLIMITED
- `enableCompaction` (可选) - 是否启用上下文压缩
- `compactionModelId` (可选) - 压缩模型 ID

#### iframe 嵌入配置 ⭐ 新增
- `enableEmbed` (可选) - 是否启用 iframe 嵌入，1 启用 0 关闭
  - **注意**：启用时会自动选择租户第一个可用 APIKEY，如果没有可用 APIKEY 则创建失败
- `embedBaseUrl` (可选) - 嵌入基础 URL，传入后响应会返回完整的 `embedUrl` 和 `iframeCode`
- `embedAllowedOrigins` (可选) - 允许嵌入的宿主域名数组
  ```json
  ["https://crm.example.com", "https://erp.example.com"]
  ```
- `embedExpireAt` (可选) - 嵌入链接过期时间
- `embedMaxDailyCalls` (可选) - 每日最大调用次数
- `embedThemeConfig` (可选) - 主题配置
- `embedHideHeader` (可选) - 是否隐藏头部，1 隐藏 0 显示
- `embedHideBranding` (可选) - 是否隐藏品牌标识，1 隐藏 0 显示

#### 能力绑定
- `skills` (可选) - 绑定的技能数组
  ```json
  [
    {
      "skillRegistryId": 21,
      "isActive": 1,
      "sortIndex": 0
    }
  ]
  ```
- `mcpTools` (可选) - 绑定的 MCP 工具数组
  ```json
  [
    {
      "toolId": 31,
      "isActive": true,
      "sort": 0
    }
  ]
  ```

**使用示例：**

```bash
# 创建数字员工（不启用嵌入）
python scripts/create_digital_employee.py --config evals/create-digital-employee.json

# 创建数字员工（启用 iframe 嵌入）
python scripts/create_digital_employee.py --config evals/create-digital-employee-with-embed.json

# 强制创建新数字员工（即使编码已存在）
python scripts/create_digital_employee.py --config config.json --no-reuse
```

**响应示例（启用嵌入时）：**

```jsonc
{
  "code": 200,
  "msg": "数字员工创建成功",
  "data": {
    "id": 1001,                    // 数字员工 ID
    "robotCode": "contract_review_expert",
    "robotName": "合同审核专家",
    "avatarUrl": "...",
    "chatModelId": 1,
    "enableEmbed": 1,              // 已启用嵌入
    "embedApiKeyId": 10,           // 绑定的 APIKEY ID
    "embedUrl": "https://agent.workopilot.com/embed/chat/1001?token=xxx&externalUserId={userId}&externalUserName={userName}",
    "iframeCode": "<iframe src=\"https://agent.workopilot.com/embed/chat/1001?token=xxx&externalUserId={userId}&externalUserName={userName}\" width=\"100%\" height=\"760\" frameborder=\"0\" allow=\"clipboard-write; microphone; autoplay\"></iframe>",
    "skillRegistryIds": [],
    "mcpToolIds": []
  }
}
```

### update_digital_employee.py - 更新数字员工 ⭐ 新增

更新已有数字员工的配置，只需提供要修改的字段。

**支持更新的字段：**

所有 `create_digital_employee.py` 支持的字段都可以更新，除了：
- `robotCode` - 不允许为空
- `robotName` - 不允许为空
- `systemPrompt` - 不允许为空

**注意事项：**
- 未传的字段保持原值
- 传空字符串表示清空（但 `robotName`、`robotCode`、`systemPrompt` 不允许清空）
- 技能、MCP 工具和 iframe 嵌入配置不由该接口修改，应调用对应配置接口

**使用示例：**

```bash
# 更新数字员工基本信息
python scripts/update_digital_employee.py \
  --employee-id 1001 \
  --config evals/update-digital-employee.json

# 只更新欢迎语和快捷问题
python scripts/update_digital_employee.py \
  --employee-id 1001 \
  --config update-welcome.json
```

**配置文件示例：**

```json
{
  "robotName": "合同审核专家Pro",
  "systemPrompt": "你是一名资深合同审核专家...",
  "welcomeMessage": "你好！我是升级版合同审核专家...",
  "maxHistory": 20,
  "enableSuggestedReplies": 1
}
```

### create_ai_service.py - 创建 AI 服务

创建一个 AI 服务，封装可复用的 AI 能力。

**使用示例：**

```bash
python scripts/create_ai_service.py --config ai-service-config.json
```

### create_attachment_classification.py - 创建附件分类

创建附件分类，用于文档智能提取。

**使用示例：**

```bash
python scripts/create_attachment_classification.py --config attachment-config.json
```

### register_iframe_card.py - 注册 iframe 技能卡片

注册一个 iframe 技能卡片，扩展数字员工的 UI 能力。

**使用示例：**

```bash
python scripts/register_iframe_card.py --config iframe-card-config.json
```

### smoke_test.py - 冒烟测试

测试配置是否正常，验证 API 连通性。

**使用示例：**

```bash
python scripts/smoke_test.py
```

## 通用参数

所有脚本都支持以下参数：

```bash
--base-url <URL>       # 喔壳 API 基础 URL（可选，默认从环境变量读取）
--api-key <KEY>        # API 密钥（可选，默认从环境变量读取）
--env-file <PATH>      # 自定义环境文件路径（可选）
--config <PATH>        # JSON 配置文件路径（必填）
```

## 幂等性说明

脚本实现轻量级幂等，避免重复创建：

- `create_digital_employee.py` - 按 `robotCode` 查询，存在则复用（除非使用 `--no-reuse`）
- `create_ai_service.py` - 按 `serviceCode` 查询，存在则复用
- `create_attachment_classification.py` - 按 `GroupCode`+`CategoryCode` 查询，存在时默认编辑覆盖

## 故障排查

### 常见问题

**1. "缺少 WORKOPILOT_API_KEY"**

解决方法：
- 创建 `.env.workopilot` 文件并配置 `WORKOPILOT_API_KEY`
- 或使用 `--api-key` 参数传入

**2. "没有可用模型"**

解决方法：
- 登录喔壳平台配置可用的大语言模型
- 确保模型已启用且配置正确

**3. "enableEmbed=1 但没有可用 APIKEY"**

解决方法：
- 先在喔壳平台创建 API Key
- 或将 `enableEmbed` 设置为 0，后续再单独配置嵌入功能

**4. "HTTP 请求失败"**

检查项：
- 网络连接是否正常
- base-url 是否正确
- API Key 是否有效

## 更多信息

详细文档请参阅：
- 技能说明：`SKILL.md`
- 数字员工接口文档：`references/digital-employee.md`
- iframe 嵌入文档：`references/iframe-embed.md`
- 鉴权配置文档：`references/auth-and-config.md`

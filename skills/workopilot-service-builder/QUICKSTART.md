# 快速上手：创建和管理数字员工

本指南帮助你在 5 分钟内完成数字员工的创建和配置。

## 第一步：配置 API Key

1. 访问喔壳平台获取 API Key：https://agent.workopilot.com/smart/api-key

2. 在项目根目录创建 `.env.workopilot` 文件：

```properties
WORKOPILOT_BASE_URL=https://agent.workopilot.com/net-api
WORKOPILOT_API_KEY=你的API密钥
```

3. 将 `.env.workopilot` 添加到 `.gitignore`：

```bash
echo ".env.workopilot" >> .gitignore
```

## 第二步：创建数字员工

### 场景 A：创建普通数字员工

创建配置文件 `my-employee.json`：

```json
{
  "robotName": "我的第一个数字员工",
  "robotCode": "my_first_employee",
  "systemPrompt": "你是一个友好的助手，帮助用户解答问题。",
  "welcomeMessage": "你好！有什么可以帮你的吗？",
  "enableHistory": 1,
  "maxHistory": 10
}
```

运行创建脚本：

```bash
python scripts/create_digital_employee.py --config my-employee.json
```

成功后会显示：
```
✅ 创建成功
   ID: 1001
   RobotId: 1001
   RobotCode: my_first_employee
```

### 场景 B：创建可嵌入的数字员工 ⭐

如果你想将数字员工嵌入到自己的系统中，使用以下配置：

创建配置文件 `embeddable-employee.json`：

```json
{
  "robotName": "客服助手",
  "robotCode": "customer_service_assistant",
  "systemPrompt": "你是一个专业的客服助手，耐心回答用户问题。",
  "welcomeMessage": "你好！我是客服助手，请问有什么可以帮到你？",
  "enableHistory": 1,
  "maxHistory": 10,
  "enableEmbed": 1,
  "embedBaseUrl": "https://agent.workopilot.com",
  "embedAllowedOrigins": [
    "https://your-domain.com"
  ]
}
```

运行创建脚本：

```bash
python scripts/create_digital_employee.py --config embeddable-employee.json
```

成功后会显示嵌入信息：
```
   🔗 iframe 嵌入信息:
      嵌入 URL: https://agent.workopilot.com/embed/chat/1001?token=xxx&externalUserId={userId}&externalUserName={userName}
      API Key ID: 10

   📋 iframe 代码:
      <iframe src="https://agent.workopilot.com/embed/chat/1001?token=xxx..." width="100%" height="760" frameborder="0" allow="clipboard-write; microphone; autoplay"></iframe>
```

将这段 iframe 代码复制到你的网页中即可嵌入数字员工！

## 第三步：更新数字员工（可选）

如果需要修改数字员工的配置，创建更新配置文件 `update-employee.json`：

```json
{
  "robotName": "升级版客服助手",
  "systemPrompt": "你是一个专业且高效的客服助手，优先解决用户的核心问题。",
  "maxHistory": 20,
  "enableSuggestedReplies": 1
}
```

运行更新脚本：

```bash
python scripts/update_digital_employee.py --employee-id 1001 --config update-employee.json
```

**注意**：只需要提供要修改的字段，其他字段保持不变。

## 常见场景速查

### 1. 创建合同审核助手

```json
{
  "robotName": "合同审核助手",
  "robotCode": "contract_reviewer",
  "systemPrompt": "你是一名专业的合同审核专家，帮助用户识别合同风险点。",
  "welcomeMessage": "请上传或粘贴需要审核的合同内容。",
  "quickQuestions": [
    {"text": "帮我检查违约条款", "sort": 1},
    {"text": "分析付款条件和风险", "sort": 2}
  ],
  "enableHistory": 1,
  "maxHistory": 10
}
```

### 2. 创建客服助手（嵌入到官网）

```json
{
  "robotName": "官网客服",
  "robotCode": "website_support",
  "systemPrompt": "你是我们公司的官网客服，熟悉产品功能和价格政策。",
  "welcomeMessage": "你好！我是官网客服，有什么可以帮你？",
  "quickQuestions": [
    {"text": "产品有哪些功能", "sort": 1},
    {"text": "价格是多少", "sort": 2},
    {"text": "如何联系销售", "sort": 3}
  ],
  "enableHistory": 1,
  "maxHistory": 5,
  "enableEmbed": 1,
  "embedBaseUrl": "https://agent.workopilot.com",
  "embedAllowedOrigins": ["https://www.your-company.com"],
  "embedHideHeader": 0
}
```

### 3. 创建 HR 招聘助理

```json
{
  "robotName": "HR 招聘助理",
  "robotCode": "hr_recruitment_assistant",
  "systemPrompt": "你是 HR 招聘助理，帮助筛选简历和评估候选人。",
  "welcomeMessage": "请提供岗位要求和候选人简历，我来帮你分析。",
  "quickQuestions": [
    {"text": "帮我筛选这份简历", "sort": 1},
    {"text": "候选人匹配度如何", "sort": 2}
  ],
  "enableHistory": 1,
  "maxHistory": 15,
  "enableToolCallDisplay": 1
}
```

## 嵌入到你的网页

如果你启用了 `enableEmbed`，可以用以下方式嵌入：

### HTML 直接嵌入

```html
<!DOCTYPE html>
<html>
<head>
    <title>我的网站</title>
</head>
<body>
    <h1>欢迎访问</h1>
    
    <!-- 嵌入数字员工 -->
    <iframe 
        src="https://agent.workopilot.com/embed/chat/1001?token=xxx&externalUserId=user123&externalUserName=张三" 
        width="100%" 
        height="760" 
        frameborder="0" 
        allow="clipboard-write; microphone; autoplay">
    </iframe>
</body>
</html>
```

### 悬浮窗方式

```html
<!DOCTYPE html>
<html>
<head>
    <title>我的网站</title>
    <style>
        #chat-button {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 60px;
            height: 60px;
            background: #1890ff;
            border-radius: 50%;
            cursor: pointer;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }
        #chat-window {
            display: none;
            position: fixed;
            bottom: 90px;
            right: 20px;
            width: 400px;
            height: 600px;
            border: 1px solid #ddd;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 20px rgba(0,0,0,0.2);
        }
    </style>
</head>
<body>
    <h1>欢迎访问</h1>
    
    <!-- 悬浮按钮 -->
    <div id="chat-button" onclick="toggleChat()">💬</div>
    
    <!-- 聊天窗口 -->
    <div id="chat-window">
        <iframe 
            src="https://agent.workopilot.com/embed/chat/1001?token=xxx&externalUserId=user123&externalUserName=张三" 
            width="100%" 
            height="100%" 
            frameborder="0" 
            allow="clipboard-write; microphone; autoplay">
        </iframe>
    </div>
    
    <script>
        function toggleChat() {
            const chatWindow = document.getElementById('chat-window');
            chatWindow.style.display = chatWindow.style.display === 'none' ? 'block' : 'none';
        }
    </script>
</body>
</html>
```

## 参数说明速查表

### 必填参数

| 参数 | 说明 | 示例 |
|-----|------|------|
| `robotName` | 数字员工名称 | `"客服助手"` |
| `systemPrompt` | 系统提示词，定义行为 | `"你是一个友好的助手"` |

### 推荐配置

| 参数 | 说明 | 推荐值 |
|-----|------|--------|
| `robotCode` | 唯一编码 | `"customer_service"` |
| `welcomeMessage` | 欢迎语 | `"你好！有什么可以帮你？"` |
| `enableHistory` | 启用历史记录 | `1` |
| `maxHistory` | 最大历史消息数 | `10` |

### iframe 嵌入参数

| 参数 | 说明 | 必填 |
|-----|------|------|
| `enableEmbed` | 启用嵌入 | 是 |
| `embedBaseUrl` | 嵌入基础 URL | 是 |
| `embedAllowedOrigins` | 允许的域名列表 | 推荐 |
| `embedHideHeader` | 隐藏头部 | 否 |
| `embedHideBranding` | 隐藏品牌 | 否 |

## 故障排查

### 问题 1：缺少 WORKOPILOT_API_KEY

**错误信息：**
```
❌ 缺少 WORKOPILOT_API_KEY
```

**解决方法：**
1. 检查 `.env.workopilot` 文件是否存在
2. 确认文件内容格式正确
3. 确认 API Key 不是占位符 `replace_with_your_api_key`

### 问题 2：没有可用模型

**错误信息：**
```
❌ 没有可用模型，无法创建数字员工
```

**解决方法：**
1. 登录喔壳平台
2. 配置至少一个大语言模型
3. 确保模型已启用

### 问题 3：enableEmbed=1 但创建失败

**错误信息：**
```
当前租户没有可用 APIKEY
```

**解决方法：**
1. 先在喔壳平台创建 API Key
2. 或暂时将 `enableEmbed` 设置为 `0`
3. 后续单独配置嵌入功能

### 问题 4：robotCode 已存在

**现象：**
脚本提示"数字员工已存在，复用"

**解决方法：**
- 如果要创建新的，修改 `robotCode` 为不同的值
- 或使用 `--no-reuse` 参数强制创建

## 下一步

现在你已经创建了数字员工，可以：

1. **调用开放 API** - 在你的应用中集成数字员工对话能力
   - 参考：`references/digital-employee.md`

2. **嵌入到网页** - 将数字员工界面嵌入你的系统
   - 参考：`references/iframe-embed.md`

3. **绑定技能和工具** - 扩展数字员工的能力
   - 参考：`references/iframe-skill-card.md`

4. **配置附件提取** - 让数字员工能处理文档
   - 参考：`references/attachment-classification.md`

## 获取帮助

- 完整文档：`SKILL.md`
- 脚本详细说明：`scripts/README.md`
- 变更日志：`CHANGELOG.md`
- 接口文档：`docs/喔壳技能/接口文档/02-数字员工开放接口.md`

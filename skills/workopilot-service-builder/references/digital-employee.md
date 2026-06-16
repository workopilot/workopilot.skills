# 数字员工接口

## 查询启用中的数字员工

```http
GET /api/ai/open/robots?baseUrl=https://agent.workopilot.com
```

响应示例（`jsonc`，带注释，不可直接作为 JSON 发送）：

```jsonc
{
  "code": 200,
  "msg": null,
  "data": null,
  "total": 1, // rows 总数
  "rows": [
    {
      "robotId": 1001, // 数字员工 ID；开放聊天和 iframe 嵌入都要用
      "robotCode": "contract_review_agent", // 数字员工编码；按编码查询 profile 时使用
      "robotName": "合同审核助手",
      "avatarUrl": "https://example.com/avatar.png",
      "businessLine": "legal",
      "businessLineName": "法务",
      "description": "辅助审核合同风险点",
      "intro": "你好，我可以帮你审核合同。",
      "enableShare": true, // true 表示可 iframe 嵌入
      "shareUrl": "https://agent.workopilot.com/embed/chat/1001?token=xxx&externalUserId={userId}&externalUserName={userName}", // iframe 链接模板
      "appMenus": [
        {
          "id": 2001,
          "menuType": "iframe",
          "displayMode": "fullscreen",
          "menuKey": "contract-detail", // 直达菜单时追加到 iframe URL
          "title": "合同详情",
          "icon": "lucide:file-text",
          "routePath": "",
          "componentPath": null,
          "iframeUrl": "https://example.com/contract",
          "directUrl": "https://agent.workopilot.com/embed/chat/1001?token=xxx&externalUserId={userId}&externalUserName={userName}&menuKey=contract-detail", // 菜单直达 URL 模板
          "sort": 10,
          "isEnabled": true
        }
      ]
    }
  ]
}
```

Agent 使用：

- 选择员工后保存 `robotId`，后续创建会话、发送消息、iframe 嵌入都需要。
- 如果要嵌入页面，优先使用 `shareUrl`；如果要打开指定菜单，使用 `appMenus[].directUrl`。

## 查询数字员工资料

```http
GET /api/ai/open/robot/profile?robotId=1001&baseUrl=https://agent.workopilot.com
GET /api/ai/robot/profile/{robotCode}
GET /api/ai/robot/profile/by-id/{id}
```

响应示例：

```jsonc
{
  "code": 200,
  "msg": null,
  "data": {
    "id": 1001, // robotId
    "robotCode": "contract_review_agent",
    "robotName": "合同审核助手",
    "avatarUrl": "https://example.com/avatar.png",
    "welcomeMessage": "你好，我可以帮你审核合同。",
    "quickQuestions": [
      {
        "text": "帮我检查违约条款",
        "sort": 1
      }
    ],
    "enableSuggestedReplies": 0,
    "enableToolCallDisplay": 1,
    "businessLine": "legal",
    "businessLineName": "法务",
    "isActive": 1,
    "enableAgentCollaboration": 0,
    "collaborationScope": null,
    "appMenus": []
  },
  "total": 0,
  "rows": null
}
```

Agent 使用：profile 适合做“已创建员工确认”和“嵌入前展示信息”，但开放聊天仍主要使用 `data.id`。

## 查询创建关联数据

```http
GET /api/ai/robot/external/create-options
```

响应示例：

```jsonc
{
  "code": 200,
  "msg": null,
  "data": {
    "models": [
      {
        "modelId": 1, // 创建员工时传 chatModelId
        "modelName": "gpt-4.1-mini",
        "modelCode": "gpt-4.1-mini",
        "modelType": "chat",
        "modelLevel": "normal",
        "providerCode": "openai",
        "providerName": "OpenAI",
        "isDefault": 1,
        "temperature": 0.7,
        "topP": 1,
        "maxTokens": 4096
      }
    ],
    "capabilities": [
      {
        "skillRegistryId": 21, // 创建员工时放入 skills[].skillRegistryId
        "skillName": "业务卡片",
        "skillCode": "business_card",
        "skillCategory": "card",
        "skillDesc": "展示业务卡片",
        "skillKind": "BUSINESS_CARD",
        "skillSource": "SYSTEM_BUILTIN",
        "packageVersion": null
      }
    ],
    "skills": [],
    "mcpTools": [
      {
        "toolId": 31, // 创建员工时放入 mcpTools[].toolId
        "toolKey": "search",
        "toolName": "搜索工具",
        "implementationType": "MCP",
        "descriptionAi": "用于搜索外部信息",
        "isPublic": "1"
      }
    ],
    "businessLines": [
      {
        "label": "法务",
        "value": "legal", // 创建员工时传 businessLine
        "dictType": "position_category",
        "isDefault": true
      }
    ]
  },
  "total": 0,
  "rows": null
}
```

Agent 使用：

- 优先选择 `models[].isDefault=1` 的 `modelId` 作为 `chatModelId`。
- 注册 iframe 技能卡片后，把返回的 `skillRegistryId` 合并到创建员工的 `skills` 中。

## 创建数字员工

```http
POST /api/ai/robot/external/create
```

请求体：

```json
{
  "robotName": "合同审核助手",
  "robotCode": "contract_review_agent",
  "avatarUrl": "https://example.com/avatar.png",
  "businessLine": "legal",
  "description": "辅助审核合同风险点",
  "chatModelId": 1,
  "systemPrompt": "你是一个严谨的合同审核助手。",
  "welcomeMessage": "你好，我可以帮你审核合同。",
  "quickQuestions": [
    {
      "text": "帮我检查违约条款",
      "sort": 1
    }
  ],
  "enableHistory": 1,
  "maxHistory": 10,
  "skills": [
    {
      "skillRegistryId": 21,
      "isActive": 1,
      "sortIndex": 0
    }
  ],
  "mcpTools": []
}
```

响应示例：

```jsonc
{
  "code": 200,
  "msg": "数字员工创建成功",
  "data": {
    "id": 1001, // 新建数字员工 ID；后续开放聊天和 iframe 嵌入使用
    "robotCode": "contract_review_agent", // 后续按编码查询时使用
    "robotName": "合同审核助手",
    "avatarUrl": "https://example.com/avatar.png",
    "welcomeMessage": "你好，我可以帮你审核合同。",
    "quickQuestions": [],
    "enableSuggestedReplies": 0,
    "enableToolCallDisplay": 1,
    "businessLine": "legal",
    "businessLineName": "法务",
    "isActive": 1,
    "enableAgentCollaboration": 0,
    "collaborationScope": null,
    "appMenus": [],
    "chatModelId": 1, // 实际绑定的聊天模型
    "skillRegistryIds": [21], // 实际绑定的技能 ID
    "mcpToolIds": [] // 实际绑定的 MCP 工具 ID
  },
  "total": 0,
  "rows": null
}
```

实际创建时建议必填：

- `robotName`
- `systemPrompt`

Agent 使用：创建成功后保存 `data.id`、`data.robotCode`。如果下一步要嵌入，调用 `/api/ai/open/robots` 获取 `shareUrl`。

## 创建或复用开放聊天会话

```http
POST /api/ai/open/chat/session
```

请求体：

```json
{
  "robotId": 1001,
  "userId": "external-user-001",
  "userName": "张三",
  "sessionId": "",
  "contextData": {
    "customerId": "C001"
  }
}
```

响应示例：

```jsonc
{
  "code": 200,
  "msg": null,
  "data": {
    "sessionId": "S001", // 发送消息、查历史、删除会话都要用
    "robotName": "合同审核助手",
    "avatarUrl": "https://example.com/avatar.png",
    "businessLine": "legal",
    "businessLineName": "法务",
    "welcomeMessage": "你好，我可以帮你审核合同。",
    "quickQuestions": [],
    "enableSuggestedReplies": 0,
    "enableToolCallDisplay": 1,
    "enableAsr": false,
    "enableTts": false
  },
  "total": 0,
  "rows": null
}
```

## 发送开放聊天消息

```http
POST /api/ai/open/chat/send?ctx.source=crm
```

请求体：

```json
{
  "robotId": 1001,
  "userId": "external-user-001",
  "userName": "张三",
  "sessionId": "S001",
  "content": "帮我总结这个客户最近的订单",
  "files": [],
  "contextData": {
    "customerId": "C001"
  },
  "stream": false
}
```

非流式响应示例：

```jsonc
{
  "code": 200,
  "msg": null,
  "data": {
    "sessionId": "S001", // 当前会话 ID
    "requestId": "req-001",
    "message": "客户最近有 3 笔订单，总金额 1200 元。", // AI 回复正文
    "cardData": "{\"title\":\"客户订单摘要\"}", // 卡片原始 JSON 字符串
    "card": {
      "type": "card",
      "cardData": {
        "title": "客户订单摘要"
      }
    },
    "suggestedReplies": [
      {
        "label": "查看明细",
        "message": "帮我查看订单明细"
      }
    ],
    "attachments": []
  },
  "total": 0,
  "rows": null
}
```

流式模式：`stream=true` 时返回 `text/event-stream`，常见事件为 `text`、`tool_call`、`tool_result`、`card`、`done`、`error`。

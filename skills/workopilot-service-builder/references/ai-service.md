# AI 服务接口

基础路由：`/api/aiagent`

## 返回结构速记

查询和创建接口返回 `ApiResult<T>`：

```json
{
  "code": 200,
  "msg": null,
  "data": {},
  "total": 0,
  "rows": []
}
```

执行接口 `/api/aiagent/run` 直接返回 `AiServiceExecuteRes`，不是 `ApiResult<T>`。

## 什么时候需要 AI 服务

当第三方系统需要把某个稳定、可复用的 AI 能力封装成接口时，应创建 AI 服务。典型场景：

- 从文本、图片、PDF 中提取结构化字段
- 根据业务输入生成摘要、报告、邮件、报价说明、审核意见
- 把一段业务规则和提示词固定下来，让外部系统通过 `/api/aiagent/run` 重复调用
- 需要异步执行、文件输入、多轮对话或标准化输出格式

如果只是让用户和数字员工自然对话，优先使用数字员工开放聊天接口；如果需要“外部系统像调用函数一样调用 AI 能力”，优先创建 AI 服务。

## inputs 与提示词占位规则

`inputs` 是 AI 服务的入参定义。Agent 必须根据用户业务需求设计 `inputs`，不要固定只用 `user_message`。

设计规则：

- 每个业务变量都应有一个清晰的 `name`，例如 `contract_text`、`customer_name`、`invoice_url`
- `name` 使用英文、数字、下划线，避免中文、空格和特殊符号
- `type` 描述数据类型，例如 `string`、`number`、`boolean`、`array`、`object`
- `desc` 写清楚该字段含义，方便开发者传参
- `ui` 可用于提示前端展示方式，例如 `input`、`textarea`、`select`、`file`
- 如果需要枚举值，可用 `options` 描述

`systemPrompt` 必须使用 `{{input_name}}` 形式引用输入字段，其中 `input_name` 就是 `inputs[*].name` 的值。创建 AI 服务时，Agent 要把提示词配置好，而不是只创建空壳服务。

示例：

```jsonc
{
  "inputs": [
    {
      "name": "contract_text", // run.inputs.contract_text 必须传同名字段
      "type": "string",
      "desc": "合同全文",
      "ui": "textarea"
    },
    {
      "name": "review_focus", // run.inputs.review_focus 必须传同名字段
      "type": "string",
      "desc": "审核重点，例如付款条款、违约责任、保密条款",
      "ui": "input"
    }
  ],
  "systemPrompt": "你是合同审核助手。请基于以下合同内容进行审核：{{contract_text}}。重点关注：{{review_focus}}。请输出风险点、原因和修改建议。"
}
```

注意：占位符使用 `{{contract_text}}`，不是 `{{inputs.contract_text}}`。`/api/aiagent/run` 时，`inputs` 对象必须包含同名 key：

```json
{
  "serviceCode": "contract_review",
  "inputs": {
    "contract_text": "合同正文...",
    "review_focus": "付款条款"
  }
}
```

Agent 创建 AI 服务前应检查：

- `inputs[*].name` 是否都能在 `systemPrompt` 中找到 `{{name}}`
- `systemPrompt` 是否明确角色、任务、输入使用方式、输出格式
- `outputType=JSON` 时，提示词是否明确 JSON 字段和不要输出额外解释
- 创建后是否用 `/api/aiagent/run` 传一组示例 `inputs` 做验证

## 查询 AI 服务

```http
POST /api/aiagent/external/list
```

请求体：

```json
{
  "serviceCode": "invoice_extract",
  "serviceName": "发票",
  "isActive": 1,
  "pageNum": 1,
  "pageSize": 20
}
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
      "id": 123, // AI 服务 ID
      "serviceName": "发票识别",
      "serviceCode": "invoice_extract", // 执行服务时传给 /api/aiagent/run
      "description": "提取发票字段并返回 JSON",
      "executionMode": "CHAT",
      "outputType": "JSON", // 影响 run 的 data 内容形态
      "isActive": 1, // 1=启用
      "isAsync": 0, // 1=默认异步，执行后关注 taskId
      "tags": "[\"外部Agent\"]",
      "groupId": 456,
      "createTime": "2026-06-15T10:00:00",
      "updateTime": "2026-06-15T10:10:00"
    }
  ]
}
```

字段说明：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `rows[].id` | long | AI 服务 ID |
| `rows[].serviceCode` | string | 执行服务时传给 `/api/aiagent/run` 的编码 |
| `rows[].isAsync` | int | `1` 表示默认异步；执行后需要关注 `taskId` |
| `rows[].outputType` | string | 输出格式：`TEXT`、`MARKDOWN`、`JSON` |

Agent 使用：如果按 `serviceCode` 查到 `rows[0]`，配置脚本应复用该服务，不要重复创建。

## 查询可用模型

```http
GET /api/aiagent/external/models
```

响应示例：

```jsonc
{
  "code": 200,
  "msg": null,
  "data": null,
  "total": 1,
  "rows": [
    {
      "aiModelId": 789, // 创建 AI 服务时优先传入 aiModelId
      "modelName": "gpt-4.1-mini",
      "modelCode": "gpt-4.1-mini",
      "modelType": "chat", // 通常应选择聊天模型
      "modelLevel": "normal",
      "providerCode": "openai",
      "providerName": "OpenAI",
      "isDefault": 1, // 默认模型
      "temperature": 0.7,
      "topP": 1,
      "maxTokens": 4096
    }
  ]
}
```

字段说明：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `rows[].aiModelId` | long | 创建 AI 服务时优先传入 `aiModelId` |
| `rows[].modelType` | string | 通常应选择聊天模型 |
| `rows[].isDefault` | int | 默认模型标记 |

Agent 使用：优先选择 `isDefault=1` 且 `modelType` 为聊天类的模型；如果用户指定模型名，则按 `modelName` 或 `modelCode` 匹配。

## 创建 AI 服务

```http
POST /api/aiagent/external/create
```

请求体：

```json
{
  "serviceName": "合同审核",
  "serviceCode": "contract_review",
  "description": "根据合同正文和审核重点输出风险点",
  "systemPrompt": "你是合同审核助手。请基于以下合同内容进行审核：{{contract_text}}。重点关注：{{review_focus}}。请以 JSON 输出 riskItems 数组，每项包含 title、reason、suggestion。",
  "outputType": "JSON",
  "isAsync": 0,
  "inputs": [
    {
      "name": "contract_text",
      "type": "string",
      "desc": "合同全文",
      "ui": "textarea"
    },
    {
      "name": "review_focus",
      "type": "string",
      "desc": "审核重点",
      "ui": "input"
    }
  ],
  "aiModelId": 789
}
```

响应示例：

```jsonc
{
  "code": 200,
  "msg": null,
  "data": {
    "id": 123, // 新建 AI 服务 ID
    "serviceName": "发票识别",
    "serviceCode": "invoice_extract", // 后续执行服务必须保存这个值
    "description": "提取发票字段并返回 JSON",
    "executionMode": "CHAT",
    "outputType": "JSON", // 执行结果期望格式
    "isActive": 1, // 1=启用
    "isAsync": 0, // 1=异步服务
    "tags": "[\"外部Agent\"]",
    "groupId": 456,
    "createTime": "2026-06-15T10:00:00",
    "updateTime": null
  },
  "total": 0,
  "rows": null
}
```

字段说明：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `data.id` | long | 新建 AI 服务 ID |
| `data.serviceCode` | string | 后续执行服务时的关键字段，必须保存 |
| `data.isAsync` | int | 创建后的异步配置 |

模型兜底规则：

1. 优先使用 `aiModelId`
2. 其次使用 `modelProvider + modelName`
3. 再使用租户默认聊天模型
4. 如果没有可用模型，返回 `500`

Agent 使用：创建完成后至少记录 `data.serviceCode`；如需立即验证，调用 `/api/aiagent/run`。

## 执行 AI 服务

```http
POST /api/aiagent/run
```

请求体：

```json
{
  "serviceCode": "contract_review",
  "routeCode": null,
  "inputs": {
    "contract_text": "甲方应在收到发票后 90 日内付款...",
    "review_focus": "付款条款和违约责任"
  },
  "conversationId": "",
  "isAsync": false,
  "files": []
}
```

同步响应示例：

```jsonc
{
  "code": 200, // 500 表示执行失败
  "message": "Success",
  "data": {
    "riskItems": [
      {
        "title": "付款周期较长",
        "reason": "约定收到发票后 90 日内付款，回款周期偏长。",
        "suggestion": "建议协商缩短至 30 日或增加逾期付款责任。"
      }
    ]
  }, // AI 服务输出，结构由 outputType 和提示词决定
  "usage": {
    "inputTokens": 100,
    "outputTokens": 50,
    "totalTokens": 150
  }, // token 消耗
  "conversationId": "conv_xxx", // 多轮对话时下次继续传
  "taskId": null // null 表示同步已完成
}
```

异步响应示例：

```jsonc
{
  "code": 200,
  "message": "任务已提交",
  "data": null,
  "usage": null,
  "conversationId": "conv_xxx",
  "taskId": 987654321 // 有值时调用 /api/aiagent/task/result 查询
}
```

字段说明：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | int | 执行状态；`500` 表示失败 |
| `message` | string | 执行消息 |
| `data` | object/string | AI 服务输出，类型取决于 `outputType` 和提示词 |
| `usage` | object | token 消耗信息 |
| `conversationId` | string | 多轮对话 ID，后续请求可继续传入 |
| `taskId` | long | 异步任务 ID，有值时需要查询任务结果 |

## 查询异步任务结果

```http
GET /api/aiagent/task/result?taskId=123
```

响应示例：

```jsonc
{
  "code": 200,
  "msg": null,
  "data": {
    "id": 123, // 任务 ID
    "taskStatus": "SUCCESS", // 任务状态
    "taskStatusId": 20, // 状态 ID，具体枚举以服务端为准
    "progress": 100, // 0-100
    "output": "{\"riskItems\":[{\"title\":\"付款周期较长\",\"reason\":\"约定收到发票后 90 日内付款，回款周期偏长。\",\"suggestion\":\"建议协商缩短至 30 日或增加逾期付款责任。\"}]}", // 最终输出，可能是 JSON 字符串
    "errorMsg": null, // 有值时说明执行失败或部分失败
    "fileResources": null,
    "costTokens": 150, // token 消耗
    "retryCount": 0,
    "createTime": "2026-06-15T10:00:00",
    "finishTime": "2026-06-15T10:01:00"
  },
  "total": 0,
  "rows": null
}
```

Agent 使用：当 `progress < 100` 或 `taskStatus` 表示处理中时继续轮询；当 `errorMsg` 有值时向用户说明失败原因；最终读取 `data.output`。

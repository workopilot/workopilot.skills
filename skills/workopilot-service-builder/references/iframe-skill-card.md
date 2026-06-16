# Iframe 技能卡片

Iframe 技能卡片用于“数字员工先理解用户问题并生成结果，再把结构化业务结果交给一个外部页面展示或继续办理”的场景。典型例子：

- 订单、客户、合同、工单、审批等业务详情展示。
- AI 先检索或生成结果，再打开一个可交互表单让用户确认。
- AI 返回摘要，卡片中展示更完整的 JSON、Markdown、图表或第三方系统页面。

不适合的场景：

- 只是把数字员工聊天窗口嵌入第三方系统，应使用 `references/iframe-embed.md`。
- 需要服务端长期保存或处理 APIKEY 的逻辑，不要放在 iframe 前端，应放到开发者后端。
- 只是执行纯文本问答，不需要额外业务页面时，不必创建 iframe 卡片。

## 需求确认

创建卡片前，Agent 必须向开发者确认或从上下文中明确以下信息：

| 问题 | 影响 |
| --- | --- |
| 卡片展示什么业务对象 | 决定 `skillName`、`skillCode`、`triggerPrompt` 和页面路由 |
| 卡片何时被数字员工触发 | 决定 `triggerPrompt`，模型只有理解触发条件后才会调用 `showCard` |
| 业务数据是直接传入还是按 ID 查询 | 决定使用 `businessData`，还是只传 `businessId` 后由 iframe 调开发者后端查询 |
| 是否需要当前登录者信息 | 需要时由开发者后端调用 runtime 用户接口 |
| iframe URL 当前是本地测试地址还是生产地址 | 本地地址可测试，发布后必须更新为公网/内网可访问地址 |

如果业务数据来源不明确，Agent 需要先解释两种接入方式并让开发者确认：

- 轻量数据：通过 `showCard.businessData` 直接传给卡片。
- 大数据或敏感数据：通过 `showCard.businessId` 传业务 ID，iframe 调开发者后端查询详情。

不要假设喔壳存在通用“获取当前业务数据”的开放接口。当前业务 ID 和业务数据来自数字员工触发卡片时传入的 `showCard` 参数，或来自开发者自己的业务系统。

## 注册卡片

```http
POST /api/ai/skill-registry/external/iframe-card
API-KEY: <WORKOPILOT_API_KEY>
Content-Type: application/json
```

请求体：

```json
{
  "skillName": "订单详情卡片",
  "skillCode": "order_detail_iframe",
  "skillCategory": "ORDER",
  "skillDesc": "展示订单详情外部页面",
  "skillIcon": "link",
  "url": "http://localhost:5173/order-detail",
  "triggerPrompt": "当已经获得可查看的订单详情结果时，调用 showCard 展示订单详情卡片。调用时必须传入 skillCode=order_detail_iframe；如果有订单ID则传 businessId；如果已有订单摘要JSON则传 businessData。",
  "titlePrompt": "根据订单结果生成一句20字内标题",
  "drawerTitle": "订单详情",
  "drawerWidth": "wide",
  "sortIndex": 100
}
```

本地开发时，`url` 可以先配置为你当前卡片的url地址， `http://localhost:5173/...` 或 `http://127.0.0.1:5173/...` 进行测试。发布后必须更新为实际部署地址，否则终端用户无法打开卡片页面。

响应示例（`jsonc`，带注释，不可直接作为 JSON 发送）：

```jsonc
{
  "code": 200,
  "msg": "Iframe技能卡片已注册",
  "data": {
    "id": 123, // skillRegistryId；创建数字员工或绑定已有数字员工时使用
    "skillName": "订单详情卡片",
    "skillCode": "order_detail_iframe", // showCard 调用时必须传这个编码
    "skillCategory": "ORDER",
    "skillDesc": "展示订单详情外部页面",
    "skillIcon": "link",
    "skillKind": "BUSINESS_CARD",
    "skillSource": "TENANT_CUSTOM",
    "ownerTenantId": "tenant_001",
    "reviewStatus": "APPROVED",
    "defaultToolsConfig": {
      "tools": [
        {
          "code": "showCard", // 数字员工可调用的工具
          "name": "showCard",
          "is_active": true
        }
      ]
    },
    "defaultCardConfig": {
      "card_type": "iframe_card",
      "trigger_prompt": "当已经获得可查看的订单详情结果时，调用 showCard 展示订单详情卡片。",
      "title_prompt": "根据订单结果生成一句20字内标题",
      "action": "open_drawer",
      "drawer_code": "order_detail_iframe_drawer"
    },
    "defaultDrawerConfig": {
      "drawer_code": "order_detail_iframe_drawer",
      "drawer_mode": "URL",
      "title": "订单详情",
      "drawer_url": "http://localhost:5173/order-detail", // iframe 打开的页面地址
      "drawer_width": "wide"
    },
    "isActive": 1,
    "sortIndex": 100
  },
  "total": 0,
  "rows": null
}
```

Agent 读取字段：

| 字段 | 用途 |
| --- | --- |
| `data.id` | `skillRegistryId`，绑定数字员工时使用 |
| `data.skillCode` | `showCard.skillCode` 必须使用这个值 |
| `data.defaultDrawerConfig.drawer_url` | 检查当前是否仍是本地测试 URL |

## 绑定数字员工

创建数字员工时，可以直接把卡片绑定进去：

```json
{
  "robotName": "订单助手",
  "systemPrompt": "你是订单助手。查询到订单详情后，如果用户需要查看完整订单信息，调用 showCard 打开订单详情卡片。",
  "skills": [
    {
      "skillRegistryId": 123,
      "isActive": 1,
      "sortIndex": 0
    }
  ]
}
```

如果数字员工已经存在，当前 APIKEY 开放接口没有独立的“更新已有数字员工并绑定卡片”接口。可选方式：

- 使用喔壳管理台绑定技能卡片。
- 使用后台登录态接口 `POST /api/ai/robot/skill/save` 绑定，注意这是 `[Authorize]` 接口，不是 APIKEY 开放接口。

后台登录态绑定请求示例（仅用于管理台或内部集成）：

```json
{
  "robotId": 10001,
  "skillRegistryId": 123,
  "isActive": 1,
  "sortIndex": 0
}
```

Agent 不要把 `POST /api/ai/robot/skill/save` 描述成第三方 APIKEY 接口。

## 数字员工如何触发卡片

注册卡片后，数字员工不会自动打开卡片。必须同时满足：

1. 卡片已注册并绑定到当前数字员工。
2. `triggerPrompt` 清楚描述何时调用卡片。
3. 数字员工的系统提示词中也说明需要在对应场景调用 `showCard`。
4. 模型在对话中调用 `showCard` 工具。

`showCard` 工具参数：

```jsonc
{
  "skillCode": "order_detail_iframe", // 必填，注册卡片返回的 data.skillCode
  "summary": "已找到订单 ORD-20260615001", // 必填，卡片副标题或摘要
  "highlights": ["客户：张三", "金额：1280元", "状态：待确认"], // 可选，最多建议 3 条
  "titleHint": "订单详情", // 可选，给卡片标题生成使用
  "businessId": "ORD-20260615001", // 可选，当前业务 ID；没有则传空字符串
  "businessData": "{\"orderNo\":\"ORD-20260615001\",\"amount\":1280}", // 可选，小型业务数据
  "businessDataType": "json" // 可选：json、markdown、text、auto
}
```

提示词建议：

```text
当用户查询订单详情、需要查看完整订单信息或需要进入订单办理页面时，
在得到订单号和必要摘要后调用 showCard。
调用参数要求：
- skillCode 固定为 order_detail_iframe
- businessId 填订单号
- 如果已经拿到订单摘要 JSON，businessData 填 JSON 字符串，businessDataType 填 json
- 不要在未确定订单号时打开卡片
```

## runtimeToken 如何获取

`runtimeToken` 是喔壳在运行时生成的上下文令牌，用来让第三方后端安全读取当前会话、数字员工、租户和用户信息。

常见获取方式：

- iframe 卡片打开时，喔壳会在卡片运行上下文中生成 runtimeToken，并可通过 URL 查询参数传入，例如 `?runtimeToken=rt_xxx`。
- 如果 URL 中没有 `runtimeToken`，先检查卡片/抽屉配置和平台版本，不要让 iframe 前端自己伪造。
- iframe 前端只读取并转发 `runtimeToken` 给开发者后端；不要在前端保存或使用 APIKEY。

iframe 前端读取示例：

```js
const params = new URLSearchParams(window.location.search);
const runtimeToken = params.get('runtimeToken') || params.get('runtime_token');
```

开发者后端调用 runtime 接口时同时带上 APIKEY 和 runtimeToken：

```http
API-KEY: <WORKOPILOT_API_KEY>
X-Runtime-Token: <runtimeToken>
```

也支持把 token 放到查询参数 `runtimeToken`，但服务端转发时优先使用 `X-Runtime-Token` 请求头。

## 获取当前运行上下文

用于获取当前租户、开发者、安装关系、数字员工、会话、消息和 token 过期时间。

```http
GET /api/ai/runtime/context
API-KEY: <WORKOPILOT_API_KEY>
X-Runtime-Token: <runtimeToken>
```

响应示例（`jsonc`，带注释，不可直接作为 JSON 发送）：

```jsonc
{
  "code": 200,
  "msg": "success",
  "data": {
    "runtimeTenantId": "tenant_customer_001", // 当前使用方租户
    "runtimeTenantName": "客户公司",
    "developerTenantId": "tenant_dev_001", // 开发者租户
    "developerId": 12,
    "developerName": "喔壳开发者",
    "installId": 456, // 应用/服务安装关系 ID
    "assetType": "ROBOT",
    "assetId": "10001",
    "globalAgentKey": "agent_xxx",
    "robotId": "10001", // 当前数字员工 ID
    "robotName": "订单助手",
    "sessionId": "sess_abc", // 当前会话 ID
    "messageId": "789", // 触发卡片的消息 ID
    "externalUserId": "u_ext_001",
    "billingOwner": "TENANT",
    "billingTenantId": "tenant_customer_001",
    "scopes": ["runtime:context", "runtime:user"],
    "expiresAt": "2026-06-15T12:30:00Z",
    "user": {
      "userId": "u_001",
      "userName": "zhangsan",
      "nickName": "张三",
      "email": "zhangsan@example.com",
      "phoneNumber": "13800000000",
      "avatar": "https://example.com/avatar.png",
      "tenantId": "tenant_customer_001",
      "tenantName": "客户公司",
      "isPlatformUser": true
    }
  },
  "total": 0,
  "rows": null
}
```

Agent 读取字段：

| 字段 | 用途 |
| --- | --- |
| `data.robotId` / `data.robotName` | 判断当前由哪个数字员工触发 |
| `data.sessionId` / `data.messageId` | 关联当前对话和消息 |
| `data.runtimeTenantId` | 区分当前使用方租户 |
| `data.user` | 如果响应包含用户信息，可直接使用；否则调用用户 profile 接口 |
| `data.expiresAt` | 判断是否需要刷新 runtimeToken |

## 获取当前登录者信息

用于 iframe 卡片需要知道“当前是谁在操作”，例如按用户权限展示按钮、记录办理人、调用开发者系统的用户映射。

```http
GET /api/ai/runtime/user/profile
API-KEY: <WORKOPILOT_API_KEY>
X-Runtime-Token: <runtimeToken>
```

响应示例（`jsonc`，带注释，不可直接作为 JSON 发送）：

```jsonc
{
  "code": 200,
  "msg": "success",
  "data": {
    "userId": "u_001", // 当前登录者 ID
    "userName": "zhangsan",
    "nickName": "张三",
    "email": "zhangsan@example.com",
    "phoneNumber": "13800000000",
    "avatar": "https://example.com/avatar.png",
    "tenantId": "tenant_customer_001",
    "tenantName": "客户公司",
    "isPlatformUser": true
  },
  "total": 0,
  "rows": null
}
```

## 获取当前业务 ID 和业务数据

当前业务 ID 和业务数据来自 `showCard`，不是 runtime 接口自动推断出来的。

推荐规则：

- 有明确业务主键时，`showCard.businessId` 必须传入，例如订单号、合同 ID、工单 ID。
- 数据量小、无敏感字段时，可以把摘要或详情 JSON 放入 `showCard.businessData`。
- 数据量大或包含敏感字段时，只传 `businessId`，iframe 前端把 `businessId` 和 `runtimeToken` 发给开发者后端，开发者后端校验上下文后查询自己的业务系统。
- `businessDataType` 用来告诉卡片如何渲染：`json`、`markdown`、`text` 或 `auto`。

iframe 页面可以从 URL、宿主传参或卡片数据中读取 `businessId` / `businessData`。如果当前平台没有把这些值直接注入 URL，开发者应以后端接口为准，通过 runtime 上下文校验后按 `businessId` 查询业务数据。

开发者后端伪代码：

```js
app.post('/api/workopilot/order-card/context', async (req, res) => {
  const { runtimeToken, businessId, businessData } = req.body;

  // 1. 服务端调用喔壳 runtime/context，校验 token 和当前租户/用户/数字员工
  // 2. 如果 businessData 已满足展示需求，可直接返回
  // 3. 如果只有 businessId，到开发者自己的订单系统查询详情
  // 4. 返回 iframe 前端需要渲染的数据
});
```

如果需求方说“获取当前业务数据”，Agent 需要追问业务数据在哪个系统、是否允许由 AI 直接传入、是否需要按业务 ID 查询，不要直接承诺喔壳有统一业务数据读取接口。

## 刷新 runtimeToken

当 runtimeToken 过期时，开发者后端可使用 `runtimeRef` 刷新。`runtimeRef` 一般来自 runtimeToken 签发结果或平台提供的运行引用。

```http
POST /api/ai/runtime/token/refresh
API-KEY: <WORKOPILOT_API_KEY>
Content-Type: application/json
```

请求体：

```json
{
  "runtimeRef": {
    "tokenType": "CARD",
    "tenantId": "tenant_customer_001",
    "robotId": 10001,
    "globalAgentKey": "agent_xxx",
    "sessionId": "sess_abc",
    "messageId": 789,
    "skillCode": "order_detail_iframe",
    "drawerCode": "order_detail_iframe_drawer",
    "assetId": "10001",
    "installId": 456
  }
}
```

响应示例（`jsonc`，带注释，不可直接作为 JSON 发送）：

```jsonc
{
  "code": 200,
  "msg": "success",
  "data": {
    "runtimeToken": "rt_new_xxx", // 新 runtimeToken
    "expiresAt": "2026-06-15T13:00:00Z",
    "runtimeRef": {
      "tokenType": "CARD",
      "tenantId": "tenant_customer_001",
      "robotId": 10001,
      "globalAgentKey": "agent_xxx",
      "sessionId": "sess_abc",
      "messageId": 789,
      "skillCode": "order_detail_iframe",
      "drawerCode": "order_detail_iframe_drawer",
      "assetId": "10001",
      "installId": 456
    }
  },
  "total": 0,
  "rows": null
}
```

## 错误码处理

runtime 接口常见错误：

| HTTP/业务码 | 场景 | 处理建议 |
| --- | --- | --- |
| `401` / `TOKEN_EXPIRED` | token 已过期 | 使用 `runtimeRef` 刷新，或提示重新打开卡片 |
| `401` / `TOKEN_INVALID` | token 无效 | 不要重试，提示重新打开卡片 |
| `401` / `TOKEN_REVOKED` | token 已撤销 | 不要重试，提示重新打开卡片 |
| `403` / `Invalid API Key` | APIKEY 错误 | 检查服务端密钥配置 |
| `403` / `API_KEY_DEVELOPER_MISMATCH` | APIKEY 与开发者不匹配 | 检查卡片归属和开发者租户 |
| `403` / `INSTALL_DISABLED` | 安装关系禁用 | 提示管理员重新启用 |

## 安全要求

- APIKEY 只能放在开发者后端、环境变量或服务端密钥配置中。
- iframe 前端只能持有短期 `runtimeToken`，不要把 APIKEY 写入前端代码。
- 本地测试 URL 只能用于开发调试，发布后必须更新为可被用户访问的正式 URL。
- 如果卡片展示敏感业务数据，优先只传 `businessId`，由开发者后端结合 runtime 用户信息和租户信息再次鉴权。

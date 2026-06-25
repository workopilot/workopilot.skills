# 应用菜单 Iframe 与 RuntimeToken 对接

本文档用于数字员工旁边的业务菜单页面对接，例如“报价单助理”旁边的“报价单历史”“客户管理”等菜单。它不是对话里的 `showCard` 技能卡片，也不是把数字员工聊天窗口嵌入第三方系统。

## 场景区分

| 类型 | 入口 | 用途 | 读取文档 |
| --- | --- | --- | --- |
| 数字员工聊天嵌入 | `/embed/chat/{robotId}` | 把完整数字员工聊天窗口嵌入第三方系统 | `iframe-embed.md` |
| Iframe 技能卡片 | 对话中调用 `showCard` 后打开抽屉 | AI 在对话里触发业务卡片 | `iframe-skill-card.md` |
| 应用菜单 iframe | `/app/{appCode}/employee/{robotId}/{menuKey}` | 数字员工工作台旁边的固定业务菜单 | 本文档 |

当用户说“数字员工旁边的菜单”“报价单历史菜单”“app 下面的菜单”“业务菜单 iframe”时，优先使用本文档。

## Agent 工作方式

应用菜单创建/更新属于喔壳配置动作，优先由 Agent 调用脚本完成：

```bash
python scripts/configure_app_menu.py \
  --employee-id 1001 \
  --action create \
  --config app-menu.json
```

不要把创建/更新菜单接口当成开发者业务系统运行时依赖。开发者真正需要实现的是：

1. 菜单 `iframeUrl` 对应的业务页面。
2. 业务后端的 `/sso/workopilot/exchange` 等换票接口。
3. 用 `runtimeToken` 调喔壳 runtime 接口校验当前租户、用户、数字员工和菜单。

配置阶段可以先把 `iframeUrl` 写成本地地址用于测试，例如 `http://localhost:5173/quote-history?...`。发布后必须再次调用 `configure_app_menu.py --action update` 更新为正式 HTTPS 地址。

## 打开链路

应用菜单的前端路由：

```text
/app/{appCode}/employee/{robotId}/{menuKey}
```

加载流程：

1. 用户登录喔壳应用工作台。
2. 前端调用 `GET /api/app/runtime/{appCode}` 获取数字员工和菜单配置。
3. 用户点击某个 iframe 菜单。
4. 前端调用 `POST /api/app/menu-runtime-token` 签发菜单级 `runtimeToken`。
5. 前端把 `runtimeToken`、`userId`、`tenantId` 追加到菜单 `iframeUrl`。
6. iframe 页面读取这些参数，并把 `runtimeToken` 发给开发者后端。
7. 开发者后端用 `API-KEY + X-Runtime-Token` 调喔壳 runtime 接口校验上下文。

## 创建和更新应用菜单

应用菜单是数字员工的附属配置。使用 APIKEY 创建或更新时，不需要传完整 `RobotAppConfigDto`，只传菜单必要字段；后端会自动把菜单配置为 `iframe` 类型，并自动启用该数字员工的应用菜单入口。

### 创建菜单

```http
POST /api/ai/robot/external/{robotId}/app-menu
API-KEY: <WORKOPILOT_API_KEY>
Content-Type: application/json
```

请求示例：

```jsonc
{
  "title": "报价单历史", // 菜单显示名称，必填
  "menuKey": "quote-history", // 可选但强烈建议传；使用英文、数字、下划线、短横线，中文标题不传时会生成随机 menu-xxxx
  "iframeUrl": "http://localhost:5173/quote-history?appCode=quotation&robotId=10001&menuKey=quote-history", // 必填，本地测试可用 localhost
  "icon": "lucide:history", // 可选；使用 lucide 图标库，也可简写为 "history"
  "sort": 10, // 可选；不传时自动排在最后
  "isEnabled": true // 可选；默认 true
}
```

响应示例：

```jsonc
{
  "code": 200,
  "msg": "应用菜单创建成功",
  "data": {
    "id": 90001,
    "menuType": "iframe",
    "displayMode": "fullscreen",
    "menuKey": "quote-history",
    "title": "报价单历史",
    "icon": "lucide:history",
    "routePath": "quote-history",
    "componentPath": null,
    "iframeUrl": "http://localhost:5173/quote-history?appCode=quotation&robotId=10001&menuKey=quote-history",
    "directUrl": null,
    "sort": 10,
    "isEnabled": true
  }
}
```

### 更新菜单

```http
PUT /api/ai/robot/external/{robotId}/app-menu/{menuKey}
API-KEY: <WORKOPILOT_API_KEY>
Content-Type: application/json
```

请求体为部分更新，未传字段保持原值。发布后把本地测试地址更新为正式 HTTPS 地址：

```jsonc
{
  "title": "报价单历史",
  "iframeUrl": "https://quote.example.com/history?appCode=quotation&robotId=10001&menuKey=quote-history",
  "icon": "lucide:file-clock",
  "sort": 10,
  "isEnabled": true
}
```

图标使用前端 Iconify/Lucide 图标名，推荐格式为 `lucide:<name>`。常用示例：`lucide:history`、`lucide:file-clock`、`lucide:table-2`、`lucide:clipboard-list`、`lucide:users`、`lucide:database`。如果只传 `history`，后端会自动保存为 `lucide:history`。

## Iframe URL 参数

应用菜单 iframe 会自动追加：

| 参数 | 说明 |
| --- | --- |
| `runtimeToken` | 菜单级短期运行时令牌 |
| `userId` | 当前喔壳登录用户 ID |
| `tenantId` | 当前喔壳租户 ID |

不会自动追加：

| 参数 | 说明 |
| --- | --- |
| `appCode` | 如业务页面需要，建议预先写进 `iframeUrl` |
| `robotId` | 如业务页面需要，建议预先写进 `iframeUrl` |
| `menuKey` | 如业务页面需要，建议预先写进 `iframeUrl` |
| `API-KEY` | 不能放到浏览器或 iframe URL 中 |
| `access_token` | 不把喔壳登录 JWT 暴露给 iframe 页面 |

菜单配置示例：

```text
https://quote.example.com/history?appCode=quotation&robotId=10001&menuKey=history
```

实际 iframe 加载地址类似：

```text
https://quote.example.com/history?appCode=quotation&robotId=10001&menuKey=history&userId=10086&tenantId=tenant_001&runtimeToken=rt_xxx
```

## 前端读取参数

iframe 页面只读取并转发 `runtimeToken`，不要在前端调用喔壳 runtime 接口，因为 runtime 接口还需要 `API-KEY`。

```js
const params = new URLSearchParams(window.location.search);

const workopilotContext = {
  runtimeToken: params.get('runtimeToken') || '',
  tenantId: params.get('tenantId') || '',
  userId: params.get('userId') || '',
  appCode: params.get('appCode') || '',
  robotId: params.get('robotId') || '',
  menuKey: params.get('menuKey') || '',
};

if (!workopilotContext.runtimeToken) {
  throw new Error('缺少喔壳菜单 runtimeToken');
}
```

## 开发者后端换取业务会话

推荐 iframe 页面先调用开发者自己的后端：

```http
POST /sso/workopilot/exchange
Content-Type: application/json
```

请求示例：

```jsonc
{
  "runtimeToken": "rt_xxx", // iframe URL 中读取
  "tenantId": "tenant_001", // 兼容展示用，最终以后端 runtime 校验结果为准
  "userId": "10086",
  "appCode": "quotation",
  "robotId": "10001",
  "menuKey": "history"
}
```

开发者后端处理流程：

1. 从服务端环境变量读取 `WORKOPILOT_API_KEY`。
2. 调用 `GET /api/ai/runtime/context` 校验 `runtimeToken`。
3. 校验 `data.assetType === "APP_MENU"`。
4. 从 `data.assetId` 解析 `appCode:robotId:menuKey`，例如 `quotation:10001:history`。
5. 校验租户映射、用户映射、菜单白名单。
6. 签发开发者系统自己的短期 token 或 `HttpOnly` cookie。

Node.js 伪代码：

```js
async function exchangeWorkopilotMenuSession(req, res) {
  const { runtimeToken } = req.body;
  const response = await fetch(
    `${process.env.WORKOPILOT_BASE_URL}/api/ai/runtime/context`,
    {
      headers: {
        'API-KEY': process.env.WORKOPILOT_API_KEY,
        'X-Runtime-Token': runtimeToken,
      },
    },
  );

  const result = await response.json();
  if (!response.ok || result.code !== 200) {
    throw new Error(result.msg || '喔壳 runtimeToken 校验失败');
  }

  const context = result.data;
  if (context.assetType !== 'APP_MENU') {
    throw new Error('runtimeToken 不是应用菜单类型');
  }

  const [appCode, robotId, menuKey] = String(context.assetId || '').split(':');

  // 继续校验租户、用户、菜单白名单，然后签发开发者业务系统自己的会话
  return createBusinessSession({
    tenantId: context.runtimeTenantId,
    user: context.user,
    appCode,
    robotId,
    menuKey,
  });
}
```

## Runtime 接口

### 获取菜单上下文

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
    "runtimeTenantId": "tenant_001", // 当前使用方租户
    "runtimeTenantName": "客户公司",
    "developerTenantId": "tenant_001", // 菜单 token 对应 APIKEY 所属租户
    "assetType": "APP_MENU", // 固定表示应用菜单 iframe
    "assetId": "quotation:10001:history", // appCode:robotId:menuKey
    "robotId": "10001",
    "robotName": "报价单助理",
    "externalUserId": "10086", // 当前喔壳用户 ID
    "billingOwner": "RUNTIME_TENANT",
    "billingTenantId": "tenant_001",
    "scopes": [
      "runtime.context.read",
      "user.profile.basic.read",
      "app.menu.read"
    ],
    "expiresAt": "2026-06-25T18:30:00+08:00",
    "user": {
      "userId": "10086",
      "userName": "zhangsan",
      "nickName": "张三",
      "tenantId": "tenant_001",
      "tenantName": "客户公司",
      "isPlatformUser": true
    }
  }
}
```

Agent 需要读取：

| 字段 | 用途 |
| --- | --- |
| `data.assetType` | 必须是 `APP_MENU` |
| `data.assetId` | 解析 `appCode:robotId:menuKey` |
| `data.runtimeTenantId` | 做租户映射 |
| `data.user` / `data.externalUserId` | 做用户映射和权限判断 |
| `data.expiresAt` | 判断 token 是否已过期 |

### 获取当前登录者信息

```http
GET /api/ai/runtime/user/profile
API-KEY: <WORKOPILOT_API_KEY>
X-Runtime-Token: <runtimeToken>
```

用于只需要用户信息、不需要菜单上下文的场景。多数应用菜单 SSO 场景建议优先调 `runtime/context`，因为它同时包含菜单、数字员工和用户信息。

## 错误处理

| 错误 | 说明 | 处理 |
| --- | --- | --- |
| `TOKEN_EXPIRED` | token 已过期 | 提示用户刷新或重新打开菜单 |
| `TOKEN_INVALID` | token 无效 | 不要重试，重新打开菜单 |
| `API Key missing` | 后端没有带 APIKEY | 检查服务端环境变量 |
| `Invalid API Key` | APIKEY 无效或过期 | 重新配置 APIKEY |
| `API_KEY_DEVELOPER_MISMATCH` | APIKEY 与 token 所属租户不匹配 | 检查菜单所属租户和后端 APIKEY |

## 安全要求

- `API-KEY` 只能放在开发者后端，不能进入 iframe 前端。
- 前端 URL 中的 `userId`、`tenantId` 只是兼容上下文，强校验必须以 runtime 接口返回为准。
- 开发者后端必须校验 `assetType`、`assetId`、租户映射和用户权限。
- 生产环境 iframe URL 使用 HTTPS。
- 如果使用本地 `localhost` URL 测试，发布后必须更新为正式地址。

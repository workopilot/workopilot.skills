# Iframe 嵌入

iframe 嵌入使用嵌入 token 和 `postMessage` 通信，不应在浏览器中使用 APIKEY。

## 嵌入地址

```text
https://your-domain/embed/chat/{robotId}?token={embedToken}&externalUserId={userId}&externalUserName={userName}
```

可选参数：

```text
&menuKey={menuKey}
```

以下开放接口可以返回 `shareUrl` 和菜单 `directUrl` 模板：

- `GET /api/ai/open/robots`
- `GET /api/ai/open/robot/profile`

## configure 消息

iframe 发送 `ready` 后，由宿主发送：

```jsonc
{
  "source": "wiseai-host", // 宿主固定使用 wiseai-host
  "type": "command", // 宿主发给 iframe 的命令
  "action": "configure", // 配置注入
  "requestId": "cfg-001", // 建议每次请求唯一，便于追踪
  "payload": {
    "contextData": {
      "hostApp": "crm", // 宿主系统标识
      "customerId": "C001" // 业务上下文，会注入数字员工运行上下文
    },
    "capabilities": {
      "contextSync": true, // 允许同步上下文
      "filePicker": false, // 是否允许 iframe 请求宿主选文件
      "hostActions": true, // 是否允许数字员工调用宿主动作
      "microphone": false, // 宿主是否协作麦克风
      "speaker": false // 宿主是否协作扬声器
    },
    "theme": "deepBlue", // 可选主题
    "frontendActions": [] // 宿主动作白名单
  }
}
```

iframe `ready` 事件示例：

```jsonc
{
  "source": "wiseai-embed", // iframe 固定使用 wiseai-embed
  "type": "event",
  "action": "ready", // 收到后宿主可以发送 configure
  "requestId": "evt-001",
  "payload": {
    "robotId": "1001",
    "robotCode": "contract_review_agent",
    "sessionId": "S001",
    "initialMode": "text",
    "contextData": {},
    "capabilities": {
      "contextSync": true,
      "filePicker": false,
      "hostActions": false,
      "microphone": false,
      "speaker": false
    }
  }
}
```

host-action 示例：

```jsonc
{
  "source": "wiseai-embed",
  "type": "host-action", // iframe 请求宿主执行动作
  "action": "openOrder", // 必须在宿主白名单 frontendActions 中
  "requestId": "host-action-001",
  "payload": {
    "orderNo": "SO001",
    "sessionId": "S001"
  }
}
```

action-result 示例：

```jsonc
{
  "source": "wiseai-host",
  "type": "action-result",
  "action": "action-result",
  "requestId": "host-action-001", // 对应 host-action 的 requestId
  "payload": {
    "success": true,
    "state": "granted", // granted/denied/blocked/unsupported
    "message": "已打开订单",
    "errorCode": null,
    "payload": {
      "orderNo": "SO001"
    }
  }
}
```

## 常见宿主命令

- `configure`
- `updateContext`
- `sendToBot`
- `sendToUser`
- `openVoice`
- `closeVoice`

## 常见 iframe 事件

- `ready`
- `state-change`
- `voice-exit`
- `session-created`
- `assistant-message-finished`
- `assistant-audio-finished`
- `business-open`

## 安全要求

- 校验 `event.origin`
- 只处理 `source === "wiseai-embed"` 的消息
- 只执行白名单内的 `host-action`
- APIKEY 只能放在服务端或本地安全配置中，不要放进 iframe URL 或前端代码

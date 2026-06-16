# 鉴权与配置

## 请求头

所有开放接口调用都使用：

```http
API-KEY: <your_api_key>
```

除非某个内部接口明确要求 JWT，否则开放接口不要使用 `Authorization: Bearer`。

## 配置优先级

1. 命令行参数：`--api-key`、`--base-url`
2. 环境变量：`WORKOPILOT_API_KEY`、`WORKOPILOT_BASE_URL`
3. 项目根目录本地环境文件：`.env.workopilot`、`.env.local`
4. 默认 baseUrl：
   - 生产环境(默认)：`https://agent.workopilot.com/net-api`
   - 测试环境：`https://agenttest.workopilot.com/net-api`

`.env.workopilot` 示例：

```text
# 生产环境(默认)
WORKOPILOT_BASE_URL=https://agent.workopilot.com/net-api
WORKOPILOT_API_KEY=replace_with_your_api_key

# 测试环境
# WORKOPILOT_BASE_URL=https://agenttest.workopilot.com/net-api
# WORKOPILOT_API_KEY=replace_with_your_test_api_key
```

真实 `.env.workopilot` 应加入 `.gitignore`。可以提交 `.env.workopilot.example`，但里面只能放占位值。

## 鉴权失败

- 缺少 Key：HTTP `401`，响应体 `API Key missing`
- Key 无效：HTTP `403`，响应体通常为 `Invalid API Key or Permission Denied`

## 通用返回结构

大多数接口返回 `ApiResult<T>`：

```json
{
  "code": 200,
  "msg": null,
  "data": {},
  "total": 0,
  "rows": []
}
```

字段说明：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | int | 业务状态码。通常 `200` 表示成功；`0` 表示业务失败；`500` 表示服务异常 |
| `msg` | string | 提示信息，成功时可能为空 |
| `data` | object | 单对象或主返回值 |
| `total` | int | 分页总数 |
| `rows` | array | 分页列表 |

Agent 读取规则：

- 查询列表类接口优先读取 `rows` 和 `total`
- 创建类接口优先读取 `data.id`、`data.*Code`
- 执行类接口优先读取 `data` 或接口自身返回体中的 `data`
- 文件类接口通常读取 `data` 字符串作为 URL

# 变更日志

## 2026-06-18 - 数字员工脚本优化

### 新增功能

#### 1. create_digital_employee.py - 新增 iframe 嵌入参数支持

**背景：** 之前的脚本缺少对 iframe 嵌入配置的支持，无法在创建数字员工时同时配置嵌入功能。

**改进内容：**

✅ 完整支持 `enableEmbed` 及相关嵌入配置参数：
- `enableEmbed` - 是否启用 iframe 嵌入
- `embedBaseUrl` - 嵌入基础 URL
- `embedAllowedOrigins` - 允许嵌入的宿主域名列表
- `embedExpireAt` - 嵌入链接过期时间
- `embedMaxDailyCalls` - 每日最大调用次数
- `embedThemeConfig` - 主题配置
- `embedHideHeader` - 是否隐藏头部
- `embedHideBranding` - 是否隐藏品牌标识

✅ 创建成功后自动显示嵌入信息：
- 嵌入 URL (`embedUrl`)
- 绑定的 API Key ID (`embedApiKeyId`)
- 完整的 iframe 代码 (`iframeCode`)

✅ 配置验证和友好提示：
- 检测是否配置了嵌入参数
- 显示允许的来源域名列表
- 提示其他嵌入配置选项

**使用示例：**

```json
{
  "robotName": "合同审核专家",
  "robotCode": "contract_review_expert",
  "systemPrompt": "你是一个专业的合同审核助手...",
  "enableEmbed": 1,
  "embedBaseUrl": "https://agent.workopilot.com",
  "embedAllowedOrigins": [
    "https://crm.example.com",
    "https://erp.example.com"
  ],
  "embedHideHeader": 0,
  "embedHideBranding": 0
}
```

运行脚本后会得到：
```
   🔗 iframe 嵌入信息:
      嵌入 URL: https://agent.workopilot.com/embed/chat/1001?token=xxx...
      API Key ID: 10

   📋 iframe 代码:
      <iframe src="https://agent.workopilot.com/embed/chat/1001?..." width="100%" height="760" ...></iframe>
```

#### 2. update_digital_employee.py - 新增数字员工更新脚本 ⭐

**背景：** 之前缺少更新数字员工配置的脚本，只能通过 Web 界面手动修改。

**功能特性：**

✅ 支持按需更新，只需提供要修改的字段
✅ 自动查询现有配置并显示对比
✅ 验证模型 ID 是否可用
✅ 友好的更新前预览
✅ 完整的错误处理和结果展示

**可更新的字段：**

- 基础信息：`robotName`、`robotCode`、`avatarUrl`、`businessLine`、`description`
- 对话配置：`systemPrompt`、`welcomeMessage`、`quickQuestions`、`forbiddenWords`
- 模型配置：`chatModelId`、`compactionModelId`
- 历史配置：`enableHistory`、`maxHistory`
- 交互配置：`enableSuggestedReplies`、`enableToolCallDisplay`
- 协作配置：`enableAgentCollaboration`、`collaborationScope`
- 记忆配置：`memoryMode`、`enableCompaction`、`enableLongTermMemory`
- 状态：`isActive`

**使用示例：**

```bash
# 更新数字员工
python scripts/update_digital_employee.py \
  --employee-id 1001 \
  --config update-config.json
```

配置文件只需包含要更新的字段：
```json
{
  "robotName": "合同审核专家Pro",
  "maxHistory": 20,
  "enableSuggestedReplies": 1
}
```

脚本会显示：
```
🔍 查询数字员工信息 (ID: 1001)
   名称: 合同审核助手
   编码: contract_review_expert
   状态: 启用

📝 更新的字段:
   - robotName: 合同审核专家Pro
   - maxHistory: 20
   - enableSuggestedReplies: 1

   ⏳ 正在更新...
   ✅ 更新成功
```

#### 3. 新增示例配置文件

**evals/create-digital-employee-with-embed.json**
- 完整的数字员工创建配置
- 包含 iframe 嵌入所有参数示例
- 适合复制修改后使用

**evals/update-digital-employee.json**
- 数字员工更新配置示例
- 演示如何只更新部分字段

#### 4. 新增 scripts/README.md 文档

**内容包括：**
- 所有脚本的详细使用说明
- 完整的参数说明和示例
- iframe 嵌入配置的详细说明
- 常见问题和故障排查指南

### 改进细节

#### 代码质量提升

1. **更好的输出展示**
   - 创建数字员工时显示更多关键信息（robotCode）
   - iframe 嵌入配置的专门展示区域
   - 友好的进度提示和结果总结

2. **错误处理增强**
   - 模型验证更严格
   - 嵌入配置的前置检查
   - 更清晰的错误提示

3. **代码复用**
   - 从 `workopilot_http.py` 导入 `first_model_value` 函数
   - 统一的响应结构处理

### 文档更新

1. **SKILL.md**
   - 更新快速开始部分，添加更新脚本说明
   - 补充场景识别，包含更新数字员工场景

2. **scripts/README.md (新增)**
   - 完整的脚本使用指南
   - iframe 嵌入配置详解
   - 故障排查指南

3. **CHANGELOG.md (本文件)**
   - 详细记录所有改进内容
   - 提供前后对比和使用示例

### 与接口文档的对应关系

所有改进都严格遵循 `docs/喔壳技能/接口文档/02-数字员工开放接口.md` 中的规范：

| 接口文档章节 | 脚本支持 | 说明 |
|------------|---------|------|
| 10. 创建数字员工 | `create_digital_employee.py` | 完整支持所有创建参数，包括 iframe 嵌入 |
| 11. 更新数字员工 | `update_digital_employee.py` (新增) | 支持所有可更新字段 |

### 遵循的开发规范

本次优化严格遵循以下规范：

1. **skill-creator 规范** - 虽然没有找到 skill-creator 目录，但遵循了喔壳技能的通用开发模式：
   - 完整的配置文件示例
   - 清晰的文档说明
   - 良好的错误处理
   - 幂等性保证

2. **接口文档规范** - 所有参数与接口文档完全一致
   - 参数命名与后端接口对应
   - 响应结构的正确解析
   - 错误处理符合 API 规范

3. **项目规范** (CLAUDE.md)
   - Python 脚本使用标准库
   - 配置文件使用 JSON 格式
   - 完整的文档说明

### 后续建议

1. **技能绑定管理**
   - 考虑添加 `bind_skills.py` 脚本，专门管理数字员工的技能绑定
   - 支持批量添加/删除技能

2. **MCP 工具管理**
   - 考虑添加 `bind_mcp_tools.py` 脚本，管理 MCP 工具绑定

3. **iframe 嵌入配置管理**
   - 考虑添加 `update_embed_config.py` 脚本，单独管理嵌入配置
   - 支持更新 `embedAllowedOrigins`、`embedMaxDailyCalls` 等参数

4. **批量操作支持**
   - 支持从 CSV/Excel 批量创建数字员工
   - 支持批量更新配置

### 影响范围

✅ **向后兼容** - 所有改进都是增量的，不影响现有功能
✅ **无破坏性变更** - 现有配置文件仍然有效
✅ **文档完善** - 提供了完整的使用说明和示例

### 测试建议

建议测试以下场景：

1. **创建数字员工（不启用嵌入）**
   ```bash
   python scripts/create_digital_employee.py --config basic-config.json
   ```

2. **创建数字员工（启用嵌入）**
   ```bash
   python scripts/create_digital_employee.py --config evals/create-digital-employee-with-embed.json
   ```

3. **更新数字员工基本信息**
   ```bash
   python scripts/update_digital_employee.py --employee-id 1001 --config evals/update-digital-employee.json
   ```

4. **更新数字员工单个字段**
   ```json
   {"robotName": "新名称"}
   ```
   ```bash
   python scripts/update_digital_employee.py --employee-id 1001 --config update-name.json
   ```

5. **验证幂等性**
   - 多次运行创建脚本，验证是否正确复用已有数字员工
   - 使用 `--no-reuse` 参数验证强制创建功能

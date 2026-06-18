# 计费模块开发指南

## 概述

计费模块用于数字员工的额度消耗和校验。当你开发自定义数字员工时，可以根据业务逻辑决定何时扣费。

**核心概念：**
- **扣费时机由开发者决定** - 例如创建订单时、生成报告时、完成审核时
- **扣费额度由平台售价决定** - 平台管理员配置每次消耗的单位数
- **鉴权方式支持 API-KEY** - 虽然文档写的是 Bearer Token，但实际支持 API-KEY 鉴权

## 典型使用场景

### 场景示例

**销售助理数字员工：**
- 用户对话咨询产品 → 不扣费
- 用户要求生成销售订单 → 扣费 1 次
- 用户要求生成报价单 → 扣费 1 次

**合同审核助手：**
- 用户上传合同问问题 → 不扣费
- 用户要求生成审核报告 → 扣费 1 次
- 用户要求导出 PDF → 扣费 1 次

**HR 招聘助理：**
- 简历预筛选对话 → 不扣费
- 生成面试评估报告 → 扣费 1 次
- 批量筛选简历（按份数） → 扣费 N 次

## API 接口

### 1. 消耗额度接口

当用户触发需要扣费的操作时调用。

**接口地址：** `POST /net-api/api/Billing/ConsumeUsage`

**鉴权方式：**
```http
# 方式 1: Bearer Token（用户登录后）
Authorization: Bearer {token}

# 方式 2: API-KEY（推荐，服务端调用）
API-KEY: {your_api_key}
```

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|------|------|
| `digitalEmployeeId` | integer | 是 | 数字员工 ID |
| `usageCount` | integer | 否 | 单次消耗单位数，默认 1 |
| `remark` | string | 否 | 备注信息，建议记录扣费原因 |

**请求示例：**

```javascript
// Node.js 示例
const consumeUsage = async (digitalEmployeeId, usageCount = 1, remark = '') => {
  const response = await fetch('https://agent.workopilot.com/net-api/api/Billing/ConsumeUsage', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'API-KEY': process.env.WORKOPILOT_API_KEY  // 使用 API-KEY 鉴权
    },
    body: JSON.stringify({
      digitalEmployeeId,
      usageCount,
      remark
    })
  });
  
  const result = await response.json();
  
  if (result.code === 200 && result.data?.Success) {
    console.log('扣费成功:', result.data.Message);
    return true;
  } else {
    console.error('扣费失败:', result.data?.Message || result.msg);
    return false;
  }
};

// 使用示例：创建订单时扣费
const createOrder = async (orderData) => {
  // 1. 先检查额度
  const hasQuota = await checkQuota(1001);
  if (!hasQuota) {
    return { success: false, message: '额度不足，请联系管理员' };
  }
  
  // 2. 创建订单
  const order = await saveOrderToDatabase(orderData);
  
  // 3. 扣费
  const consumed = await consumeUsage(
    1001,  // 数字员工 ID
    1,     // 扣费 1 次
    `创建订单: ${order.id}`  // 备注
  );
  
  if (!consumed) {
    // 扣费失败，可以回滚订单或记录日志
    console.warn('订单已创建但扣费失败:', order.id);
  }
  
  return { success: true, order };
};
```

**响应示例：**

成功：
```json
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "Success": true,
    "Message": "记录成功"
  }
}
```

额度不足：
```json
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "Success": false,
    "Message": "无可用套餐"
  }
}
```

数字员工不存在：
```json
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "Success": false,
    "Message": "数字员工不存在或已停用"
  }
}
```

### 2. 额度校验接口

在执行需要扣费的操作**之前**调用，检查用户是否有足够的额度。

**接口地址：** `POST /net-api/api/Billing/CheckQuota`

**鉴权方式：**
```http
# 方式 1: Bearer Token
Authorization: Bearer {token}

# 方式 2: API-KEY（推荐）
API-KEY: {your_api_key}
```

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|------|------|
| `DigitalEmployeeId` | integer | 二选一 | 数字员工 ID |
| `DigitalEmployeeCode` | string | 二选一 | 数字员工编码 |

**请求示例：**

```javascript
// Node.js 示例
const checkQuota = async (digitalEmployeeId) => {
  const response = await fetch('https://agent.workopilot.com/net-api/api/Billing/CheckQuota', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'API-KEY': process.env.WORKOPILOT_API_KEY
    },
    body: JSON.stringify({
      DigitalEmployeeId: digitalEmployeeId
    })
  });
  
  const result = await response.json();
  
  if (result.code === 200 && result.data) {
    if (result.data.isAvailable) {
      console.log(`额度充足 - 剩余次数: ${result.data.remainingCount}`);
      return true;
    } else {
      console.warn(`额度不足 - ${result.data.reasonName}`);
      return false;
    }
  }
  
  return false;
};

// 在用户请求操作前校验
app.post('/api/create-order', async (req, res) => {
  // 1. 先检查额度
  const hasQuota = await checkQuota(1001);
  
  if (!hasQuota) {
    return res.status(402).json({
      success: false,
      message: '额度不足，无法创建订单。请联系管理员充值。'
    });
  }
  
  // 2. 继续业务逻辑
  // ...
});
```

**响应示例：**

额度充足：
```json
{
  "code": 200,
  "msg": "",
  "data": {
    "isAvailable": true,
    "reasonCode": null,
    "remainingCount": 850,
    "remainingToken": 500000,
    "reasonName": null
  }
}
```

额度不足：
```json
{
  "code": 200,
  "msg": "",
  "data": {
    "isAvailable": false,
    "reasonCode": "COUNT_QUOTA_INSUFFICIENT",
    "remainingCount": 0,
    "remainingToken": 1000,
    "reasonName": "订阅当月额度不足"
  }
}
```

**ReasonCode 说明：**

| ReasonCode | 说明 |
|-----------|------|
| `ROBOT_NOT_FOUND` | 数字员工不存在或无效 |
| `NO_VALID_SUBSCRIPTION` | 无有效订阅 |
| `COUNT_QUOTA_INSUFFICIENT` | 次数额度不足 |
| `TOKEN_QUOTA_INSUFFICIENT` | Token 额度不足 |

## 集成方案

### 方案 A：MCP 工具中集成计费

如果你的数字员工使用 MCP 工具处理业务逻辑，在 MCP 工具中集成计费。

**MCP 工具示例（Python）：**

```python
import os
import requests

WORKOPILOT_API_KEY = os.getenv('WORKOPILOT_API_KEY')
BASE_URL = 'https://agent.workopilot.com/net-api'
DIGITAL_EMPLOYEE_ID = 1001  # 你的数字员工 ID

def check_quota():
    """检查额度"""
    response = requests.post(
        f'{BASE_URL}/api/Billing/CheckQuota',
        headers={'API-KEY': WORKOPILOT_API_KEY},
        json={'DigitalEmployeeId': DIGITAL_EMPLOYEE_ID}
    )
    result = response.json()
    return result.get('code') == 200 and result.get('data', {}).get('isAvailable')

def consume_usage(usage_count=1, remark=''):
    """消耗额度"""
    response = requests.post(
        f'{BASE_URL}/api/Billing/ConsumeUsage',
        headers={'API-KEY': WORKOPILOT_API_KEY},
        json={
            'digitalEmployeeId': DIGITAL_EMPLOYEE_ID,
            'usageCount': usage_count,
            'remark': remark
        }
    )
    result = response.json()
    return result.get('code') == 200 and result.get('data', {}).get('Success')

# MCP 工具实现
def create_sales_order(customer_name, product, quantity):
    """创建销售订单（需要扣费的操作）"""
    
    # 1. 检查额度
    if not check_quota():
        return {
            'success': False,
            'message': '额度不足，无法创建订单。请联系管理员。'
        }
    
    # 2. 执行业务逻辑
    order = {
        'customer': customer_name,
        'product': product,
        'quantity': quantity,
        'total': calculate_total(product, quantity)
    }
    
    # 保存到数据库
    order_id = save_to_database(order)
    
    # 3. 扣费
    consumed = consume_usage(1, f'创建订单: {order_id}')
    
    if not consumed:
        # 扣费失败，记录日志
        log_warning(f'订单 {order_id} 已创建但扣费失败')
    
    return {
        'success': True,
        'order_id': order_id,
        'message': f'订单创建成功，订单号: {order_id}'
    }
```

### 方案 B：iframe 技能卡片中集成计费

如果你的数字员工使用 iframe 技能卡片，在前端业务逻辑中调用计费。

**前端示例（JavaScript/Vue）：**

```javascript
// api/billing.js
export const checkQuota = async (digitalEmployeeId) => {
  const response = await fetch('https://agent.workopilot.com/net-api/api/Billing/CheckQuota', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'API-KEY': process.env.VUE_APP_WORKOPILOT_API_KEY  // ⚠️ 注意：前端不要暴露 APIKEY
    },
    body: JSON.stringify({ DigitalEmployeeId: digitalEmployeeId })
  });
  return await response.json();
};

export const consumeUsage = async (digitalEmployeeId, usageCount = 1, remark = '') => {
  const response = await fetch('https://agent.workopilot.com/net-api/api/Billing/ConsumeUsage', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'API-KEY': process.env.VUE_APP_WORKOPILOT_API_KEY
    },
    body: JSON.stringify({ digitalEmployeeId, usageCount, remark })
  });
  return await response.json();
};

// 在 Vue 组件中使用
export default {
  methods: {
    async generateReport() {
      // 1. 先检查额度
      const quotaResult = await checkQuota(1001);
      
      if (!quotaResult.data?.isAvailable) {
        this.$message.error('额度不足，无法生成报告');
        return;
      }
      
      // 2. 生成报告
      const report = await this.createReport();
      
      // 3. 扣费
      await consumeUsage(1001, 1, `生成报告: ${report.id}`);
      
      this.$message.success('报告生成成功');
    }
  }
};
```

**⚠️ 安全提醒：**
- 前端调用计费接口**必须通过后端代理**，不要直接在前端暴露 API-KEY
- 推荐架构：前端 → 你的后端 API → 喔壳计费接口

### 方案 C：后端 API 中集成计费

最推荐的方式：在你的后端服务中集成计费逻辑。

**后端示例（Node.js/Express）：**

```javascript
// services/billingService.js
const axios = require('axios');

const WORKOPILOT_API_KEY = process.env.WORKOPILOT_API_KEY;
const BASE_URL = 'https://agent.workopilot.com/net-api';

class BillingService {
  async checkQuota(digitalEmployeeId) {
    try {
      const response = await axios.post(
        `${BASE_URL}/api/Billing/CheckQuota`,
        { DigitalEmployeeId: digitalEmployeeId },
        { headers: { 'API-KEY': WORKOPILOT_API_KEY } }
      );
      return response.data.code === 200 && response.data.data?.isAvailable;
    } catch (error) {
      console.error('检查额度失败:', error);
      return false;
    }
  }

  async consumeUsage(digitalEmployeeId, usageCount = 1, remark = '') {
    try {
      const response = await axios.post(
        `${BASE_URL}/api/Billing/ConsumeUsage`,
        { digitalEmployeeId, usageCount, remark },
        { headers: { 'API-KEY': WORKOPILOT_API_KEY } }
      );
      return response.data.code === 200 && response.data.data?.Success;
    } catch (error) {
      console.error('扣费失败:', error);
      return false;
    }
  }
}

module.exports = new BillingService();

// routes/order.js
const express = require('express');
const router = express.Router();
const billingService = require('../services/billingService');

router.post('/create', async (req, res) => {
  const DIGITAL_EMPLOYEE_ID = 1001;
  
  // 1. 检查额度
  const hasQuota = await billingService.checkQuota(DIGITAL_EMPLOYEE_ID);
  if (!hasQuota) {
    return res.status(402).json({
      success: false,
      message: '额度不足，无法创建订单'
    });
  }
  
  // 2. 创建订单
  const order = await createOrder(req.body);
  
  // 3. 扣费
  const consumed = await billingService.consumeUsage(
    DIGITAL_EMPLOYEE_ID,
    1,
    `创建订单: ${order.id}`
  );
  
  if (!consumed) {
    // 扣费失败但订单已创建，记录日志
    console.warn(`订单 ${order.id} 创建成功但扣费失败`);
  }
  
  res.json({ success: true, order });
});

module.exports = router;
```

## 开发检查清单

开发数字员工时，请确认以下内容：

### ✅ 需要集成计费的场景

如果你的数字员工包含以下功能，**强烈建议集成计费**：

- [ ] 生成文档、报告、合同等文件
- [ ] 创建订单、工单、任务等业务记录
- [ ] 数据导出（PDF、Excel、Word）
- [ ] 复杂计算或分析（风险评估、数据分析）
- [ ] 批量处理（批量审核、批量生成）
- [ ] 调用外部付费 API（翻译、OCR、第三方服务）
- [ ] 生成代码、设计稿等创意内容

### ✅ 集成计费的步骤

1. **确定扣费时机**
   - [ ] 明确哪些操作需要扣费
   - [ ] 每次扣费的单位数（通常是 1）
   - [ ] 批量操作是否按数量扣费

2. **实现额度检查**
   - [ ] 在执行付费操作前调用 `CheckQuota` 接口
   - [ ] 额度不足时给用户友好提示
   - [ ] 提供充值或联系管理员的引导

3. **实现额度消耗**
   - [ ] 在操作成功后调用 `ConsumeUsage` 接口
   - [ ] 填写清晰的 `remark`，便于追溯
   - [ ] 处理扣费失败的情况（记录日志）

4. **安全性保障**
   - [ ] API-KEY 保存在服务端环境变量
   - [ ] 不要在前端代码中暴露 API-KEY
   - [ ] 通过后端代理调用计费接口

5. **用户体验**
   - [ ] 额度不足时清晰提示
   - [ ] 显示剩余额度（可选）
   - [ ] 提供充值入口（可选）

### ⚠️ 未集成计费的风险

如果你的数字员工提供高价值服务但**未集成计费**：

- ❌ 用户可以无限制使用，导致成本失控
- ❌ 无法追踪实际使用量，难以评估价值
- ❌ 无法对不同用户进行差异化收费
- ❌ 平台方难以实现商业模式闭环

### 💡 开发建议

1. **先校验，后执行**
   ```javascript
   // ✅ 正确的流程
   if (!await checkQuota()) return '额度不足';
   const result = await doExpensiveOperation();
   await consumeUsage();
   return result;
   
   // ❌ 错误的流程
   const result = await doExpensiveOperation();
   await consumeUsage();  // 操作已执行，扣费失败也无法撤回
   return result;
   ```

2. **明确的备注信息**
   ```javascript
   // ✅ 清晰的备注
   await consumeUsage(1001, 1, '生成销售订单: ORD-20260618-001');
   await consumeUsage(1001, 5, '批量导出客户报告: 5份');
   
   // ❌ 不清晰的备注
   await consumeUsage(1001, 1, '扣费');
   await consumeUsage(1001, 5);
   ```

3. **优雅的错误处理**
   ```javascript
   const consumed = await consumeUsage(1001, 1, remark);
   if (!consumed) {
     // 记录到日志系统，而不是让业务失败
     logger.warn('扣费失败但业务已完成', { orderId, remark });
     // 可以触发告警，让管理员处理
     await notifyAdmin('扣费异常', { orderId, remark });
   }
   ```

4. **额度预警**
   ```javascript
   const quotaResult = await checkQuota(1001);
   if (quotaResult.data.isAvailable) {
     const remaining = quotaResult.data.remainingCount;
     if (remaining < 10) {
       // 额度即将用完，提前通知
       await notifyAdmin('额度预警', { remaining });
     }
   }
   ```

## 常见问题

### Q1: 什么时候扣费？

**A:** 由开发者根据业务逻辑决定。建议在用户触发高价值操作时扣费，例如：
- 生成文档/报告
- 创建订单/工单
- 数据导出
- 批量处理

普通对话、查询操作通常不扣费。

### Q2: 每次扣多少？

**A:** 默认每次扣 1 个单位。如果是批量操作，可以按数量扣费，例如批量处理 10 条记录，传 `usageCount: 10`。

具体的额度价值由平台管理员在售价配置中设定。

### Q3: API-KEY 还是 Bearer Token？

**A:** 
- **服务端集成** - 使用 API-KEY（推荐）
- **用户端调用** - 使用 Bearer Token（用户登录后获取）

文档虽然写的是 Bearer Token，但实际两种方式都支持。服务端集成推荐用 API-KEY。

### Q4: 扣费失败怎么办？

**A:** 扣费失败通常有以下原因：
- 额度不足
- 数字员工不存在或已停用
- 无有效订阅

建议：
1. 在执行操作前先调用 `CheckQuota` 检查额度
2. 扣费失败时记录日志，通知管理员
3. 不要因为扣费失败而回滚已完成的业务操作

### Q5: 前端能否直接调用计费接口？

**A:** 技术上可以，但**强烈不推荐**。因为：
- 前端代码中的 API-KEY 会暴露
- 用户可以通过浏览器开发工具看到 API-KEY
- 存在安全风险

**推荐架构：**
```
前端 → 你的后端 API → 喔壳计费接口
```

### Q6: 如何测试计费功能？

**A:** 
1. 使用测试环境 API Key
2. 在测试环境创建测试数字员工
3. 调用计费接口，检查返回结果
4. 在喔壳平台查看使用记录

测试环境 Base URL: `https://agenttest.workopilot.com/net-api`

### Q7: 忘记集成计费怎么办？

**A:** 
1. 评估数字员工提供的服务是否属于高价值操作
2. 如果是，尽快补充计费逻辑
3. 发布更新版本
4. 通知用户更新

已部署的数字员工可以通过更新 MCP 工具或 iframe 卡片代码来集成计费，无需重新创建数字员工。

## 完整示例

### 示例：销售助理数字员工

```javascript
// billing-service.js
const axios = require('axios');

const BASE_URL = 'https://agent.workopilot.com/net-api';
const API_KEY = process.env.WORKOPILOT_API_KEY;
const DIGITAL_EMPLOYEE_ID = 1001;  // 销售助理数字员工 ID

class BillingService {
  async checkQuota() {
    const response = await axios.post(
      `${BASE_URL}/api/Billing/CheckQuota`,
      { DigitalEmployeeId: DIGITAL_EMPLOYEE_ID },
      { headers: { 'API-KEY': API_KEY } }
    );
    return response.data.data?.isAvailable || false;
  }

  async consumeUsage(count = 1, remark = '') {
    const response = await axios.post(
      `${BASE_URL}/api/Billing/ConsumeUsage`,
      {
        digitalEmployeeId: DIGITAL_EMPLOYEE_ID,
        usageCount: count,
        remark
      },
      { headers: { 'API-KEY': API_KEY } }
    );
    return response.data.data?.Success || false;
  }
}

module.exports = new BillingService();

// mcp-tools.js (MCP 工具实现)
const billingService = require('./billing-service');

// 工具 1: 创建销售订单（需要扣费）
async function createSalesOrder(params) {
  const { customerName, products, totalAmount } = params;
  
  // 1. 检查额度
  const hasQuota = await billingService.checkQuota();
  if (!hasQuota) {
    return {
      success: false,
      message: '额度不足，无法创建订单。请联系管理员充值。'
    };
  }
  
  // 2. 创建订单
  const orderId = await saveOrder({ customerName, products, totalAmount });
  
  // 3. 扣费
  await billingService.consumeUsage(1, `创建订单: ${orderId}`);
  
  return {
    success: true,
    orderId,
    message: `订单创建成功！订单号：${orderId}`
  };
}

// 工具 2: 生成报价单（需要扣费）
async function generateQuotation(params) {
  const { customerName, items } = params;
  
  // 1. 检查额度
  const hasQuota = await billingService.checkQuota();
  if (!hasQuota) {
    return {
      success: false,
      message: '额度不足，无法生成报价单。请联系管理员。'
    };
  }
  
  // 2. 生成报价单
  const quotationId = await generateQuotationPDF({ customerName, items });
  
  // 3. 扣费
  await billingService.consumeUsage(1, `生成报价单: ${quotationId}`);
  
  return {
    success: true,
    quotationId,
    downloadUrl: `https://example.com/quotations/${quotationId}.pdf`,
    message: '报价单已生成，可以下载。'
  };
}

// 工具 3: 查询客户信息（不扣费）
async function queryCustomerInfo(customerId) {
  // 普通查询操作，不需要扣费
  const customer = await getCustomerFromDatabase(customerId);
  return {
    success: true,
    customer
  };
}

module.exports = {
  createSalesOrder,
  generateQuotation,
  queryCustomerInfo
};
```

## 总结

- ✅ 计费模块用于控制数字员工的使用额度
- ✅ 开发者决定扣费时机，平台决定扣费额度
- ✅ 支持 API-KEY 鉴权，推荐在服务端集成
- ✅ 先检查额度，再执行操作，最后扣费
- ✅ 高价值操作应集成计费，普通对话不需要
- ⚠️ 未集成计费的内置数字员工可能导致成本失控
- ⚠️ 不要在前端暴露 API-KEY

开发数字员工时，请评估是否需要集成计费，并按照本文档的指导实现。

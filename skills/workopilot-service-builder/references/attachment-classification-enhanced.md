# 附件分类与提取 - 完整开发指南

## 概述

附件分类与提取是喔壳的**核心高频功能**，特别适用于文档智能化场景。

**核心价值:**
- **使用频率极高** - 90% 的场景使用"直接提取"模式  
- **节省人力** - 合同/发票/简历等文件自动提取，不用人工抄写
- **提升准确率** - 避免人工录入的错误和遗漏
- **秒级响应** - 上传即提取，实时填充表单

---

## 两种使用模式详解

### 模式 A: 分类 + 提取(完整流程)

**适用场景:** 企业收到大量杂乱的文件(邮件附件、扫描件、照片等),不知道每个文件是合同还是发票还是简历,需要系统自动识别。

**流程:**
```
1. 上传文件
2. 调用 /api/Classfication/ClassifyFile (系统自动识别类型)
3. 获取分类结果 { categoryCode: "contract-purchase" }
4. 根据 categoryCode 调用 /api/Classfication/ExtractFile
5. 获取结构化数据
```

**何时使用:**
- 文件来源复杂,类型多样
- 需要文件管理系统(自动归档、分类存储)
- 用户不知道上传的是什么类型

**使用频率:** ~10%

### 模式 B: 直接提取(高频使用) ⭐⭐⭐

**适用场景:** 业务系统中有明确的文件上传入口,用户在"创建合同"页面上传合同,系统已知是采购合同。

**流程:**
```
1. 上传文件到"创建合同"页面
2. 直接调用 /api/Classfication/ExtractFile,传入 categoryCode: "contract-purchase"
3. 获取结构化数据
4. 自动填充合同表单
```

**何时使用:**
- 业务流程明确(在合同页面就是上传合同)
- 需要快速提取结构化数据
- 不需要分类这个中间步骤

**使用频率:** ~90%

**为什么模式 B 更常用?**

大多数企业的业务系统都有明确的功能入口:
- 合同管理系统 → 用户在"创建合同"页面 → 上传的就是合同
- 发票管理系统 → 用户在"录入发票"页面 → 上传的就是发票
- 招聘系统 → 用户在"简历筛选"页面 → 上传的就是简历

文件类型是确定的,所以**直接提取**最高效。

---

## 核心概念

### 1. 附件分组(AttachmentGroup)

**用途:** 组织和管理多个相关的分类

**示例:**
```
- 合同分组 (contract)
  ├─ 采购合同 (contract-purchase)
  ├─ 销售合同 (contract-sales)
  └─ 租赁合同 (contract-lease)
  
- 财务分组 (finance)
  ├─ 增值税发票 (invoice-vat)
  ├─ 收据 (receipt)
  └─ 银行流水 (bank-statement)
```

**何时创建分组:**
- 有多个相关的附件类型
- 需要统一管理和展示

### 2. 附件分类(AttachmentClassification)

**用途:** 定义具体的文件类型和提取规则

**核心字段:**
- `CategoryCode`: 唯一标识(如 "contract-purchase")
- `CategoryName`: 显示名称(如 "采购合同")
- `ExtractRules`: **最重要** - 定义要提取哪些字段

### 3. 提取规则(ExtractRules)

**用途:** 告诉 AI 从文档中提取什么数据,以什么格式

**字段结构:**
```json
{
  "FieldKey": "partyA",              // 字段名(代码中使用)
  "FieldDesc": "甲方",                // 显示名称
  "FieldType": "STRING",             // 数据类型
  "AiPrompt": "合同中的甲方公司名称,通常在页眉或第一段,格式为完整公司名称,包含'有限公司'等后缀",
  "ExtractScheme": "AI",
  "IsRequired": true
}
```

**`AiPrompt` 是关键!** 这个字段决定提取准确率,要写清楚:
- 字段在文档中的位置特征
- 格式要求
- 特殊情况处理

---

## 提取规则设计技巧

### AiPrompt 编写最佳实践

#### ❌ 不好的 AiPrompt

```json
{
  "FieldKey": "amount",
  "AiPrompt": "金额"  // 太简单,AI 不知道提取哪个金额
}
```

问题:
- 文档中可能有多个金额(含税/不含税/定金/尾款)
- 没有说明格式要求
- AI 可能提取错误的金额

#### ✅ 好的 AiPrompt

```json
{
  "FieldKey": "amount",
  "AiPrompt": "合同总金额,不含税,纯数字,不含货币符号和千分位逗号。如果文档中有多个金额,提取标注为'合同总额'或'总价'的那个。示例: 500000 (表示50万)"
}
```

改进点:
- 明确是"合同总金额"(不是定金或分期)
- 说明"不含税"(区分含税和不含税)
- 格式要求"纯数字,不含货币符号"
- 多个金额时的选择规则
- 提供示例帮助理解

### 设计原则

**原则 1: 位置描述**

告诉 AI 字段通常在哪里:
```json
{
  "FieldKey": "contractNo",
  "AiPrompt": "合同编号,通常在页眉右上角或第一行,格式类似 HT-2026-001"
}
```

**原则 2: 格式要求**

明确数据格式:
```json
{
  "FieldKey": "signDate",
  "AiPrompt": "合同签订日期,必须转换为 YYYY-MM-DD 格式,例如 2026-06-15。即使文档中是'2026年6月15日',也要转换为 2026-06-15"
}
```

**原则 3: 特殊情况**

说明边界情况处理:
```json
{
  "FieldKey": "expiryDate",
  "AiPrompt": "合同终止日期,格式 YYYY-MM-DD。如果是长期合同未标注到期日期,返回 null"
}
```

**原则 4: 提供示例**

复杂字段给出示例:
```json
{
  "FieldKey": "contactPerson",
  "FieldType": "JSON",
  "AiPrompt": "双方联系人信息,返回 JSON 格式。示例: {\"partyA\": {\"name\": \"张三\", \"phone\": \"13800138000\"}, \"partyB\": {\"name\": \"李四\", \"phone\": \"13900139000\"}}"
}
```

---

## 完整开发流程

### 第一步: 需求分析

**用户需求:** "我有个合同管理系统,用户上传合同后要自动提取信息"

**需要确认:**
1. 合同有哪些类型?(采购、销售、租赁...)
2. 每种合同要提取哪些字段?
3. 字段的格式要求?(日期格式、金额单位...)
4. 是否需要分类?(通常不需要,用户在合同页面上传就是合同)

### 第二步: 设计提取规则

**以采购合同为例:**

```json
{
  "group": {
    "GroupCode": "contract",
    "GroupName": "合同",
    "SceneType": "contract_management",
    "ClassficationMode": "FILE",
    "Description": "各类合同文件",
    "IsActive": 1
  },
  "categories": [
    {
      "CategoryCode": "contract-purchase",
      "CategoryName": "采购合同",
      "ExtractMethod": "OCR_LLM",
      "Description": "企业采购设备、物料、服务等的合同文件",
      "ExtractPrompt": "这是一份采购合同,请提取以下关键信息",
      "EnableStructure": 1,
      "IsActive": 1,
      "ExtractRules": [
        {
          "FieldKey": "contractNo",
          "FieldDesc": "合同编号",
          "FieldType": "STRING",
          "AiPrompt": "合同唯一编号,通常在页眉右上角或第一行,格式类似 HT-2026-001",
          "ExtractScheme": "AI",
          "IsRequired": true
        },
        {
          "FieldKey": "partyA",
          "FieldDesc": "甲方(买方)",
          "FieldType": "STRING",
          "AiPrompt": "合同中的甲方公司全称,通常是采购方,格式为完整公司名称包含'有限公司'等后缀",
          "ExtractScheme": "AI",
          "IsRequired": true
        },
        {
          "FieldKey": "partyB",
          "FieldDesc": "乙方(卖方)",
          "FieldType": "STRING",
          "AiPrompt": "合同中的乙方公司全称,通常是供应商,格式为完整公司名称",
          "ExtractScheme": "AI",
          "IsRequired": true
        },
        {
          "FieldKey": "subject",
          "FieldDesc": "合同标的",
          "FieldType": "STRING",
          "AiPrompt": "采购的物品或服务名称,可能在'标的'或'采购内容'章节",
          "ExtractScheme": "AI",
          "IsRequired": false
        },
        {
          "FieldKey": "amount",
          "FieldDesc": "合同金额",
          "FieldType": "NUMBER",
          "AiPrompt": "合同总金额(不含税),纯数字不含逗号。如果只有含税金额,也提取出来。单位:元",
          "ExtractScheme": "AI",
          "IsRequired": true
        },
        {
          "FieldKey": "taxAmount",
          "FieldDesc": "税额",
          "FieldType": "NUMBER",
          "AiPrompt": "增值税金额,纯数字。如果文档中没有单独列出,返回 null",
          "ExtractScheme": "AI",
          "IsRequired": false
        },
        {
          "FieldKey": "totalAmount",
          "FieldDesc": "价税合计",
          "FieldType": "NUMBER",
          "AiPrompt": "含税总金额,纯数字",
          "ExtractScheme": "AI",
          "IsRequired": false
        },
        {
          "FieldKey": "currency",
          "FieldDesc": "币种",
          "FieldType": "STRING",
          "AiPrompt": "货币代码,如 CNY、USD、EUR。如果文档未标注,中文合同默认 CNY",
          "ExtractScheme": "AI",
          "IsRequired": false
        },
        {
          "FieldKey": "signDate",
          "FieldDesc": "签订日期",
          "FieldType": "DATE",
          "AiPrompt": "合同签订日期,格式 YYYY-MM-DD。通常在合同末尾盖章处",
          "ExtractScheme": "AI",
          "IsRequired": true
        },
        {
          "FieldKey": "effectiveDate",
          "FieldDesc": "生效日期",
          "FieldType": "DATE",
          "AiPrompt": "合同生效日期,格式 YYYY-MM-DD。如果未明确标注,与签订日期相同",
          "ExtractScheme": "AI",
          "IsRequired": false
        },
        {
          "FieldKey": "expiryDate",
          "FieldDesc": "到期日期",
          "FieldType": "DATE",
          "AiPrompt": "合同终止日期,格式 YYYY-MM-DD。如果是长期合同未标注,返回 null",
          "ExtractScheme": "AI",
          "IsRequired": false
        },
        {
          "FieldKey": "paymentTerms",
          "FieldDesc": "付款条款",
          "FieldType": "STRING",
          "AiPrompt": "详细的付款方式和时间节点,完整提取文档中的付款条款章节内容",
          "ExtractScheme": "AI",
          "IsRequired": false
        },
        {
          "FieldKey": "deliveryAddress",
          "FieldDesc": "交付地址",
          "FieldType": "STRING",
          "AiPrompt": "货物交付地址或服务提供地点",
          "ExtractScheme": "AI",
          "IsRequired": false
        }
      ]
    }
  ]
}
```

**设计技巧:**
1. **字段要全面** - 覆盖业务需要的所有信息
2. **类型要准确** - STRING/NUMBER/DATE/JSON
3. **AiPrompt 要详细** - 位置、格式、特殊情况
4. **考虑兼容性** - 某些字段可能不存在,允许 null

### 第三步: 检查分类是否存在

```bash
# 查询系统中是否已有"采购合同"分类
curl -X GET "${BASE_URL}/api/Classfication/GetCategoryData" \
  -H "API-KEY: ${API_KEY}"

# 检查返回的 data 数组中是否有 code: "contract-purchase"
# 如果没有,说明需要创建
```

### 第四步: 创建分类和提取规则

```bash
# 保存上面的 JSON 为 contract-purchase-config.json
# 使用脚本创建
python scripts/create_attachment_classification.py \
  --config contract-purchase-config.json

# 脚本会:
# 1. 检查分类是否存在
# 2. 不存在则创建
# 3. 存在则更新 ExtractRules (默认覆盖)
# 4. 返回分类 ID 和编码
```

### 第五步: 在业务系统中调用提取

```javascript
// 合同管理系统 - 创建合同页面

async function handleContractUpload(file) {
  try {
    // 1. 上传文件到服务器(喔壳或自己的文件服务)
    const uploadResult = await uploadFile(file);
    const fileUrl = uploadResult.url;
    
    // 2. 调用喔壳附件提取接口
    const extractResult = await fetch(`${WORKOPILOT_BASE_URL}/api/Classfication/ExtractFile`, {
      method: 'POST',
      headers: {
        'API-KEY': WORKOPILOT_API_KEY,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        categoryCode: 'contract-purchase',     // 指定分类编码
        extractMode: 'DOCUMENT',              // 按文档提取
        fileUrls: [{
          url: fileUrl,
          fileName: file.name
        }]
      })
    });
    
    if (!extractResult.ok) {
      throw new Error('提取失败: ' + extractResult.statusText);
    }
    
    const result = await extractResult.json();
    
    if (result.code !== 200) {
      throw new Error('提取失败: ' + result.msg);
    }
    
    // 3. 获取批次号,轮询结果
    const batchNo = result.data;
    const extractedData = await pollExtractResult(batchNo);
    
    // 4. 自动填充表单
    fillContractForm(extractedData);
    
    // 5. 提示用户确认
    showNotification('合同信息已自动填充,请核对后提交');
    
  } catch (error) {
    console.error('处理失败:', error);
    showError('合同信息提取失败: ' + error.message);
  }
}

// 轮询提取结果
async function pollExtractResult(batchNo, maxAttempts = 30) {
  for (let i = 0; i < maxAttempts; i++) {
    const response = await fetch(
      `${WORKOPILOT_BASE_URL}/api/Classfication/GetClassificationResult?batchNo=${batchNo}`,
      {
        headers: { 'API-KEY': WORKOPILOT_API_KEY }
      }
    );
    
    const result = await response.json();
    
    if (result.code === 200 && result.data.code === 1) {
      // 处理完成
      const fileResult = result.data.result[0];
      if (fileResult.status === 'SUCCESS') {
        // 提取 extractDataJson
        const extractedData = JSON.parse(
          fileResult.classificationResults[0].extractDataJson
        );
        return extractedData;
      } else {
        throw new Error(fileResult.message);
      }
    }
    
    // 等待 2 秒后重试
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
  
  throw new Error('提取超时');
}

// 填充表单
function fillContractForm(data) {
  document.getElementById('contractNo').value = data.contractNo || '';
  document.getElementById('partyA').value = data.partyA || '';
  document.getElementById('partyB').value = data.partyB || '';
  document.getElementById('subject').value = data.subject || '';
  document.getElementById('amount').value = data.amount || '';
  document.getElementById('signDate').value = data.signDate || '';
  document.getElementById('effectiveDate').value = data.effectiveDate || '';
  document.getElementById('expiryDate').value = data.expiryDate || '';
  document.getElementById('paymentTerms').value = data.paymentTerms || '';
}
```

### 第六步: 优化提取准确率

如果提取结果不准确,调整策略:

**策略 1: 优化 AiPrompt**

```json
// 原来: "AiPrompt": "金额"
// 改为:
"AiPrompt": "合同总金额(不含税),纯数字,位于'合同金额'或'总价'标签后。如果文档中有'定金'和'尾款',提取它们的总和"
```

**策略 2: 调整提取技术**

```json
{
  // 如果是扫描件,强制使用 OCR
  "ExtractMethod": "OCR_LLM"
  
  // 如果是复杂排版(表格、多栏),使用 Vision 模型
  "ExtractMethod": "VISION"
}
```

**策略 3: 提供示例文档**

- 找几份实际的合同文件
- 测试提取结果
- 根据结果调整 AiPrompt

**策略 4: 重新创建分类**(覆盖旧规则)

```bash
python scripts/create_attachment_classification.py \
  --config contract-purchase-config.json
  # 脚本会自动覆盖 ExtractRules
```

---

## 两种提取技术详解

### OCR + LLM (OCR_LLM)

**工作流程:**
```
1. OCR 识别文档中的所有文字
2. LLM 理解文字并提取结构化数据
3. 返回 JSON
```

**适用场景:**
- 扫描件、照片
- 纯文本文档
- 文字清晰可识别

**优点:**
- OCR 准确率高
- 文字识别能力强
- 成本相对较低

**示例:** 合同 PDF、发票照片、身份证扫描件

### Vision-Language 模型 (VISION)

**工作流程:**
```
1. 将文档作为图像输入 VL 模型
2. 模型理解图像和文字,直接提取数据
3. 返回 JSON
```

**适用场景:**
- 复杂排版(多栏、表格、混排)
- 包含图表、印章、签名等视觉元素
- 需要理解文档布局

**优点:**
- 理解复杂排版
- 处理视觉元素
- 一步到位

**示例:** 复杂表格、带图表的报告、多栏排版的合同

### 如何选择?

**让系统自动选择(推荐):**
```json
{
  "categoryCode": "contract-purchase",
  // 不指定 ExtractMethod,系统根据文件类型自动选择
}
```

**手动指定:**
```json
{
  "categoryCode": "contract-purchase",
  "ExtractMethod": "OCR_LLM"  // 或 "VISION"
}
```

**经验规则:**
- **扫描件、纯文本** → OCR_LLM
- **复杂排版、多栏、表格** → VISION
- **不确定** → 让系统自动选择

---

## 常见附件类型参考

### 合同类
- 采购合同 (contract-purchase)
- 销售合同 (contract-sales)
- 租赁合同 (contract-lease)
- 劳动合同 (contract-labor)
- 保密协议 (contract-nda)

### 财务类
- 增值税发票 (invoice-vat)
- 普通发票 (invoice-regular)
- 收据 (receipt)
- 银行流水 (bank-statement)
- 报销单 (expense-report)

### 人力类
- 简历 (resume)
- 身份证 (id-card)
- 学历证书 (diploma)
- 工资条 (payslip)
- 入职登记表 (onboarding-form)

### 业务类
- 订单 (order)
- 报价单 (quotation)
- 出库单 (delivery-note)
- 验收单 (acceptance-certificate)
- 产品规格书 (product-spec)

---

## 故障排查

### 问题 1: 提取结果为空或字段缺失

**可能原因:**
- 文件内容中不包含目标字段
- AiPrompt 不清晰,AI 无法定位
- 文件格式不支持或损坏

**解决方案:**
1. 检查文件内容是否包含字段
2. 优化 AiPrompt,写得更详细
3. 尝试不同的 ExtractMethod
4. 检查文件是否损坏(重新上传)

### 问题 2: 字段值不准确

**可能原因:**
- AiPrompt 歧义导致 AI 理解偏差
- 文档中有多个相似字段,AI 选错了

**解决方案:**
1. AiPrompt 中明确字段位置("通常在页眉"、"标注为'合同总额'")
2. AiPrompt 中明确格式("纯数字,不含逗号")
3. 提供示例值
4. 如果是复杂布局,尝试 VISION 模式

### 问题 3: 日期、金额格式不符合预期

**可能原因:**
- 文档中的格式多样(2026-06-15 vs 2026年6月15日)
- AI 没有统一格式

**解决方案:**

在 AiPrompt 中明确要求格式:
```json
{
  "FieldKey": "signDate",
  "FieldType": "DATE",
  "AiPrompt": "合同签订日期,必须转换为 YYYY-MM-DD 格式,例如 2026-06-15。即使文档中是'2026年6月15日'或'二〇二六年六月十五日',都要转换为 2026-06-15"
}
```

### 问题 4: 提取速度慢

**可能原因:**
- 文件过大(几十 MB 的扫描件)
- Vision 模型处理时间长
- 文档页数过多

**解决方案:**
1. 压缩文件大小(降低分辨率、转换格式)
2. 如果是纯文本,强制使用 OCR 模式
3. 异步处理,不要阻塞用户界面
4. 显示进度条,让用户知道正在处理

### 问题 5: 批次查询一直返回处理中

**可能原因:**
- 服务端处理异常
- 网络问题
- 文件无法识别

**解决方案:**
1. 检查轮询逻辑(是否有超时机制)
2. 检查返回的 status 字段是否有错误信息
3. 联系技术支持,提供 batchNo

---

## 最佳实践总结

### 1. 设计提取规则时

- ✅ AiPrompt 要详细,说明位置、格式、特殊情况
- ✅ 提供示例值,帮助 AI 理解
- ✅ 考虑字段可选性(某些字段可能不存在)
- ✅ 测试多份实际文档,持续优化

- ❌ 不要 AiPrompt 过于简单("金额")
- ❌ 不要忘记说明格式要求
- ❌ 不要把所有字段都设为必填

### 2. 调用接口时

- ✅ 实现轮询机制,等待处理完成
- ✅ 设置超时时间,避免无限等待
- ✅ 显示进度提示,改善用户体验
- ✅ 处理异常情况,给出友好提示

- ❌ 不要同步等待(会阻塞界面)
- ❌ 不要忘记错误处理
- ❌ 不要假设一定会成功

### 3. 优化准确率时

- ✅ 从实际文档出发,测试并调整
- ✅ 逐步优化 AiPrompt,每次改一点
- ✅ 记录哪些 AiPrompt 效果好,积累经验
- ✅ 必要时尝试不同的 ExtractMethod

- ❌ 不要一次改太多,无法定位问题
- ❌ 不要凭想象编写 AiPrompt
- ❌ 不要忽视文档的多样性

---

## 总结

附件分类与提取是喔壳的**核心高频功能**:

1. **90% 使用"直接提取"模式** - 已知文件类型,快速提取
2. **AiPrompt 是关键** - 决定提取准确率,要详细说明
3. **自动选择技术** - 系统会根据文件类型选择最优方案
4. **持续优化** - 根据实际文档测试和调整

**开发流程:**
需求分析 → 设计提取规则 → 创建分类 → 调用接口 → 优化准确率

**关键成功因素:**
- 详细的 AiPrompt
- 充分的实际文档测试
- 合理的异常处理
- 良好的用户体验

按照本指南操作,可以快速实现文档智能化,大幅提升业务效率! 🚀

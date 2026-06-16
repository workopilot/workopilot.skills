# 附件分类接口 - API 参考

> **💡 寻找完整开发指南?**  
> 本文档侧重 API 接口参考。如需完整的开发流程、提取规则设计技巧、代码示例和故障排查,请阅读:  
> 👉 **[attachment-classification-enhanced.md](./attachment-classification-enhanced.md)** - 附件分类与提取完整开发指南

---

附件分类和信息提取是两个不同场景：

- 分类：面对合同、订单、签到表、混合扫描件等非标附件，先判断每页或每个文件属于哪类，再进入后续业务处理。
- 提取：已知附件类型，或分类完成后需要结构化字段时，按分类的取数配置提取字段。

如果当前租户没有目标附件分类，先使用 `ClassifyExtend` 创建分组、分类和 `ExtractRules`。如果已经有分类，先调用通用分类数据接口确认 `categoryCode`，再分类或提取。

## 场景选择

| 需求 | 推荐接口 |
| --- | --- |
| 不知道附件属于合同、订单还是签到表 | `POST /api/Classfication/ClassifyFile` |
| 分类后同时提取结构化字段 | `ClassifyFile` 请求中传 `extractFields: true` |
| 已经知道附件类型，只要取结构化字段 | `POST /api/Classfication/ExtractFile` |
| 获取当前可用分类 | `GET /api/Classfication/GetCategoryDataAsync` |
| 当前租户缺少分类/取数字段配置 | `POST /api/ClassifyExtend/SaveAttachmentGroup` + `POST /api/ClassifyExtend/AddAttachmentCategory` |

## 创建分类和取数配置

`ClassifyExtend` 文档中的完整路径通常写作 `/net-api/api/ClassifyExtend/...`。本技能脚本的 `baseUrl` 默认已经包含 `/net-api`，因此脚本内部调用相对路径 `/api/ClassifyExtend/...`。

### 一键创建脚本

```bash
python path/to/scripts/create_attachment_classification.py --config attachment-classification.json
```

分类已存在时，脚本默认调用编辑接口并覆盖 `ExtractRules`。如果只想复用已有分类，不覆盖取数配置：

```bash
python path/to/scripts/create_attachment_classification.py --config attachment-classification.json --no-edit-existing
```

配置示例：

```json
{
  "group": {
    "GroupCode": "BUSINESS_DOC",
    "GroupName": "业务附件",
    "SceneType": "order_process",
    "ClassficationMode": "FILE",
    "Description": "合同、订单、签到表等业务附件",
    "IsActive": 1
  },
  "categories": [
    {
      "CategoryCode": "CONTRACT",
      "CategoryName": "合同",
      "ExtractMethod": "OCR_LLM",
      "Description": "识别合同类附件",
      "ExtractPrompt": "判断附件是否为合同，并关注合同编号、甲方、乙方、金额、签署日期。",
      "EnableStructure": 1,
      "IsActive": 1,
      "ExtractRules": [
        {
          "FieldKey": "contract_no",
          "FieldDesc": "合同编号",
          "AiPrompt": "提取合同编号，没有则返回空字符串",
          "ExtractScheme": "AI",
          "FieldType": "STRING",
          "IsRequired": true
        },
        {
          "FieldKey": "amount",
          "FieldDesc": "合同金额",
          "AiPrompt": "提取合同总金额，仅返回数字",
          "ExtractScheme": "AI",
          "FieldType": "NUMBER",
          "IsRequired": false
        }
      ]
    }
  ]
}
```

脚本输出示例（`jsonc`，带注释，不可直接作为 JSON 发送）：

```jsonc
{
  "group": {
    "action": "created", // created 或 reused
    "id": 12, // 后续分类 Category 的 GroupIds 可使用
    "data": {
      "Id": 12,
      "GroupCode": "BUSINESS_DOC",
      "GroupName": "业务附件"
    }
  },
  "categories": [
    {
      "action": "created", // created、updated 或 reused
      "id": 34, // categoryId；限定分类时可传 categoryIds
      "categoryCode": "CONTRACT", // 分类/提取时常用
      "data": {
        "Id": 34,
        "CategoryCode": "CONTRACT",
        "CategoryName": "合同",
        "GroupIds": [12]
      }
    }
  ]
}
```

### ClassifyExtend 接口

创建或编辑附件分类组：

```http
POST /api/ClassifyExtend/SaveAttachmentGroup
API-KEY: <your_api_key>
Content-Type: application/json
```

请求示例：

```json
{
  "GroupCode": "BUSINESS_DOC",
  "GroupName": "业务附件",
  "SceneType": "order_process",
  "ClassficationMode": "FILE",
  "Description": "合同、订单、签到表等业务附件",
  "IsActive": 1
}
```

查询附件分类组：

```http
GET /api/ClassifyExtend/GetAttachmentGroups
API-KEY: <your_api_key>
```

新增附件分类并同步创建取数配置：

```http
POST /api/ClassifyExtend/AddAttachmentCategory
API-KEY: <your_api_key>
Content-Type: application/json
```

编辑附件分类并覆盖取数配置：

```http
POST /api/ClassifyExtend/EditAttachmentCategory
API-KEY: <your_api_key>
Content-Type: application/json
```

查询附件分类：

```http
GET /api/ClassifyExtend/GetAttachmentCategories?GroupId=12&CategoryCode=CONTRACT
API-KEY: <your_api_key>
```

查询分类取数配置：

```http
GET /api/ClassifyExtend/GetExtractRules?categoryId=34
API-KEY: <your_api_key>
```

`AddAttachmentCategory` / `EditAttachmentCategory` 请求核心字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `Id` | long | 编辑时传分类 ID |
| `CategoryCode` | string | 分类编码，后续分类和提取会用到 |
| `CategoryName` | string | 分类名称 |
| `GroupIds` | array<long> | 所属分组 ID |
| `ExtractMethod` | string | `OCR_LLM` 或 `VISION` |
| `Description` | string | 分类说明 |
| `ExtractPrompt` | string | 分类/提取提示词 |
| `EnableStructure` | int | 是否开启文档结构/封面检测 |
| `IsActive` | int | 1 启用，0 禁用 |
| `ExtractRules` | array | 结构化字段配置 |

`ExtractRules` 子项：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `FieldKey` | string | 字段英文名，例如 `contract_no` |
| `FieldDesc` | string | 字段中文说明 |
| `AiPrompt` | string | 字段专用提取提示词 |
| `ExtractScheme` | string | `AI` 或 `REGEX` |
| `FieldType` | string | `NUMBER`、`STRING`、`JSON`、`DATE` |
| `IsRequired` | bool | 是否必填 |
| `Remark` | string | 备注 |

## 获取当前分类

在分类或提取前，先查询当前租户有哪些分类：

```http
GET /api/Classfication/GetCategoryDataAsync
API-KEY: <your_api_key>
```

如果返回中没有业务需要的分类，引导开发者创建分组、分类和取数字段配置。

## 附件分类

```http
POST /api/Classfication/ClassifyFile
API-KEY: <your_api_key>
```

请求体可以是 JSON，也可以是 multipart form data。

JSON 请求体：

```json
{
  "groupCode": "CONTRACT",
  "categoryCodes": ["CONTRACT_MAIN", "INVOICE"],
  "fileUrls": [
    {
      "url": "https://example.com/files/demo.pdf",
      "fileName": "demo.pdf"
    }
  ],
  "businessId": "BIZ-001",
  "extractFields": true
}
```

响应示例：

```jsonc
{
  "code": 200,
  "msg": null,
  "data": "batch_no_xxx", // 批次号；查询分类结果时传 batchNo
  "total": 0,
  "rows": null
}
```

Agent 使用：保存 `data`，轮询 `/api/Classfication/GetClassificationResultAsync?batchNo=...`。

## 查询分类结果

```http
GET /api/Classfication/GetClassificationResultAsync?batchNo=batch_no_xxx
API-KEY: <your_api_key>
```

响应示例：

```jsonc
{
  "code": 200,
  "msg": null,
  "data": {
    "code": 1, // 0=处理中，1=已完成
    "progress": 100,
    "result": [
      {
        "fileName": "demo.pdf",
        "totalPages": 2,
        "elapsedMs": 3200,
        "status": "SUCCESS",
        "message": "处理完成",
        "operateMode": 1, // 1=按页，2=按文档
        "classificationResults": [
          {
            "fileUrl": "https://example.com/files/page1.png",
            "fileName": "demo_1.png",
            "categoryId": 10,
            "categoryCode": "INVOICE",
            "categoryName": "发票",
            "isCover": false,
            "ocrText": "发票文本",
            "extractDataJson": "{\"amount\":120.5}" // extractFields=true 时可能有提取结果
          }
        ],
        "segments": [
          {
            "categoryId": 10,
            "categoryName": "发票",
            "startPage": 1,
            "endPage": 2,
            "confidence": 0.98
          }
        ]
      }
    ]
  },
  "total": 0,
  "rows": null
}
```

Agent 使用：

- `data.code=0` 时继续轮询。
- `data.code=1` 时读取 `data.result[].classificationResults`。
- 如果需要提取字段，优先读取 `extractDataJson`。

分类完成后读取：

- `data.result[].classificationResults[].categoryCode`：分类结果。
- `data.result[].classificationResults[].extractDataJson`：`extractFields=true` 时的结构化取数结果。
- `data.result[].segments`：按文档分段时的段落分类结果。

## 查询分类数据

```http
GET /api/Classfication/GetCategoryDataAsync
API-KEY: <your_api_key>
```

响应示例：

```jsonc
{
  "code": 200,
  "msg": null,
  "data": [
    {
      "id": 1, // 分类 ID，可传入 categoryIds
      "code": "INVOICE", // 分类编码，可传入 categoryCodes 或 ExtractFile.categoryCode
      "name": "发票"
    }
  ],
  "total": 0,
  "rows": null
}
```

## 信息提取

```http
POST /api/Classfication/ExtractFile
API-KEY: <your_api_key>
```

JSON 请求体：

```json
{
  "categoryCode": "INVOICE",
  "extractMode": "DOCUMENT",
  "fileUrls": [
    {
      "url": "https://example.com/files/invoice.pdf",
      "fileName": "invoice.pdf"
    }
  ]
}
```

响应示例：

```jsonc
{
  "code": 200,
  "msg": null,
  "data": "batch_no_or_result", // 当前实现返回字符串；通常作为批次/结果标识继续查询或记录
  "total": 0,
  "rows": null
}
```

`extractMode` 支持 `PAGE` 和 `DOCUMENT`。当前代码会把 `FILE` 转成 `DOCUMENT`。

Agent 使用：当用户已经知道附件属于某个分类，或者分类后需要对某一类附件单独取数时，调用 `ExtractFile`。如果用户说“分类完再取结构化数据”，优先在 `ClassifyFile` 中设置 `extractFields: true`，然后通过分类结果接口读取 `extractDataJson`。

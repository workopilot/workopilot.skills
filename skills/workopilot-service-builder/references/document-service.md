# Document 文档服务接口

重要路由规则：`DocumentController` 继承 `BaseController` 的 `api/[controller]/[Action]` 路由。部分方法自身带模板，会追加在 Action 名后面。

正确路径：

| 功能 | 方法 | 路径 |
| --- | --- | --- |
| Markdown 转 PDF | `POST` | `/api/Document/ConvertMarkdownToPdf` |
| HTML 转 PDF | `POST` | `/api/Document/ConvertHtmlToPdf` |
| 上传文件 | `POST` | `/api/Document/UploadDocument/Upload` |
| OCR | `POST` | `/api/Document/OcrDocument/Ocr` |
| 写入 Excel | `POST` | `/api/Document/WriteExcelDocument/WriteExcel` |

不要使用 `/api/Document/Upload`、`/api/Document/Ocr` 或 `/api/Document/WriteExcel`。

## Markdown 转 PDF

```http
POST /api/Document/ConvertMarkdownToPdf
```

请求体：

```json
{
  "content": "# Report",
  "theme": "default"
}
```

响应示例：

```jsonc
{
  "code": 200,
  "msg": null,
  "data": "https://agent.workopilot.com/files/report.pdf", // 生成后的 PDF 文件 URL
  "total": 0,
  "rows": null
}
```

Agent 使用：读取 `data` 作为 PDF 地址，可回填给用户、传给 AI 服务 `files`，或写入业务系统。

## HTML 转 PDF

```http
POST /api/Document/ConvertHtmlToPdf
```

响应结构与 Markdown 转 PDF 相同，`data` 为 PDF URL。

## 上传文件

```http
POST /api/Document/UploadDocument/Upload
Content-Type: multipart/form-data
```

Multipart 字段：

- `file`

响应示例：

```jsonc
{
  "code": 200,
  "msg": null,
  "data": "https://agent.workopilot.com/files/demo.pdf", // 上传后的文件访问 URL
  "total": 0,
  "rows": null
}
```

Agent 使用：读取 `data`，后续可传给 OCR、附件分类、AI 服务执行的 `files`。

## OCR

```http
POST /api/Document/OcrDocument/Ocr
Content-Type: multipart/form-data
```

Multipart 字段：

- `file`：可选，优先使用
- `url`：可选，未上传文件时使用

`file` 和 `url` 至少传一个。

响应示例：

```jsonc
{
  "code": 200,
  "msg": "Success",
  "data": "识别出的文本内容", // OCR 文本
  "total": 0,
  "rows": null
}
```

Agent 使用：读取 `data` 作为纯文本，可以传入 AI 服务 `inputs` 或直接返回给用户。

## 写入 Excel

```http
POST /api/Document/WriteExcelDocument/WriteExcel
```

请求体：

```json
{
  "columns": [
    {
      "col_filed": "name",
      "col_name": "姓名"
    }
  ],
  "data": [
    {
      "name": "张三"
    }
  ],
  "is_cloud": true
}
```

`is_cloud=true` 响应：

```jsonc
{
  "code": 200,
  "msg": "生成成功",
  "data": "https://agent.workopilot.com/files/export.xlsx", // Excel 文件 URL
  "total": 0,
  "rows": null
}
```

`is_cloud=false` 响应不是 JSON，而是 `.xlsx` 文件流：

```http
Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
Content-Disposition: attachment; filename=export_20260615120000.xlsx
```

当前代码里的字段名就是 `col_filed`，不要改成 `col_field`。

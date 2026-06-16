#!/usr/bin/env python3
import argparse
from urllib.parse import urlencode

from workopilot_http import (
    add_common_args,
    get_models,
    load_json_config,
    open_management_page,
    print_json,
    request_json,
    require_success,
    resolve_config,
    select_model,
)


def first_present(item, *keys):
    for key in keys:
        if isinstance(item, dict) and key in item and item[key] not in (None, ""):
            return item[key]
    return None


def list_data(result):
    if isinstance(result, dict):
        data = result.get("data")
        if isinstance(data, list):
            return data
        rows = result.get("rows")
        if isinstance(rows, list):
            return rows
    return []


def find_by_code(items, code, *keys):
    if not code:
        return None
    expected = str(code).lower()
    for item in items:
        value = first_present(item, *keys)
        if value and str(value).lower() == expected:
            return item
    return None


def get_groups(base_url, api_key):
    result = request_json(base_url, api_key, "GET", "/api/ClassifyExtend/GetAttachmentGroups")
    require_success(result, "查询附件分类组")
    return list_data(result)


def save_group(base_url, api_key, group):
    result = request_json(base_url, api_key, "POST", "/api/ClassifyExtend/SaveAttachmentGroup", group)
    require_success(result, "保存附件分类组")
    return result


def get_categories(base_url, api_key, group_id=None, category_code=None, category_name=None):
    query = {}
    if group_id:
        query["GroupId"] = group_id
    if category_code:
        query["CategoryCode"] = category_code
    if category_name:
        query["CategoryName"] = category_name
    path = "/api/ClassifyExtend/GetAttachmentCategories"
    if query:
        path += "?" + urlencode(query)
    result = request_json(base_url, api_key, "GET", path)
    require_success(result, "查询附件分类")
    return list_data(result)


def save_category(base_url, api_key, category, existing=None, edit_existing=True):
    if existing and edit_existing:
        payload = dict(category)
        payload["Id"] = first_present(existing, "Id", "id")
        result = request_json(base_url, api_key, "POST", "/api/ClassifyExtend/EditAttachmentCategory", payload)
        require_success(result, "编辑附件分类")
        return {"action": "updated", "result": result, "id": payload["Id"]}
    result = request_json(base_url, api_key, "POST", "/api/ClassifyExtend/AddAttachmentCategory", category)
    require_success(result, "创建附件分类")
    return {"action": "created", "result": result}


def normalize_group(payload):
    group = payload.get("group") or payload.get("Group") or payload.get("attachmentGroup") or payload.get("AttachmentGroup")
    if not group:
        return None
    normalized = dict(group)
    normalized.setdefault("IsActive", 1)
    normalized.setdefault("ClassficationMode", "FILE")
    return normalized


def normalize_categories(payload):
    categories = (
        payload.get("categories")
        or payload.get("Categories")
        or payload.get("attachmentCategories")
        or payload.get("AttachmentCategories")
    )
    if categories is None:
        single = payload.get("category") or payload.get("Category")
        categories = [single] if single else []
    return [dict(item) for item in categories if isinstance(item, dict)]


def main():
    parser = add_common_args(argparse.ArgumentParser(description="创建喔壳附件分类和结构化取数字段"))
    parser.add_argument(
        "--no-edit-existing",
        action="store_true",
        help="分类编码已存在时不覆盖原有提取配置，只返回已存在分类",
    )
    args = parser.parse_args()
    base_url, api_key = resolve_config(args)
    payload = load_json_config(args.config)

    print("\n" + "=" * 60)
    print("创建附件分类")
    print("=" * 60 + "\n")

    # 获取可用模型
    models = get_models(base_url, api_key)
    if not models:
        print("\n❌ 没有可用模型，无法创建附件分类")
        print("请在喔壳平台配置模型后再试")
        raise SystemExit(1)

    # 选择合适的模型 - 附件提取优先使用 qwen 和 Deepseek
    model_id = select_model(
        models,
        purpose="附件提取",
        prefer_models=["qwen", "deepseek", "gpt-4", "gpt4", "gpt-3.5", "gpt35"]
    )

    output = {"group": None, "categories": []}
    group = normalize_group(payload)
    group_id = None

    if group:
        group_code = first_present(group, "GroupCode", "groupCode")
        print(f"\n📂 处理分类组: {group_code}")
        groups = get_groups(base_url, api_key)
        existing_group = find_by_code(groups, group_code, "GroupCode", "groupCode")
        if existing_group:
            group_id = first_present(existing_group, "Id", "id")
            print(f"   ✅ 分类组已存在，复用 ID: {group_id}")
            output["group"] = {"action": "reused", "id": group_id, "data": existing_group}
        else:
            print(f"   📝 创建新分类组...")
            save_group(base_url, api_key, group)
            groups = get_groups(base_url, api_key)
            created_group = find_by_code(groups, group_code, "GroupCode", "groupCode")
            group_id = first_present(created_group or {}, "Id", "id")
            print(f"   ✅ 分类组创建成功，ID: {group_id}")
            output["group"] = {"action": "created", "id": group_id, "data": created_group}

    categories = normalize_categories(payload)
    print(f"\n📋 处理 {len(categories)} 个附件分类...")

    for idx, category in enumerate(categories, 1):
        category.setdefault("IsActive", 1)

        # 设置模型 ID
        if not first_present(category, "ModelId", "modelId"):
            category["ModelId"] = model_id
            print(f"\n   [{idx}] 设置模型 ID: {model_id}")

        category_code = first_present(category, "CategoryCode", "categoryCode")
        category_name = first_present(category, "CategoryName", "categoryName", "Name", "name")
        print(f"   [{idx}] 分类: {category_name} ({category_code})")

        if group_id and not first_present(category, "GroupIds", "groupIds"):
            category["GroupIds"] = [group_id]

        # 检查是否已存在
        print(f"       🔍 检查分类是否已存在...")
        existing = find_by_code(
            get_categories(base_url, api_key, category_code=category_code),
            category_code,
            "CategoryCode",
            "categoryCode",
        )

        if existing:
            category_id = first_present(existing, "Id", "id")
            if args.no_edit_existing:
                print(f"       ✅ 分类已存在，跳过更新 (ID: {category_id})")
                output["categories"].append(
                    {
                        "action": "reused",
                        "id": category_id,
                        "categoryCode": category_code,
                        "data": existing,
                    }
                )
                continue
            else:
                print(f"       📝 分类已存在，更新配置 (ID: {category_id})")
        else:
            print(f"       📝 创建新分类...")

        saved = save_category(base_url, api_key, category, existing=existing, edit_existing=not args.no_edit_existing)

        refreshed = find_by_code(
            get_categories(base_url, api_key, category_code=category_code),
            category_code,
            "CategoryCode",
            "categoryCode",
        )

        result_id = first_present(refreshed or {}, "Id", "id") or saved.get("id")
        action_text = "更新" if saved["action"] == "updated" else "创建"
        print(f"       ✅ {action_text}成功 (ID: {result_id})")

        output["categories"].append(
            {
                "action": saved["action"],
                "id": result_id,
                "categoryCode": category_code,
                "data": refreshed,
            }
        )

    print("\n" + "=" * 60)
    print("✅ 附件分类配置完成")
    print("=" * 60)

    # 打开管理页面
    open_management_page("attachment_config", "查看已创建的附件分类")

    print("\n📄 详细结果:")
    print_json(output)


if __name__ == "__main__":
    main()

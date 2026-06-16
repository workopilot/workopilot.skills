#!/usr/bin/env python3
import argparse
import sys
from workopilot_http import add_common_args, load_json_config, print_json, request_json, require_success, resolve_config


def warn_prompt_placeholders(payload):
    prompt = payload.get("systemPrompt") or payload.get("SystemPrompt") or ""
    inputs = payload.get("inputs") or payload.get("Inputs") or []
    missing = []
    for item in inputs:
        if not isinstance(item, dict):
            continue
        name = item.get("name") or item.get("Name")
        if not name:
            continue
        placeholder = "{{" + str(name) + "}}"
        if placeholder not in prompt:
            missing.append(placeholder)
    if missing:
        print(
            "警告：systemPrompt 未引用部分 inputs 占位符："
            + ", ".join(missing)
            + "。请确认提示词是否已按 {{input_name}} 使用入参。",
            file=sys.stderr,
        )


def main():
    parser = add_common_args(argparse.ArgumentParser(description="创建喔壳 AI 服务"))
    parser.add_argument("--no-reuse", action="store_true", help="即使 serviceCode 已存在也继续创建")
    args = parser.parse_args()
    base_url, api_key = resolve_config(args)
    payload = load_json_config(args.config)
    warn_prompt_placeholders(payload)

    service_code = payload.get("serviceCode") or payload.get("ServiceCode")
    if service_code and not args.no_reuse:
        existing = request_json(
            base_url,
            api_key,
            "POST",
            "/api/aiagent/external/list",
            {"serviceCode": service_code, "pageNum": 1, "pageSize": 1},
        )
        require_success(existing, "查询 AI 服务")
        rows = existing.get("rows") or []
        if rows:
            print_json({"reused": True, "data": rows[0]})
            return

    result = request_json(base_url, api_key, "POST", "/api/aiagent/external/create", payload)
    require_success(result, "创建 AI 服务")
    print_json({"reused": False, "result": result})


if __name__ == "__main__":
    main()

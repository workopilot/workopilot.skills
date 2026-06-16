#!/usr/bin/env python3
import argparse
from workopilot_http import add_common_args, print_json, request_json, require_success, resolve_config


def main():
    parser = add_common_args(argparse.ArgumentParser(description="验证喔壳 APIKEY 和 baseUrl 是否可用"))
    parser.add_argument("--check", choices=["ai", "robots", "models"], default="ai")
    args = parser.parse_args()
    base_url, api_key = resolve_config(args)

    checks = []
    if args.check in ("ai", "models"):
        result = request_json(base_url, api_key, "GET", "/api/aiagent/external/models")
        require_success(result, "查询 AI 模型")
        checks.append({"name": "models", "total": result.get("total", 0)})

    if args.check in ("ai", "robots"):
        result = request_json(base_url, api_key, "GET", "/api/ai/open/robots")
        require_success(result, "查询数字员工")
        checks.append({"name": "robots", "total": result.get("total", 0)})

    print_json({"ok": True, "baseUrl": base_url, "checks": checks})


if __name__ == "__main__":
    main()

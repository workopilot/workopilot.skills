#!/usr/bin/env python3
import argparse
from workopilot_http import add_common_args, load_json_config, print_json, request_json, require_success, resolve_config


def main():
    parser = add_common_args(argparse.ArgumentParser(description="创建喔壳数字员工"))
    parser.add_argument("--no-reuse", action="store_true", help="即使 robotCode 已存在也继续创建")
    args = parser.parse_args()
    base_url, api_key = resolve_config(args)
    payload = load_json_config(args.config)

    robot_code = payload.get("robotCode") or payload.get("RobotCode")
    if robot_code and not args.no_reuse:
        existing = request_json(base_url, api_key, "GET", f"/api/ai/robot/profile/{robot_code}")
        if isinstance(existing, dict) and existing.get("code") == 200 and existing.get("data"):
            print_json({"reused": True, "data": existing["data"]})
            return

    result = request_json(base_url, api_key, "POST", "/api/ai/robot/external/create", payload)
    require_success(result, "创建数字员工")
    print_json({"reused": False, "result": result})


if __name__ == "__main__":
    main()

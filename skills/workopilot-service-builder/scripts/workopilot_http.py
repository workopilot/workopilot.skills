#!/usr/bin/env python3
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

# 默认使用生产环境
# 生产环境: https://agent.workopilot.com/net-api
# 测试环境: https://agenttest.workopilot.com/net-api
DEFAULT_BASE_URL = "https://agent.workopilot.com/net-api"


def load_env_file(path):
    values = {}
    if not path:
        return values
    p = Path(path)
    if not p.exists():
        return values
    for raw in p.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def find_env_file(explicit=None):
    if explicit:
        return explicit
    cwd = Path.cwd()
    for candidate in (".env.workopilot", ".env.local"):
        p = cwd / candidate
        if p.exists():
            return str(p)
    return None


def add_common_args(parser):
    parser.add_argument("--base-url", default=None, help="喔壳 baseUrl")
    parser.add_argument("--api-key", default=None, help="喔壳 APIKEY")
    parser.add_argument("--env-file", default=None, help=".env.workopilot 文件路径")
    parser.add_argument("--config", default=None, help="JSON 配置文件路径")
    return parser


def resolve_config(args):
    env_file = find_env_file(getattr(args, "env_file", None))
    file_values = load_env_file(env_file)
    base_url = (
        getattr(args, "base_url", None)
        or os.environ.get("WORKOPILOT_BASE_URL")
        or file_values.get("WORKOPILOT_BASE_URL")
        or DEFAULT_BASE_URL
    ).rstrip("/")
    api_key = (
        getattr(args, "api_key", None)
        or os.environ.get("WORKOPILOT_API_KEY")
        or file_values.get("WORKOPILOT_API_KEY")
    )
    if not api_key or api_key == "replace_with_your_api_key":
        raise SystemExit(
            "缺少 WORKOPILOT_API_KEY。请设置环境变量、传入 --api-key，"
            "或在项目根目录创建 .env.workopilot。不要把真实 APIKEY 存在技能目录中。"
        )
    return base_url, api_key


def load_json_config(path):
    if not path:
        raise SystemExit("缺少 --config 配置文件路径")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def request_json(base_url, api_key, method, path, body=None, query=None):
    url = base_url + path
    if query:
        url += "?" + urllib.parse.urlencode(query)
    data = None
    headers = {"API-KEY": api_key}
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method.upper())
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            text = resp.read().decode("utf-8")
            if not text:
                return None
            return json.loads(text)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"HTTP 请求失败：{exc.code} {method} {url}\n{detail}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"请求失败：{method} {url}\n{exc}") from exc


def print_json(value):
    print(json.dumps(value, ensure_ascii=False, indent=2))


def require_success(result, label):
    if isinstance(result, dict) and result.get("code") not in (None, 200):
        raise SystemExit(f"{label}失败：\n{json.dumps(result, ensure_ascii=False, indent=2)}")
    return result


if __name__ == "__main__":
    print("workopilot_http.py 是共享工具模块，请运行具体任务脚本。")

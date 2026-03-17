#!/usr/bin/env python3
"""
Kimi Web Search 脚本

使用 Moonshot AI 的 $web_search 内置函数实现联网搜索功能。
"""

import os
import sys
import json
import argparse
from typing import Any, Dict, List, Optional
from pathlib import Path

from openai import OpenAI
from openai.types.chat.chat_completion import Choice


def load_env_from_skill_dir():
    """从技能目录加载 .env 文件"""
    skill_dir = Path(__file__).parent.parent
    env_file = skill_dir / ".env"

    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ.setdefault(key.strip(), value.strip().strip('"\''))


def get_api_key() -> str:
    """获取 Kimi API Key"""
    load_env_from_skill_dir()
    api_key = os.environ.get("KIMI_API_KEY") or os.environ.get("MOONSHOT_API_KEY")
    if not api_key:
        raise ValueError(
            "未找到 Kimi API Key。请在技能目录的 .env 文件中设置 KIMI_API_KEY 或 MOONSHOT_API_KEY"
        )
    return api_key


def search_impl(arguments: Dict[str, Any]) -> Any:
    """
    Kimi Web Search 工具的具体实现。
    在使用 Moonshot AI 提供的 $web_search 时，只需原封不动返回 arguments 即可。
    """
    return arguments


def create_client() -> OpenAI:
    """创建 OpenAI 客户端实例"""
    return OpenAI(
        base_url="https://api.moonshot.cn/v1",
        api_key=get_api_key(),
    )


def perform_search(
    query: str,
    model: str = "kimi-k2-turbo-preview",
    temperature: float = 0.6,
    max_tokens: int = 32768,
    system_prompt: Optional[str] = None,
    verbose: bool = False,
) -> Dict[str, Any]:
    """
    执行联网搜索并返回结果。

    Args:
        query: 搜索查询内容
        model: 使用的模型名称
        temperature: 采样温度
        max_tokens: 最大生成 token 数
        system_prompt: 系统提示词
        verbose: 是否显示详细信息

    Returns:
        包含搜索结果的字典
    """
    client = create_client()

    messages: List[Dict[str, str]] = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    else:
        messages.append({"role": "system", "content": "你是 Kimi，一个有帮助的 AI 助手。"})

    messages.append({"role": "user", "content": query})

    result = {
        "query": query,
        "content": "",
        "usage": {},
        "search_tokens": 0,
    }

    finish_reason = None
    iteration = 0
    max_iterations = 5

    while (finish_reason is None or finish_reason == "tool_calls") and iteration < max_iterations:
        iteration += 1

        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            tools=[
                {
                    "type": "builtin_function",
                    "function": {"name": "$web_search"},
                }
            ],
        )

        usage = completion.usage
        choice = completion.choices[0]
        finish_reason = choice.finish_reason

        if finish_reason == "tool_calls":
            messages.append(choice.message)

            for tool_call in choice.message.tool_calls:
                tool_call_name = tool_call.function.name
                tool_call_arguments = json.loads(tool_call.function.arguments)

                if tool_call_name == "$web_search":
                    search_usage = tool_call_arguments.get("usage", {})
                    search_tokens = search_usage.get("total_tokens", 0)
                    result["search_tokens"] = search_tokens

                    if verbose:
                        print(f"搜索内容 tokens: {search_tokens}", file=sys.stderr)

                    tool_result = search_impl(tool_call_arguments)
                else:
                    tool_result = f"Error: unable to find tool by name '{tool_call_name}'"

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_call_name,
                    "content": json.dumps(tool_result),
                })
        else:
            content = choice.message.content
            result["content"] = content

            if usage:
                result["usage"] = {
                    "prompt_tokens": usage.prompt_tokens,
                    "completion_tokens": usage.completion_tokens,
                    "total_tokens": usage.total_tokens,
                }

                if verbose:
                    print(f"提示 tokens: {usage.prompt_tokens}", file=sys.stderr)
                    print(f"生成 tokens: {usage.completion_tokens}", file=sys.stderr)
                    print(f"总 tokens: {usage.total_tokens}", file=sys.stderr)

    return result


def main():
    parser = argparse.ArgumentParser(description="Kimi Web Search 工具")
    parser.add_argument("query", help="搜索查询内容")
    parser.add_argument("--model", default="kimi-k2-turbo-preview", help="使用的模型")
    parser.add_argument("--temperature", type=float, default=0.6, help="采样温度")
    parser.add_argument("--max-tokens", type=int, default=32768, help="最大生成 token 数")
    parser.add_argument("--system", dest="system_prompt", help="系统提示词")
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细信息")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出")

    args = parser.parse_args()

    try:
        result = perform_search(
            query=args.query,
            model=args.model,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
            system_prompt=args.system_prompt,
            verbose=args.verbose,
        )

        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(result["content"])

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

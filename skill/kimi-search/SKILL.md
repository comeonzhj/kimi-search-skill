---
name: kimi-search
description: This skill should be used when users want to perform web searches using Kimi (Moonshot AI) API. It enables internet search functionality through Kimi's built-in $web_search tool. Use when users ask to search for information online, get latest news, research topics, or need web search capabilities with Kimi AI.
---

# Kimi Search

## Overview

This skill enables web search functionality using Kimi (Moonshot AI) API's built-in `$web_search` tool. It provides a simple way to perform internet searches and get AI-powered summaries of search results.

## When to Use

Use this skill when:
- Users want to search for current information online
- Users need to research topics with up-to-date data
- Users ask about recent news, events, or developments
- Users need web search combined with AI analysis
- Users want to use Kimi's internet search capability

## Quick Start

### 1. Configure API Key

Create a `.env` file in the skill directory with your Kimi API Key:

```bash
cp .env.example .env
# Edit .env and add your API key
KIMI_API_KEY=your_api_key_here
```

Get your API key from: https://platform.moonshot.cn/

### 2. Install Dependencies

```bash
pip install openai
```

### 3. Use the Search Script

```bash
# Basic search
python3 scripts/kimi_search.py "搜索内容"

# With verbose output
python3 scripts/kimi_search.py "搜索内容" --verbose

# JSON output with usage stats
python3 scripts/kimi_search.py "搜索内容" --json

# Custom model and parameters
python3 scripts/kimi_search.py "搜索内容" --model kimi-k2-turbo-preview --temperature 0.7
```

## Usage in Code

To use Kimi Web Search programmatically, import and call the `perform_search` function:

```python
from scripts.kimi_search import perform_search

result = perform_search(
    query="请搜索 Moonshot AI 最新动态",
    model="kimi-k2-turbo-preview",
    temperature=0.6,
    max_tokens=32768,
    verbose=True
)

print(result["content"])  # AI-generated response based on search results
print(result["usage"])    # Token usage statistics
```

## How It Works

Kimi's `$web_search` is a built-in function that works differently from regular tool calls:

1. When Kimi detects a need for web search, it returns `finish_reason="tool_calls"` with `$web_search` as the tool name
2. The search is **executed by Kimi internally** - you simply return the arguments back to the model
3. Kimi performs the search, reads the results, and generates a response
4. The response includes the AI-generated summary of search results

This design makes the search process simple and reliable while maintaining full compatibility with the standard tool calling flow.

## Important Notes

### Model Selection

Always use `kimi-k2-turbo-preview` model for web search tasks because:
- Web search results consume significant tokens
- Larger context window accommodates search results
- Prevents "Input token length too long" errors

### Token Usage

Web search results are counted in `prompt_tokens`. The search process generates two types of token usage:
- `search_tokens`: Tokens consumed by the search results content
- Regular chat tokens: Input and output tokens from the conversation

Use `--verbose` or `--json` flags to see detailed token usage.

### Cost

Each web search call costs ¥0.03 (3 cents) in addition to regular token costs.

### Error Handling

Common errors and solutions:
- **API Key not found**: Check `.env` file exists and contains `KIMI_API_KEY`
- **Rate limit exceeded**: Wait a moment and retry
- **Token limit exceeded**: Use `kimi-k2-turbo-preview` model
- **Search no results**: Try rephrasing the query

## Resources

### scripts/kimi_search.py

Main executable script for performing web searches. Can be used as:
- Command-line tool with various options
- Python module for programmatic use

### .env.example

Template for environment configuration. Copy to `.env` and add your API key.

## Examples

### Search for Tech News

```bash
python3 scripts/kimi_search.py "最新的AI技术新闻"
```

### Research a Topic

```bash
python3 scripts/kimi_search.py "量子计算的基本原理和应用" --verbose
```

### Get Current Events

```bash
python3 scripts/kimi_search.py "今天的热门新闻" --json
```

### Custom System Prompt

```bash
python3 scripts/kimi_search.py "Python 最新版本特性" --system "你是一个专业的编程助手"
```

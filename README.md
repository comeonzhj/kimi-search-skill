# Kimi Search Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Claude Code skill for performing web searches using Kimi (Moonshot AI) API's built-in `$web_search` tool.

## Features

- 🔍 **Web Search** - Perform internet searches with Kimi's AI-powered search
- 🤖 **AI Summarization** - Get intelligent summaries of search results
- 📊 **Token Usage Stats** - Track API usage and costs
- 🔧 **Easy Integration** - Use as CLI tool or Python module
- 🔐 **Secure** - API key stored locally in `.env` file

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/kimi-search-skill.git
cd kimi-search-skill
```

### 2. Install Dependencies

```bash
pip install openai
```

### 3. Configure API Key

Copy the example environment file and add your Kimi API Key:

```bash
cp skill/kimi-search/.env.example skill/kimi-search/.env
```

Edit `skill/kimi-search/.env` and add your API key:

```bash
KIMI_API_KEY=your_kimi_api_key_here
```

Get your API key from: https://platform.moonshot.cn/

## Usage

### Command Line

```bash
# Basic search
python3 skill/kimi-search/scripts/kimi_search.py "最新的AI技术新闻"

# Verbose output with token usage
python3 skill/kimi-search/scripts/kimi_search.py "量子计算原理" --verbose

# JSON output
python3 skill/kimi-search/scripts/kimi_search.py "Python 最新版本" --json

# Custom parameters
python3 skill/kimi-search/scripts/kimi_search.py "搜索内容" \
  --model kimi-k2-turbo-preview \
  --temperature 0.7 \
  --max-tokens 16384
```

### Python Module

```python
import sys
sys.path.insert(0, 'skill/kimi-search/scripts')
from kimi_search import perform_search

result = perform_search(
    query="请搜索 Moonshot AI 最新动态",
    model="kimi-k2-turbo-preview",
    temperature=0.6,
    verbose=True
)

print(result["content"])  # AI-generated response
print(result["usage"])    # Token usage statistics
```

### As a Claude Code Skill

1. Copy the skill to your Claude Code skills directory:

```bash
cp -r skill/kimi-search ~/.claude/skills/
```

2. The skill will be automatically available in Claude Code. Use it by saying:
   - "搜索最新的科技新闻"
   - "用 Kimi 搜索量子计算资料"
   - "帮我查一下今天的热点"

## How It Works

Kimi's `$web_search` is a built-in function that enables internet search:

1. When Kimi detects a need for web search, it returns `finish_reason="tool_calls"`
2. The search is **executed internally by Kimi** - simply return the arguments back
3. Kimi performs the search, reads results, and generates a response
4. The response includes the AI-generated summary

## API Reference

### `perform_search()`

```python
perform_search(
    query: str,                    # Search query
    model: str = "kimi-k2-turbo-preview",
    temperature: float = 0.6,
    max_tokens: int = 32768,
    system_prompt: Optional[str] = None,
    verbose: bool = False
) -> Dict[str, Any]
```

Returns a dictionary with:
- `content`: AI-generated response
- `usage`: Token usage statistics
- `search_tokens`: Tokens consumed by search results

## Important Notes

### Model Selection

Always use `kimi-k2-turbo-preview` for web search because:
- Web search results consume significant tokens
- Larger context window accommodates search results
- Prevents "Input token length too long" errors

### Cost

- Each web search call costs ¥0.03 (3 cents)
- Additional token costs apply based on usage

### Token Usage

Web search results are included in `prompt_tokens`. Use `--verbose` to see detailed breakdown.

## Project Structure

```
kimi-search-skill/
├── README.md
├── LICENSE
├── skill/
│   └── kimi-search/
│       ├── SKILL.md              # Skill documentation
│       ├── .env.example          # Environment template
│       ├── .env                  # Your API key (not in git)
│       └── scripts/
│           └── kimi_search.py    # Main search script
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Moonshot AI](https://www.moonshot.cn/) for providing the Kimi API and `$web_search` tool
- Claude Code for the skill framework

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/kimi-search-skill/issues) page
2. Create a new issue with a detailed description

---

⭐ If you find this project helpful, please give it a star!

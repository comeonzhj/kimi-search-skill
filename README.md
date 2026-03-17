# Kimi Search Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一个用于在 Claude Code 中通过 Kimi (Moonshot AI) API 进行联网搜索的技能插件。

## 功能特性

- 🔍 **联网搜索** - 使用 Kimi AI 进行智能网络搜索
- 🤖 **AI 智能总结** - 自动总结搜索结果
- 📊 **Token 使用统计** - 追踪 API 使用量和费用
- 🔧 **多种使用方式** - 支持命令行工具和 Python 模块调用
- 🔐 **安全可靠** - API Key 本地存储在 `.env` 文件中

## 安装

### 1. 克隆仓库

```bash
git clone https://github.com/comeonzhj/kimi-search-skill.git
cd kimi-search-skill
```

### 2. 安装依赖

```bash
pip install openai
```

### 3. 配置 API Key

复制环境变量模板并添加你的 Kimi API Key：

```bash
cp skill/kimi-search/.env.example skill/kimi-search/.env
```

编辑 `skill/kimi-search/.env` 文件，添加你的 API Key：

```bash
KIMI_API_KEY=your_kimi_api_key_here
```

获取 API Key：https://platform.moonshot.cn/

## 使用方法

### 命令行方式

```bash
# 基础搜索
python3 skill/kimi-search/scripts/kimi_search.py "最新的AI技术新闻"

# 显示详细信息（包含 Token 使用量）
python3 skill/kimi-search/scripts/kimi_search.py "量子计算原理" --verbose

# JSON 格式输出
python3 skill/kimi-search/scripts/kimi_search.py "Python 最新版本" --json

# 自定义参数
python3 skill/kimi-search/scripts/kimi_search.py "搜索内容" \
  --model kimi-k2-turbo-preview \
  --temperature 0.7 \
  --max-tokens 16384
```

### Python 模块方式

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

print(result["content"])  # AI 生成的回答
print(result["usage"])    # Token 使用统计
```

### 作为 Claude Code 技能使用

1. 复制技能到 Claude Code 技能目录：

```bash
cp -r skill/kimi-search ~/.claude/skills/
```

2. 然后在 Claude Code 中直接使用，例如：
   - "搜索最新的科技新闻"
   - "用 Kimi 搜索量子计算资料"
   - "帮我查一下今天的热点"

## 工作原理

Kimi 的 `$web_search` 是一个内置函数，实现联网搜索功能：

1. 当 Kimi 检测到需要联网搜索时，返回 `finish_reason="tool_calls"`
2. 搜索由 **Kimi 内部执行** - 只需将参数原样返回即可
3. Kimi 执行搜索、读取结果并生成回答
4. 最终返回包含 AI 智能总结的内容

## API 参考

### `perform_search()`

```python
perform_search(
    query: str,                    # 搜索查询内容
    model: str = "kimi-k2-turbo-preview",
    temperature: float = 0.6,
    max_tokens: int = 32768,
    system_prompt: Optional[str] = None,
    verbose: bool = False
) -> Dict[str, Any]
```

返回字典包含：
- `content`: AI 生成的回答内容
- `usage`: Token 使用统计
- `search_tokens`: 搜索结果消耗的 Token 数

## 重要说明

### 模型选择

进行联网搜索时，**务必**使用 `kimi-k2-turbo-preview` 模型，原因：
- 搜索结果会消耗大量 Token
- 大上下文窗口可以容纳搜索结果
- 避免 "Input token length too long" 错误

### 费用说明

- 每次联网搜索调用收费 ¥0.03（3分钱）
- 额外的 Token 消耗按标准费率计费

### Token 使用

搜索结果会计入 `prompt_tokens`。使用 `--verbose` 参数可查看详细的 Token 使用明细。

## 项目结构

```
kimi-search-skill/
├── README.md                   # 项目说明文档
├── LICENSE                     # MIT 许可证
├── skill/
│   └── kimi-search/
│       ├── SKILL.md            # 技能文档
│       ├── .env.example        # 环境变量模板
│       ├── .env                # API Key 配置文件（未上传到 Git）
│       └── scripts/
│           └── kimi_search.py  # 核心搜索脚本
```

## 贡献指南

欢迎提交 Pull Request！贡献步骤：

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

本项目使用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 致谢

- [Moonshot AI](https://www.moonshot.cn/) 提供 Kimi API 和 `$web_search` 工具
- Claude Code 提供技能框架

## 问题反馈

遇到问题或有建议：

1. 查看 [Issues](https://github.com/comeonzhj/kimi-search-skill/issues) 页面
2. 创建新 Issue 并详细描述问题

---

⭐ 如果本项目对你有帮助，请给个 Star！

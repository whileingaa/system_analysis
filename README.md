# 系统监控AI助理

一个用于学习的轻量级AI助理，能够监控系统性能并通过LLM提供优化建议。

## 🎯 功能特性

- ✅ **系统监控**: 实时监控CPU、内存、磁盘、网络使用情况
- ✅ **AI建议**: 基于系统状态自动生成优化建议
- ✅ **对话功能**: 支持与AI进行系统优化相关的对话
- ✅ **历史记录**: 保存和管理对话历史
- ✅ **告警功能**: 当系统指标超过阈值时发出告警

## 📁 项目结构

```
system_analysis/
├── main.py                     # 旧版主入口（已废弃）
├── core/                       # 核心功能模块
│   ├── __init__.py            # 模块导出
│   ├── system_monitor.py      # 系统监控
│   ├── advisor.py             # AI建议引擎
│   ├── history_manager.py     # 历史记录管理
│   └── utils.py               # 工具函数
├── config/                     # 配置文件
│   └── settings.json          # 系统配置
├── data/                       # 数据存储
│   └── history.json           # 对话历史
├── tests/                      # 测试文件（可选）
└── README.md                   # 项目说明
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install psutil openai
```

### 2. 配置API Key

编辑 `config/settings.json`，填入你的OpenAI API Key：

```json
{
  "llm": {
    "api_key": "your-actual-api-key",
    "model": "gpt-3.5-turbo",
    "base_url": "https://api.openai.com/v1"
  }
}
```

### 3. 基础使用示例

运行example.py

```python
from core import (
    get_status,
    auto_advise,
    user_advise,
    get_history_list,
    switch_conversation,
    create_conversation
)

# 1. 获取系统状态
status = get_status()
print(f"CPU: {status['cpu']}%")
print(f"内存: {status['memory']}%")
print(f"摘要: {status['summary']}")

# 2. 获取AI建议
conv_id, advice = auto_advise(status)
print(f"\n建议:\n{advice}")

# 3. 与AI对话
response = user_advise(conv_id, "如何降低CPU使用率？")
print(f"\nAI回复:\n{response}")

# 4. 查看历史对话
history = get_history_list()
for conv in history:
    print(f"- [{conv['id']}] {conv['title']}")

# 5. 切换对话
messages = switch_conversation(conv_id)
for msg in messages:
    print(f"{msg['role']}: {msg['content'][:50]}...")
```

## 📚 核心API文档

### 系统监控 (`system_monitor.py`)

#### `get_status() -> Dict[str, Any]`
获取系统状态信息

**返回值:**
```python
{
    "cpu": 72.5,              # CPU使用率(%)
    "memory": 65.3,           # 内存使用率(%)
    "disk": 45.8,             # 磁盘使用率(%)
    "network_sent": 1024000,  # 网络发送字节
    "network_recv": 2048000,  # 网络接收字节
    "summary": "系统运行正常",
    "timestamp": "2024-10-25 14:30:22",
    "details": { ... }        # 详细信息
}
```

#### `get_top_processes(limit: int = 5) -> List[Dict]`
获取占用资源最多的进程

#### `check_alerts(status: Dict, thresholds: Dict = None) -> List[str]`
检查是否有需要告警的指标

### AI建议 (`advisor.py`)

#### `auto_advise(status: Dict[str, Any]) -> tuple[str, str]`
根据系统状态自动生成优化建议

**参数:**
- `status`: 系统状态字典（来自`get_status()`）

**返回值:**
- `(conv_id, advice)`: 对话ID和建议内容

**示例:**
```python
status = get_status()
conv_id, advice = auto_advise(status)
print(f"对话ID: {conv_id}")
print(f"建议: {advice}")
```

#### `user_advise(conv_id: str, text: str) -> str`
处理用户与AI的对话

**参数:**
- `conv_id`: 对话ID
- `text`: 用户输入的文本

**返回值:**
- AI的回复内容

**示例:**
```python
response = user_advise(conv_id, "如何优化内存使用？")
print(response)
```

### 历史管理 (`history_manager.py`)

#### `get_history_list() -> List[Dict[str, str]]`
获取历史对话列表

**返回值:**
```python
[
    {
        "id": "20241025_143022_123456",
        "title": "CPU性能分析",
        "timestamp": "2024-10-25 14:30:22"
    },
    ...
]
```

#### `create_conversation(title: str = None) -> str`
创建新对话

**返回值:** 新对话的ID

#### `switch_conversation(conv_id: str) -> List[Dict[str, str]]`
切换到指定对话

**返回值:** 消息列表
```python
[
    {
        "role": "user",
        "content": "如何优化CPU？",
        "timestamp": "2024-10-25 14:30:22"
    },
    {
        "role": "assistant",
        "content": "您可以尝试...",
        "timestamp": "2024-10-25 14:30:25"
    }
]
```

## ⚙️ 配置说明

`config/settings.json` 配置项：

```json
{
  "llm": {
    "api_key": "your-api-key",      // API密钥
    "model": "gpt-3.5-turbo",       // 模型名称
    "base_url": "https://...",      // API基础URL
    "temperature": 0.7,             // 温度参数
    "max_tokens": 1000              // 最大token数
  },
  "monitoring": {
    "update_interval": 5,           // 更新间隔(秒)
    "cpu_warning_threshold": 80,    // CPU告警阈值
    "memory_warning_threshold": 85, // 内存告警阈值
    "disk_warning_threshold": 90    // 磁盘告警阈值
  },
  "data": {
    "history_path": "./data/history.json",  // 历史记录路径
    "max_conversations": 100                 // 最大对话数
  }
}
```

## 🔧 高级用法

### 使用类接口

```python
from core.advisor import Advisor
from core.history_manager import HistoryManager
from core.system_monitor import get_status

# 自定义配置
advisor = Advisor("./my_config.json")
history_mgr = HistoryManager("./my_history.json")

# 获取状态并生成建议
status = get_status()
conv_id, advice = advisor.auto_advise(status)

# 管理对话
messages = history_mgr.switch_conversation(conv_id)
history_mgr.add_message(conv_id, "user", "新问题")
```

### 自定义告警阈值

```python
from core import get_status, check_alerts

status = get_status()
custom_thresholds = {
    "cpu": 70,
    "memory": 80,
    "disk": 85
}
alerts = check_alerts(status, custom_thresholds)
for alert in alerts:
    print(alert)
```

### 获取进程信息

```python
from core import get_top_processes

processes = get_top_processes(limit=10)
for proc in processes:
    print(f"{proc['name']}: CPU={proc['cpu']}%, Memory={proc['memory']}%")
```

## 🎨 UI集成建议

核心功能已完成，可以轻松集成到任何UI框架：

### Streamlit示例

```python
import streamlit as st
from core import get_status, auto_advise, user_advise, get_history_list

# 显示系统状态
status = get_status()
st.metric("CPU", f"{status['cpu']}%")
st.metric("内存", f"{status['memory']}%")

# 获取建议按钮
if st.button("获取建议"):
    conv_id, advice = auto_advise(status)
    st.session_state.current_conv = conv_id
    st.write(advice)

# 对话输入
if user_input := st.chat_input("输入消息"):
    response = user_advise(st.session_state.current_conv, user_input)
    st.write(response)
```

### Flask示例

```python
from flask import Flask, jsonify, request
from core import get_status, auto_advise, user_advise

app = Flask(__name__)

@app.route('/api/status')
def api_status():
    return jsonify(get_status())

@app.route('/api/advise', methods=['POST'])
def api_advise():
    status = get_status()
    conv_id, advice = auto_advise(status)
    return jsonify({"conv_id": conv_id, "advice": advice})

@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.json
    response = user_advise(data['conv_id'], data['text'])
    return jsonify({"response": response})
```

## 📝 注意事项

1. **API Key安全**: 不要将API Key提交到版本控制系统
2. **依赖安装**: 确保安装了`psutil`和`openai`库
3. **权限要求**: 某些系统监控功能可能需要管理员权限
4. **错误处理**: 所有函数都有基本的错误处理，会返回错误信息而不是抛出异常

## 🔮 扩展方向

- [ ] 支持更多LLM提供商（Claude、通义千问等）
- [ ] 添加GPU/温度监控
- [ ] 实现自动告警推送（邮件/webhook）
- [ ] 数据库支持（SQLite/PostgreSQL）
- [ ] 支持插件系统
- [ ] 性能数据可视化
- [ ] 导出报告功能

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

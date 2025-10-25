# API 参考文档

完整的API接口说明文档。

---

## 📊 系统监控模块 (`core.system_monitor`)

### `get_status() -> Dict[str, Any]`

获取系统状态信息。

**返回值：**
```python
{
    "cpu": 72.5,              # CPU使用率 (%)
    "memory": 65.3,           # 内存使用率 (%)
    "disk": 45.8,             # 磁盘使用率 (%)
    "network_sent": 1024000,  # 网络发送字节数
    "network_recv": 2048000,  # 网络接收字节数
    "summary": "系统运行正常", # 状态摘要
    "timestamp": "2024-10-25 14:30:22",
    "details": {              # 详细信息
        "cpu": {...},
        "memory": {...},
        "disk": {...},
        "network": {...},
        "process_count": 256,
        "system": {...}
    }
}
```

**示例：**
```python
from core import get_status

status = get_status()
print(f"CPU使用率: {status['cpu']}%")
if status['cpu'] > 80:
    print("⚠️ CPU负载过高！")
```

---

### `get_top_processes(limit: int = 5) -> List[Dict[str, Any]]`

获取占用资源最多的进程。

**参数：**
- `limit` (int): 返回的进程数量，默认5

**返回值：**
```python
[
    {
        "pid": 1234,
        "name": "chrome.exe",
        "cpu": 15.2,
        "memory": 8.5
    },
    ...
]
```

**示例：**
```python
from core import get_top_processes

processes = get_top_processes(limit=10)
for proc in processes:
    print(f"{proc['name']}: CPU={proc['cpu']}%")
```

---

### `get_system_uptime() -> str`

获取系统运行时间。

**返回值：** 运行时间字符串，如 "2天5小时30分钟"

**示例：**
```python
from core import get_system_uptime

uptime = get_system_uptime()
print(f"系统已运行: {uptime}")
```

---

### `check_alerts(status: Dict[str, Any], thresholds: Dict[str, float] = None) -> List[str]`

检查是否有需要告警的指标。

**参数：**
- `status` (dict): 系统状态字典（来自`get_status()`）
- `thresholds` (dict, optional): 告警阈值，默认为 `{"cpu": 80, "memory": 85, "disk": 90}`

**返回值：** 告警信息列表

**示例：**
```python
from core import get_status, check_alerts

status = get_status()

# 使用默认阈值
alerts = check_alerts(status)

# 使用自定义阈值
custom = {"cpu": 70, "memory": 75, "disk": 80}
alerts = check_alerts(status, custom)

for alert in alerts:
    print(alert)  # 如: "⚠️ CPU使用率过高: 85%"
```

---

## 🤖 AI建议模块 (`core.advisor`)

### `auto_advise(status: Dict[str, Any]) -> tuple[str, str]`

根据系统状态自动生成优化建议。

**参数：**
- `status` (dict): 系统状态字典（来自`get_status()`）

**返回值：** `(conv_id, advice)` - 对话ID和建议内容

**示例：**
```python
from core import get_status, auto_advise

status = get_status()
conv_id, advice = auto_advise(status)

print(f"对话ID: {conv_id}")
print(f"AI建议:\n{advice}")
```

**注意事项：**
- 需要在配置文件中设置有效的API Key
- 会自动创建新对话并保存到历史记录
- 调用会产生LLM API费用

---

### `user_advise(conv_id: str, text: str) -> str`

处理用户与AI的对话。

**参数：**
- `conv_id` (str): 对话ID
- `text` (str): 用户输入的文本

**返回值：** AI的回复内容

**示例：**
```python
from core import user_advise

# 在现有对话中继续交流
response = user_advise(conv_id, "如何降低CPU使用率？")
print(response)

# 多轮对话
questions = [
    "为什么内存占用这么高？",
    "有什么简单的优化方法吗？",
    "需要重启系统吗？"
]

for q in questions:
    response = user_advise(conv_id, q)
    print(f"Q: {q}")
    print(f"A: {response}\n")
```

---

### `Advisor` 类

高级用户可以直接使用 Advisor 类进行更灵活的配置。

**初始化：**
```python
from core.advisor import Advisor

advisor = Advisor(config_path="./my_config.json")
```

**方法：**
- `auto_advise(status)` - 自动生成建议
- `user_advise(conv_id, text)` - 处理对话
- `continue_conversation(conv_id, user_input)` - user_advise的别名

---

## 📚 历史管理模块 (`core.history_manager`)

### `get_history_list() -> List[Dict[str, str]]`

获取历史对话列表。

**返回值：**
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

**示例：**
```python
from core import get_history_list

history = get_history_list()
print(f"共有 {len(history)} 条历史对话")

for conv in history:
    print(f"[{conv['timestamp']}] {conv['title']}")
```

---

### `create_conversation(title: str = None) -> str`

创建新对话。

**参数：**
- `title` (str, optional): 对话标题，默认自动生成

**返回值：** 新对话的ID

**示例：**
```python
from core import create_conversation

# 自动生成标题
conv_id = create_conversation()

# 指定标题
conv_id = create_conversation("性能优化讨论")
print(f"已创建对话: {conv_id}")
```

---

### `switch_conversation(conv_id: str) -> Optional[List[Dict[str, str]]]`

切换到指定对话。

**参数：**
- `conv_id` (str): 对话ID

**返回值：** 消息列表，如果对话不存在返回None

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

**示例：**
```python
from core import switch_conversation

messages = switch_conversation(conv_id)
if messages:
    for msg in messages:
        role = "用户" if msg['role'] == 'user' else "AI"
        print(f"[{msg['timestamp']}] {role}: {msg['content']}")
else:
    print("对话不存在")
```

---

### `add_message(conv_id: str, role: str, content: str) -> bool`

向对话添加消息。

**参数：**
- `conv_id` (str): 对话ID
- `role` (str): 角色，"user" 或 "assistant"
- `content` (str): 消息内容

**返回值：** 是否成功

**示例：**
```python
from core import create_conversation, add_message

conv_id = create_conversation("测试对话")
add_message(conv_id, "user", "你好")
add_message(conv_id, "assistant", "你好！有什么可以帮你的吗？")
```

---

### `HistoryManager` 类

高级用户可以使用 HistoryManager 类获得更多控制。

**初始化：**
```python
from core.history_manager import HistoryManager

manager = HistoryManager(history_path="./my_history.json")
```

**方法：**
- `get_history_list()` - 获取对话列表
- `create_conversation(title, initial_message)` - 创建对话
- `get_conversation(conv_id)` - 获取完整对话信息
- `switch_conversation(conv_id)` - 切换对话
- `add_message(conv_id, role, content)` - 添加消息
- `delete_conversation(conv_id)` - 删除对话
- `clear_all_history()` - 清空所有历史
- `update_conversation_title(conv_id, new_title)` - 更新标题

**示例：**
```python
from core.history_manager import HistoryManager

manager = HistoryManager()

# 删除对话
manager.delete_conversation(conv_id)

# 更新标题
manager.update_conversation_title(conv_id, "新标题")

# 清空历史
manager.clear_all_history()
```

---

## 🛠️ 工具函数模块 (`core.utils`)

### `load_config(config_path: str = "./config/settings.json") -> Dict[str, Any]`

加载配置文件。

**示例：**
```python
from core.utils import load_config

config = load_config()
api_key = config['llm']['api_key']
```

---

### `save_config(config: Dict[str, Any], config_path: str = "./config/settings.json") -> bool`

保存配置文件。

**示例：**
```python
from core.utils import load_config, save_config

config = load_config()
config['llm']['temperature'] = 0.8
save_config(config)
```

---

### `generate_conversation_id() -> str`

生成唯一的对话ID（基于时间戳）。

**返回值：** 如 "20241025_143022_123456"

---

### `format_timestamp(timestamp: str = None) -> str`

格式化时间戳为可读格式。

**示例：**
```python
from core.utils import format_timestamp

# 格式化现在的时间
now = format_timestamp()  # "2024-10-25 14:30:22"

# 格式化指定时间戳
time_str = format_timestamp("20241025_143022_123456")
```

---

### `format_bytes(bytes_value: int) -> str`

格式化字节数为可读格式。

**示例：**
```python
from core.utils import format_bytes

print(format_bytes(1024))           # "1.00 KB"
print(format_bytes(1024*1024))      # "1.00 MB"
print(format_bytes(1024*1024*1024)) # "1.00 GB"
```

---

### `truncate_text(text: str, max_length: int = 50) -> str`

截断文本到指定长度。

**示例：**
```python
from core.utils import truncate_text

long_text = "这是一段很长的文本..." * 10
short = truncate_text(long_text, 50)
print(short)  # 最多50个字符，超出部分显示为...
```

---

## 🔄 完整使用流程示例

```python
from core import (
    get_status,
    auto_advise,
    user_advise,
    get_history_list,
    switch_conversation,
    create_conversation
)

# 1. 启动应用 - 获取系统状态
print("=== 系统状态 ===")
status = get_status()
print(f"CPU: {status['cpu']}%")
print(f"内存: {status['memory']}%")
print(f"磁盘: {status['disk']}%")

# 2. 获取AI建议
print("\n=== 获取AI建议 ===")
conv_id, advice = auto_advise(status)
print(f"建议: {advice}")

# 3. 与AI对话
print("\n=== 与AI对话 ===")
response = user_advise(conv_id, "有什么快速优化的方法吗？")
print(f"AI: {response}")

# 4. 查看历史
print("\n=== 历史对话 ===")
history = get_history_list()
for conv in history[:5]:  # 显示前5条
    print(f"- {conv['title']} [{conv['timestamp']}]")

# 5. 切换对话
print("\n=== 切换对话 ===")
messages = switch_conversation(conv_id)
for msg in messages[-3:]:  # 显示最后3条消息
    role = "用户" if msg['role'] == 'user' else "AI"
    print(f"{role}: {msg['content'][:50]}...")
```

---

## ⚙️ 配置文件格式

`config/settings.json`:

```json
{
  "llm": {
    "api_key": "sk-...",
    "model": "gpt-3.5-turbo",
    "base_url": "https://api.openai.com/v1",
    "temperature": 0.7,
    "max_tokens": 1000
  },
  "monitoring": {
    "update_interval": 5,
    "cpu_warning_threshold": 80,
    "memory_warning_threshold": 85,
    "disk_warning_threshold": 90
  },
  "data": {
    "history_path": "./data/history.json",
    "max_conversations": 100
  }
}
```

---

## 🚨 错误处理

所有函数都包含错误处理，不会抛出异常，而是返回错误信息：

```python
from core import auto_advise, get_status

status = get_status()
conv_id, advice = auto_advise(status)

if "失败" in advice or "错误" in advice:
    print(f"发生错误: {advice}")
    # 可能的错误：
    # - "请先安装openai库"
    # - "请在配置文件中设置有效的API Key"
    # - "OpenAI API调用失败: ..."
else:
    print(f"成功: {advice}")
```

---

## 📝 类型提示

所有函数都有完整的类型提示：

```python
def get_status() -> Dict[str, Any]: ...
def auto_advise(status: Dict[str, Any]) -> tuple[str, str]: ...
def user_advise(conv_id: str, text: str) -> str: ...
def get_history_list() -> List[Dict[str, str]]: ...
```

使用IDE时可以获得完整的自动补全和类型检查。

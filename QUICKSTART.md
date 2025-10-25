# 快速开始指南

## 📦 安装依赖

```bash
pip install psutil openai
```

## ⚙️ 配置API Key

1. 复制配置示例文件：
   ```bash
   copy config\settings.example.json config\settings.json
   ```

2. 编辑 `config/settings.json`，填入你的OpenAI API Key：
   ```json
   {
     "llm": {
       "api_key": "sk-your-actual-api-key-here"
     }
   }
   ```

## 🚀 运行测试

```bash
# 基础功能测试
python test_basic.py

# 完整功能演示
python example.py
```

## 💻 基本使用

### 1. 监控系统状态

```python
from core import get_status

status = get_status()
print(f"CPU: {status['cpu']}%")
print(f"内存: {status['memory']}%")
print(f"磁盘: {status['disk']}%")
```

### 2. 获取AI建议

```python
from core import get_status, auto_advise

status = get_status()
conv_id, advice = auto_advise(status)
print(advice)
```

### 3. 与AI对话

```python
from core import user_advise

response = user_advise(conv_id, "如何优化CPU使用率？")
print(response)
```

### 4. 管理历史对话

```python
from core import get_history_list, switch_conversation

# 获取历史列表
history = get_history_list()
for conv in history:
    print(f"{conv['title']} - {conv['timestamp']}")

# 切换到某个对话
messages = switch_conversation(conv_id)
for msg in messages:
    print(f"{msg['role']}: {msg['content']}")
```

## 🎨 集成到UI

### Streamlit示例

```python
import streamlit as st
from core import get_status, auto_advise, user_advise

st.title("系统监控AI助理")

# 显示系统状态
status = get_status()
col1, col2, col3 = st.columns(3)
col1.metric("CPU", f"{status['cpu']}%")
col2.metric("内存", f"{status['memory']}%")
col3.metric("磁盘", f"{status['disk']}%")

# 获取建议
if st.button("获取AI建议"):
    conv_id, advice = auto_advise(status)
    st.session_state.conv_id = conv_id
    st.write(advice)

# 对话界面
if "conv_id" in st.session_state:
    user_input = st.chat_input("输入你的问题")
    if user_input:
        response = user_advise(st.session_state.conv_id, user_input)
        st.write(response)
```

运行：
```bash
pip install streamlit
streamlit run app.py
```

### Flask示例

```python
from flask import Flask, jsonify, request
from core import get_status, auto_advise, user_advise

app = Flask(__name__)

@app.route('/api/status')
def status():
    return jsonify(get_status())

@app.route('/api/advise', methods=['POST'])
def advise():
    status = get_status()
    conv_id, advice = auto_advise(status)
    return jsonify({"conv_id": conv_id, "advice": advice})

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    response = user_advise(data['conv_id'], data['message'])
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
```

## 📁 项目结构

```
system_analysis/
├── core/                    # 核心功能（已实现✅）
│   ├── system_monitor.py   # 系统监控
│   ├── advisor.py          # AI建议引擎
│   ├── history_manager.py  # 历史管理
│   └── utils.py            # 工具函数
├── config/                  # 配置文件
│   ├── settings.json       # 实际配置（需要配置）
│   └── settings.example.json # 配置示例
├── data/                    # 数据存储
│   └── history.json        # 对话历史
├── test_basic.py           # 基础测试
├── example.py              # 完整示例
└── README.md               # 详细文档
```

## ❓ 常见问题

### Q: 如何使用其他LLM提供商？

A: 修改 `config/settings.json` 中的 `base_url` 和 `model`。支持OpenAI兼容的API接口。

### Q: CPU显示为0%是正常的吗？

A: 是的，`psutil.cpu_percent()` 在首次调用时可能返回0。实际使用时会正常显示。

### Q: 如何清空历史记录？

```python
from core.history_manager import get_manager
manager = get_manager()
manager.clear_all_history()
```

### Q: 如何自定义告警阈值？

```python
from core import check_alerts

custom_thresholds = {
    "cpu": 70,
    "memory": 80,
    "disk": 85
}
alerts = check_alerts(status, custom_thresholds)
```

## 📝 注意事项

1. **API Key安全**：不要将包含真实API Key的配置文件提交到Git
2. **首次运行**：第一次调用CPU监控可能返回0，这是正常的
3. **权限要求**：某些系统监控功能可能需要管理员权限
4. **网络连接**：AI功能需要网络连接来调用LLM API

## 🔗 相关资源

- 完整文档：查看 `README.md`
- 代码示例：查看 `example.py`
- 测试代码：查看 `test_basic.py`

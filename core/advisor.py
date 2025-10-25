"""
AI建议模块
负责调用LLM生成系统优化建议和处理用户对话
"""
import json
from typing import Dict, Any, Optional
from .utils import load_config
from .history_manager import get_manager, create_conversation, add_message


class Advisor:
    """AI顾问类"""
    
    def __init__(self, config_path: str = "./config/settings.json"):
        """
        初始化AI顾问
        
        Args:
            config_path: 配置文件路径
        """
        self.config = load_config(config_path)
        self.llm_config = self.config.get("llm", {})
        self.history_manager = get_manager()
        
    def _call_llm(self, messages: list, system_prompt: str = None) -> str:
        """
        调用LLM API
        
        Args:
            messages: 消息列表
            system_prompt: 系统提示词
            
        Returns:
            LLM的回复
        """
        try:
            return self._call_openai(messages, system_prompt)
        except Exception as e:
            return f"调用LLM失败: {str(e)}"
    
    def _call_openai(self, messages: list, system_prompt: str = None) -> str:
        """
        调用OpenAI API
        
        Args:
            messages: 消息列表
            system_prompt: 系统提示词
            
        Returns:
            LLM的回复
        """
        try:
            # 尝试导入openai库
            try:
                import openai
            except ImportError:
                return "请先安装openai库: pip install openai"
            
            api_key = self.llm_config.get("api_key", "")
            if not api_key or api_key == "your-api-key-here":
                return "请在配置文件中设置有效的API Key"
            
            # 设置API配置
            client = openai.OpenAI(
                api_key=api_key,
                base_url=self.llm_config.get("base_url", "https://api.openai.com/v1")
            )
            
            # 准备消息
            api_messages = []
            if system_prompt:
                api_messages.append({"role": "system", "content": system_prompt})
            
            for msg in messages:
                api_messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                })
            
            # 调用API
            response = client.chat.completions.create(
                model=self.llm_config.get("model", "gpt-3.5-turbo"),
                messages=api_messages,
                temperature=self.llm_config.get("temperature", 0.7),
                max_tokens=self.llm_config.get("max_tokens", 1000)
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"OpenAI API调用失败: {str(e)}\n\n提示：请确保已安装openai库并配置了正确的API Key"
    
    def auto_advise(self, status: Dict[str, Any]) -> tuple[str, str]:
        """
        根据系统状态自动生成优化建议
        
        Args:
            status: 系统状态字典（来自system_monitor.get_status()）
            
        Returns:
            (conv_id, advice) - 对话ID和建议内容
        """
        # 构建系统提示词
        system_prompt = """你是一个专业的系统性能分析助手。
根据用户提供的系统状态数据，分析系统性能并给出具体的优化建议。
建议应该：
1. 简洁明了，条理清晰
2. 针对具体问题提供可操作的解决方案
3. 考虑不同严重程度的问题
4. 使用友好的语气
"""
        
        # 构建用户消息
        user_message = f"""请分析以下系统状态并给出优化建议：

CPU使用率: {status.get('cpu', 0)}%
内存使用率: {status.get('memory', 0)}%
磁盘使用率: {status.get('disk', 0)}%
系统摘要: {status.get('summary', '未知')}

请提供详细的分析和建议。"""
        
        # 调用LLM
        messages = [{"role": "user", "content": user_message}]
        advice = self._call_llm(messages, system_prompt)
        
        # 创建新对话并保存
        conv_id = create_conversation("系统性能分析")
        add_message(conv_id, "user", user_message)
        add_message(conv_id, "assistant", advice)
        
        return conv_id, advice
    
    def user_advise(self, conv_id: str, text: str) -> str:
        """
        处理用户与AI的对话
        
        Args:
            conv_id: 对话ID
            text: 用户输入的文本
            
        Returns:
            AI的回复
        """
        # 获取对话历史
        conversation = self.history_manager.get_conversation(conv_id)
        if not conversation:
            return "对话不存在，请先创建新对话"
        
        # 构建系统提示词
        system_prompt = """你是一个专业的系统性能分析和优化助手。
你可以：
1. 回答关于系统性能、资源管理的问题
2. 提供系统优化建议
3. 解释技术概念
4. 帮助用户诊断和解决系统问题

请用友好、专业的语气与用户交流。"""
        
        # 获取历史消息
        history_messages = conversation.get("messages", [])
        
        # 调用LLM
        response = self._call_llm(history_messages + [{"role": "user", "content": text}], system_prompt)
        
        # 保存消息
        add_message(conv_id, "user", text)
        add_message(conv_id, "assistant", response)
        
        return response
    
    def continue_conversation(self, conv_id: str, user_input: str) -> str:
        """
        继续现有对话（user_advise的别名）
        
        Args:
            conv_id: 对话ID
            user_input: 用户输入
            
        Returns:
            AI的回复
        """
        return self.user_advise(conv_id, user_input)


# 提供便捷的函数接口
_default_advisor = None

def get_advisor(config_path: str = "./config/settings.json") -> Advisor:
    """获取默认的advisor实例"""
    global _default_advisor
    if _default_advisor is None:
        _default_advisor = Advisor(config_path)
    return _default_advisor


def auto_advise(status: Dict[str, Any]) -> tuple[str, str]:
    """
    根据系统状态自动生成优化建议
    
    Args:
        status: 系统状态字典
        
    Returns:
        (conv_id, advice) - 对话ID和建议内容
    """
    return get_advisor().auto_advise(status)


def user_advise(conv_id: str, text: str) -> str:
    """
    处理用户与AI的对话
    
    Args:
        conv_id: 对话ID
        text: 用户输入的文本
        
    Returns:
        AI的回复
    """
    return get_advisor().user_advise(conv_id, text)

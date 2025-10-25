"""
工具函数模块
提供通用的辅助功能
"""
import json
import os
from datetime import datetime
from typing import Dict, Any


def load_config(config_path: str = "./config/settings.json") -> Dict[str, Any]:
    """
    加载配置文件
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        配置字典
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # 返回默认配置
        return {
            "llm": {
                "provider": "openai",
                "api_key": "",
                "model": "gpt-3.5-turbo",
                "temperature": 0.7,
                "max_tokens": 1000
            },
            "monitoring": {
                "update_interval": 5,
                "cpu_warning_threshold": 80,
                "memory_warning_threshold": 85,
                "disk_warning_threshold": 90
            }
        }


def save_config(config: Dict[str, Any], config_path: str = "./config/settings.json") -> bool:
    """
    保存配置文件
    
    Args:
        config: 配置字典
        config_path: 配置文件路径
        
    Returns:
        是否保存成功
    """
    try:
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"保存配置失败: {e}")
        return False


def generate_conversation_id() -> str:
    """
    生成对话ID（基于时间戳）
    
    Returns:
        对话ID字符串
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S_%f")


def format_timestamp(timestamp: str = None) -> str:
    """
    格式化时间戳为可读格式
    
    Args:
        timestamp: 时间戳字符串，如果为None则使用当前时间
        
    Returns:
        格式化后的时间字符串
    """
    if timestamp is None:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        # 尝试解析时间戳格式
        dt = datetime.strptime(timestamp, "%Y%m%d_%H%M%S_%f")
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return timestamp


def format_bytes(bytes_value: int) -> str:
    """
    格式化字节数为可读格式
    
    Args:
        bytes_value: 字节数
        
    Returns:
        格式化后的字符串（如 "1.5 GB"）
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"


def ensure_data_directory(data_path: str) -> bool:
    """
    确保数据目录存在
    
    Args:
        data_path: 数据文件路径
        
    Returns:
        是否成功
    """
    try:
        directory = os.path.dirname(data_path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        return True
    except Exception as e:
        print(f"创建目录失败: {e}")
        return False


def truncate_text(text: str, max_length: int = 50) -> str:
    """
    截断文本到指定长度
    
    Args:
        text: 原始文本
        max_length: 最大长度
        
    Returns:
        截断后的文本
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

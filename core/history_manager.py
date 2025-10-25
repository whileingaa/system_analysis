"""
历史记录管理模块
负责对话历史的存储、读取和管理
"""
import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
from .utils import generate_conversation_id, format_timestamp, truncate_text, ensure_data_directory


class HistoryManager:
    """历史记录管理器"""
    
    def __init__(self, history_path: str = "./data/history.json"):
        """
        初始化历史管理器
        
        Args:
            history_path: 历史记录文件路径
        """
        self.history_path = history_path
        ensure_data_directory(history_path)
        self._ensure_history_file()
    
    def _ensure_history_file(self):
        """确保历史记录文件存在"""
        if not os.path.exists(self.history_path):
            self._save_data({"conversations": []})
    
    def _load_data(self) -> Dict[str, Any]:
        """加载历史数据"""
        try:
            with open(self.history_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"conversations": []}
    
    def _save_data(self, data: Dict[str, Any]):
        """保存历史数据"""
        try:
            with open(self.history_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"保存历史记录失败: {e}")
    
    def get_history_list(self) -> List[Dict[str, str]]:
        """
        获取历史对话列表
        
        Returns:
            对话列表，每个元素包含 id 和 title
            [
                {"id": "20241025_143022_123456", "title": "CPU性能分析", "timestamp": "2024-10-25 14:30:22"},
                ...
            ]
        """
        data = self._load_data()
        conversations = data.get("conversations", [])
        
        # 返回简化的列表信息
        result = []
        for conv in conversations:
            result.append({
                "id": conv.get("id", ""),
                "title": conv.get("title", "未命名对话"),
                "timestamp": conv.get("created_at", "")
            })
        
        # 按时间倒序排列（最新的在前面）
        result.reverse()
        return result
    
    def create_conversation(self, title: str = None, initial_message: Dict[str, str] = None) -> str:
        """
        创建新对话
        
        Args:
            title: 对话标题，如果为None则自动生成
            initial_message: 初始消息（可选）
            
        Returns:
            新对话的ID
        """
        conv_id = generate_conversation_id()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if title is None:
            title = f"对话 {timestamp}"
        
        conversation = {
            "id": conv_id,
            "title": title,
            "created_at": timestamp,
            "updated_at": timestamp,
            "messages": []
        }
        
        # 如果有初始消息，添加进去
        if initial_message:
            conversation["messages"].append(initial_message)
        
        # 保存到历史记录
        data = self._load_data()
        data["conversations"].append(conversation)
        self._save_data(data)
        
        return conv_id
    
    def get_conversation(self, conv_id: str) -> Optional[Dict[str, Any]]:
        """
        获取指定对话的完整信息
        
        Args:
            conv_id: 对话ID
            
        Returns:
            对话信息字典，如果不存在返回None
        """
        data = self._load_data()
        for conv in data["conversations"]:
            if conv["id"] == conv_id:
                return conv
        return None
    
    def switch_conversation(self, conv_id: str) -> Optional[List[Dict[str, str]]]:
        """
        切换到指定对话
        
        Args:
            conv_id: 对话ID
            
        Returns:
            消息列表，如果对话不存在返回None
            [
                {"role": "user", "content": "...", "timestamp": "..."},
                {"role": "assistant", "content": "...", "timestamp": "..."},
                ...
            ]
        """
        conversation = self.get_conversation(conv_id)
        if conversation:
            return conversation.get("messages", [])
        return None
    
    def add_message(self, conv_id: str, role: str, content: str) -> bool:
        """
        向对话添加消息
        
        Args:
            conv_id: 对话ID
            role: 角色 ("user" 或 "assistant")
            content: 消息内容
            
        Returns:
            是否成功
        """
        data = self._load_data()
        
        for conv in data["conversations"]:
            if conv["id"] == conv_id:
                message = {
                    "role": role,
                    "content": content,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                conv["messages"].append(message)
                conv["updated_at"] = message["timestamp"]
                
                # 如果是第一条用户消息，用它来更新标题
                if role == "user" and len(conv["messages"]) == 1:
                    conv["title"] = truncate_text(content, 30)
                
                self._save_data(data)
                return True
        
        return False
    
    def delete_conversation(self, conv_id: str) -> bool:
        """
        删除指定对话
        
        Args:
            conv_id: 对话ID
            
        Returns:
            是否成功
        """
        data = self._load_data()
        conversations = data["conversations"]
        
        original_length = len(conversations)
        data["conversations"] = [c for c in conversations if c["id"] != conv_id]
        
        if len(data["conversations"]) < original_length:
            self._save_data(data)
            return True
        return False
    
    def clear_all_history(self) -> bool:
        """
        清空所有历史记录
        
        Returns:
            是否成功
        """
        try:
            self._save_data({"conversations": []})
            return True
        except Exception as e:
            print(f"清空历史记录失败: {e}")
            return False
    
    def update_conversation_title(self, conv_id: str, new_title: str) -> bool:
        """
        更新对话标题
        
        Args:
            conv_id: 对话ID
            new_title: 新标题
            
        Returns:
            是否成功
        """
        data = self._load_data()
        
        for conv in data["conversations"]:
            if conv["id"] == conv_id:
                conv["title"] = new_title
                conv["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._save_data(data)
                return True
        
        return False


# 提供便捷的函数接口
_default_manager = None

def get_manager(history_path: str = "./data/history.json") -> HistoryManager:
    """获取默认的历史管理器实例"""
    global _default_manager
    if _default_manager is None:
        _default_manager = HistoryManager(history_path)
    return _default_manager


def get_history_list() -> List[Dict[str, str]]:
    """获取历史对话列表"""
    return get_manager().get_history_list()


def switch_conversation(conv_id: str) -> Optional[List[Dict[str, str]]]:
    """切换到指定对话"""
    return get_manager().switch_conversation(conv_id)


def create_conversation(title: str = None) -> str:
    """创建新对话"""
    return get_manager().create_conversation(title)


def add_message(conv_id: str, role: str, content: str) -> bool:
    """向对话添加消息"""
    return get_manager().add_message(conv_id, role, content)

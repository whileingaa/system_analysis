"""
系统监控AI助理 - 核心模块
"""

from .system_monitor import (
    get_status,
    get_top_processes,
    get_system_uptime,
    check_alerts
)

from .advisor import (
    auto_advise,
    user_advise,
    get_advisor,
    Advisor
)

from .history_manager import (
    get_history_list,
    switch_conversation,
    create_conversation,
    add_message,
    get_manager,
    HistoryManager
)

from .utils import (
    load_config,
    save_config,
    generate_conversation_id,
    format_timestamp,
    format_bytes
)

__all__ = [
    # 系统监控
    'get_status',
    'get_top_processes',
    'get_system_uptime',
    'check_alerts',
    
    # AI建议
    'auto_advise',
    'user_advise',
    'get_advisor',
    'Advisor',
    
    # 历史管理
    'get_history_list',
    'switch_conversation',
    'create_conversation',
    'add_message',
    'get_manager',
    'HistoryManager',
    
    # 工具函数
    'load_config',
    'save_config',
    'generate_conversation_id',
    'format_timestamp',
    'format_bytes'
]

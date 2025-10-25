"""
系统监控AI助理 - 使用示例

这个文件演示了如何使用核心功能模块
"""

from core import (
    # 系统监控
    get_status,
    get_top_processes,
    get_system_uptime,
    check_alerts,
    
    # AI建议
    auto_advise,
    user_advise,
    
    # 历史管理
    get_history_list,
    switch_conversation,
    create_conversation,
    
    # 工具函数
    format_bytes,
    load_config
)


def demo_system_monitor():
    """演示系统监控功能"""
    print("=" * 60)
    print("1. 系统监控演示")
    print("=" * 60)
    
    # 获取系统状态
    status = get_status()
    print(f"\n📊 系统状态:")
    print(f"  CPU使用率: {status['cpu']}%")
    print(f"  内存使用率: {status['memory']}%")
    print(f"  磁盘使用率: {status['disk']}%")
    print(f"  状态摘要: {status['summary']}")
    print(f"  检测时间: {status['timestamp']}")
    
    # 检查告警
    alerts = check_alerts(status)
    if alerts:
        print(f"\n⚠️ 告警信息:")
        for alert in alerts:
            print(f"  {alert}")
    else:
        print(f"\n✅ 系统运行正常，无告警")
    
    # 显示详细信息
    details = status.get('details', {})
    if details:
        print(f"\n📝 详细信息:")
        
        # CPU详情
        cpu = details.get('cpu', {})
        print(f"  CPU核心数: 物理{cpu.get('count_physical', 0)}核 / 逻辑{cpu.get('count_logical', 0)}核")
        
        # 内存详情
        memory = details.get('memory', {})
        print(f"  内存使用: {format_bytes(memory.get('used', 0))} / {format_bytes(memory.get('total', 0))}")
        print(f"  可用内存: {format_bytes(memory.get('available', 0))}")
        
        # 磁盘详情
        disk = details.get('disk', {})
        print(f"  磁盘使用: {format_bytes(disk.get('used', 0))} / {format_bytes(disk.get('total', 0))}")
        print(f"  可用空间: {format_bytes(disk.get('free', 0))}")
        
        # 网络详情
        network = details.get('network', {})
        print(f"  网络发送: {format_bytes(network.get('bytes_sent', 0))}")
        print(f"  网络接收: {format_bytes(network.get('bytes_recv', 0))}")
    
    # 获取系统运行时间
    uptime = get_system_uptime()
    print(f"\n⏱️ 系统运行时间: {uptime}")
    
    # 获取占用资源最多的进程
    print(f"\n🔝 占用资源最多的5个进程:")
    processes = get_top_processes(limit=5)
    for i, proc in enumerate(processes, 1):
        print(f"  {i}. {proc['name']} (PID: {proc['pid']})")
        print(f"     CPU: {proc['cpu']}% | 内存: {proc['memory']:.2f}%")


def demo_ai_advisor():
    """演示AI建议功能"""
    print("\n" + "=" * 60)
    print("2. AI建议演示")
    print("=" * 60)
    
    # 获取系统状态
    status = get_status()
    
    print(f"\n🤖 正在分析系统状态并生成建议...")
    print(f"   (注意: 这需要调用LLM API，请确保已配置API Key)")
    
    try:
        # 生成自动建议
        conv_id, advice = auto_advise(status)
        
        print(f"\n✅ 建议生成成功!")
        print(f"   对话ID: {conv_id}")
        print(f"\n💡 AI建议:")
        print("-" * 60)
        print(advice)
        print("-" * 60)
        
        # 继续对话
        print(f"\n💬 继续与AI对话...")
        follow_up = "有什么简单的方法可以快速释放一些内存？"
        print(f"   用户: {follow_up}")
        
        response = user_advise(conv_id, follow_up)
        print(f"\n   AI: {response}")
        
        return conv_id
        
    except Exception as e:
        print(f"\n❌ 生成建议失败: {e}")
        print(f"   提示: 请检查config/settings.json中的API配置")
        return None


def demo_history_manager(conv_id=None):
    """演示历史管理功能"""
    print("\n" + "=" * 60)
    print("3. 历史管理演示")
    print("=" * 60)
    
    # 获取历史对话列表
    history_list = get_history_list()
    
    if not history_list:
        print(f"\n📭 暂无历史对话记录")
        
        # 创建一个示例对话
        print(f"\n创建示例对话...")
        demo_id = create_conversation("示例对话")
        print(f"✅ 已创建对话: {demo_id}")
        
        history_list = get_history_list()
    
    print(f"\n📚 历史对话列表 (共{len(history_list)}条):")
    for i, conv in enumerate(history_list[:5], 1):  # 只显示前5条
        print(f"  {i}. [{conv['id']}]")
        print(f"     标题: {conv['title']}")
        print(f"     时间: {conv['timestamp']}")
    
    if len(history_list) > 5:
        print(f"  ... 还有{len(history_list) - 5}条对话")
    
    # 切换到指定对话
    if conv_id or history_list:
        target_id = conv_id if conv_id else history_list[0]['id']
        print(f"\n🔄 切换到对话: {target_id}")
        
        messages = switch_conversation(target_id)
        if messages:
            print(f"\n💬 对话内容 (共{len(messages)}条消息):")
            for msg in messages:
                role = "👤 用户" if msg['role'] == 'user' else "🤖 AI"
                content = msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content']
                print(f"\n{role} [{msg['timestamp']}]:")
                print(f"  {content}")
        else:
            print(f"  该对话暂无消息")


def demo_config():
    """演示配置管理"""
    print("\n" + "=" * 60)
    print("4. 配置信息")
    print("=" * 60)
    
    config = load_config()
    
    print(f"\n⚙️ 当前配置:")
    print(f"  LLM提供商: {config.get('llm', {}).get('provider', 'unknown')}")
    print(f"  LLM模型: {config.get('llm', {}).get('model', 'unknown')}")
    print(f"  API配置: {'✅ 已配置' if config.get('llm', {}).get('api_key') not in ['', 'your-api-key-here', None] else '❌ 未配置'}")
    
    monitoring = config.get('monitoring', {})
    print(f"\n📊 监控配置:")
    print(f"  CPU告警阈值: {monitoring.get('cpu_warning_threshold', 80)}%")
    print(f"  内存告警阈值: {monitoring.get('memory_warning_threshold', 85)}%")
    print(f"  磁盘告警阈值: {monitoring.get('disk_warning_threshold', 90)}%")


def main():
    """主函数"""
    print("🚀 系统监控AI助理 - 功能演示")
    print("=" * 60)
    
    # 1. 系统监控演示
    demo_system_monitor()
    
    # 2. AI建议演示
    conv_id = demo_ai_advisor()
    
    # 3. 历史管理演示
    demo_history_manager(conv_id)
    
    # 4. 配置信息
    demo_config()
    
    print("\n" + "=" * 60)
    print("✅ 演示完成!")
    print("=" * 60)
    print("\n💡 提示:")
    print("  - 如需使用AI功能，请在 config/settings.json 中配置API Key")
    print("  - 查看 README.md 了解详细使用文档")
    print("  - 查看 core/ 目录下的各个模块了解更多功能")


if __name__ == "__main__":
    main()

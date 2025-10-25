"""
快速测试脚本 - 测试基本功能是否正常工作
"""

def test_system_monitor():
    """测试系统监控功能"""
    print("🧪 测试系统监控功能...")
    try:
        from core.system_monitor import get_status, get_top_processes
        
        status = get_status()
        assert 'cpu' in status
        assert 'memory' in status
        assert 'disk' in status
        print(f"✅ 系统监控: CPU={status['cpu']}%, 内存={status['memory']}%, 磁盘={status['disk']}%")
        
        processes = get_top_processes(3)
        print(f"✅ 进程监控: 获取到{len(processes)}个进程")
        return True
    except Exception as e:
        print(f"❌ 系统监控测试失败: {e}")
        return False


def test_history_manager():
    """测试历史管理功能"""
    print("\n🧪 测试历史管理功能...")
    try:
        from core.history_manager import (
            create_conversation, 
            get_history_list, 
            add_message,
            switch_conversation
        )
        
        # 创建对话
        conv_id = create_conversation("测试对话")
        print(f"✅ 创建对话: {conv_id}")
        
        # 添加消息
        add_message(conv_id, "user", "测试消息")
        add_message(conv_id, "assistant", "测试回复")
        print(f"✅ 添加消息成功")
        
        # 获取历史列表
        history = get_history_list()
        print(f"✅ 历史列表: 共{len(history)}条对话")
        
        # 切换对话
        messages = switch_conversation(conv_id)
        assert len(messages) == 2
        print(f"✅ 切换对话: 包含{len(messages)}条消息")
        
        return True
    except Exception as e:
        print(f"❌ 历史管理测试失败: {e}")
        return False


def test_utils():
    """测试工具函数"""
    print("\n🧪 测试工具函数...")
    try:
        from core.utils import (
            format_bytes, 
            generate_conversation_id,
            truncate_text
        )
        
        # 测试格式化字节
        assert "1.00 KB" == format_bytes(1024)
        assert "1.00 MB" == format_bytes(1024 * 1024)
        print(f"✅ 字节格式化: {format_bytes(1024*1024*1024)}")
        
        # 测试生成ID
        conv_id = generate_conversation_id()
        assert len(conv_id) > 0
        print(f"✅ 生成ID: {conv_id}")
        
        # 测试截断文本
        text = truncate_text("这是一个很长的测试文本" * 10, 30)
        assert len(text) <= 30
        print(f"✅ 文本截断: {text}")
        
        return True
    except Exception as e:
        print(f"❌ 工具函数测试失败: {e}")
        return False


def test_config():
    """测试配置加载"""
    print("\n🧪 测试配置管理...")
    try:
        from core.utils import load_config
        
        config = load_config()
        assert 'llm' in config
        assert 'monitoring' in config
        print(f"✅ 配置加载成功")
        print(f"   - LLM模型: {config['llm'].get('model')}")
        
        return True
    except Exception as e:
        print(f"❌ 配置管理测试失败: {e}")
        return False


def test_advisor_structure():
    """测试AI顾问模块结构（不实际调用API）"""
    print("\n🧪 测试AI顾问模块结构...")
    try:
        from core.advisor import Advisor, get_advisor
        
        advisor = get_advisor()
        assert advisor is not None
        assert hasattr(advisor, 'auto_advise')
        assert hasattr(advisor, 'user_advise')
        print(f"✅ AI顾问模块结构正确")
        print(f"   提示: 实际使用需要配置API Key")
        
        return True
    except Exception as e:
        print(f"❌ AI顾问模块测试失败: {e}")
        return False


def main():
    """运行所有测试"""
    print("=" * 60)
    print("🚀 系统监控AI助理 - 快速测试")
    print("=" * 60)
    
    tests = [
        ("系统监控", test_system_monitor),
        ("历史管理", test_history_manager),
        ("工具函数", test_utils),
        ("配置管理", test_config),
        ("AI顾问", test_advisor_structure),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name}测试异常: {e}")
            results.append((name, False))
    
    # 打印测试结果
    print("\n" + "=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} - {name}")
    
    print(f"\n总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！系统已就绪。")
        print("\n💡 下一步:")
        print("   1. 编辑 config/settings.json 配置API Key")
        print("   2. 运行 python example.py 查看完整演示")
        print("   3. 开始构建您的UI界面")
    else:
        print("\n⚠️ 部分测试失败，请检查错误信息")
    
    print("=" * 60)


if __name__ == "__main__":
    main()

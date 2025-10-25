"""
系统监控模块
负责获取系统性能数据（CPU、内存、磁盘、网络等）
"""
import psutil
import platform
from typing import Dict, Any, List
from datetime import datetime


def get_status() -> Dict[str, Any]:
    """
    获取系统状态信息
    
    Returns:
        包含系统各项指标的字典:
        {
            "cpu": float,           # CPU使用率 (%)
            "memory": float,        # 内存使用率 (%)
            "disk": float,          # 磁盘使用率 (%)
            "network_sent": int,    # 网络发送字节数
            "network_recv": int,    # 网络接收字节数
            "summary": str,         # 系统状态摘要
            "timestamp": str,       # 时间戳
            "details": dict         # 详细信息
        }
    """
    try:
        # CPU信息
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count(logical=False)
        cpu_count_logical = psutil.cpu_count(logical=True)
        
        # 内存信息
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        memory_used = memory.used
        memory_total = memory.total
        
        # 磁盘信息
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        disk_used = disk.used
        disk_total = disk.total
        
        # 网络信息
        net_io = psutil.net_io_counters()
        network_sent = net_io.bytes_sent
        network_recv = net_io.bytes_recv
        
        # 进程信息
        process_count = len(psutil.pids())
        
        # 系统信息
        system_info = {
            "platform": platform.system(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor()
        }
        
        # 生成状态摘要
        summary = generate_summary(cpu_percent, memory_percent, disk_percent)
        
        return {
            "cpu": round(cpu_percent, 2),
            "memory": round(memory_percent, 2),
            "disk": round(disk_percent, 2),
            "network_sent": network_sent,
            "network_recv": network_recv,
            "summary": summary,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "details": {
                "cpu": {
                    "percent": cpu_percent,
                    "count_physical": cpu_count,
                    "count_logical": cpu_count_logical
                },
                "memory": {
                    "percent": memory_percent,
                    "used": memory_used,
                    "total": memory_total,
                    "available": memory.available
                },
                "disk": {
                    "percent": disk_percent,
                    "used": disk_used,
                    "total": disk_total,
                    "free": disk.free
                },
                "network": {
                    "bytes_sent": network_sent,
                    "bytes_recv": network_recv,
                    "packets_sent": net_io.packets_sent,
                    "packets_recv": net_io.packets_recv
                },
                "process_count": process_count,
                "system": system_info
            }
        }
    except Exception as e:
        return {
            "cpu": 0,
            "memory": 0,
            "disk": 0,
            "network_sent": 0,
            "network_recv": 0,
            "summary": f"获取系统状态失败: {str(e)}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "details": {}
        }


def generate_summary(cpu: float, memory: float, disk: float) -> str:
    """
    根据系统指标生成状态摘要
    
    Args:
        cpu: CPU使用率
        memory: 内存使用率
        disk: 磁盘使用率
        
    Returns:
        状态摘要字符串
    """
    issues = []
    
    if cpu > 80:
        issues.append("CPU负载过高")
    elif cpu > 60:
        issues.append("CPU负载较高")
    
    if memory > 85:
        issues.append("内存占用过高")
    elif memory > 70:
        issues.append("内存占用较高")
    
    if disk > 90:
        issues.append("磁盘空间不足")
    elif disk > 80:
        issues.append("磁盘空间紧张")
    
    if not issues:
        return "系统运行正常"
    else:
        return "注意: " + "、".join(issues)


def get_top_processes(limit: int = 5) -> List[Dict[str, Any]]:
    """
    获取占用资源最多的进程
    
    Args:
        limit: 返回的进程数量
        
    Returns:
        进程信息列表
    """
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                pinfo = proc.info
                processes.append({
                    'pid': pinfo['pid'],
                    'name': pinfo['name'],
                    'cpu': pinfo['cpu_percent'],
                    'memory': pinfo['memory_percent']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # 按CPU使用率排序
        processes.sort(key=lambda x: x['cpu'], reverse=True)
        return processes[:limit]
    except Exception as e:
        print(f"获取进程信息失败: {e}")
        return []


def get_system_uptime() -> str:
    """
    获取系统运行时间
    
    Returns:
        运行时间字符串
    """
    try:
        boot_time = psutil.boot_time()
        uptime_seconds = datetime.now().timestamp() - boot_time
        
        days = int(uptime_seconds // (24 * 3600))
        hours = int((uptime_seconds % (24 * 3600)) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        
        parts = []
        if days > 0:
            parts.append(f"{days}天")
        if hours > 0:
            parts.append(f"{hours}小时")
        if minutes > 0:
            parts.append(f"{minutes}分钟")
        
        return "".join(parts) if parts else "少于1分钟"
    except Exception as e:
        return f"获取失败: {e}"


def check_alerts(status: Dict[str, Any], thresholds: Dict[str, float] = None) -> List[str]:
    """
    检查是否有需要告警的指标
    
    Args:
        status: 系统状态字典
        thresholds: 告警阈值字典
        
    Returns:
        告警信息列表
    """
    if thresholds is None:
        thresholds = {
            "cpu": 80,
            "memory": 85,
            "disk": 90
        }
    
    alerts = []
    
    if status.get("cpu", 0) > thresholds["cpu"]:
        alerts.append(f"⚠️ CPU使用率过高: {status['cpu']}%")
    
    if status.get("memory", 0) > thresholds["memory"]:
        alerts.append(f"⚠️ 内存使用率过高: {status['memory']}%")
    
    if status.get("disk", 0) > thresholds["disk"]:
        alerts.append(f"⚠️ 磁盘使用率过高: {status['disk']}%")
    
    return alerts

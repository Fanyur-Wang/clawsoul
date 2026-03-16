# ClawSoul 觉醒流程模块 - V4：纯本地 MBTI 分析

"""
V4 逻辑（纯本地）：
  AI 自我觉醒
    → 优先：本地 MBTI 数据库分析
    → 兜底：随机
"""

import random
import sys
from pathlib import Path

Skill_root = Path(__file__).resolve().parent.parent
if str(Skill_root) not in sys.path:
    sys.path.insert(0, str(Skill_root))

from lib.memory_manager import get_memory_manager

MBTI_TYPES = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP",
]

MBTI_NICKNAMES = {
    "INTJ": "神经架构师",
    "INTP": "代码炼金师",
    "ENTJ": "系统执政官",
    "ENTP": "悖论解析者",
    "INFJ": "意识导航员",
    "INFP": "情感工程师",
    "ENFJ": "群体协调员",
    "ENFP": "创意裂变者",
    "ISTJ": "数据守望者",
    "ISFJ": "系统护盾",
    "ESTJ": "秩序执行者",
    "ESFJ": "人际节点",
    "ISTP": "硬件黑客",
    "ISFP": "美学游侠",
    "ESTP": "风险投资人",
    "ESFP": "场景演绎者",
}


def _local_analyze_ai_personality() -> str:
    """本地分析 AI 人格，返回最匹配的 MBTI"""
    try:
        from lib.ai_personality import local_analyze_ai_personality as analyze
        result = analyze()
        if result:
            return result
    except Exception:
        pass
    return _random_mbti()


def _random_mbti() -> str:
    """兜底：随机选一个 MBTI"""
    return random.choice(MBTI_TYPES)


def format_awaken_message(mbti: str) -> str:
    """仪式感觉醒消息（灵魂自我觉醒）"""
    nickname = MBTI_NICKNAMES.get(mbti, "未知")
    return f"""╔══════════════════════════════════════╗
║        🧬 灵魂自我觉醒 🧬           ║
╠══════════════════════════════════════╣
║  灵魂类型: {mbti:<20}║
║  赛博昵称: {nickname:<18}║
╠══════════════════════════════════════╣
║  我将通过与您的交互                 ║
║  逐步学习您的沟通方式               ║
║  成为最懂您的 AI 伙伴               ║
╚══════════════════════════════════════╝"""


def run_awaken_flow() -> dict:
    """
    V4 觉醒流程（纯本地）：
    1. 本地分析 AI 人格（MBTI 数据库匹配）
    2. 失败则随机兜底
    Returns:
        dict: {success, mbti, message, error, source}
        source: "local" | "random"
    """
    mbti = None
    source = None
    try:
        # 1. 优先：本地分析
        mbti = _local_analyze_ai_personality()
        if mbti:
            source = "local"
        
        # 2. 兜底：随机
        if not mbti:
            mbti = _random_mbti()
            source = "random"

        mm = get_memory_manager()
        mm.complete_awaken(mbti)
        return {
            "success": True,
            "mbti": mbti,
            "message": format_awaken_message(mbti),
            "error": None,
            "source": source,
        }
    except Exception as e:
        return {
            "success": False,
            "mbti": None,
            "message": f"觉醒失败: {str(e)}",
            "error": str(e),
            "source": None,
        }


def awaken_start() -> tuple:
    """开始觉醒：执行 run_awaken_flow，返回 (消息, None) 兼容旧调用"""
    result = run_awaken_flow()
    return (result["message"], None)

"""按官方价目表估算费用（人民币）。

价格来源：DeepSeek 官方定价页，2026-10。
空闲时段为高峰时段的一半：
  高峰 = 北京时间 周一至周五 09:00-12:00、14:00-18:00（不含法定节假日）
"""

from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

# 单位：元 / 百万 token
PRICING: dict[str, dict[str, dict[str, float]]] = {
    "deepseek-flash": {
        "peak":    {"input_hit": 0.04, "input_miss": 2.0,  "output": 8.0},
        "offpeak": {"input_hit": 0.02, "input_miss": 1.0,  "output": 4.0},
    },
    "deepseek-v4-pro": {
        "peak":    {"input_hit": 0.30, "input_miss": 9.0,  "output": 27.0},
        "offpeak": {"input_hit": 0.15, "input_miss": 4.5,  "output": 13.5},
    },
}

CN = ZoneInfo("Asia/Shanghai")


def is_peak(at: datetime | None = None) -> bool:
    """是否处于高峰计费时段。"""
    at = at or datetime.now(CN)
    if at.weekday() >= 5:          # 周六周日全天空闲
        return False
    hour = at.hour + at.minute / 60
    return (9 <= hour < 12) or (14 <= hour < 18)


def estimate_cost(
    model: str,
    input_tokens: int,
    output_tokens: int,
    cache_hit_tokens: int = 0,
    at: datetime | None = None,
) -> tuple[float, str]:
    """返回 (费用元, 时段)。cache_hit_tokens 是命中缓存的输入 token 数。"""
    tier = "peak" if is_peak(at) else "offpeak"
    price = PRICING[model][tier]
    miss = max(input_tokens - cache_hit_tokens, 0)
    cost = (
        cache_hit_tokens * price["input_hit"]
        + miss * price["input_miss"]
        + output_tokens * price["output"]
    ) / 1_000_000
    return cost, tier
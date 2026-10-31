"""第一次调用：问一句，看它答什么，顺便算这次花了多少钱。"""

import logging

from src.config import settings
from src.llm import client, safe_chat
from src.pricing import estimate_cost


# FILLER = "这是一段用于测试长上下文输入的填充文本，它本身没有信息量。"
# REPEAT = 640  # 先随便给个数，跑一次看实际 token 再调

# messages = [
#     {"role": "system", "content": FILLER * REPEAT},
#     {"role": "user", "content": "用一句话总结上面这段话。"},
# ]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

messages = [
    {"role": "system", "content": "你是一个说话简洁的助手，回答不超过三句话。"},
    {"role": "user", "content": "用三句话解释什么是 AI Agent。"},
]

# 正常路径：直接调 client，这样才能拿到 usage 算钱
resp = client.chat.completions.create(
    model=settings.model,
    messages=messages,
    temperature=0.7,
)
answer = resp.choices[0].message.content
print(answer)

# print(resp.choices[0].message.content)

usage = resp.usage
cost, tier = estimate_cost(
    settings.model,
    usage.prompt_tokens,
    usage.completion_tokens,
    cache_hit_tokens=getattr(usage, "prompt_cache_hit_tokens", 0) or 0,
)

print("\n---")
print(f"输入 {usage.prompt_tokens} / 输出 {usage.completion_tokens} token")
print(f"本次花费 ¥{cost:.6f}（{tier} 时段）")
"""模型客户端。所有调用都从这里走，方便以后加日志、重试、限流。"""

import logging

from openai import APIError, APITimeoutError, RateLimitError, OpenAI

from src.config import settings

logger = logging.getLogger(__name__)

client = OpenAI(
    api_key=settings.deepseek_api_key,
    base_url=settings.base_url,
    timeout=60.0,      # 单次请求最多等 60 秒
    max_retries=2,     # 网络抖动自动重试 2 次
)


def safe_chat(
    messages: list[dict[str, str]],
    fallback: str = "抱歉，我这边有点忙，请稍后再试。",
) -> str:
    """带兜底的调用：失败时返回一句人话，而不是把异常抛给调用方。"""
    try:
        resp = client.chat.completions.create(
            model=settings.model,
            messages=messages,
            timeout=20,          # 业务层更短的超时：用户等不了 60 秒
        )
        return resp.choices[0].message.content or fallback

    except (APITimeoutError, RateLimitError) as exc:
        logger.warning("safe_chat 兜底（%s）：%s", type(exc).__name__, exc)
        return fallback
    except APIError as exc:
        logger.warning("safe_chat 兜底（%s）：%s", type(exc).__name__, exc)
        return fallback
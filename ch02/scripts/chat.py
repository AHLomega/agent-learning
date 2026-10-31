"""流式多轮对话。输入 /exit 退出，/new 清空上下文。"""

from src.config import settings
from src.llm import client
from src.pricing import estimate_cost


def main() -> None:
    history: list[dict[str, str]] = [
        {"role": "system", "content": "你是一个简洁的中文助手。"}
    ]
    total = 0.0
    print("输入 /exit 退出，/new 清空上下文\n")

    while True:
        try:
            user = input("你 > ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user:
            continue
        if user in ("/exit", "/quit"):
            break
        if user == "/new":
            history = history[:1]
            print("（上下文已清空）\n")
            continue

        history.append({"role": "user", "content": user})

        stream = client.chat.completions.create(
            model=settings.model,
            messages=history,
            stream=True,
            stream_options={"include_usage": True},
        )

        print("AI > ", end="", flush=True)
        parts: list[str] = []
        usage = None

        for chunk in stream:
            if not chunk.choices:          # 最后一个 chunk 只带 usage
                usage = chunk.usage or usage
                continue
            delta = chunk.choices[0].delta.content or ""
            if delta:
                parts.append(delta)
                print(delta, end="", flush=True)
            if chunk.usage:
                usage = chunk.usage

        print()
        history.append({"role": "assistant", "content": "".join(parts)})

        if usage:
            cost, tier = estimate_cost(
                settings.model,
                usage.prompt_tokens,
                usage.completion_tokens,
                cache_hit_tokens=getattr(usage, "prompt_cache_hit_tokens", 0) or 0,
            )
            total += cost
            print(
                f"[tokens {usage.prompt_tokens}+{usage.completion_tokens} | "
                f"¥{cost:.6f} | 累计 ¥{total:.4f} | {tier}]\n"
            )


if __name__ == "__main__":
    main()
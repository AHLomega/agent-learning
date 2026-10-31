"""命令行成本估算：python -m scripts.cost --in 3000 --out 800"""

import argparse

from src.pricing import PRICING, estimate_cost


def main() -> None:
    parser = argparse.ArgumentParser(description="估算一次模型调用的费用（人民币）")
    parser.add_argument("--model", default="deepseek-flash", choices=list(PRICING))
    parser.add_argument("--in", dest="input_tokens", type=int, required=True)
    parser.add_argument("--out", dest="output_tokens", type=int, required=True)
    parser.add_argument("--cache-hit", type=int, default=0)
    args = parser.parse_args()

    cost, tier = estimate_cost(
        args.model, args.input_tokens, args.output_tokens, args.cache_hit
    )
    print(f"模型：{args.model}    时段：{tier}")
    print(f"输入 {args.input_tokens} / 输出 {args.output_tokens} / 缓存命中 {args.cache_hit}")
    print(f"预计费用：¥{cost:.6f}")


if __name__ == "__main__":
    main()
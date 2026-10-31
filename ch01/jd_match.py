"""jd_match.py — 把一份 JD 拆成能力清单，算出你的匹配度。

用法：
    python jd_match.py jd.txt my_skills.txt
"""

from __future__ import annotations

import sys
from pathlib import Path

# 技能 -> (权重, 同义词)。权重 1-3，3 表示岗位核心能力。
SKILLS: dict[str, tuple[int, list[str]]] = {
    "Python":       (3, ["python"]),
    "异步/并发":    (2, ["异步", "async", "asyncio", "并发"]),
    "API 设计":     (2, ["restful", "rest api", "接口设计", "fastapi", "flask"]),
    "Agent 框架":   (3, ["langchain", "langgraph", "llamaindex", "autogen",
                         "semantic kernel", "dify", "coze"]),
    "RAG/检索":     (3, ["rag", "检索增强", "知识库", "向量检索", "embedding", "召回"]),
    "工具调用":     (3, ["function calling", "工具调用", "tool call", "mcp"]),
    "Prompt":       (2, ["prompt", "提示词"]),
    "多轮/记忆":    (2, ["多轮", "记忆", "memory", "会话管理"]),
    "任务规划":     (2, ["规划", "planning", "任务拆解", "自主决策"]),
    "数据库":       (2, ["mysql", "postgres", "mongodb", "redis", "sql"]),
    "容器/部署":    (2, ["docker", "kubernetes", "k8s", "ci/cd", "部署"]),
    "评测/可观测":  (2, ["评测", "评估", "evals", "trace", "监控", "可观测"]),
    "工程素养":     (1, ["git", "单元测试", "代码规范", "文档"]),
}

def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8").lower()

def main() -> None:
    if len(sys.argv) != 3:
        print(__doc__)
        raise SystemExit(1)

    jd_text = read(sys.argv[1])
    my_text = read(sys.argv[2])

    required: list[tuple[int, str]] = []
    hit: list[tuple[int, str]] = []
    miss: list[tuple[int, str]] = []

    for skill, (weight, aliases) in SKILLS.items():
        if not any(a in jd_text for a in aliases):
            continue                      # JD 没要求，跳过
        required.append((weight, skill))
        if any(a in my_text for a in aliases):
            hit.append((weight, skill))
        else:
            miss.append((weight, skill))

    total = sum(w for w, _ in required) or 1
    got = sum(w for w, _ in hit)

    print(f"\n这份 JD 要求 {len(required)} 项能力，你命中 {len(hit)} 项")
    print(f"匹配度：{got / total:.0%}\n")

    print("✅ 已具备：")
    for w, s in sorted(hit, reverse=True):
        print(f"   [{w}] {s}")

    print("\n❌ 缺口（按重要性排序）：")
    for w, s in sorted(miss, reverse=True):
        print(f"   [{w}] {s}")

    print("\n下一步：把缺口里权重 3 的，写进你这周的 TODO。\n")

if __name__ == "__main__":
    main()
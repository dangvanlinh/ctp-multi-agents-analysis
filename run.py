"""
CTP Multi-Agent Debate System
=============================
Chạy theo topic (agent tự yêu cầu data):
  python run.py --topic "Phân tích tính năng VIP"
  python run.py --topic "Tối ưu retention 1-6 tháng" --rounds 3

Chạy với data có sẵn (flow cũ):
  python run.py --data "custom data here"
  python run.py --file data.txt --rounds 2

Cần API keys trong file .env:
  ANTHROPIC_API_KEY=sk-ant-...
  OPENAI_API_KEY=sk-...
  GOOGLE_API_KEY=AI...
"""

import argparse
from dotenv import load_dotenv

load_dotenv(override=True)

DEFAULT_DATA = """CURRENT: Rev ~70M, ~700 PU (~350 new), ARPPU ~100k, ARPT ~1.0, Repay next month ~28%
KPI: Rev ~300M (4.3x), ~1000 PU (~600 new), ARPPU ~300k, ARPT ~3.0, Repay ~57%

OPEN ISSUES:
1. Welcome Back offer chưa khác biệt vs first-time offer
2. DKXX stacking: Lv3(+5%) + Lv6(+8%) cộng dồn(42%) hay thay thế(39%)?
3. Gem bonus +30% Lv6 có phá economy?
4. Lv4 thin — chỉ 1 benefit
5. 12 dice skins/year sustainable?
6. Streak benefit chưa cụ thể
7. Pull mechanic within-month repay chưa có"""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CTP Multi-Agent Debate")
    parser.add_argument("--rounds", type=int, default=2, help="Số rounds debate (default: 2)")
    parser.add_argument("--topic", type=str, default=None, help="Topic phân tích (agent sẽ tự yêu cầu data)")
    parser.add_argument("--data", type=str, default=None, help="Custom data input string")
    parser.add_argument("--file", type=str, default=None, help="Đọc data input từ file")
    parser.add_argument("--knowledge", type=str, default="knowledge", help="Knowledge directory")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode: can thiệp giữa các rounds")
    parser.add_argument("--no-query", action="store_true", help="Skip auto-query Superset (manual data only)")
    args = parser.parse_args()

    print("""
╔══════════════════════════════════════════╗
║   🎯 CTP Multi-Agent Debate System      ║
║   Analyst → 3 Reviewers → Synthesis      ║
╚══════════════════════════════════════════╝
    """)

    from orchestrator import run_debate, request_data

    if args.topic:
        # Flow B: Agent yêu cầu data → Auto-query → User insight → Debate
        auto_query = not args.no_query
        mode = "Topic-driven + Auto-query" if auto_query else "Topic-driven (manual)"
        print(f"📌 Mode: {mode}")
        print(f"📌 Topic: {args.topic}")

        data, knowledge = request_data(args.topic, knowledge_dir=args.knowledge, auto_query=auto_query)

        if data is None:
            print("❌ Không thể tiếp tục.")
        else:
            print(f"\n{'🔥'*30}")
            print(f"   BẮT ĐẦU DEBATE")
            print(f"{'🔥'*30}")
            run_debate(data, max_rounds=args.rounds, knowledge_dir=args.knowledge, interactive=args.interactive, topic=args.topic)
    else:
        # Flow A: User đưa data trước (flow cũ)
        if args.file:
            with open(args.file, "r", encoding="utf-8") as f:
                data = f.read()
        else:
            data = args.data or DEFAULT_DATA

        run_debate(data, max_rounds=args.rounds, knowledge_dir=args.knowledge, interactive=args.interactive)

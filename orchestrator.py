"""Debate orchestrator — runs the Analyst → Reviewers → Synthesis loop."""

import json
import os
import re
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

from agents import call_claude, call_gpt, call_gemini, stream_claude, get_last_stream_usage, TokenTracker
from agents import ANALYST_ROLE, REVIEWER_ROLES, SYNTHESIZER_ROLE, DATA_REQUEST_ROLE, SQL_GENERATOR_ROLE
from knowledge import load_knowledge
from superset.client import query_superset, format_results_markdown


# ============================================================
# Pure phase functions (no I/O — used by both CLI and Streamlit)
# ============================================================

def build_system_prompts(knowledge):
    """Build system prompts cho tất cả agents."""
    return {
        "analyst": ANALYST_ROLE + "\n\n# GAME KNOWLEDGE BASE\n" + knowledge,
        "reviewers": {
            k: v + "\n\n# GAME KNOWLEDGE BASE\n" + knowledge
            for k, v in REVIEWER_ROLES.items()
        },
        "synthesizer": SYNTHESIZER_ROLE + "\n\n# GAME KNOWLEDGE BASE\n" + knowledge,
        "data_request": DATA_REQUEST_ROLE + "\n\n# GAME KNOWLEDGE BASE\n" + knowledge,
    }


def phase0_data_request(topic, knowledge, tracker=None):
    """Phase 0: Trả về text yêu cầu data. Không I/O."""
    system = DATA_REQUEST_ROLE + "\n\n# GAME KNOWLEDGE BASE\n" + knowledge
    text, usage = call_claude(
        system,
        f"Topic phân tích: {topic}\n\nHãy xác định những data nào cần thêm để phân tích topic này."
    )
    if tracker and usage:
        tracker.log("Phase 0 - Data Request", **usage)
    return text


def phase0_data_request_stream(topic, knowledge, tracker=None):
    """Phase 0: Yield text chunks yêu cầu data (streaming)."""
    system = DATA_REQUEST_ROLE + "\n\n# GAME KNOWLEDGE BASE\n" + knowledge
    yield from stream_claude(
        system,
        f"Topic phân tích: {topic}\n\nHãy xác định những data nào cần thêm để phân tích topic này."
    )
    if tracker:
        usage = get_last_stream_usage()
        if usage:
            tracker.log("Phase 0 - Data Request", **usage)


def build_data_input(topic, data_request, collected_parts):
    """Ghép topic + data request + user data thành input cho analyst."""
    if collected_parts:
        return (
            f"## Topic: {topic}\n\n"
            f"## Data đã yêu cầu:\n{data_request}\n\n"
            f"## Data được cung cấp:\n" + "\n\n".join(collected_parts)
        )
    return (
        f"## Topic: {topic}\n\n"
        f"(Không có data bổ sung, phân tích dựa trên knowledge base)"
    )


# ============================================================
# Phase 0.5: Auto-query Superset
# ============================================================

def phase05_generate_queries(topic, data_request_text, knowledge, tracker=None):
    """Agent sinh SQL queries dựa trên topic + data request. Trả về text."""
    system = SQL_GENERATOR_ROLE + "\n\n# GAME KNOWLEDGE BASE\n" + knowledge
    prompt = (
        f"Topic phân tích: {topic}\n\n"
        f"Data cần thiết (từ Phase 0):\n{data_request_text}\n\n"
        f"Hãy viết SQL queries để lấy các data BẮT BUỘC từ ClickHouse."
    )
    text, usage = call_claude(system, prompt)
    if tracker and usage:
        tracker.log("Phase 0.5 - SQL Generator", **usage)
    return text


def phase05_generate_queries_stream(topic, data_request_text, knowledge, tracker=None):
    """Agent sinh SQL queries (streaming)."""
    system = SQL_GENERATOR_ROLE + "\n\n# GAME KNOWLEDGE BASE\n" + knowledge
    prompt = (
        f"Topic phân tích: {topic}\n\n"
        f"Data cần thiết (từ Phase 0):\n{data_request_text}\n\n"
        f"Hãy viết SQL queries để lấy các data BẮT BUỘC từ ClickHouse."
    )
    yield from stream_claude(system, prompt)
    if tracker:
        usage = get_last_stream_usage()
        if usage:
            tracker.log("Phase 0.5 - SQL Generator", **usage)


def phase05_parse_queries(agent_output: str) -> list[dict]:
    """Parse JSON query list từ agent output."""
    # Tìm JSON block trong output
    match = re.search(r'```json\s*\n?(.*?)\n?```', agent_output, re.DOTALL)
    if match:
        raw = match.group(1).strip()
    else:
        # Thử parse trực tiếp nếu không có code block
        start = agent_output.find('[')
        end = agent_output.rfind(']')
        if start != -1 and end != -1:
            raw = agent_output[start:end + 1]
        else:
            return []

    try:
        queries = json.loads(raw)
        if isinstance(queries, list):
            return queries
    except json.JSONDecodeError:
        pass
    return []


def phase05_execute_queries(queries: list[dict]) -> tuple[str, list[dict]]:
    """
    Execute parsed queries on Superset.
    Returns (markdown_report, results_list).
    results_list: [{"name": ..., "description": ..., "sql": ..., "data": [...], "error": ...}]
    """
    results = []
    md_parts = ["# Data từ Superset (Auto-Query)\n"]
    md_parts.append(f"**Thời gian query:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    for q in queries:
        name = q.get("name", "unknown")
        desc = q.get("description", "")
        sql = q.get("sql", "")

        if not sql:
            results.append({"name": name, "description": desc, "sql": sql, "data": [], "error": "No SQL"})
            continue

        try:
            data = query_superset(sql)
            results.append({"name": name, "description": desc, "sql": sql, "data": data, "error": None})
            md_parts.append(format_results_markdown(data, query_name=f"{name} — {desc}", sql=sql))
        except Exception as e:
            results.append({"name": name, "description": desc, "sql": sql, "data": [], "error": str(e)})
            md_parts.append(f"### {name}\n> Error: {e}\n")

    return "\n".join(md_parts), results


def phase05_save_data(markdown_report: str, topic: str) -> str:
    """Lưu query results ra file markdown. Trả về filepath."""
    os.makedirs("data", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = re.sub(r'[^\w\s-]', '', topic)[:40].strip().replace(' ', '_')
    filename = f"data/query_{safe_topic}_{timestamp}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(markdown_report)

    return filename


def phase05_build_data_with_insights(topic, data_request_text, markdown_report, user_insights=""):
    """Ghép tất cả data + insights thành input cho analyst."""
    parts = [
        f"## Topic: {topic}\n",
        f"## Data đã yêu cầu:\n{data_request_text}\n",
        f"## Data từ Database (auto-query):\n{markdown_report}\n",
    ]
    if user_insights.strip():
        parts.append(f"## Insight bổ sung từ user:\n{user_insights}\n")
    return "\n".join(parts)


def phase1_analyst(data_input, last_synthesis, round_num, analyst_system, tracker=None):
    """Phase 1: Analyst phân tích. Trả về text."""
    if round_num == 1:
        prompt = f"Phân tích data và đề xuất giải pháp:\n\n{data_input}"
    else:
        prompt = (
            f"Revise giải pháp dựa trên feedback:\n\n{last_synthesis}"
            f"\n\nData gốc:\n{data_input}"
        )
    text, usage = call_claude(analyst_system, prompt)
    if tracker and usage:
        tracker.log(f"Round {round_num} - Analyst", **usage)
    return text


def phase1_analyst_stream(data_input, last_synthesis, round_num, analyst_system, tracker=None):
    """Phase 1: Analyst phân tích (streaming). Yield text chunks."""
    if round_num == 1:
        prompt = f"Phân tích data và đề xuất giải pháp:\n\n{data_input}"
    else:
        prompt = (
            f"Revise giải pháp dựa trên feedback:\n\n{last_synthesis}"
            f"\n\nData gốc:\n{data_input}"
        )
    yield from stream_claude(analyst_system, prompt)
    if tracker:
        usage = get_last_stream_usage()
        if usage:
            tracker.log(f"Round {round_num} - Analyst", **usage)


def phase2_build_review_prompt(analyst_resp, data_input, last_synthesis, round_num):
    """Build prompt cho reviewers."""
    prior_context = ""
    if round_num > 1 and last_synthesis:
        prior_context = (
            f"\n\n--- TỔNG HỢP ROUND TRƯỚC ---\n{last_synthesis}\n"
            f"--- HẾT TỔNG HỢP ---\n\n"
        )
    return (
        f"Đề xuất từ Analyst (Round {round_num}):\n\n{analyst_resp}"
        f"\n\nData context:\n{data_input}{prior_context}"
        f"\n\nHãy review critically. Nếu có tổng hợp round trước, "
        f"focus vào điểm chưa giải quyết và đánh giá analyst đã revise tốt chưa."
    )


def phase2_reviewers(reviewer_systems, review_prompt, tracker=None, round_num=1):
    """Phase 2: Chạy 3 reviewers song song. Trả về list of (key, name, emoji, color, resp)."""
    return _run_reviewers_parallel(reviewer_systems, review_prompt, tracker, round_num)


def phase3_synthesize(reviews, synth_system, tracker=None, round_num=1):
    """Phase 3: Tổng hợp. Trả về text."""
    synth_input = "\n\n---\n\n".join(
        [f"### {name}:\n{resp}" for _, name, _, _, resp in reviews]
    )
    text, usage = call_claude(synth_system, f"Tổng hợp:\n\n{synth_input}")
    if tracker and usage:
        tracker.log(f"Round {round_num} - Synthesizer", **usage)
    return text


def phase3_synthesize_stream(reviews, synth_system, tracker=None, round_num=1):
    """Phase 3: Tổng hợp (streaming). Yield text chunks."""
    synth_input = "\n\n---\n\n".join(
        [f"### {name}:\n{resp}" for _, name, _, _, resp in reviews]
    )
    yield from stream_claude(synth_system, f"Tổng hợp:\n\n{synth_input}")
    if tracker:
        usage = get_last_stream_usage()
        if usage:
            tracker.log(f"Round {round_num} - Synthesizer", **usage)


def check_convergence(synthesis_text):
    """Check convergence. Trả về string hoặc None."""
    return _parse_convergence(synthesis_text)


# ============================================================
# Display helpers
# ============================================================

COLORS = {
    "purple": "\033[95m", "blue": "\033[94m", "green": "\033[92m",
    "yellow": "\033[93m", "red": "\033[91m",
    "reset": "\033[0m", "bold": "\033[1m", "dim": "\033[2m",
}


def print_agent(emoji, name, color_code, text):
    """In output có màu cho dễ đọc."""
    c = COLORS.get(color_code, "")
    r, b = COLORS["reset"], COLORS["bold"]
    print(f"\n{c}{b}{'─'*60}{r}")
    print(f"{c}{b}{emoji} {name}{r}")
    print(f"{c}{b}{'─'*60}{r}")
    print(text)
    print()


# ============================================================
# Reviewer definitions
# ============================================================

REVIEWERS = [
    {
        "key": "reviewer_opus",
        "name": "Opus Reviewer",
        "emoji": "🧠",
        "color": "blue",
        "call_fn": call_claude,
        "role_key": "claude",
    },
    {
        "key": "reviewer_gpt",
        "name": "GPT-4o Reviewer",
        "emoji": "⚡",
        "color": "green",
        "call_fn": call_gpt,
        "role_key": "gpt",
    },
    {
        "key": "reviewer_gemini",
        "name": "Gemini Reviewer",
        "emoji": "💎",
        "color": "yellow",
        "call_fn": call_gemini,
        "role_key": "gemini",
    },
]


# ============================================================
# Phase 0: Data Request
# ============================================================

def request_data(topic, knowledge_dir="knowledge", auto_query=True):
    """Phase 0 + 0.5: Xác định data → Auto-query Superset → Chờ user review + insight."""

    tracker = TokenTracker()

    print(f"\n{'='*60}")
    print(f"📚 Loading knowledge base...")
    print(f"{'='*60}")
    knowledge = load_knowledge(knowledge_dir)

    if not knowledge:
        print("❌ Không có knowledge. Thêm .md files vào knowledge/ folder.")
        return None, None

    print(f"\n✅ Knowledge loaded: {len(knowledge)} characters total")

    # --- Phase 0: Xác định data cần ---
    print(f"\n{'='*60}")
    print(f"🔍 PHASE 0: Xác định data cần thiết")
    print(f"📌 Topic: {topic}")
    print(f"{'='*60}")

    print(f"\n⏳ Analyst đang đọc knowledge base và xác định data cần...")
    data_request = phase0_data_request(topic, knowledge, tracker)
    print_agent("📋", "DATA REQUEST", "purple", data_request)

    # --- Phase 0.5: Auto-query Superset ---
    markdown_report = ""
    if auto_query:
        print(f"\n{'='*60}")
        print(f"🗄️  PHASE 0.5: Auto-query từ Superset")
        print(f"{'='*60}")

        print(f"\n⏳ Agent đang viết SQL queries...")
        sql_output = phase05_generate_queries(topic, data_request, knowledge, tracker)
        print_agent("📝", "SQL QUERIES", "blue", sql_output)

        queries = phase05_parse_queries(sql_output)
        if queries:
            print(f"\n✅ Parsed {len(queries)} queries. Đang execute trên Superset...")
            markdown_report, results = phase05_execute_queries(queries)

            # Save to file
            filepath = phase05_save_data(markdown_report, topic)
            print(f"\n💾 Data saved: {filepath}")

            # Show summary
            success = sum(1 for r in results if r["error"] is None and r["data"])
            failed = sum(1 for r in results if r["error"] is not None)
            empty = sum(1 for r in results if r["error"] is None and not r["data"])
            print(f"   ✅ {success} queries thành công")
            if empty:
                print(f"   ⚠️  {empty} queries không có data")
            if failed:
                print(f"   ❌ {failed} queries lỗi")

            print(f"\n📂 Xem data tại: {filepath}")
        else:
            print("⚠️  Không parse được SQL queries từ agent output.")

    # Print token usage so far
    _print_token_summary(tracker)

    # --- Chờ user review + input insight ---
    print(f"\n{'─'*60}")
    print("📊 Data đã được query tự động (xem file ở trên).")
    print("   Bạn có thể bổ sung thêm insight/data:")
    print("   - Paste trực tiếp insight/số liệu")
    print("   - Nhập đường dẫn file: file:path/to/data.csv")
    print("   - Gõ 'done' khi đã sẵn sàng phân tích")
    print("   - Gõ 'skip' để phân tích với data đã query")
    print(f"{'─'*60}")

    user_insights = []
    while True:
        user_input = input("\n💡 Insight → ").strip()

        if user_input.lower() in ("done", "skip", ""):
            break
        elif user_input.startswith("file:"):
            file_paths = user_input[5:].split(",")
            for fp in file_paths:
                fp = fp.strip()
                try:
                    with open(fp, "r", encoding="utf-8") as f:
                        content = f.read()
                    user_insights.append(f"--- FILE: {os.path.basename(fp)} ---\n{content}")
                    print(f"  ✅ Loaded: {fp} ({len(content)} chars)")
                except Exception as e:
                    print(f"  ❌ Error loading {fp}: {e}")
        else:
            user_insights.append(user_input)
            print(f"  ✅ Insight received ({len(user_input)} chars)")

    # Build final data input
    combined_data = phase05_build_data_with_insights(
        topic, data_request, markdown_report, "\n\n".join(user_insights)
    )

    return combined_data, knowledge


# ============================================================
# Core debate loop
# ============================================================

def run_debate(data_input, max_rounds=2, knowledge_dir="knowledge", interactive=False):
    """Main debate loop."""

    tracker = TokenTracker()

    # Load knowledge
    print(f"\n{'='*60}")
    print(f"📚 Loading knowledge base...")
    print(f"{'='*60}")
    knowledge = load_knowledge(knowledge_dir)

    if not knowledge:
        print("❌ Không có knowledge. Thêm .md files vào knowledge/ folder.")
        return

    print(f"\n✅ Knowledge loaded: {len(knowledge)} characters total")

    # Build system prompts (role + knowledge)
    analyst_system = ANALYST_ROLE + "\n\n# GAME KNOWLEDGE BASE\n" + knowledge
    reviewer_systems = {
        k: v + "\n\n# GAME KNOWLEDGE BASE\n" + knowledge
        for k, v in REVIEWER_ROLES.items()
    }
    synth_system = SYNTHESIZER_ROLE + "\n\n# GAME KNOWLEDGE BASE\n" + knowledge

    debate_log = []
    last_synthesis = ""

    for round_num in range(1, max_rounds + 1):
        print(f"\n{'🔥'*30}")
        print(f"   ROUND {round_num}/{max_rounds}")
        print(f"{'🔥'*30}")

        # --- Step 1: Analyst ---
        print(f"\n⏳ Opus Analyst đang phân tích...")
        analyst_resp = phase1_analyst(
            data_input, last_synthesis, round_num, analyst_system, tracker
        )
        print_agent("🔬", "OPUS ANALYST", "purple", analyst_resp)
        debate_log.append(("analyst", analyst_resp))

        # --- Step 2: Reviewers (parallel) ---
        review_prompt = phase2_build_review_prompt(
            analyst_resp, data_input, last_synthesis, round_num
        )

        print(f"⏳ 3 Reviewers đang review song song...")
        reviews = _run_reviewers_parallel(reviewer_systems, review_prompt, tracker, round_num)

        for log_key, name, emoji, color, resp in reviews:
            print_agent(emoji, name.upper(), color, resp)
            debate_log.append((log_key, resp))

        # --- Step 3: Synthesize ---
        print(f"⏳ Đang tổng hợp feedback...")
        last_synthesis = phase3_synthesize(reviews, synth_system, tracker, round_num)
        print_agent("📋", "TỔNG HỢP", "red", last_synthesis)
        debate_log.append(("synthesizer", last_synthesis))

        # Print token usage after each round
        _print_token_summary(tracker)

        # Check convergence
        convergence = _parse_convergence(last_synthesis)
        if convergence:
            print(f"  📊 Convergence: {convergence}")
            if "HỘI TỤ" in convergence.upper() and "CHƯA" not in convergence.upper():
                print(f"\n✅ Debate đã hội tụ tại round {round_num}. Dừng sớm.")
                break

        # Interactive mode: ask user between rounds
        if interactive and round_num < max_rounds:
            print(f"\n{'─'*60}")
            print("🎮 INTERACTIVE MODE — Chọn hành động:")
            print("  [enter]  Tiếp tục round tiếp theo")
            print("  [s]      Dừng debate, lưu kết quả")
            print("  [gợi ý]  Nhập chỉ dẫn cho Analyst round tiếp")
            print(f"{'─'*60}")
            user_input = input("→ ").strip()

            if user_input.lower() == "s":
                print("\n⏹️  User dừng debate.")
                break
            elif user_input:
                data_input = (
                    f"{data_input}\n\n"
                    f"--- CHỈ DẪN TỪ USER ---\n{user_input}\n--- HẾT CHỈ DẪN ---"
                )

    # Save
    save_debate_log(debate_log, max_rounds)

    # Final token summary
    print(f"\n{'='*60}")
    print(f"✅ DEBATE HOÀN THÀNH — {max_rounds} rounds")
    print(f"{'='*60}")
    _print_token_summary(tracker, detailed=True)

    return debate_log


def _run_reviewers_parallel(reviewer_systems, review_prompt, tracker=None, round_num=1):
    """Gọi 3 reviewers song song, trả về kết quả theo thứ tự cố định."""
    results = {}

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {}
        for rev in REVIEWERS:
            system = reviewer_systems[rev["role_key"]]
            future = executor.submit(rev["call_fn"], system, review_prompt)
            futures[future] = rev

        for future in as_completed(futures):
            rev = futures[future]
            result = future.result()
            # All providers now return (text, usage) tuples
            if isinstance(result, tuple):
                resp, usage = result
            else:
                resp, usage = result, None
            if resp:
                results[rev["key"]] = resp
                if tracker and usage:
                    tracker.log(f"Round {round_num} - {rev['name']}", **usage)

    # Return in consistent order
    ordered = []
    for rev in REVIEWERS:
        if rev["key"] in results:
            ordered.append((
                rev["key"], rev["name"], rev["emoji"],
                rev["color"], results[rev["key"]]
            ))
    return ordered


def _parse_convergence(synthesis_text):
    """Trích xuất đánh giá convergence từ synthesis output."""
    # Tìm dòng chứa "Đánh giá:" trong section CONVERGENCE
    match = re.search(
        r"(?:Đánh giá|đánh giá)\s*:\s*\[?\s*(HỘI TỤ|CHƯA HỘI TỤ|PHÂN KỲ)",
        synthesis_text, re.IGNORECASE
    )
    if match:
        return match.group(1).upper()

    # Fallback: tìm keywords
    lower = synthesis_text.lower()
    if "hội tụ" in lower and "chưa" not in lower.split("hội tụ")[0][-20:]:
        return "HỘI TỤ"
    return None


def _print_token_summary(tracker, detailed=False):
    """In token usage summary ra CLI."""
    if not tracker.entries:
        return

    print(f"\n{'─'*60}")
    print(f"💰 TOKEN USAGE")
    print(f"{'─'*60}")

    for row in tracker.summary_by_agent():
        print(f"  {row['agent']:40s} │ {row['input']:>8,} in │ {row['output']:>8,} out │ ${row['cost']:.4f}")

    print(f"{'─'*60}")
    print(f"  {'TOTAL':40s} │ {tracker.total_input:>8,} in │ {tracker.total_output:>8,} out │ ${tracker.total_cost:.4f}")
    print(f"{'─'*60}")

    if detailed:
        print(f"\n  By model:")
        for row in tracker.summary_by_model():
            print(f"    {row['model']:38s} │ {row['input']:>8,} in │ {row['output']:>8,} out │ ${row['cost']:.4f}")


# ============================================================
# Save debate log
# ============================================================

AGENT_DISPLAY_NAMES = {
    "analyst": "🔬 Opus Analyst",
    "reviewer_opus": "🧠 Opus Reviewer",
    "reviewer_gpt": "⚡ GPT-4o Reviewer",
    "reviewer_gemini": "💎 Gemini Reviewer",
    "synthesizer": "📋 Tổng hợp",
}


def save_debate_log(log, rounds):
    """Lưu debate log ra file markdown."""
    os.makedirs("outputs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"outputs/debate_{timestamp}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# CTP Agent Debate Log\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"**Rounds:** {rounds}\n\n---\n\n")

        for agent, text in log:
            name = AGENT_DISPLAY_NAMES.get(agent, agent)
            f.write(f"## {name}\n\n{text}\n\n---\n\n")

    print(f"\n💾 Log saved: {filename}")

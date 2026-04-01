"""
CTP Multi-Agent Debate System — Streamlit UI
=============================================
Chay: streamlit run app.py
"""

import os
import glob
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

# Load .env from the same directory as this script
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"), override=True)

from orchestrator import (
    build_system_prompts,
    phase0_data_request_stream,
    build_data_input,
    phase05_generate_queries_stream,
    phase05_parse_queries,
    phase05_execute_queries,
    phase05_save_data,
    phase05_build_data_with_insights,
    phase1_analyst_stream,
    phase2_build_review_prompt,
    phase2_reviewers,
    phase3_synthesize_stream,
    check_convergence,
    save_debate_log,
    REVIEWERS,
    AGENT_DISPLAY_NAMES,
)
from agents import TokenTracker
from knowledge import load_knowledge


# ============================================================
# Page config
# ============================================================

st.set_page_config(
    page_title="CTP Debate System",
    page_icon="🎯",
    layout="wide",
)


# ============================================================
# Helper functions (defined before use)
# ============================================================

def format_export(state):
    """Format debate data thanh markdown cho export."""
    lines = [
        "# CTP Agent Debate Log",
        f"**Topic:** {state['topic']}",
        f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Rounds:** {len(state['rounds_data'])}",
        "",
        "---",
        "",
    ]
    for i, rd in enumerate(state["rounds_data"]):
        lines.append(f"## Round {i + 1}")
        lines.append("")
        lines.append("### 🔬 Analyst")
        lines.append(rd.get("analyst", ""))
        lines.append("")
        lines.append("---")
        lines.append("")
        for _, name, emoji, _, resp in rd.get("reviews", []):
            lines.append(f"### {emoji} {name}")
            lines.append(resp)
            lines.append("")
            lines.append("---")
            lines.append("")
        lines.append("### 📋 Synthesis")
        lines.append(rd.get("synthesis", ""))
        lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines)


def render_round(rd):
    """Render 1 round data da hoan thanh."""
    # Analyst
    st.markdown("#### 🔬 Analyst")
    st.markdown(rd.get("analyst", ""))

    st.divider()

    # Reviewers
    st.markdown("#### 🧠⚡💎 Reviewers")
    reviews = rd.get("reviews", [])
    if reviews:
        tabs = st.tabs([f"{r[2]} {r[1]}" for r in reviews])
        for tab, (key, name, emoji, color, resp) in zip(tabs, reviews):
            with tab:
                st.markdown(resp)

    st.divider()

    # Synthesis
    st.markdown("#### 📋 Synthesis")
    st.markdown(rd.get("synthesis", ""))

    convergence = rd.get("convergence")
    if convergence:
        if "HỘI TỤ" in convergence and "CHƯA" not in convergence:
            st.success(f"📊 {convergence}")
        else:
            st.info(f"📊 {convergence}")


def render_token_sidebar(tracker):
    """Render token usage trong sidebar."""
    if not tracker or not tracker.entries:
        return

    st.sidebar.divider()
    st.sidebar.subheader("💰 Token Usage")

    # Total metrics
    col1, col2 = st.sidebar.columns(2)
    col1.metric("Total Tokens", f"{tracker.total_input + tracker.total_output:,}")
    col2.metric("Total Cost", f"${tracker.total_cost:.4f}")

    # Breakdown by agent
    with st.sidebar.expander("Chi tiet theo agent", expanded=False):
        for row in tracker.summary_by_agent():
            st.markdown(
                f"**{row['agent']}**  \n"
                f"`{row['input']:,}` in / `{row['output']:,}` out — "
                f"**${row['cost']:.4f}**"
            )

    # Breakdown by model
    with st.sidebar.expander("Chi tiet theo model", expanded=False):
        for row in tracker.summary_by_model():
            st.markdown(
                f"**{row['model']}**  \n"
                f"`{row['input']:,}` in / `{row['output']:,}` out — "
                f"**${row['cost']:.4f}**"
            )


# ============================================================
# Session state init
# ============================================================

DEFAULTS = {
    "phase": 0,           # 0=input, 1=data_requesting, 2=auto_query, 3=debating
    "topic": "",
    "max_rounds": 2,
    "knowledge": "",
    "system_prompts": None,
    "data_request_text": "",
    "sql_agent_output": "",
    "query_results_md": "",
    "query_data_file": "",
    "data_input": "",
    "rounds_data": [],    # list of dicts: {analyst, reviews, synthesis, convergence}
    "current_round": 0,
    "debate_complete": False,
    "debate_log": [],     # for export
    "token_tracker": None,
}

for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Ensure tracker exists
if st.session_state.token_tracker is None:
    st.session_state.token_tracker = TokenTracker()


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:
    st.header("CTP Debate System")
    st.caption("Multi-Agent Analysis & Review")

    st.divider()

    # History
    st.subheader("Debate History")
    output_files = sorted(glob.glob("outputs/debate_*.md"), reverse=True)
    if output_files:
        for f in output_files[:10]:
            name = os.path.basename(f).replace("debate_", "").replace(".md", "")
            if st.button(f"📄 {name}", key=f"hist_{f}", use_container_width=True):
                with open(f, "r", encoding="utf-8") as fh:
                    st.session_state["viewing_history"] = fh.read()
    else:
        st.caption("Chua co debate nao.")

    st.divider()

    # Export
    if st.session_state.debate_complete and st.session_state.rounds_data:
        md_content = format_export(st.session_state)
        st.download_button(
            "📥 Export Markdown",
            md_content,
            file_name=f"debate_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    # Reset
    if st.session_state.phase > 0:
        if st.button("🔄 Debate moi", use_container_width=True):
            for k, v in DEFAULTS.items():
                st.session_state[k] = v
            st.session_state.token_tracker = TokenTracker()
            st.rerun()

# Render token usage in sidebar (always, if data exists)
render_token_sidebar(st.session_state.token_tracker)


# ============================================================
# View: History
# ============================================================

if "viewing_history" in st.session_state and st.session_state["viewing_history"]:
    st.markdown(st.session_state["viewing_history"])
    if st.button("← Quay lai"):
        del st.session_state["viewing_history"]
        st.rerun()
    st.stop()


# ============================================================
# Main UI
# ============================================================

st.title("🎯 CTP Multi-Agent Debate")
st.caption("Analyst → 3 Reviewers → Synthesis")

# ── Phase 0: Topic Input ──────────────────────────────────

if st.session_state.phase == 0:
    st.subheader("📌 Topic phan tich")

    topic = st.text_area(
        "Nhap topic can phan tich:",
        placeholder="Vi du: Phan tich tinh nang VIP, Toi uu retention 1-6 thang...",
        height=100,
    )
    max_rounds = st.slider("So rounds debate:", 1, 5, 2)

    col1, col2 = st.columns(2)
    with col1:
        start_topic = st.button("🔍 Bat dau — Agent yeu cau data", type="primary", use_container_width=True)
    with col2:
        start_direct = st.button("⚡ Phan tich truc tiep (khong can data)", use_container_width=True)

    if start_topic and topic.strip():
        knowledge = load_knowledge()
        if not knowledge:
            st.error("Khong tim thay knowledge base. Them .md files vao knowledge/ folder.")
            st.stop()

        st.session_state.topic = topic.strip()
        st.session_state.max_rounds = max_rounds
        st.session_state.knowledge = knowledge
        st.session_state.system_prompts = build_system_prompts(knowledge)
        st.session_state.phase = 1
        st.rerun()

    elif start_direct and topic.strip():
        knowledge = load_knowledge()
        if not knowledge:
            st.error("Khong tim thay knowledge base.")
            st.stop()

        st.session_state.topic = topic.strip()
        st.session_state.max_rounds = max_rounds
        st.session_state.knowledge = knowledge
        st.session_state.system_prompts = build_system_prompts(knowledge)
        st.session_state.data_input = build_data_input(topic.strip(), "", [])
        st.session_state.phase = 3
        st.rerun()

    elif (start_topic or start_direct) and not topic.strip():
        st.warning("Vui long nhap topic.")

    st.stop()


# ── Phase 1: Data Request ─────────────────────────────────

if st.session_state.phase == 1:
    st.subheader(f"📌 Topic: {st.session_state.topic}")

    with st.expander("📋 Phase 0: Agent yeu cau data", expanded=True):
        if not st.session_state.data_request_text:
            with st.spinner("Agent dang doc knowledge base va xac dinh data can..."):
                full_text = st.write_stream(
                    phase0_data_request_stream(
                        st.session_state.topic,
                        st.session_state.knowledge,
                        tracker=st.session_state.token_tracker,
                    )
                )
                st.session_state.data_request_text = full_text
                st.rerun()  # rerun to update sidebar token display
        else:
            st.markdown(st.session_state.data_request_text)

    # Data collection UI
    st.subheader("📊 Cung cap data")

    uploaded_files = st.file_uploader(
        "Upload files (CSV, TXT, ...)",
        accept_multiple_files=True,
        type=["csv", "txt", "tsv", "json"],
    )

    pasted_data = st.text_area(
        "Hoac paste data truc tiep:",
        height=200,
        placeholder="Paste CSV, so lieu, hoac bat ky data nao...",
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        auto_query_btn = st.button("🗄️ Auto-query Superset", type="primary", use_container_width=True)
    with col2:
        submit_data = st.button("▶ Debate (manual data)", use_container_width=True)
    with col3:
        skip_data = st.button("⏭ Skip — knowledge only", use_container_width=True)

    if auto_query_btn:
        # Go to Phase 2: auto-query
        st.session_state.phase = 2
        st.rerun()

    if submit_data or skip_data:
        parts = []
        if submit_data:
            for f in (uploaded_files or []):
                try:
                    content = f.read().decode("utf-8")
                    parts.append(f"--- FILE: {f.name} ---\n{content}")
                except Exception as e:
                    st.error(f"Loi doc file {f.name}: {e}")

            if pasted_data.strip():
                parts.append(pasted_data.strip())

        st.session_state.data_input = build_data_input(
            st.session_state.topic,
            st.session_state.data_request_text,
            parts,
        )
        st.session_state.phase = 3
        st.rerun()

    st.stop()


# ── Phase 2: Auto-Query Superset ─────────────────────────

if st.session_state.phase == 2:
    prompts = st.session_state.system_prompts
    st.subheader(f"📌 Topic: {st.session_state.topic}")

    # Show Phase 0 data request
    if st.session_state.data_request_text:
        with st.expander("📋 Phase 0: Data Request", expanded=False):
            st.markdown(st.session_state.data_request_text)

    # Step 1: Agent sinh SQL queries
    with st.expander("📝 SQL Queries (Agent-generated)", expanded=True):
        if not st.session_state.sql_agent_output:
            with st.spinner("Agent dang viet SQL queries..."):
                full_text = st.write_stream(
                    phase05_generate_queries_stream(
                        st.session_state.topic,
                        st.session_state.data_request_text,
                        st.session_state.knowledge,
                        tracker=st.session_state.token_tracker,
                    )
                )
                st.session_state.sql_agent_output = full_text
                st.rerun()  # rerun to update sidebar token display
        else:
            st.markdown(st.session_state.sql_agent_output)

    # Step 2: Execute queries
    if st.session_state.sql_agent_output and not st.session_state.query_results_md:
        queries = phase05_parse_queries(st.session_state.sql_agent_output)
        if queries:
            with st.spinner(f"Dang chay {len(queries)} queries tren Superset..."):
                markdown_report, results = phase05_execute_queries(queries)
                st.session_state.query_results_md = markdown_report

                # Save to file
                filepath = phase05_save_data(markdown_report, st.session_state.topic)
                st.session_state.query_data_file = filepath

                # Summary
                success = sum(1 for r in results if r["error"] is None and r["data"])
                failed = sum(1 for r in results if r["error"] is not None)
                empty = sum(1 for r in results if r["error"] is None and not r["data"])

                if success:
                    st.success(f"✅ {success} queries thanh cong")
                if empty:
                    st.warning(f"⚠️ {empty} queries khong co data")
                if failed:
                    st.error(f"❌ {failed} queries loi")
                st.info(f"💾 Data saved: {filepath}")
        else:
            st.error("Khong parse duoc SQL queries tu agent output.")

    # Step 3: Show query results
    if st.session_state.query_results_md:
        with st.expander("📊 Query Results", expanded=True):
            st.markdown(st.session_state.query_results_md)

        # Step 4: User adds insights before debate
        st.divider()
        st.subheader("💡 Bo sung insight truoc khi phan tich")
        st.caption("Xem data o tren, them insight/context con thieu. De trong neu khong can bo sung.")

        user_insights = st.text_area(
            "Insight bo sung:",
            height=150,
            placeholder="VD: Tuan nay co event lon nen DAU tang dot bien, khong phai organic growth...",
        )

        uploaded_extra = st.file_uploader(
            "Upload them data (optional)",
            accept_multiple_files=True,
            type=["csv", "txt", "tsv", "json"],
            key="extra_upload",
        )

        col1, col2 = st.columns(2)
        with col1:
            start_debate = st.button("▶ Bat dau Debate", type="primary", use_container_width=True)
        with col2:
            back_btn = st.button("← Quay lai Phase 1", use_container_width=True)

        if back_btn:
            st.session_state.phase = 1
            st.session_state.sql_agent_output = ""
            st.session_state.query_results_md = ""
            st.session_state.query_data_file = ""
            st.rerun()

        if start_debate:
            # Collect extra insights
            insight_parts = []
            if user_insights.strip():
                insight_parts.append(user_insights.strip())
            for f in (uploaded_extra or []):
                try:
                    content = f.read().decode("utf-8")
                    insight_parts.append(f"--- FILE: {f.name} ---\n{content}")
                except Exception as e:
                    st.error(f"Loi doc file {f.name}: {e}")

            # Build data input with auto-queried data + insights
            st.session_state.data_input = phase05_build_data_with_insights(
                st.session_state.topic,
                st.session_state.data_request_text,
                st.session_state.query_results_md,
                "\n\n".join(insight_parts),
            )
            st.session_state.phase = 3
            st.rerun()

    st.stop()


# ── Phase 3: Debate ───────────────────────────────────────

if st.session_state.phase == 3:
    prompts = st.session_state.system_prompts

    st.subheader(f"📌 Topic: {st.session_state.topic}")

    # Show data request if it exists
    if st.session_state.data_request_text:
        with st.expander("📋 Data Request", expanded=False):
            st.markdown(st.session_state.data_request_text)

    # Display completed rounds
    for i, rd in enumerate(st.session_state.rounds_data):
        with st.expander(f"🔥 Round {i + 1} — Hoan thanh", expanded=False):
            render_round(rd)

    # Run current round if not complete
    if not st.session_state.debate_complete:
        round_idx = st.session_state.current_round
        round_num = round_idx + 1
        max_r = st.session_state.max_rounds

        # Get last synthesis for context
        last_synthesis = ""
        if st.session_state.rounds_data:
            last_synthesis = st.session_state.rounds_data[-1].get("synthesis", "")

        st.markdown(f"### 🔥 Round {round_num}/{max_r}")
        round_data = {}

        # ── Phase 1: Analyst (streaming) ──
        with st.expander("🔬 Analyst", expanded=True):
            with st.spinner("Analyst dang phan tich..."):
                analyst_text = st.write_stream(
                    phase1_analyst_stream(
                        st.session_state.data_input,
                        last_synthesis,
                        round_num,
                        prompts["analyst"],
                        tracker=st.session_state.token_tracker,
                    )
                )
                round_data["analyst"] = analyst_text

        # ── Phase 2: Reviewers (parallel) ──
        with st.expander("🧠⚡💎 Reviewers", expanded=True):
            review_prompt = phase2_build_review_prompt(
                analyst_text,
                st.session_state.data_input,
                last_synthesis,
                round_num,
            )

            with st.spinner("3 Reviewers dang review song song..."):
                reviews = phase2_reviewers(
                    prompts["reviewers"],
                    review_prompt,
                    tracker=st.session_state.token_tracker,
                    round_num=round_num,
                )
                round_data["reviews"] = reviews

            if reviews:
                tabs = st.tabs([f"{r[2]} {r[1]}" for r in reviews])
                for tab, (key, name, emoji, color, resp) in zip(tabs, reviews):
                    with tab:
                        st.markdown(resp)
            else:
                st.warning("Khong co reviewer nao tra ve ket qua.")

        # ── Phase 3: Synthesis (streaming) ──
        with st.expander("📋 Synthesis", expanded=True):
            with st.spinner("Dang tong hop..."):
                synth_text = st.write_stream(
                    phase3_synthesize_stream(
                        reviews,
                        prompts["synthesizer"],
                        tracker=st.session_state.token_tracker,
                        round_num=round_num,
                    )
                )
                round_data["synthesis"] = synth_text

            # Convergence
            convergence = check_convergence(synth_text)
            round_data["convergence"] = convergence

            if convergence:
                if "HỘI TỤ" in convergence and "CHƯA" not in convergence:
                    st.success(f"📊 Convergence: {convergence}")
                else:
                    st.info(f"📊 Convergence: {convergence}")

        # Save round data
        st.session_state.rounds_data.append(round_data)

        # Update debate log for export
        st.session_state.debate_log.append(("analyst", analyst_text))
        for key, name, emoji, color, resp in reviews:
            st.session_state.debate_log.append((key, resp))
        st.session_state.debate_log.append(("synthesizer", synth_text))

        # Check if done
        converged = (
            convergence
            and "HỘI TỤ" in convergence
            and "CHƯA" not in convergence
        )

        if converged or round_num >= max_r:
            st.session_state.debate_complete = True

            # Auto-save
            save_debate_log(st.session_state.debate_log, len(st.session_state.rounds_data))

            st.divider()
            if converged:
                st.success(f"✅ Debate hoi tu tai round {round_num}!")
            else:
                st.info(f"✅ Debate hoan thanh — {max_r} rounds.")

            # Rerun to update sidebar with final token usage
            st.rerun()
        else:
            st.session_state.current_round += 1
            st.divider()
            if st.button(f"▶ Tiep tuc Round {round_num + 1}", type="primary"):
                st.rerun()

    else:
        # Debate complete
        st.divider()
        st.success("✅ Debate da hoan thanh!")

        md_content = format_export(st.session_state)
        st.download_button(
            "📥 Download ket qua (.md)",
            md_content,
            file_name=f"debate_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
            mime="text/markdown",
        )

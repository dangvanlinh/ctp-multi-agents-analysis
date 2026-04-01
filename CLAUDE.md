# CTP Multi-Agent Debate System

## Project Purpose
This is a multi-agent AI debate system for game design decisions on Cờ Tỷ Phú (CTP), a Vietnamese P2W mobile board game.

## Architecture
- `run.py` — CLI entrypoint
- `app.py` — Streamlit web UI
- `orchestrator.py` — Debate flow: Phase 0 (data request) → Phase 0.5 (auto-query) → Phase 1-3 (debate loop)
- `superset/client.py` — Superset SQL Lab client (ClickHouse queries)
- `agents/roles.py` — System prompts for all agent types
- `agents/providers.py` — Claude / GPT-4o / Gemini API wrappers
- `knowledge/` — Markdown knowledge base files, loaded into all agents' system prompts
- `outputs/` — Debate logs saved as markdown
- `data/` — Auto-query results saved as markdown (for user review)

## Key Commands
- `streamlit run app.py` — Streamlit web UI (khuyến nghị)
- `python run.py --topic "Phân tích VIP"` — CLI: topic-driven + auto-query Superset
- `python run.py --topic "..." --no-query` — CLI: topic-driven, manual data only
- `python run.py --topic "..." --rounds 3` — CLI: topic-driven, 3 rounds
- `python run.py` — CLI: data-driven (flow cũ, default 2 rounds)
- `python run.py --file data.txt` — CLI: data-driven từ file

## Knowledge Management
When the user asks to update knowledge or add insights:
1. Identify which file in `knowledge/` is most appropriate
2. Add the insight in the correct section
3. Use Vietnamese for game-specific content

Files:
- `game-design.md` — Core mechanics, P2W philosophy
- `player-behavior.md` — Segments, churn, behavioral insights
- `economy.md` — VIP structure, pricing, gem balance
- `resolved.md` — Locked decisions (CHỐT) — DO NOT contradict these
- `analysis-flows.md` — Analytical frameworks

## APIs Used
- Anthropic (Claude) — Analyst + SQL Generator + 1 Reviewer + Synthesizer
- OpenAI (GPT-4o) — 1 Reviewer
- Google (Gemini) — 1 Reviewer
- Superset (ClickHouse) — Auto-query game data via SQL Lab API
All agents read from same knowledge base.

## Auto-Query Flow
When topic-driven mode is used:
1. Phase 0: Agent xác định data cần thiết
2. Phase 0.5: Agent viết SQL → query Superset → lưu data vào `data/`
3. User review data + bổ sung insight
4. Phase 1-3: Debate loop với data + insight

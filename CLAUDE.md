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
- `data/` — Auto-query results saved as markdown (for user review). **KHÔNG đọc folder này khi tìm hiểu project** — chỉ chứa output tạm từ auto-query, không phải source code hay config.

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
4. Confirm with user before writing insights (trừ khi user nói rõ "lưu luôn")

### Cấu trúc Knowledge

**General (cross-feature):**
- `game-design.md` — Core mechanics, P2W philosophy
- `player-behavior.md` — Segments, churn, behavioral insights
- `economy.md` — Tổng quan economy, pricing, revenue breakdown
- `resolved.md` — Locked decisions (CHỐT) — DO NOT contradict these
- `analysis-flows.md` — Analytical frameworks

**Per-feature (chi tiết từng tính năng):**
- `features/_index.md` — **Bản đồ tổng quan**: revenue contribution, cross-dependencies giữa features. Đọc file này trước khi phân tích bất kỳ feature nào.
- `features/vip.md` — VIP: design, data monthly, insights, backlog
- `features/event-skb.md` — Event Săn Kho Báu
- `features/event-chd.md` — Event Cung Hoàng Đạo
- `features/season-pass.md` — Season Pass
- `features/gacha.md` — Gacha thường
- `features/hidden-shop.md` — Hidden Shop

**Mỗi feature file có cấu trúc:**
1. `Related:` — cross-reference tới features liên quan
2. `Design hiện tại` — mechanic, giá, reward
3. `Data & Insights (confirmed)` — số liệu + kết luận đã xác nhận, ghi rõ thời điểm
4. `Backlog` — câu hỏi mở, cần điều tra thêm
5. `Đề xuất (chưa chốt)` — ideas chưa quyết định

**Quy tắc update:**
- Mỗi tháng update data mới vào `Monthly Performance` table
- Khi có insight mới confirmed → thêm vào `Data & Insights`
- Câu hỏi mở → thêm vào `Backlog`, tick [x] khi đã trả lời
- Khi phân tích feature, luôn đọc `_index.md` để biết cross-dependencies

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

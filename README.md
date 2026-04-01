# CTP Multi-Agent Debate System

## Hệ thống này làm gì?
4 AI agents debate về game design CTP (Cờ Tỷ Phú):
- **🔬 Analyst** (Claude): Phân tích data, đề xuất giải pháp với projected impact
- **🧠 Reviewer 1** (Claude): Critical review, đối chiếu với knowledge base
- **⚡ Reviewer 2** (GPT-4o): Critical review, đối chiếu với knowledge base
- **💎 Reviewer 3** (Gemini): Critical review, đối chiếu với knowledge base

3 Reviewers cùng role, khác model AI — điểm nào cả 3 đều đồng ý = đồng thuận mạnh.

## Flow hoạt động

### Flow A: Topic-driven + Auto-query (khuyến nghị)
```
Topic → Agent đọc knowledge → Xác định data cần thiết
      → Agent viết SQL queries → Auto-query Superset (ClickHouse)
      → Lưu data ra file → User xem + bổ sung insight
      → Analyst phân tích (data + insight)
      → 3 Reviewers review song song (đối chiếu knowledge)
      → Synthesizer tổng hợp đồng thuận / tranh cãi
      → Convergence check → Lặp lại N rounds
```

### Flow B: Topic-driven manual (không auto-query)
```
Topic → Analyst đọc knowledge → Yêu cầu data cần thiết
      → User cung cấp data (paste/file)
      → Debate loop
```

### Flow C: Data-driven (user đưa data trước — flow cũ)
```
Data input → Analyst đề xuất
           → 3 Reviewers review song song
           → Synthesizer tổng hợp
           → Convergence check → Lặp lại N rounds
```

## Setup

### Cài dependencies
```bash
pip install -r requirements.txt
```

### Setup API keys
Tạo file `.env`:
```
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=AI...

# Superset (ClickHouse auto-query)
SUPERSET_URL=https://bitool-hn2.zingplay.com
SUPERSET_ACCESS_TOKEN=your_session_token_here
SUPERSET_DB_ID=5
```

## Cách dùng

### Topic-driven + Auto-query (khuyến nghị)
Agent tự xác định data → viết SQL → query Superset → lưu file → chờ insight:
```bash
python run.py --topic "Phân tích tính năng VIP"
python run.py --topic "Tối ưu retention 1-6 tháng" --rounds 3
```
Sau khi auto-query xong, data lưu tại `data/query_*.md`. Bạn có thể:
- **Xem file data** để kiểm tra kết quả query
- **Bổ sung insight**: paste trực tiếp hoặc `file:path/to/data.csv`
- **`done`** — bắt đầu debate với data đã query + insight
- **`skip`** — debate ngay với data đã query

### Topic-driven (không auto-query)
```bash
python run.py --topic "Phân tích VIP" --no-query
```
Agent liệt kê data cần, bạn cung cấp thủ công.

### Data-driven (flow cũ)
```bash
python run.py                          # default data
python run.py --data "custom data"     # inline data
python run.py --file data.txt          # từ file
python run.py --rounds 3               # 3 rounds
```

### Interactive mode (can thiệp giữa rounds)
```bash
python run.py --topic "..." -i --rounds 3
```
Sau mỗi round, bạn có thể:
- **Enter** — tiếp tục round tiếp
- **`s`** — dừng debate, lưu kết quả
- **Nhập text** — inject chỉ dẫn cho Analyst round tiếp

### Streamlit UI (khuyến nghị)
```bash
streamlit run app.py
```
Mở browser tại `localhost:8501`. Có thể:
- Nhập topic → agent yêu cầu data → upload CSV/paste data → debate
- Xem từng phase (Analyst / Reviewers / Synthesis) trong expander
- 3 Reviewers hiển thị trong tabs riêng
- Export kết quả ra markdown
- Xem lại history các debate trước

### Kết quả
Output tự động lưu vào `outputs/debate_YYYYMMDD_HHMMSS.md`

## Cấu trúc project
```
ctp-multi-agents-analysis/
├── agents/
│   ├── __init__.py       — exports
│   ├── providers.py      — Claude / GPT-4o / Gemini API calls
│   └── roles.py          — system prompts
├── knowledge/            — tri thức game (edit tại đây)
│   ├── game-design.md    — Core mechanics, luật chơi, P2W philosophy
│   ├── player-behavior.md— Player segments, churn, insights
│   ├── economy.md        — KPIs, VIP, DKXX, gem balance, pricing
│   ├── resolved.md       — Quyết định đã CHỐT (agents không được thay đổi)
│   └── analysis-flows.md — Các framework phân tích
├── outputs/              — Debate logs (tự tạo)
├── superset/             — Superset ClickHouse client
│   ├── __init__.py       — exports
│   └── client.py         — Login, CSRF, query execution
├── data/                 — Auto-query results (tự tạo)
├── orchestrator.py       — Debate flow + phase functions + convergence
├── knowledge.py          — Knowledge loader
├── app.py                — Streamlit web UI
├── run.py                — CLI entrypoint
├── requirements.txt
└── .env                  — API keys + Superset token (không commit)
```

## Update tri thức

### Thêm insight mới
Mở file tương ứng trong `knowledge/` và thêm vào. Tất cả agents đều đọc cùng knowledge base.

### Dùng Claude Code để update
```bash
claude "Thêm insight: whale CTP chủ yếu nạp vì DKXX, không phải cosmetic"
```

### Quyết định đã chốt
Khi CHỐT quyết định → update `resolved.md`. Agents sẽ không được đề xuất thay đổi các quyết định này.

## Features
- **Auto-query Superset** — Agent tự viết SQL, query ClickHouse, lưu data ra file
- **Human-in-the-loop** — User review data + bổ sung insight trước khi phân tích
- **Parallel API calls** — 3 reviewers chạy song song, giảm latency ~3x
- **Cross-round context** — Round 2+ reviewers nhận synthesis round trước
- **Convergence tracking** — Auto-detect khi debate hội tụ, dừng sớm
- **Interactive mode** — User can thiệp, inject chỉ dẫn giữa rounds

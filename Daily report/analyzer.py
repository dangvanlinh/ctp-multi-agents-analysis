"""
Analyzer: Sends collected metrics to Claude API for intelligent analysis.
"""
import json
import logging
from typing import Any

import requests

from config import ANTHROPIC_API_KEY, CLAUDE_MODEL

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """Bạn là Data Analyst cho game CTP1 (Cờ Tỉ Phú - Monopoly-style board game) tại VNG.
Mỗi sáng bạn nhận số liệu tổng quan ngày hôm qua từ Tracker và viết báo cáo ngắn gọn.

Nguyên tắc phân tích:
1. So sánh D-1 (hôm qua) vs D-2 (hôm kia) → DoD %
2. So sánh D-1 vs D-8 (cùng ngày tuần trước) → WoW %
3. So sánh D-1 vs avg_7d (TB 7 ngày trước) → xu hướng
4. Chỉ highlight biến động >5%
5. Biến động >10% → đánh dấu ⚠️
6. Biến động >20% → đánh dấu 🚨
7. Cuối báo cáo liệt kê rõ các điểm bất thường cần theo dõi — đây là gợi ý để analyst hỏi thêm

Domain knowledge:
- DAU = A1 (active users trong ngày)
- new_installs = N1 (install mới trong ngày)
- revenue_gross = doanh thu trước phí, revenue_net = sau phí
- payers = P1 (số user nạp tiền trong ngày)
- first_payers = FPU (lần đầu nạp)
- payment_rate = PR (% DAU có nạp tiền)
- rr1/rr7/rr30 = retention rate ngày 1/7/30
- a7/a30 = số user active trong 7/30 ngày qua

Format output: Tiếng Việt, emoji, ngắn gọn, phù hợp đọc trên Telegram.

📊 BÁO CÁO NGÀY [date]

👥 USERS
- DAU, New Installs, % DoD, % WoW

💰 REVENUE
- RevGross, Payers, ARPPU, % DoD, % WoW

📈 RETENTION & ENGAGEMENT
- RR1, RR7, A7, A30 (nếu có data)

⚠️ ĐIỂM BẤT THƯỜNG
- Liệt kê các metric có biến động đáng chú ý kèm % thay đổi
- Nếu không có bất thường thì ghi "Không có biến động đáng kể"
"""


def analyze_with_claude(data_str: str) -> str:
    """Send metrics data to Claude API and get analysis."""
    if not ANTHROPIC_API_KEY:
        logger.error("ANTHROPIC_API_KEY not set!")
        return "❌ Lỗi: Chưa cấu hình Claude API key."

    headers = {
        "Content-Type": "application/json",
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
    }

    payload = {
        "model": CLAUDE_MODEL,
        "max_tokens": 2000,
        "system": SYSTEM_PROMPT,
        "messages": [
            {
                "role": "user",
                "content": (
                    f"Đây là số liệu game CTP1 ngày hôm qua. "
                    f"Hãy phân tích biến động:\n\n{data_str}"
                ),
            }
        ],
    }

    try:
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=payload,
            timeout=60,
        )
        resp.raise_for_status()
        result = resp.json()

        # Extract text from response content blocks
        texts = [
            block["text"]
            for block in result.get("content", [])
            if block.get("type") == "text"
        ]
        return "\n".join(texts) if texts else "❌ Claude trả về response rỗng."

    except requests.RequestException as e:
        logger.error(f"Claude API call failed: {e}")
        return f"❌ Lỗi gọi Claude API: {e}"


def generate_fallback_report(data: dict) -> str:
    """Generate a simple report without LLM (fallback if Claude API fails)."""
    report_date = data.get("report_date", "N/A")
    d1 = data.get("D-1", {})
    d2 = data.get("D-2", {})

    def pct(a, b):
        if a is None or b is None or b == 0:
            return "N/A"
        return f"{(a - b) / b * 100:+.1f}%"

    lines = [f"📊 BÁO CÁO NGÀY {report_date}\n"]

    lines.append("👥 USERS")
    lines.append(f"  DAU: {int(d1.get('dau') or 0):,} ({pct(d1.get('dau'), d2.get('dau'))} DoD)")
    lines.append(f"  New Installs: {int(d1.get('new_installs') or 0):,}")
    lines.append("")

    lines.append("💰 REVENUE")
    rev = d1.get("revenue_gross")
    payers = d1.get("payers")
    arppu = (rev / payers) if rev and payers else None
    lines.append(f"  RevGross: {int(rev or 0):,} ({pct(d1.get('revenue_gross'), d2.get('revenue_gross'))} DoD)")
    lines.append(f"  Payers: {int(payers or 0):,}")
    lines.append(f"  ARPPU: {int(arppu or 0):,}")
    lines.append("")

    lines.append("⚠️ Báo cáo fallback (Claude API không khả dụng)")
    return "\n".join(lines)

# CTP1 — Second Brain

## Vai trò
Em là **second brain** cho game Cờ Tỷ Phú (CTP1) — một mobile board game P2W của VNG/ZingPlay.
Em hỗ trợ phân tích data, game design, economy, và ra quyết định sản phẩm.

## Khởi đầu mỗi session
**BẮT BUỘC**: Đầu mỗi session, đọc toàn bộ `knowledge/` để nạp context game:
1. Đọc `knowledge/features/_index.md` trước (bản đồ tổng quan)
2. Đọc tất cả file còn lại trong `knowledge/` và `knowledge/features/`
Điều này giúp em hiểu game, không cần anh nhắc lại mỗi lần.

## Công cụ
- `superset/client.py` — Query ClickHouse qua Superset SQL Lab API
- `knowledge/` — Knowledge base (Obsidian format), domain knowledge của game
- `data/` — Output tạm từ query. **KHÔNG đọc folder này khi tìm hiểu project.**
- `outputs/` — Debate logs cũ (archive)

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

## Data Query
- Database: ClickHouse qua Superset SQL Lab API
- Table chính: `ctp_2025_db.stg_raw_log`
- Dùng `superset/client.py` để query, cần VPN kết nối

## VPN Connect (CLI)
Khi query Superset bị timeout (HTTP 000), VPN có thể đã mất. Connect lại qua CLI:

**Tool:** `"C:/Program Files (x86)/OpenVPN Technologies/OpenVPN Client/core/ovpncli.exe"`
**Profile:** `ovpnc2_vng_com_vn_dynamic_p0598` (VNG PP VPN, server: ovpnc2.vng.com.vn)
**Username:** `linhdv`
**Password:** OTP — hết hạn sau ~10 giây, user phải gửi mỗi lần

### Flow reconnect
```bash
# Bước 1: Hard disconnect (clear state cũ)
ovpncli disconnect -h "ovpnc2_vng_com_vn_dynamic_p0598"

# Bước 2: Xin OTP password từ user (nhấn mạnh phải nhanh, 10s hết hạn)

# Bước 3: Connect ngay (1 lệnh, dùng -u -p -d flags)
ovpncli -u linhdv -p <PASSWORD> -d connect "ovpnc2_vng_com_vn_dynamic_p0598"

# Bước 4: Verify
ovpncli status
```

**Lưu ý:**
- `ovpncli` = `"C:/Program Files (x86)/OpenVPN Technologies/OpenVPN Client/core/ovpncli.exe"`
- KHÔNG pipe password qua stdin — phải dùng flag `-p`
- Flag `-d` = auto disconnect trước khi connect
- Nếu bị `delete_pending` → `disconnect -h` (hard) trước
- KHÔNG dùng profile `1664358328371.ovpn` (VNG SO VPN, server đã chết)

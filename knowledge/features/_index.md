# Feature Map — Cờ Tỷ Phú (CTP)

> File này là bản đồ tổng quan tất cả features + cross-dependencies.
> Mỗi feature có file riêng trong folder này.

## Revenue Contribution (T3/2026)

| Feature | Rev/tháng | Share | File |
|---------|-----------|-------|------|
| GEM (via Event SKB+CHĐ) | ~760M | 55.5% | [event-skb](event-skb.md), [event-chd](event-chd.md) |
| GOLD + GOLD_BONUS + BIG_RICH | ~358M | 26.1% | — |
| NEW_JOURNEY | ~125M | 9.1% | — |
| VIP | ~82M | 6.0% | [vip](vip.md) |
| SEASON_PASS | ~43M | 3.1% | [season-pass](season-pass.md) |

Tổng rev T3/2026: ~1.37 tỷ/tháng

## Cross-Dependencies

```
Event SKB/CHĐ ──── ra nhân vật mới ────→ VIP (x2 EXP để max nhanh)
     │                                      │
     │                                      ↓
     ├── bán nhân vật premium ──→ GEM nạp (whale driver chính)
     │
     ↓
Gacha thường ── gần như vô dụng (0.4% coin out), bị event thay thế hoàn toàn

Hidden Shop ── sink cho whale, active 30/30 ngày, không phụ thuộc event

Season Pass ── subscription song song VIP, ít PU nhất (14/ngày)
```

### Chi tiết dependencies
- **VIP ↔ Event SKB/CHĐ**: x2 EXP là driver chính mua VIP. User mua VIP để max nhân vật mới từ event. VIP timing gắn chặt với event ra skill mới.
- **Event ↔ GEM**: Event là lý do chính whale nạp GEM. Không có event hấp dẫn → user không tiêu coin → không nạp → rev giảm.
- **Event → Gacha**: Event bán nhân vật đã mix skill xịn → gacha thường (random skill) gần như vô giá trị với informed user.
- **Hidden Shop**: Sink duy nhất active 30/30 ngày, chỉ ~6 PU/ngày nhưng ARPPU cao nhất (4,540 coin). Whale-only.
- **VIP ↔ Season Pass**: Cùng là subscription nhưng khác target. VIP cho x2 EXP (gameplay), Season Pass cho reward khác.

## Overall Insights (cross-feature)
- Game phụ thuộc cực lớn vào GEM (55.5%) + Event cycle → risk cao nếu event không hấp dẫn
- Recurring revenue (VIP + Season Pass) chỉ 9.1% total → thiếu nguồn rev ổn định
- Core user >180 ngày gánh 63.4% total revenue → dependency cực cao vào veteran
- Revenue tăng T2→T3 phần lớn do UA investment (A1/N1 tăng), cần normalize khi đánh giá feature

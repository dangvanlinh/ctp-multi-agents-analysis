# Báo cáo Monthly Performance — Cờ Tỷ Phú T3/2026

> Ngày báo cáo: 04/04/2026
> Kỳ data: 28/02 – 31/03/2026

---

## 1. Tổng quan

| Chỉ số | T2/2026 | T3/2026 | Thay đổi |
|--------|---------|---------|----------|
| **Total Revenue** | 1.16 tỷ | **1.52 tỷ** | **+31%** |
| Paying Users (PU) | 2,282 | 4,603 | +102% |
| ARPPU | 508k | 330k | -35% |

**Nhận định chung:** Revenue tăng +31% nhưng chủ yếu nhờ UA investment đổ user mới (PU tăng gấp đôi). ARPPU giảm 35% do user mới pha loãng — chưa phải tín hiệu game tự cải thiện monetization.

---

## 2. Revenue Breakdown

### 2.1. Theo nguồn nạp

| Nguồn | Rev T3 | Share | vs T2 | Nhận xét |
|-------|--------|-------|-------|----------|
| **GEM** | 875M | 55.5% | -1.5% | Giảm nhẹ dù PU tăng → ARPPU GEM giảm |
| GOLD gộp | 379M | 26.1% | +291% | Tăng cực mạnh nhờ new user từ UA |
| NEW_JOURNEY | 125M | 9.1% | +82% | First-pay package cho user mới |
| VIP | 87M | 6.0% | +58% | Tăng tương đương UA growth, không outperform |
| SEASON_PASS | 43M | 3.1% | +58% | Ít PU nhất (~14/ngày), feature yếu nhất |

### 2.2. Theo nơi tiêu GEM (Coin Out)

| Kênh tiêu GEM | Share | Ghi chú |
|----------------|-------|---------|
| **Event CHĐ** (nhân vật) | 31.6% | Sink lớn nhất, ~340M rev estimate |
| **Event SKB** (nhân vật) | 20.1% | ~216M rev estimate |
| Trang sức event (Lazer + Trứng) | 17.9% | Whale-targeted |
| Hidden Shop | 8.8% | Sink duy nhất chạy 30/30 ngày |
| Gacha thường (nhân vật) | 0.4% | Gần như chết — user chỉ mua qua event |

**Highlight:** Event SKB + CHĐ gộp = ~556M/tháng, chiếm hơn 1/3 tổng revenue game. Game phụ thuộc rất lớn vào event cycle.

---

## 3. Phân tích User

### 3.1. Revenue theo tuổi user

| Nhóm user | Rev | Share |
|-----------|-----|-------|
| **Core >6 tháng** | 957M | **63.4%** |
| Mid 1–6 tháng | 169M | 11.2% |
| New <1 tháng | 383M | 25.4% |

- **Core >6 tháng gánh gần 2/3 doanh thu** — dependency cực cao vào veteran.
- **"Vùng chết" 2–6 tháng chỉ 5.7%** — thấp hơn cả Day0 riêng lẻ. User sau tháng đầu hoặc churn hoặc dormant.
- New user <1 tháng monetize tốt (25.4%), Day0+Day1 riêng đã 9.8% → onboarding monetization đang hoạt động.

### 3.2. Repay Rate 30 ngày (T2 → T3)

| Segment | Repay Rate | Mất |
|---------|------------|-----|
| **Tổng** | **27.4%** | **72.6%** |
| New (<7d) | 22.0% | 78% |
| 7–30d | 21.9% | 78% |
| 30–90d | 26.1% | 74% |
| 90–180d | 30.6% | 69% |
| Core (>180d) | 36.7% | 63% |

**72.6% payer mất sau 30 ngày** — vấn đề lớn ở mọi segment. Kể cả Core cũng mất 63%.

---

## 4. Feature Highlights

### 4.1. VIP — Vấn đề renewal

| Metric | Giá trị |
|--------|---------|
| Rev T3 | 87M (+58% vs T2) |
| PU | 724 |
| **Mua 1 lần rồi bỏ** | **82.8%** |
| Repeat 2+ lần | 17.2% |
| User "zombie" (chơi nhưng ngừng nạp) | ~593 |

- **82.8% user chỉ mua VIP 1 lần** — renewal là vấn đề lớn nhất.
- 77% user 1-lần vẫn chơi game nhưng 85% trong số đó ngừng nạp tiền hoàn toàn.
- Window kích repay: **0–15 ngày sau hết hạn**, sau đó gần như mất luôn.
- Core >180d là backbone: repeat 1.74x, ARPPU 176k, đồng thời nạp GEM 3.71M ARPPU.

**Đề xuất đang chuẩn bị:** VIP Level System (Lv1–5) để tăng retention và ARPT. Target: 350M+/tháng (hiện 87M). Đang trong giai đoạn debate trước production.

### 4.2. Event SKB + CHĐ — Revenue backbone

- Gộp ~556M/tháng → chiếm **>36% tổng rev**
- CHĐ coin out cao hơn SKB đáng kể (31.6% vs 20.1%) — cần investigate tại sao
- Là driver chính khiến whale nạp GEM

### 4.3. Season Pass — Feature yếu nhất

- 43M/tháng, chỉ 14 PU/ngày
- Thiếu data chi tiết (renewal rate, reward detail, overlap với VIP)
- Cần full audit

---

## 5. Risks & Red Flags

| Risk | Mức độ | Chi tiết |
|------|--------|----------|
| **GEM dependency** | Cao | 55.5% rev từ 1 nguồn, volatile (chênh 5.6x giữa ngày cao/thấp) |
| **Core user dependency** | Cao | 63.4% rev từ veteran >6 tháng. Nếu churn → mất >nửa doanh thu |
| **Repay rate thấp** | Cao | 72.6% payer mất/tháng ở mọi segment |
| **UA-driven growth** | Trung bình | Rev tăng 31% chủ yếu nhờ UA, không phải feature improve. Giảm UA → rev drop |
| **Recurring rev thấp** | Trung bình | VIP + Season Pass chỉ 9.1% — thiếu nguồn revenue ổn định |

---

## 6. Action Plan — Ưu tiên T4/2026

### Ưu tiên cao
1. **VIP Level System** — Finalize design, debate balance → quyết định launch timeline
2. **Core retention monitoring** — Setup churn signals sớm cho nhóm >180d (giảm tần suất nạp, giảm session)
3. **Investigate CHĐ > SKB gap** — Hiểu tại sao CHĐ outperform để optimize cả 2

### Ưu tiên trung bình
4. **Fix churn 1–6 tháng** — Cần mid-game content/progression (milestone reward, competitive content)
5. **Season Pass audit** — Full review reward, renewal, user overlap với VIP
6. **Cuối tháng event timing** — 28–31 hàng tháng là spending peak, align event lớn vào window này

---

## 7. Data Gaps cần bổ sung

| Thiếu | Cần để làm gì |
|-------|---------------|
| DAU/MAU T3 vs T2 | Đánh giá retention tổng thể |
| Retention D1/D7/D30 cohort | Xác định churn point chính xác |
| UA cost (CAC, ROAS) | Đánh giá hiệu quả UA investment |
| SKB/CHĐ PU theo user age | Hiểu ai mua event, optimize targeting |
| New user conversion (A1→first pay) | Đo onboarding monetization chính xác |

---

*Report generated from CTP Multi-Agent Analysis System knowledge base. Data period: T3/2026.*

# VIP

Related: [event-skb](event-skb.md), [event-chd](event-chd.md) (x2 EXP driver), [_index](_index.md)

## Design hiện tại
- **Giá**: 100k VNĐ / 10 ngày
- **Tỷ giá GEM**: 100k = 1,000G (mua thẳng) vs VIP cho 1,500G → VIP rẻ hơn 33% về GEM
- **Phần thưởng**:
  - **1,500 GEM**: 750G nhận ngay khi nạp, 750G còn lại chia đều 9 ngày tiếp theo (~83G/ngày)
  - **50 rương vàng**: chia đều 10 ngày (5 rương/ngày). Rương vàng có tỷ lệ ra thẻ A, skill random từ pool
  - **3 rương tím + 3 rương cam**: nhận ngày cuối (ngày 10) — mechanic retention giữ user mua VIP đến hết kỳ
  - **x2 EXP nhân vật** khi chơi game — **benefit giá trị nhất, exclusive chỉ VIP mới có, không có nguồn khác**. Cực kỳ quan trọng với old user khi SKB/CHĐ ra nhân vật mới xịn cần max nhanh.
  - **10 chìa khóa đục lỗ trang sức** — cho old user (cần đục lỗ thẻ A trở lên để gắn trang sức)

## Data & Insights (confirmed)

### Monthly Performance

| Tháng | Rev | Share | PU | Daily PU range | Ghi chú |
|-------|-----|-------|----|----------------|---------|
| T2/2026 | 55.3M | 4.78% | 445 | 11-32 | |
| T3/2026 | 87.4M | 5.75% | 724 | 17-49 | UA tăng mạnh → A1/N1 tăng |

> **Lưu ý**: VIP PU tăng +63% T2→T3 nhưng do UA investment tăng (A1/N1 tăng), chưa thể kết luận VIP tự cải thiện. Cần normalize theo A1/N1.

### VIP Buyers theo User Age (lần mua đầu, T2-T3/2026)

| Segment | Users | % | Revenue | ARPPU | TB lần mua |
|---------|-------|---|---------|-------|------------|
| <7d (Mới) | 361 | 33.1% | 42.8M | 118k | 1.17 |
| 7-30d (Sớm) | 207 | 19.0% | 24.5M | 118k | 1.17 |
| 30-90d (TB) | 172 | 15.8% | 21.5M | 125k | 1.19 |
| 90-180d (Trung thành) | 100 | 9.2% | 14.4M | 144k | 1.43 |
| >180d (Core) | 252 | 23.1% | 44.4M | 176k | 1.74 |

- New user 33% PU nhưng gần như không renewal (1.17 lần)
- Core user 23% PU nhưng 30% rev, repeat cao nhất (1.74x)
- ARPPU tăng dần theo tuổi: 118k → 176k

### Renewal / Retention (T2-T3/2026)

| Số lần mua | Users | % |
|------------|-------|---|
| 1 lần | 904 | 82.8% |
| 2 lần | 106 | 9.7% |
| 3+ lần | 82 | 7.5% |

- **82.8% user chỉ mua VIP 1 lần rồi bỏ** — vấn đề lớn nhất
- Chỉ 17.2% mua lại lần 2+
- Trong 60 ngày, VIP 10 ngày lý tưởng nên mua 6 lần, nhưng max chỉ 1 user mua 10 lần

### Cross-Spending của VIP Buyers (T2-T3/2026)

| Nguồn | Revenue | PU | ARPPU |
|-------|---------|-----|-------|
| GEM | 1.205 tỷ | 680 | 1.77M |
| VIP | 147.6M | 1,092 | 135k |
| GOLD | 79.3M | 266 | 298k |
| BIG_RICH | 65.3M | 379 | 172k |
| GOLD_BONUS | 55.5M | 300 | 185k |
| SEASON_PASS | 44.5M | 312 | 143k |

- 62% VIP buyers cũng nạp GEM (ARPPU 1.77M)
- VIP chỉ chiếm 9% spending của chính VIP buyers → VIP là sản phẩm phụ, GEM là main purchase

### GEM Spending của VIP Buyers theo Age (T2-T3/2026)

| Segment | GEM Payers | % PU | GEM Revenue | % Rev | ARPPU |
|---------|-----------|------|-------------|-------|-------|
| <7d (Mới) | 211 | 31% | 250M | 21% | 1.19M |
| 7-30d (Sớm) | 126 | 19% | 136M | 11% | 1.08M |
| 30-90d (TB) | 114 | 17% | 148M | 12% | 1.30M |
| 90-180d (Trung thành) | 69 | 10% | 77M | 6% | 1.12M |
| >180d (Core) | 160 | 24% | 593M | 49% | 3.71M |

- **Core >180d: 160 người nhưng 49% GEM rev (593M), ARPPU 3.71M — gấp 3x các nhóm khác. Whale thực sự.**
- New <7d đông nhất (211) nhưng ARPPU chỉ 1.19M — mua thử, chưa phải big spender
- Vùng giữa 7-180d ARPPU đều ~1.1-1.3M, không nổi bật → confirm churn cliff

### Deep-dive: Tại sao 82.8% chỉ mua VIP 1 lần? (T2-T3/2026)

**Phễu:**
| Phễu | Users | % |
|------|-------|---|
| Tổng VIP buyers | 1,092 | 100% |
| Mua 1 lần | 904 | 82.8% |
| → Vẫn chơi game sau VIP hết | ~700 | ~77% của 904 |
| → Nhưng không nạp gì | ~593 | ~85% của 700 |
| Mua lại (repeat) | 188 | 17.2% |
| → Mua lại trong 15 ngày | ~145 | ~77% của 188 |

**Insight confirmed:**
1. **77% user 1-lần vẫn chơi game nhưng 85% ngừng nạp tiền** — VIP không đủ value để rebuy, và là cửa cuối trước khi user thành F2P. ~593 user đang chơi, từng chịu chi tiền, nhưng giờ thành F2P → pool lớn nhất để win back.
2. **77% renewal xảy ra trong 15 ngày sau hết hạn** — window kích repay tốt nhất là 0-15 ngày. Binary: subscribe hoặc bỏ hẳn. Nếu không kích trong 15 ngày → mất luôn.

### Key Confirmed Insights
1. **x2 EXP là lý do chính old user mua VIP** — các reward khác (rương, chìa khóa) là filler với informed user
2. **VIP kẹt giữa 2 segment**: old user chỉ cần x2 EXP, new user chưa cần x2 EXP (chưa có nhân vật xịn để nâng)
3. **Core >180d là backbone**: vừa mua VIP repeat (1.74x) vừa nạp GEM cực mạnh (593M). Mất nhóm này = mất cả VIP recurring + phần lớn GEM
4. **VIP growth T2→T3 do UA investment**, không phải VIP tự improve
5. **77% user 1-lần vẫn chơi nhưng ngừng nạp tiền** — VIP là cửa cuối trước F2P, ~593 user là pool win-back
6. **Window kích repay VIP = 0-15 ngày sau hết hạn** — sau 15 ngày gần như mất luôn

## Backlog (cần điều tra thêm)
- [x] ~~Tại sao 82.8% chỉ mua 1 lần?~~ → đã deep-dive, xem phễu ở trên
  - [x] ~~Sau khi VIP hết hạn, user còn chơi không?~~ → 77% vẫn chơi
  - [x] ~~Nhóm repeat mua lại sau bao lâu?~~ → 77% trong 15 ngày
  - [x] ~~User 1-lần có nạp GEM sau khi VIP hết không?~~ → 85% không nạp gì
- [x] ~~VIP conversion rate (PU/A1) có thực sự cải thiện hay chỉ tăng theo UA?~~ → confirmed: tăng do UA, không phải VIP improve
- [ ] New user cần benefit gì khác ngoài x2 EXP?
- [ ] VIP share target bao nhiêu % là hợp lý?
- [ ] Segment VIP như thế nào để phục vụ nhiều tập user?

## Vấn đề cốt lõi (đã xác định)

**VIP value không đủ để repay** — popup kích mua đã có, vấn đề là giá trị không đủ mạnh.

| Segment | Cần gì | VIP hiện tại đáp ứng? |
|---------|--------|-----------------------|
| New (<7d) | Chưa rõ, chưa có NV xịn | ❌ x2 EXP vô dụng |
| Mid (7-180d) | Đang build roster | ❌ Rương random value thấp |
| Core (>180d) | x2 EXP max NV mới | ✅ Nhưng chỉ cần khi có NV mới |

593 user ngừng chi tiền hoàn toàn → khó tìm lý do cụ thể, nhưng kích repay VIP là path tốt nhất vì đã trả 1 lần.

## Core Pillars (nguyên tắc update)
1. **Fix 2 vấn đề VIP**: repay trong tháng (ARPT 1→3) + repay tháng sau (repeat 17%→50%)
2. **Không cắn nhau với event đang chạy**: SKB, CHĐ, Trứng, Lazer — VIP bổ sung, không thay thế. SKB+CHĐ = >50% coin out.

## KPI Target

**Rev target: 350tr+/tháng** (hiện ~72tr)

| Metric | Hiện tại | KPI |
|--------|----------|-----|
| Rev/tháng | ~72tr | 350tr+ |
| PU | 724 | 1,162 |
| New PU | 594 (82%) | 800 (+200) |
| Repay next month | 130 (17%) | 362 (+232) |
| ARPPU | 100k | 300k |
| ARPT | 1.0 | 3 |

**Model compound** (800 PU mới, new retain 50%, old retain 80%, new×2 + old×3):

| Tháng | PU mới | Old retained | Active PU | Lượt | Rev |
|-------|--------|-------------|-----------|------|-----|
| T1 | 800 | 362 (50%×724) | 1,162 | 2,686 | 269M |
| T2 | 800 | 690 | 1,490 | 3,670 | 367M |
| T3 | 800 | 952 | 1,752 | 4,456 | 446M |
| T4 | 800 | 1,162 | 1,962 | 5,086 | 509M |
| T6+ | 800 | ~2,000 | ~2,800 | ~7,600 | ~760M |

> Old retain 80% → pool tích lũy theo thời gian, converge ~2,000. Đạt 350M ngay T2.

## Solution: VIP Level System

> Design doc chi tiết: `docs/vip-level-system-design.md`
> UI mockup: `vip_ui_mockup.html`
> Word doc cho dev: `data/VIP_Design_Doc_v4.docx`

### Core Mechanic (ĐÃ CHỐT)
- VIP có 5 cấp (Lv1-Lv5). Giá 100k/10 ngày tất cả level
- Mua liên tiếp = +1 Level. Không mua + hết 3 ngày grace = Reset Lv0
- VIP tính theo ngày (reset 00:00), không theo giờ
- Chỉ thấy benefit level tiếp theo +1 (tạo curiosity)

### Config Benefit (ĐÃ CHỐT)

| Lv | GEM | R.Vàng | Chìa khóa | R.Tím | EXP | R.Cam | Cosmetic | DKXX | Upgrade R | Bonus %G |
|----|-----|--------|-----------|-------|-----|-------|----------|------|-----------|---------|
| 1 | 1,500G | 50 | 10 | 5 | — | 5 | Khung+FX Vip1 | — | — | TBD |
| 2 | 1,500G | 50 | 10 | 10 | x2 | 10 | Khung+FX Vip2 | +3% | — | TBD |
| 3 | 1,500G | 50 | 10 | 15 | x3 | 15 | Khung+FX Vip3 | +5% | Unlock | TBD |
| 4 | 1,500G | 50 | 10 | 20 | x3 | 15 | Khung+FX Vip4 | +8% | +10% rate | TBD |
| 5 | 1,500G | 50 | 10 | 30 | x4 | 20 | Frame lobby | +10% | +15% rate | TBD |

### Benefit Delivery (ĐÃ CHỐT)
- **Daily Claim** (phải login nhận, mất nếu không): GEM, rương vàng, rương tím (đều 10 ngày), rương cam (5 ngày cuối), chìa khóa
- **Auto-Active** (mua VIP là có): EXP, DKXX, Upgrade R, Cosmetic, Bonus %G

### Edge Cases Đã Chốt (14 decisions)
1. **Mua trước hạn**: Nhận hết quà còn lại + lên level ngay
2. **Mua nhiều lần liền**: Bắt buộc 1 lần = 1 level (nhảy level chỉ cho offer)
3. **Benefit delivery**: Chia 2 segment (daily claim cho new, auto-active cho whale)
4. **Timezone**: Tính theo ngày, reset 00:00
5. **Grace period**: 3 ngày sau hết VIP, không quà, không buff
6. **Reset level**: Reset Lv0 (mất hết) — loss aversion core mechanic
7. **Lapsed rule**: PARK — chờ data live
8. **Upgrade R khi VIP hết**: Khóa ngay (instant action)
9. **CLB B + VIP**: Cộng dồn bonus rate
10. **Arrow navigation**: Trái xem đã qua, phải +1 rồi "???", Lv5="Max Level"
11. **Noti**: Không push noti, dùng in-game claim UI
12. **Nút Kích Hoạt**: 7 states — chưa claim thì chưa cho renew
13. **Rương tím/cam schedule**: Tím đều 10 ngày, cam 5 ngày cuối
14. **New user offer**: ĐÃ CHỐT — lần đầu mua trong đời → Lv2 ngay (100k). Cần UI mockup.

### Upgrade R (ĐÃ CHỐT)
- CLB B+ hoặc VIP Lv3+ → unlock Upgrade R
- VIP hết → khóa ngay, thẻ đã upgrade giữ nguyên
- CLB B + VIP → cộng dồn rate

### Loss Aversion — 3 chiều
- **Social**: Mất khung, FX tung XX → bạn bè thấy
- **Gameplay**: Mất DKXX + x3/x4 EXP → chơi tệ đi
- **Economy**: Mất Bonus %G + Upgrade R → nạp đắt hơn

### CHƯA CHỐT
- [ ] **Bonus %G**: Chưa chốt migration từ shop trung. Data: 65% GEM payer chưa VIP, shop hiện 5-20% free. Hướng: giữ shop 10% flat + VIP thêm on top.
- [ ] **Lapsed rule**: Park — chờ data live. Default: lapsed mua lại = Lv1.
- [ ] DKXX balance, A/B test plan

### Art & UI Tasks
- [ ] Ref art thẻ VIP các cấp, UI thay đổi theo level
- [ ] Ref khung quà trong UI VIP
- [ ] Ref cosmetic: khung avatar, FX tung XX, khung deco NV lobby, BG lobby
- [ ] Redesign nút VIP ở bottom bar main screen
- [ ] New user offer popup UI mockup

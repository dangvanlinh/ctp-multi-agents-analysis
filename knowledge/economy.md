# Economy & Monetization - CTP

## Thuật ngữ
- **G** = Gem = Coin = cùng 1 item (premium currency). Trong DB log tên field là "coin". Tài liệu này thống nhất gọi là **G**.
- Tỷ giá: **100,000 VNĐ = 1,000G**
- GOLD = in-game currency (tiền vàng chơi game), KHÁC với G

## Current Metrics
| Tháng | Total Rev | PU | ARPPU |
|-------|-----------|-----|-------|
| T2/2026 | 1.16 tỷ | 2,282 | 508k |
| T3/2026 | 1.52 tỷ | 4,603 | 330k |

Tăng trưởng +31% rev nhưng ARPPU giảm — do UA đổ user mới (PU +102%), ARPPU bị pha loãng.


## KPI Targets

## Revenue Breakdown (tháng 3/2026, data thực)
- **GEM: 55.5% (~760M)** — chiếm hơn nửa total rev, phụ thuộc cực lớn vào 1 mặt hàng
- GOLD + GOLD_BONUS + BIG_RICH: 26.1% (~358M) — nguồn rev thứ 2, tất cả đều là gold (BIG_RICH là offer gold)
- NEW_JOURNEY (100k + 50k + IAP): 9.1% (~125M) — new user rev thấp, phần lớn rev từ existing users
- VIP: 6.0% (~82M) — thấp so với tiềm năng, VIP chưa đủ value để upsell
- SEASON_PASS: 3.1% (~43M)

## Revenue Insights (confirmed)
- G là premium currency chính, dùng để chơi event mua nhân vật xịn và trang sức xịn. Rev chính đến từ nạp G.
- G rev rất volatile: ngày cao 53M, ngày thấp 9.4M (chênh 5.6x). Lý do: tập whale ít người nhưng thi thoảng nạp nhiều để lấy nhân vật → đẩy rev G spike mạnh.
- Rev phụ thuộc vào tập core user ít nhưng chi nhiều. Nếu tập này churn, rev drop rất mạnh.
- **Rev breakdown là theo nguồn nạp** (G, GOLD, VIP...), còn **coin out là theo nơi tiêu G** (SKB, CHĐ, Hidden Shop...). G rev = tiền vào, event coin out = G đi đâu. Không cộng trực tiếp sẽ double count.

## PU Insights (confirmed, tháng 3/2026)
- GEM chỉ ~63 PU/ngày nhưng ARPPU cao nhất: 405k/ngày. Confirm: revenue phụ thuộc vào nhóm whale nhỏ nạp GEM rất nhiều.
- BIG_RICH đông PU nhất (~93/ngày) nhưng ARPPU thấp nhất (42k). Đây là entry-level package, mass-market.
- VIP chỉ ~27 PU/ngày, ARPPU ~103k — vừa ít người mua vừa chi không cao. Subscription theo tháng. Chưa hấp dẫn whale (so với GEM 405k ARPPU), cũng chưa đủ value để mid-spender convert đông.
- SEASON_PASS ~14 PU/ngày, ARPPU ~102k. Subscription theo tháng. Ít PU nhất trong các mặt hàng chính, rev chỉ 3.1% (~43M).
- Recurring revenue (VIP + SEASON_PASS) chỉ 9.1% total rev — game phụ thuộc gần như hoàn toàn vào one-time purchase (GEM). Thiếu nguồn rev ổn định, predictable.

## Coin Out / Gem Sink (tháng 3/2026, data thực)
Total coin out: ~10.77M

### Event bán đồ xịn (whale-targeted) — 69.6% coin out
- Nhân vật: EventConGiapBuyPack/CHĐ (31.6%) + BuyRollGift/SKB (20.1%) = 51.7%
- Trang sức: TreasureDigBuyLaserGun (9.9%) + GBuyHammer/đập trứng (8.0%) = 17.9%
- Event là động lực chính khiến whale nạp GEM. Không có event hấp dẫn → user không tiêu coin → không nạp → rev giảm.

### Event bán nhân vật — SKB + CHĐ (confirmed)
- **SKB (Săn kho báu / BuyRollGift)** và **CHĐ (Cung hoàng đạo / 12 con giáp / EventConGiapBuyPack)** là 2 event chính bán nhân vật premium
- Mechanic khác nhau nhưng cùng bán nhân vật xịn, cùng đẳng cấp, cùng giá
- **Chạy cả tháng**: cả SKB và CHĐ đều chạy xuyên suốt tháng, không phải xen kẽ 2 tuần
- Mỗi tháng ra 1 skill mới (nhân vật mới)
- **Rev estimate: SKB ~216M + CHĐ ~340M = ~556M/tháng → chiếm >1/3 tổng rev game**
- SKB design: 4 cạnh, tổng 1,000G/vòng, pity thẻ A (2tr) / S (5tr) / R (10tr)
- CHĐ: cùng giá pity, mechanic khác

### Hidden Shop — 8.8% coin out
- BuyHiddenShop (8.0%) + BuyHiddenShopPendant (0.8%)
- Sink duy nhất active 30/30 ngày, không phụ thuộc event cycle
- Volatile: ngày thấp 6k, ngày cao 79k

### Gacha thường (không qua event)
- GachaPendant/trang sức (9.0%) — sink trang sức ngoài event
- OpenGacha/nhân vật (0.4%) — gần như không có ai gacha nhân vật thường, chỉ mua qua event

### Khác
- BuyLobbyItem (4.2%): ~595 PU/ngày nhưng ARPPU chỉ 25 coin — micro-purchase phổ biến, không phải coin sink thực sự
- Loan (1.5%): ~298 PU/ngày nhưng ARPPU chỉ 18 coin — mass-use nhưng không phải coin sink
- BallHuntBuyToken (4.7%)
- UpgradeCharacterRProtect (0.1%) — rất ít người dùng protect khi nâng R

### Coin Out PU Insights (confirmed)
- HiddenShop: chỉ ~6 PU/ngày nhưng ARPPU cao nhất (4,540 coin) — sink cho whale/heavy spender, không phải mass-market
- OpenGacha chỉ 6 PU/ngày — gần như không ai gacha nhân vật thường, user chỉ mua nhân vật qua event

## Revenue by User Age (tháng 3/2026, data thực)
Tổng revenue: ~1,509.6M (32 ngày: 02/28–03/31)

### Tỷ trọng theo nhóm tuổi user
- **Core >6 tháng: 63.4% (~957.5M)** — gánh gần 2/3 revenue toàn game
- Mid 1–6 tháng: 11.2% (~168.9M) — trong đó 1–2 tháng chiếm 5.5%, còn 2–6 tháng chỉ 5.7%
- Early <1 tháng: 25.4% (~383.1M) — Day0+Day1 riêng đã chiếm 9.8%

### Insights (confirmed)
1. **Core >6 tháng gánh 63.4% revenue** — dependency cực cao vào veteran users. Nếu cohort này churn, game mất hơn nửa doanh thu. Kết hợp với GEM dependency (55.5% rev) → risk kép: whale + veteran overlap.
2. **"Vùng chết" 2–6 tháng chỉ 5.7%** — thấp hơn cả Day0 (4.6%) hoặc Day1 (5.2%) riêng lẻ. Đây là churn cliff rõ: user sau 1–2 tháng hoặc churn hoặc dormant, rất ít chuyển thành payer lâu dài.
3. **User mới <1 tháng đóng góp 25.4%** — acquisition → monetization early hiệu quả. Day0 (4.6%) và Day1 (5.2%) spend tốt, cho thấy onboarding monetization đang hoạt động.
4. **Spending giảm sau tháng đầu** — dải 1–2 tháng (5.5%) cao hơn cả 2–6 tháng gộp lại (5.7%). Không có "warm-up curve" rõ ràng, user không spend nhiều hơn theo thời gian mà giảm nhanh.

### Khuyến nghị hành động
- **Ưu tiên giữ chân Core >6 tháng**: Theo dõi churn signals sớm (giảm tần suất nạp, giảm coin out, giảm session). Cần retention mechanic riêng cho nhóm này (exclusive content, loyalty reward).
- **Fix churn 1–6 tháng**: Đây là vùng revenue "bốc hơi" — cần mid-game progression/content mạnh hơn để giữ user qua giai đoạn 30–180 ngày (milestone reward, guild system, competitive content).
- **Tối ưu thêm Day0/Day1**: Onboarding monetization đang tốt, có thể push thêm (first-purchase bonus, time-limited starter pack) để tăng conversion rate cho new users.
- **Cuối tháng là golden window cho core users**: 03/30–03/31 có ARPU cao nhất (6,947–9,804/user), nên timing event lớn vào 28–31 hàng tháng để capture spending peak.

## T2 vs T3 Trend (confirmed)
| Sản phẩm | Rev T2 | Rev T3 | Tăng trưởng |
|----------|--------|--------|-------------|
| GEM | 888M | 875M | -1.5% |
| Gold (gộp) | 97M | 379M | +291% |
| First Pay | 72M | 131M | +82% |
| VIP | 55M | 87M | +58% |
| SEASON_PASS | 29M | 46M | +58% |

- GEM giảm dù PU tăng → ARPPU GEM giảm
- Gold/First Pay tăng cực mạnh nhờ UA đổ new user
- VIP/Season Pass tăng 58% — tương đương UA growth, không outperform

## Repay Rate 30 ngày (T2→T3, confirmed)
| Segment | Users | Repay Rate | Mất |
|---------|-------|------------|-----|
| Tổng | 2,282 | 27.4% | 1,657 |
| <7d (New) | 640 | 22.0% | 499 |
| 7-30d | 430 | 21.9% | 336 |
| 30-90d | 376 | 26.1% | 278 |
| 90-180d | 245 | 30.6% | 170 |
| >180d (Core) | 591 | 36.7% | 374 |

- 72.6% payer mất sau 30 ngày — vấn đề lớn của game
- New user mất 78%, Core vẫn mất 63%

## Pricing Philosophy

## VIP
> Chi tiết design, data & backlog → xem [features/vip.md](features/vip.md)

## Monetization Insights (confirmed)

### Gacha thường vs Event — tại sao gacha coin out thấp
- Rương/gacha thường mở ra thẻ random skill, pool skill rất rộng → rất khó ra được skill xịn hoặc combo skill xịn
- User hiểu biết (thường sau age 7 ngày) nhận ra điều này → không gacha thường nữa
- Event SKB (Săn kho báu), CHĐ (Cung hoàng đạo) bán sẵn thẻ đã được mix skill xịn → đây mới là con đường chính để có nhân vật mạnh
- Kết quả: gacha nhân vật thường chỉ 0.4% coin out, gần như không ai dùng. User chỉ mua nhân vật qua event
- **Implication cho design**: Bất kỳ reward nào dạng "rương random" đều có perceived value thấp với informed user. Reward dạng "chọn được" hoặc "đảm bảo chất lượng" có perceived value cao hơn nhiều
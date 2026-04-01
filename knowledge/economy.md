# Economy & Monetization - CTP

## Current Metrics (tháng 3/2026)
- Revenue: ~1.37 tỷ/tháng (30 ngày, trung bình ~45.6M/ngày)


## KPI Targets

## Revenue Breakdown (tháng 3/2026, data thực)
- **GEM: 55.5% (~760M)** — chiếm hơn nửa total rev, phụ thuộc cực lớn vào 1 mặt hàng
- GOLD + GOLD_BONUS + BIG_RICH: 26.1% (~358M) — nguồn rev thứ 2, tất cả đều là gold (BIG_RICH là offer gold)
- NEW_JOURNEY (100k + 50k + IAP): 9.1% (~125M) — new user rev thấp, phần lớn rev từ existing users
- VIP: 6.0% (~82M) — thấp so với tiềm năng, VIP chưa đủ value để upsell
- SEASON_PASS: 3.1% (~43M)

## Revenue Insights (confirmed)
- GEM là coin chính, dùng để chơi event mua nhân vật xịn và trang sức xịn. Rev chính đến từ GEM.
- GEM rev rất volatile: ngày cao 53M, ngày thấp 9.4M (chênh 5.6x). Lý do: tập whale ít người nhưng thi thoảng nạp nhiều để lấy nhân vật → đẩy rev GEM spike mạnh.
- Rev phụ thuộc vào tập core user ít nhưng chi nhiều. Nếu tập này churn, rev drop rất mạnh.

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
- Chạy xen kẽ: mỗi event 2 tuần/tháng, luân phiên → luôn có 1 event bán nhân vật active
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

## Pricing Philosophy

## VIP Design (hiện tại)
- Giá: 100k VNĐ / 10 ngày
- Tỷ giá GEM: 100k = 1,000G (mua thẳng) vs VIP cho 1,500G → VIP rẻ hơn 33% về GEM
- Phần thưởng:
  - **1,500 GEM**: 750G nhận ngay khi nạp, 750G còn lại chia đều 9 ngày tiếp theo (~83G/ngày)
  - **50 rương vàng**: chia đều 10 ngày (5 rương/ngày). Rương vàng có tỷ lệ ra thẻ A, skill random từ pool
  - **3 rương tím + 3 rương cam**: nhận ngày cuối (ngày 10) — mechanic retention giữ user mua VIP đến hết kỳ
  - **x2 EXP nhân vật** khi chơi game — **benefit giá trị nhất, exclusive chỉ VIP mới có, không có nguồn khác**. Cực kỳ quan trọng với old user khi SKB/CHD ra nhân vật mới xịn cần max nhanh. Game nâng cấp rất tốn thời gian nếu không có x2 EXP.
  - **10 chìa khóa đục lỗ trang sức** — cho old user (cần đục lỗ thẻ A trở lên để gắn trang sức)

### VIP Insights (confirmed)
- **x2 EXP là lý do chính old user mua VIP** — các reward khác (rương, chìa khóa) là filler với informed user
- **VIP kẹt giữa 2 segment**: old user chỉ cần x2 EXP (1 benefit duy nhất có giá trị), new user chưa cần x2 EXP (chưa có nhân vật xịn để nâng)
- Cần data: VIP PU theo user age, renewal rate, timing vs event cycle

## Monetization Insights (confirmed)

### Gacha thường vs Event — tại sao gacha coin out thấp
- Rương/gacha thường mở ra thẻ random skill, pool skill rất rộng → rất khó ra được skill xịn hoặc combo skill xịn
- User hiểu biết (thường sau age 7 ngày) nhận ra điều này → không gacha thường nữa
- Event SKB (Săn kho báu), CHĐ (Cung hoàng đạo) bán sẵn thẻ đã được mix skill xịn → đây mới là con đường chính để có nhân vật mạnh
- Kết quả: gacha nhân vật thường chỉ 0.4% coin out, gần như không ai dùng. User chỉ mua nhân vật qua event
- **Implication cho design**: Bất kỳ reward nào dạng "rương random" đều có perceived value thấp với informed user. Reward dạng "chọn được" hoặc "đảm bảo chất lượng" có perceived value cao hơn nhiều
# Decision Log

Ghi lại mọi quyết định quan trọng về game design, economy, feature. Mục đích:
- Biết **tại sao** quyết như vậy (không chỉ **gì**)
- Khi context thay đổi → biết decision nào cần revisit
- Anti-pattern: quyết rồi quên lý do → lặp lại debate cũ

## Format mỗi decision

```
### [ID] Tên decision
- **Date**: YYYY-MM-DD
- **Feature**: feature liên quan
- **Decision**: Chốt gì
- **Reasoning**: Tại sao chọn option này
- **Alternatives considered**: Các option khác đã cân nhắc + tại sao reject
- **Data support**: Data/insight nào support quyết định
- **Risk/assumption**: Giả định nào nếu sai thì cần revisit
- **Status**: CHỐT | PARK (chờ data) | REVISIT (cần xem lại)
```

---

## VIP Level System

### D001 — VIP 5 level, giá flat 100k
- **Date**: 2026-03
- **Feature**: VIP
- **Decision**: VIP chia 5 cấp (Lv1-Lv5), giá 100k/10 ngày tất cả level. Mua liên tiếp = +1 level.
- **Reasoning**: Giá flat giữ barrier thấp cho new user. Progression tạo lý do mua tiếp (hiện 82.8% chỉ mua 1 lần). Level system tạo loss aversion khi rớt.
- **Alternatives considered**:
  - Giá tăng theo level (150k, 200k...) → reject vì tăng barrier, giảm PU. Target là tăng ARPT (số lần mua), không phải ARPPU.
  - 3 level thay vì 5 → reject vì quá ít tầng, progression nhanh quá, hết motivation sớm.
  - 10 level → reject vì quá nhiều, mỗi level benefit nhỏ, không meaningful.
- **Data support**: 82.8% chỉ mua 1 lần (T2-T3/2026). ARPT hiện tại ~1.0, target 3.0. Cần mechanic khiến user muốn mua tiếp, không phải mua đắt hơn.
- **Risk/assumption**: Giả định user sẽ thấy level progression đủ hấp dẫn để mua tiếp. Nếu benefit giữa các level quá nhỏ → vẫn bỏ sau 1-2 lần.
- **Status**: CHỐT

### D002 — Grace period 3 ngày, reset Lv0
- **Date**: 2026-03
- **Feature**: VIP
- **Decision**: Hết VIP + 3 ngày không mua lại = reset về Lv0 (mất hết level). Trong grace không có quà, không có buff.
- **Reasoning**: Loss aversion là core mechanic. Reset hoàn toàn tạo stakes cao nhất. Grace 3 ngày cho user thời gian quyết định, không quá khắc nghiệt.
- **Alternatives considered**:
  - Rớt 1 level thay vì reset → reject vì loss aversion yếu, user có thể "trượt" dần mà không urgent.
  - Không grace, reset ngay → reject vì quá harsh, user bận 1-2 ngày là mất hết.
  - Grace 7 ngày → reject vì quá dài, giảm urgency mua lại.
- **Data support**: 77% renewal xảy ra trong 15 ngày sau hết hạn. Window kích repay thực tế rất ngắn — binary: mua hoặc bỏ.
- **Risk/assumption**: Nếu reset quá harsh → user bỏ luôn thay vì mua lại. Cần monitor churn rate sau reset ở data live.
- **Status**: CHỐT

### D003 — x2 EXP chuyển từ Lv1 sang Lv2
- **Date**: 2026-03
- **Feature**: VIP
- **Decision**: Lv1 không có x2 EXP. x2 EXP bắt đầu từ Lv2. Lv3+ có x3, Lv5 có x4.
- **Reasoning**: x2 EXP là benefit giá trị nhất, exclusive VIP. Nếu cho ngay Lv1 thì old user mua 1 lần là đủ (vẫn lặp pattern cũ). Đẩy lên Lv2 = buộc mua ít nhất 2 kỳ mới có benefit chính.
- **Alternatives considered**:
  - x2 EXP ở Lv1 (giữ nguyên hiện tại) → reject vì không tạo lý do mua lần 2.
  - x2 EXP ở Lv3 → reject vì quá xa, new user mất 30 ngày mới có → churn trước khi đạt.
- **Data support**: Core >180d mua VIP chủ yếu vì x2 EXP. Các benefit khác là filler. Cần dùng x2 EXP như carrot cho progression.
- **Risk/assumption**: New user lần đầu mua VIP Lv1 không có x2 EXP → perceived value thấp → có thể giảm first purchase rate. Mitigation: new user offer Lv2 ngay.
- **Status**: CHỐT

### D004 — New user offer: lần đầu mua = Lv2 ngay
- **Date**: 2026-04
- **Feature**: VIP
- **Decision**: User chưa từng mua VIP, lần đầu mua = nhảy thẳng Lv2 (100k). Có x2 EXP ngay.
- **Reasoning**: Giải quyết conflict D003 (x2 EXP ở Lv2 nhưng new user cần thử VIP lần đầu). Cho Lv2 ngay = perceived value cao lần đầu + tạo hook để mua tiếp lên Lv3.
- **Alternatives considered**:
  - Giảm giá lần đầu (50k cho Lv1) → reject vì vẫn không có x2 EXP, value thấp.
  - Cho free trial 3 ngày Lv1 → reject vì Lv1 value thấp, trial không impress.
- **Data support**: 33% VIP PU là new <7d, ARPPU 118k, gần như không renewal (1.17x). Cần hook mạnh hơn cho lần đầu.
- **Risk/assumption**: Nếu Lv2 ngay thì user có thể thấy "đã đủ" và không muốn lên Lv3. Mitigation: Lv3 unlock x3 EXP + Upgrade R = jump lớn.
- **Status**: CHỐT

### D005 — Benefit delivery: daily claim + auto-active
- **Date**: 2026-03
- **Feature**: VIP
- **Decision**: Chia 2 loại: daily claim (GEM, rương — phải login nhận) và auto-active (EXP, DKXX, cosmetic — mua là có).
- **Reasoning**: Daily claim tạo daily engagement, tăng retention. Auto-active cho whale không muốn micromanage. Hai segment khác nhau, serve cả hai.
- **Data support**: VIP kẹt giữa 2 segment: new user cần engagement loop, core user cần passive buff.
- **Risk/assumption**: Daily claim nếu quá nhiều item = annoying. Cần UI claim nhanh (1 tap claim all).
- **Status**: CHỐT

### D006 — Rương cam: config 5 rương (trước là 3)
- **Date**: 2026-04
- **Feature**: VIP
- **Decision**: Rương cam tăng từ 3 lên 5 ở Lv1, scale lên 10-15-15-20 ở Lv2-5. Nhận 5 ngày cuối.
- **Reasoning**: Rương cam là reward "end of cycle" — retention mechanic giữ user chơi đến hết kỳ. Tăng số lượng vì config cũ (3 rương ngày cuối) quá ít, không đủ motivation.
- **Alternatives considered**:
  - Rải đều 10 ngày → reject vì mất mechanic "end of cycle reward".
  - Giữ 3 rương → reject vì 3 rương cam giá trị thấp, không đủ pull.
- **Data support**: Rương cam có tỷ lệ ra thẻ tốt hơn rương tím/vàng. Là reward perceived value cao.
- **Status**: CHỐT

---

## Economy

(Chưa có decision ghi nhận — backfill khi có)

---

## Event

(Chưa có decision ghi nhận — backfill khi có)

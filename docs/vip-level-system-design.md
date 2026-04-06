# VIP Level System — Design Doc

> Status: **Draft — cần review trước production**
> Date: 2026-04-06
> UI Mockup: `vip_ui_mockup.html`

---

## 1. Overview

Redesign VIP từ subscription đơn giản (100k/10 ngày, 82.8% mua 1 lần) thành hệ thống level progression với loss aversion, kích repay trong tháng và repay tháng sau.

**Core Pillars:**
1. Fix 2 vấn đề VIP: repay trong tháng (ARPT 1→3) + repay tháng sau (repeat 17%→50%)
2. Không cắn nhau với event đang chạy (SKB, CHĐ, Trứng, Lazer)

---

## 2. Core Mechanic

- VIP có **5 cấp** (Lv1-Lv5)
- Giá: **100k VNĐ / 10 ngày** (tất cả level)
- Mua liên tiếp = +1 Level
- Không mua khi hết hạn + hết grace period = **reset về Lv0**
- Chỉ thấy benefit level tiếp theo +1, level xa bị ẩn (tạo curiosity)

---

## 3. Config Benefit

| Lv | GEM | R.Vàng | Chìa khóa | R.Tím | EXP | R.Cam | Cosmetic | DKXX | Upgrade R | Bonus %G |
|----|-----|--------|-----------|-------|-----|-------|----------|------|-----------|---------|
| 1 | 1,500G | 50 | 10 | 5 | — | 5 | Khung+FX Vip1 | — | — | TBD |
| 2 | 1,500G | 50 | 10 | 10 | x2 | 5 | Khung+FX Vip2 | +3% | — | TBD |
| 3 | 1,500G | 50 | 10 | 15 | x3 | 10 | Khung+FX Vip3 | +5% | Unlock | TBD |
| 4 | 1,500G | 50 | 10 | 20 | x3 | 10 | Khung+FX Vip4 | +8% | +10% rate | TBD |
| 5 | 1,500G | 50 | 10 | 30 | x4 | 15 | Frame lobby | +10% | +15% rate | TBD |

> **Bonus %G**: Chưa chốt design. Cần giải quyết vấn đề migration từ shop trung (hiện free 5-20% theo gói). Xem mục 9.

---

## 4. Benefit Delivery — 2 Loại

### 4.1 Daily Claim (phải login nhận, mất nếu không login)
- GEM (83G/ngày)
- Rương vàng (5/ngày)
- Rương tím (chia đều 10 ngày)
- Rương cam (chia cho 5 ngày cuối: ngày 6-10)
- Chìa khóa (chia đều 10 ngày)

**VD Lv2 (10 tím, 5 cam):**

| Ngày | R.Tím | R.Cam |
|------|-------|-------|
| 1-5 | 1/ngày | — |
| 6-10 | 1/ngày | 1/ngày |

> Mục đích: Kích new user login hàng ngày → tăng retention rate. Rương cam cuối kỳ = incentive không bỏ ngang.

### 4.2 Auto-Active (mua VIP là có, không cần login)
- x2/x3/x4 EXP
- DKXX boost
- Upgrade R access
- Cosmetic (khung, FX)
- Bonus %G khi nạp (nếu chốt)

> Mục đích: Whale cần buff này khi chơi, không cần login claim. Giữ whale happy.

**Decision log:**
- Options: A) Tất cả daily claim, B) Tất cả auto-active, C) Chia 2 segment
- Chốt: **C** — mỗi segment có behavior target khác nhau
- Pro: New login hàng ngày, whale không bị phiền
- Con: Phức tạp hơn cho dev (2 loại delivery)

---

## 5. Timing & Countdown

### 5.1 VIP tính theo ngày
- Mua ngày nào thì hết 00:00 ngày thứ 11
- Daily claim reset lúc 00:00

**Decision log:**
- Options: A) Tính theo giờ chính xác, B) Tính theo ngày
- Chốt: **B**
- Pro: Dễ hiểu, align daily claim
- Con: User mua 23:59 được "free" gần 1 ngày — negligible

### 5.2 Grace period khi hết VIP
- Hết 10 ngày → user có **3 ngày** để mua tiếp
- Trong 3 ngày: không nhận quà daily (VIP đã hết), benefit auto-active cũng mất
- Không mua trong 3 ngày → **reset Lv0**

### 5.3 Countdown Lv5
- Lv5 cũng được 3 ngày grace (giống các level khác)

**Decision log (Reset):**
- Options: A) Reset Lv0, B) Reset Lv3, C) Giảm 1 level/kỳ
- Chốt: **A — Reset Lv0**
- Pro: Loss aversion mạnh nhất
- Con: Harsh, nhưng 3 ngày grace đủ dài, nếu drop thì mềm hơn cũng không giữ được

---

## 6. Mua VIP — Rules

### 6.1 Mua trước hạn
Khi user mua VIP tiếp trong khi VIP hiện tại chưa hết:
1. Nhận trọn quà còn lại của level hiện tại vào inbox ngay
2. Level hiện tại kết thúc
3. Level mới kích hoạt ngay, 10 ngày mới bắt đầu

**Decision log:**
- Options: A) Đợi hết kỳ mới lên, B) Lên ngay mất ngày cũ, C) Nhận hết quà + lên ngay
- Chốt: **C**
- Pro: User không mất gì, lên level ngay, kích mua sớm = tăng ARPT
- Con: Burst quà gộp — nhưng là quà đáng lẽ nhận rồi

### 6.2 Mua nhiều lần liền
- **Không cho phép** mua nhiều lần cùng lúc để nhảy level
- Bắt buộc 1 lần mua = 1 level
- Nhảy level chỉ dành cho offer new user / lapsed

**Decision log:**
- Options: A) Cho nhảy level, B) 1 lần = 1 level
- Chốt: **B**
- Pro: User trải nghiệm từng level, attach dần, loss aversion mạnh
- Con: Whale không fast-track — nhưng đó là intent

---

## 7. Nút Kích Hoạt — Điều kiện hiển thị

| Trạng thái | Nút Claim | Nút Kích hoạt |
|-----------|-----------|---------------|
| Chưa là VIP | Không có | **Hiện** |
| Đang VIP, còn >3 ngày, chưa claim | **Hiện** | Ẩn |
| Đang VIP, còn >3 ngày, đã claim | Không | Ẩn |
| Đang VIP, còn ≤3 ngày, chưa claim | **Hiện** | Ẩn (chờ claim) |
| Đang VIP, còn ≤3 ngày, đã claim | Không | **Hiện** (renew) |
| Hết VIP, trong 3 ngày grace | Không | **Hiện** (urgent) |
| Hết VIP, quá 3 ngày → Lv0 | Không | **Hiện** (mua lại Lv1) |

> Rule: Chưa claim quà hôm nay → chưa cho renew. Đảm bảo user luôn nhận quà trước khi quyết định mua tiếp.

---

## 8. Upgrade R

- Hiện tại: chỉ CLB hạng B+ mới upgrade R
- VIP Lv3+: unlock thêm đường Upgrade R (mở thêm, không gating mới)
- VIP hết → **khóa ngay** quyền Upgrade R (instant action, không có process dở dang)
- Thẻ R đã upgrade xong → **giữ nguyên**, không revert
- CLB B + VIP cùng lúc → bonus rate **cộng dồn**

**Decision log (khóa khi VIP hết):**
- Options: A) Cho hoàn thành đang chạy, B) Khóa ngay
- Chốt: **B** — Upgrade R là bấm nút instant, không có trạng thái "đang upgrade"

**Decision log (CLB + VIP):**
- Options: A) Cộng dồn, B) Lấy cao nhất
- Chốt: **A** — không punish user đạt CLB B

---

## 9. Chưa chốt — Cần design thêm

### 9.1 Bonus %G (PARKED)
- **Vấn đề**: Shop trung hiện cho bonus 5-20% free theo gói (50k→5%, 1M→20%)
- 65% GEM payer không mua VIP → nếu remove shop bonus, họ mất hết
- 81% transactions là gói ≤200k (bonus ≤10%), chỉ 6% mua gói 1M (20%)
- **Hướng đang xem xét**: Giữ shop 10% flat, VIP cộng thêm +5%/level
- **Blocker**: Cần tính balance kỹ hơn, concern về GEM inflation

### 9.2 Lapsed Rule (PARKED)
- **Vấn đề**: Offer skip Lv2 cho lapsed user có thể bị gaming (bỏ VIP → chờ KM → mua khi cần x2 EXP → loop)
- **Chờ**: Data live về lapsed behavior rồi mới design
- **Default**: Lapsed user mua lại = bắt đầu từ Lv1, không có KM

### 9.3 New User Offer
- Lần mua đầu tiên trong đời → skip lên Lv2 ngay
- Cần design offer UI riêng — **park cho anh design mockup**

---

## 10. UI

### 10.1 Screens đã mockup (`vip_ui_mockup.html`)
1. **Chưa VIP** — preview Lv1, nút Kích hoạt, benefit mờ
2. **Đang VIP** — benefit sáng, nút Claim quà, countdown, arrows xem level
3. **VIP ≤3 ngày** — progress đỏ, warning, nút Claim + nút Renew (disabled đến khi claim)
4. **Hết VIP — 3 ngày grace** — tất cả benefit khóa, countdown reset, nút Kích hoạt urgent

### 10.2 Arrow Navigation
- Trái: xem lại level đã qua
- Phải: chỉ tới level hiện tại +1, tiếp theo "???"
- Lv5 phải: "Max Level"

### 10.3 Cần design thêm (PARKED)
- [ ] Redesign nút VIP ở bottom bar main screen (hiện có sẵn, cần thêm level + countdown)
- [ ] New user offer popup
- [ ] Ref art thẻ VIP các cấp, UI thay đổi theo level
- [ ] Ref khung quà trong UI
- [ ] Ref cosmetic: khung avatar, FX tung XX, khung deco NV lobby, BG lobby

---

## 11. Noti/Communication
- **Không push noti** — dùng in-game UI khi login
- Daily claim popup = touchpoint tự nhiên để nhắc countdown VIP
- User không login → không biết VIP sắp hết — nhưng nếu không login thì noti cũng không giữ được

---

## 12. KPI Target

**Rev target: 350tr+/tháng** (hiện ~72tr)

Model compound (800 PU mới, new retain 50%, old retain 80%, new×2 + old×3):

| Tháng | PU mới | Old retained | Active PU | Lượt | Rev |
|-------|--------|-------------|-----------|------|-----|
| T1 | 800 | 362 | 1,162 | 2,686 | 269M |
| T2 | 800 | 690 | 1,490 | 3,670 | 367M |
| T3 | 800 | 952 | 1,752 | 4,456 | 446M |
| T6+ | 800 | ~2,000 | ~2,800 | ~7,600 | ~760M |

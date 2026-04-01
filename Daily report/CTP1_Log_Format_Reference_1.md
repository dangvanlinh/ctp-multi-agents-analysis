# CTP1 Log Format Reference

> Tài liệu tham khảo log format cho agent phân tích CTP1.
> Database: ClickHouse v24.3.12.75 — Table: `stg_raw_log`

---

## 1. Table Schema (`stg_raw_log`)

| Column | Type | Mô tả |
|--------|------|--------|
| `log_time` | DateTime | Thời gian ghi log (đã là DateTime, không cần cast) |
| `market` | String | Thị trường |
| `social` | String | Kênh social |
| `platform` | String | Nền tảng (iOS/Android/...) |
| `client_version` | String | Phiên bản client |
| `user_id` | String | ID người chơi |
| `username` | String | Tên người chơi |
| `log_group` | String | Nhóm log (không dùng để filter, chỉ tham khảo) |
| `log_action` | String | Hành động log (**luôn filter theo cột này**) |
| `level` | Int | Level người chơi (reserved keyword — cần backtick) |
| `user_age` | Int | Tuổi tài khoản (ngày) |
| `coin` | Int | Coin |
| `gold` | Int | **Rank** của người chơi (KHÔNG phải gold currency — reserved keyword) |
| `money` | Int | **Gold currency** của người chơi |
| `extra_1` → `extra_25` | String | Các trường mở rộng, ý nghĩa thay đổi theo `log_action` |

### Column Mapping (DB ↔ Format Doc ↔ biTool)

| DB column | Format doc gọi là | biTool hiển thị |
|-----------|-------------------|-----------------|
| `gold` | rank | gold |
| `money` | gold | money |

> ⚠️ **Trap**: `gold` trong DB = rank, `money` trong DB = gold currency. Luôn verify trước khi viết query.

---

## 2. Query Rules

- **Luôn filter theo `log_action`**, không dùng `log_group` để filter.
- **Date filter**: `toDate(log_time, 'Asia/Ho_Chi_Minh')` — ví dụ: `toDate(log_time, 'Asia/Ho_Chi_Minh') = '2026-03-05'`
- `log_time` đã là DateTime — không cần cast thêm.
- **Backtick-escape reserved keywords**: `` `gold` ``, `` `level` ``, `` `rank` ``

---

## 3. Log Action Details

### 3.1 Payment (`log_action = 'Payment'`)

| Extra | Tên | Mô tả |
|-------|-----|--------|
| `extra_2` | revenue | Doanh thu thực tế (VND) |
| `extra_4` | revFrom | Nguồn revenue |

**revFrom values (`extra_4`)**:
- `GOLD` — Mua gold
- `GOLD_BONUS` — Mua gold bonus
- `GEM` — Mua gem
- `BIG_RICH` — Gói Big Rich
- `SEASON_PASS` — Season Pass
- `VIP` — Đăng ký/gia hạn VIP
- `UNKNOW-50` — Gói nạp lần đầu 50k
- `UNKNOW-51` — Gói nạp lần đầu 100k
- `UNKNOW-52` — Gói nạp lần đầu 100k (IAP)

> ⚠️ **Lưu ý**: Cột `money` trong Payment = gold balance của user tại thời điểm thanh toán, **KHÔNG phải revenue**. Revenue nằm ở `extra_2`.

> Payment/Payment2 = 2 rows per event. **Mặc định query `Payment`**.

---

### 3.2 Login (`log_action = 'Login'` / `'Login2'`)

`log_group = USER`

**Login extra fields:**

| Extra | Tên | Mô tả |
|-------|-----|--------|
| `extra_1` | sessionId | ID phiên đăng nhập |
| `extra_2` | rankLastWeek | Rank tuần trước |
| `extra_3` | — | Giá trị cố định = 1 |
| `extra_4` | — | Giá trị cố định = 0 |
| `extra_5` | userType | Loại user |
| `extra_6` | userPayType | `PayUser` hoặc `NonPay` |
| `extra_7` | clientVersion | Phiên bản client |
| `extra_8` | highestRank | Rank cao nhất đạt được |
| `extra_9` | maxRev30 | Revenue cao nhất 30 ngày |
| `extra_10` | downloadSource | Nguồn tải app |

**Login2 extra fields:**

| Extra | Tên | Mô tả |
|-------|-----|--------|
| `extra_1` | goldInMail | Gold trong hòm thư |
| `extra_2` | goldInAcc | Gold trong tài khoản |
| `extra_3` | totalGold | Tổng gold |
| `extra_4` | curCharId | ID nhân vật hiện tại |
| `extra_5` | curCharType | Loại nhân vật hiện tại |
| `extra_6` | curCharLevel | Level nhân vật hiện tại |
| `extra_7` | curCharType_curTypeLevel | Type_Level nhân vật |
| `extra_8` | numMatchPlayed | Số trận đã chơi |
| `extra_9` | winRate | Tỷ lệ thắng |
| `extra_10` | numGamesLast50 | Số trận chơi trong 50 trận gần nhất |

**Cả Login/Login2 đều có thêm**: `paySegment`, `playSegment`, `maxRevenue30`, `journeyType`, `clientVersion`

> Login/Login2 = 2 rows per event. **Mặc định query `Login`**.

---

### 3.3 UseResource (`log_action = 'UseResource'`)

| Extra | Tên | Mô tả |
|-------|-----|--------|
| `extra_1` | resourceType | Loại tài nguyên: `Gold` hoặc `Gem` (viết hoa chữ đầu) |
| `extra_4` | quantity | Số lượng gold/gem trao đổi |
| `extra_5` | source_out | Nguồn tiêu tài nguyên |

**source_out values (`extra_5`)**:

| source_out | Mô tả |
|------------|--------|
| `PlayMatch` | Chơi trận |
| `LoseGame` | Thua trận |
| `Loan` | Vay gold |
| `BuyGold` | Mua gold |
| `BuyGoldBonus` | Mua gold bonus |
| `BuyGoldOffer` | Mua gold offer |
| `BuyLobbyItem` | Mua item lobby |
| `BuyOfferNewFlowAfterTut` | Mua offer sau tutorial |
| `PurchaseBeginnerPack` | Mua gói người mới |
| `EventConGiapBuyPack` | Mua pack event Con Giáp |
| `BuySeasonPass` | Mua Season Pass |
| `BuyTournamentTicket` | Mua vé giải đấu |
| `VIPRegister` | Đăng ký VIP |
| `UpgradeCharacter` | Nâng cấp nhân vật |
| `UpgradeCharacterR` | Nâng cấp nhân vật (R) |
| `UpgradeCharacterRProtect` | Nâng cấp nhân vật (R) có bảo vệ |
| `GachaPendant` | Gacha mặt dây chuyền |
| `GBuyEffect` | Mua hiệu ứng |
| `ClanCreate` | Tạo clan |
| `ClanDonate` | Donate clan |
| `ClanRequest` | Yêu cầu clan |
| `APPVn` | APPVn |
| `BallHuntBuyToken` | Mua token Săn Bóng |
| `BuyHiddenShop` | Mua Hidden Shop |
| `BuyRollGift` | Spend G cho Săn Kho Báu (SKB) |
| `GBuyHammer` | Mua búa cho Đập Trứng |
| `GGVn` | GGVn |
| `OpenGacha` | Mở Gacha |
| `TreasureDigBuyLaserGun` | Spend G mua laser gun cho Cổ Vật |

---

### 3.4 Event Cổ Vật (`log_group = EVENT_TREASURE_DIG`)

#### EventTreasureDigDig

| Extra | Tên | Mô tả |
|-------|-----|--------|
| `extra_1` | curRegionId | ID vùng hiện tại |
| `extra_2` | dugPositions | Các vị trí đã đào |
| `extra_3` | foundGems | Gems đã tìm thấy |
| `extra_4` | totalPaymentForRegion | Tổng thanh toán cho vùng |
| `extra_5` | totalUsedFreeDigs | Tổng lượt đào miễn phí đã dùng |
| `extra_6` | numTurnDig | Số lượt đào |
| `extra_7` | laserGun | Số laser gun |

#### EventTreasureDigBuyLaserGun

| Extra | Tên | Mô tả |
|-------|-----|--------|
| `extra_1` | quantity | Số lượng mua |
| `extra_2` | totalCost | Tổng chi phí |
| `extra_3` | laserGun | Số laser gun |
| `extra_4` | numTurnDig | Số lượt đào |

#### EventTreasureDigOpenChest

| Extra | Tên | Mô tả |
|-------|-----|--------|
| `extra_1` | regionId | ID vùng |
| `extra_2` | rewards | Phần thưởng |
| `extra_3` | laserGun | Số laser gun |
| `extra_4` | numTurnDig | Số lượt đào |

> Tất cả log Event Cổ Vật: `extra_14` = segment

#### LogClient (Cổ Vật)

`log_action = 'LogClient'`

| Extra | Tên | Mô tả |
|-------|-----|--------|
| `extra_1` | — | Giá trị cố định = `treasure_hunt` |
| `extra_2` | step | `2` = từ icon event, `3` = từ banner |
| `extra_3` | action | `JoinEventThroughBanner`, `BuyGuns`, `ClickIconEvent`, `SeePopup` |

---

## 4. Common Query Patterns

### DAU (Daily Active Users)
```sql
SELECT
    toDate(log_time, 'Asia/Ho_Chi_Minh') AS dt,
    uniqExact(user_id) AS dau
FROM stg_raw_log
WHERE log_action = 'Login'
    AND toDate(log_time, 'Asia/Ho_Chi_Minh') = '2026-03-05'
GROUP BY dt
```

### Daily Revenue
```sql
SELECT
    toDate(log_time, 'Asia/Ho_Chi_Minh') AS dt,
    sum(toInt64OrZero(extra_2)) AS total_revenue_vnd,
    uniqExact(user_id) AS paying_users
FROM stg_raw_log
WHERE log_action = 'Payment'
    AND toDate(log_time, 'Asia/Ho_Chi_Minh') = '2026-03-05'
GROUP BY dt
```

### Revenue by Source
```sql
SELECT
    extra_4 AS rev_from,
    sum(toInt64OrZero(extra_2)) AS revenue_vnd,
    uniqExact(user_id) AS paying_users
FROM stg_raw_log
WHERE log_action = 'Payment'
    AND toDate(log_time, 'Asia/Ho_Chi_Minh') = '2026-03-05'
GROUP BY rev_from
ORDER BY revenue_vnd DESC
```

### Gold Spend by Source
```sql
SELECT
    extra_5 AS source_out,
    sum(toInt64OrZero(extra_4)) AS total_gold_spent,
    uniqExact(user_id) AS users
FROM stg_raw_log
WHERE log_action = 'UseResource'
    AND extra_1 = 'Gold'
    AND toDate(log_time, 'Asia/Ho_Chi_Minh') = '2026-03-05'
GROUP BY source_out
ORDER BY total_gold_spent DESC
```

---

## 5. ClickHouse Tips & Traps

- **LEFT JOIN + range conditions**: Range filter so sánh columns giữa 2 bảng phải đặt ở `WHERE`, không đặt trong `JOIN ON`. Pattern đúng: pre-aggregate right-side data vào CTE, rồi LEFT JOIN trên equality.
- **CTE column aliasing**: Khi CTE select `table.column`, ClickHouse giữ prefix — luôn alias rõ ràng (vd: `l.user_id AS user_id`).
- **NULL behavior**: Non-Nullable columns default `1970-01-01 00:00:00` (DateTime) và `''` (String) — dùng `if(... = toDateTime('1970-01-01'), NULL, ...)` và `nullIf(..., '')`.
- **Reserved keywords**: `` `gold` ``, `` `level` ``, `` `rank` `` phải backtick-escape.

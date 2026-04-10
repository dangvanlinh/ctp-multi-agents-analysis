# Event Đập Trứng (GBuyHammer)

Related: [economy](../economy.md), [event-skb](event-skb.md), [event-chd](event-chd.md)

## Design hiện tại

- **Mục đích**: Bán trang sức SR
- **Chỉ bán trang sức** — không bán nhân vật hay item khác
- **Tier**: Tương tự event Tinh Thạch (cùng hệ thống tier)
- **Currency**: G (gem)
- **Giá**: 30G / búa
- **Log action**: `GBuyHammer`

### Mechanic
- Map grid **3×8 = 24 trứng**, trong đó **8 trứng vàng** chứa mảnh item xịn, **16 trứng trắng** chứa item thường
- Vị trí trứng vàng **random mỗi ngày**, số lượng cố định 8/24
- User **thấy được** trứng vàng vs trắng, trứng vàng hiển thị ảnh mảnh item bên trong
- Tuy nhiên user **KHÔNG chọn được** đập trứng nào — sau mỗi lần đập, hệ thống di chuyển **random 4 hướng** (mỗi hướng 25%) đến trứng kế tiếp
- → Yếu tố **may rủi** nằm ở đường di chuyển, không phải vị trí trứng vàng
- Đập trứng vàng → nhận **1 mảnh ghép** của giải đó + **2 phần thưởng khác** đi cùng
- Đập trứng trắng → nhận item thường
- Mảnh item xịn: cần ghép đủ **4 mảnh cùng loại** → nhận item trang sức SR
- **5 item trang sức xịn** với giá trị tăng dần

### Map system
- Mỗi ngày mới login → hệ thống **random** đưa user vào 1 trong các map có sẵn (theo config ở trên)
- Vị trí bắt đầu trên map cũng được hệ thống **random**
- Số lượng trứng vàng của mỗi loại giải theo config cố định, nhưng **vị trí random** trên map
- Map reset theo ngày

### Tính toán chi phí
- Đập hết 1 map (24 trứng): 24 × 30G = **720G** → guaranteed 8 mảnh + bonus rewards
- Số trứng vàng trúng phụ thuộc vào **luck di chuyển random** — không tối ưu được
- Để ghép đủ 1 item cần 4 mảnh cùng loại (trong 5 loại), mảnh nào trúng cũng random

## Revenue & Coin Out

- Coin out T3/2026: ~8.0% total coin out (~862k coin)
- Thuộc nhóm "Event bán đồ xịn — trang sức" cùng với TreasureDigBuyLaserGun (9.9%)
- Tổng nhóm trang sức: ~17.9% coin out

## Data & Insights (confirmed)

*(Chưa có data chi tiết — cần query thêm)*

## Backlog

- [ ] Revenue riêng event đập trứng (tách khỏi nhóm trang sức chung)
- [ ] PU/ngày, ARPPU của event
- [ ] Conversion rate từ active user → mua búa
- [ ] So sánh hiệu quả bán trang sức: Đập Trứng vs Tinh Thạch vs Lazer
- [ ] Tier detail: giá mỗi tier, pity system (nếu có)

## Đề xuất (chưa chốt)

*(Chưa có)*

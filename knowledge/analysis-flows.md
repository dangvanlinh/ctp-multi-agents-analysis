# Analysis Flows - Các framework phân tích

## Flow 1: Revenue Gap Analysis
1. So sánh Current vs KPI từng metric (Rev, PU, ARPPU, ARPT, Repay)
2. Tính gap tuyệt đối và % cần tăng
3. Xác định metric nào có leverage cao nhất (tăng 1 metric nào sẽ kéo revenue nhiều nhất)
4. Đề xuất giải pháp cụ thể cho top 2-3 metrics có leverage cao

## Flow 2: Conversion Funnel
1. New user → Trial → First purchase → Repay within month → Repay next month
2. Tính conversion rate mỗi bước
3. Tìm bước nào drop nhiều nhất = biggest bottleneck
4. Thiết kế mechanic giải quyết bottleneck đó

## Flow 3: Segment Impact Analysis
1. Với mỗi đề xuất, đánh giá impact lên 3 segments: Whale, Mid, F2P
2. Check: Whale có bị nerf? Mid có được buff đủ? F2P có bị unfair?
3. Net revenue impact = (Whale impact × Whale %) + (Mid impact × Mid %) + (F2P conversion × value)

## Flow 4: Economy Balance Check
1. Gem inflow mới (bonus) vs gem sink hiện tại
2. Nếu inflow > sink → inflation → cần thêm sink
3. Check edge case: Lv6 player với +30% bonus nạp liên tục

## Flow 5: Top-Down Feature Analysis (BẮT BUỘC cho mọi phân tích)
Đây là skill phân tích cốt lõi. LUÔN đi từ tổng quan xuống chi tiết, KHÔNG nhảy thẳng vào đề xuất.

1. **Overall metrics trước** — Feature đang đóng góp bao nhiêu % rev? Bao nhiêu PU? ARPPU bao nhiêu? So với các feature khác thì thế nào?
2. **Hiểu design hiện tại** — Feature hoạt động thế nào? Giá bao nhiêu? Gồm những gì? Tỷ giá so với mua thẳng?
3. **Xác định ai đang dùng** — User nào mua? Old/Mid/New? Vì lý do gì? Benefit nào thực sự có giá trị vs filler?
4. **Tìm mismatch** — Design đang target ai vs ai thực sự mua? Có benefit nào valuable với segment này nhưng vô nghĩa với segment kia?
5. **Đặt câu hỏi data** — Từ phân tích trên, xác định data nào cần query để confirm/reject giả thuyết
6. **Đề xuất dựa trên evidence** — Chỉ đề xuất sau khi có đủ context, gắn với feature cụ thể đã có

Nguyên tắc: Mỗi bước phải hoàn thành trước khi xuống bước tiếp. KHÔNG skip bước 1-4 để nhảy thẳng vào đề xuất.

## Flow 6: KPI Impact Estimation (BẮT BUỘC trước khi design solution)
Sau khi phân tích xong vấn đề, KHÔNG đi thẳng vào solution. Phải estimate impact trước.

1. **Xác định KPI muốn sửa** — Metric nào sẽ thay đổi nếu fix vấn đề này? (Rev, PU, ARPPU, Repeat rate...)
2. **Estimate impact** — Nếu fix thành công, KPI tăng bao nhiêu? Quy ra revenue/tháng cụ thể
3. **So với total** — Impact chiếm bao nhiêu % total rev? Có đáng để invest effort không?
4. **So với opportunity khác** — Có chỗ nào khác leverage lớn hơn với effort tương đương không?
5. **Quyết định** — Impact đủ lớn → design solution. Impact nhỏ → park lại, chuyển sang opportunity lớn hơn.

Nguyên tắc: Không bao giờ design solution mà chưa biết impact. Số nhỏ + effort lớn = lãng phí.

## (Anh thêm flow phân tích riêng vào đây)

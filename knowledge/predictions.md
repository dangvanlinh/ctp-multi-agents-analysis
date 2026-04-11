# Prediction Log

Ghi lại mọi dự đoán về impact, kết quả feature, player behavior. Mục đích:
- Tạo **feedback loop**: đoán → đo → sai ở đâu → học
- Calibrate judgment theo thời gian (đoán quá lạc quan? quá bi quan?)
- Phân biệt insight thật vs wishful thinking

## Format mỗi prediction

```
### [P-ID] Tên prediction
- **Date**: YYYY-MM-DD (ngày đoán)
- **Feature**: feature liên quan
- **Prediction**: Đoán gì, con số cụ thể
- **Basis**: Dựa trên data/logic gì để đoán
- **Check date**: Khi nào kiểm tra (deadline)
- **Metric to check**: Query/cách đo cụ thể
- **Result**: (điền sau) Thực tế ra sao
- **Accuracy**: (điền sau) Đúng / Sai / Partially
- **Lesson**: (điền sau) Sai vì đâu, lần sau adjust gì
```

---

## VIP Level System

### P001 — VIP Level System đạt 350M/tháng trong T2 sau launch
- **Date**: 2026-04-07
- **Feature**: VIP
- **Prediction**: VIP rev đạt ~367M vào tháng thứ 2 sau launch, dựa trên compound model (800 new PU, 50% new retain, 80% old retain, ARPPU 100k, ARPT new=2 old=3).
- **Basis**: Compound model trong vip.md. Assumptions: level system tăng ARPT từ 1.0 → 2-3, loss aversion giữ old PU 80%.
- **Check date**: T+2 tháng sau launch
- **Metric to check**: `SELECT sum(vnd_net) FROM fct_payment__overview WHERE payment_item = 'VIP' AND report_date BETWEEN launch+30 AND launch+60`
- **Result**: —
- **Accuracy**: —
- **Lesson**: —

### P002 — Renewal rate tăng từ 17% lên 50%+
- **Date**: 2026-04-07
- **Feature**: VIP
- **Prediction**: VIP renewal rate (mua lần 2+) tăng từ 17.2% lên 50%+ nhờ level progression + loss aversion.
- **Basis**: Hiện 82.8% mua 1 lần. Level system tạo 2 lý do mua tiếp: (1) unlock benefit mới, (2) sợ mất level. Benchmark: subscription games thường 40-60% renewal khi có progression.
- **Check date**: T+2 tháng sau launch
- **Metric to check**: `SELECT countIf(buy_count >= 2) / count(*) FROM vip_buyers WHERE first_buy >= launch_date`
- **Result**: —
- **Accuracy**: —
- **Lesson**: —

### P003 — New user offer Lv2 tăng first-purchase conversion
- **Date**: 2026-04-07
- **Feature**: VIP
- **Prediction**: VIP first-purchase rate (new user mua VIP lần đầu) tăng 20-30% so với trước khi có new user offer, nhờ perceived value cao hơn (có x2 EXP ngay).
- **Basis**: Hiện new user <7d là 33% VIP PU nhưng ARPPU thấp nhất (118k) và gần không renewal (1.17x). x2 EXP là benefit #1, cho ngay Lv2 = hook mạnh hơn.
- **Check date**: T+1 tháng sau launch
- **Metric to check**: So sánh VIP conversion rate (VIP PU / A1) trước vs sau launch, filter new user <7d.
- **Result**: —
- **Accuracy**: —
- **Lesson**: —

### P004 — Core user >180d retain 80%+ với loss aversion
- **Date**: 2026-04-07
- **Feature**: VIP
- **Prediction**: Core user (>180d) đã đạt Lv3+ sẽ retain ở mức 80%+ (mua tiếp kỳ sau), nhờ loss aversion 3 chiều (social: mất khung, gameplay: mất EXP/DKXX, economy: mất bonus).
- **Basis**: Core hiện repeat 1.74x (cao nhất trong segments). Với thêm loss aversion (reset Lv0 sau grace), motivation giữ level sẽ mạnh hơn. ARPPU core 176k = sẵn sàng chi.
- **Check date**: T+3 tháng sau launch (cần thời gian core đạt Lv3+)
- **Metric to check**: Retention rate = % core user Lv3+ mua tiếp kỳ kế.
- **Result**: —
- **Accuracy**: —
- **Lesson**: —

---

## Monthly Review

### Template review hàng tháng
```
## Review tháng [MM/YYYY]
- Predictions checked: P-xxx, P-xxx
- Đúng: x/y
- Sai: x/y
- Bias observed: (lạc quan quá? bi quan quá? miss factor nào?)
- Adjustment: (lần sau đoán thế nào cho chuẩn hơn)
```

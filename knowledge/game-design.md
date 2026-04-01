# Game Design - Cờ Tỷ Phú (CTP)

## Tổng quan
- Mobile online board game, P2W model (Vietnamese Monopoly-style)
- Target market: Việt Nam, casual + mid-core players

## Core Mechanics
- game dựa trên bàn chơi cờ tỷ phú cơ bản và update thêm các rule để thêm đa dạng chiến thuật.
- core cơ bản: bàn chơi cơ bản có 32 slot chia làm 4 cạnh, người chơi tung 2 viên xx và di chuyển trên map, tới vị trí có thể mua nhà mới (nếu là ô đất trống), trả phí mua lại nhà (nếu là nhà của đối thủ).
- game có các loại ô đất:
    - ô đặc biệt: tù, start, du lịch, festival
    - ô đất: có thể xây nhà, nâng cấp (cấp 1->cấp 5). cấp 5 là landmark và ko thể mua lại. còn lại các cấp dưới có thể bị mua lại sau khi trả phí. đối thủ đi tới ô đất của mình sẽ trả phí tham quan. 
    - ô resort: mỗi cạnh có 1 ô du lịch. ô này không mua lại được.
- ở 4 góc là các slot đặc biệt bao gồm:  
    - tù (ng chơi vào tù sẽ mất lượt và chuyển lượt. lượt sau muốn ra tù phải hoặc tung xx ra kq đổ đôi, hoặc trả tiền để thoát tù). 
    - Start (khi qua hoặc đứng tại start được tăng tiền hỗ trợ. nếu đứng trên start được chọn một nhà của  mình để nâng cấp lên). 
    - Ô du lịch: người chơi tới ô du lịch thì lượt sau sẽ được chọn một ô bất kỳ trên map để di chuyển tới
    - ô festiva: người chơi vào ô này có thể tổ chức lễ hội làm x2 tiền phí tham quan. x2 tăng theo số lần tổ chức lên x3,x4. một thời điểm chỉ có 1 ô dc tổ chức lễ hội

- người chơi thắng bằng 4 cách:
    - làm đối thủ phá sản
    - thắng khi xây đủ 3 cặp màu
    - khi thắng 1 hàng
    - khi xây đủ 5 ô resort
- bàn chơi từ 2 đến 4 người.

- người chơi có các item như sau:
- thẻ nhân vật: đây là item chính:
    - thẻ nv chứa các skill passive được kích hoạt tùy theo điều kiện của skill. ví dụ khi đi qua o start có 50% x2 số tiền được cấp.
    - Thẻ nv có các hạng D,C,B,A,S,R. tương ứng với số passive 0,1,2,3,4,5. mỗi hạng có 5 sao, nâng cấp max 5 sao sẽ lên một hạng. ng chơi nâng cấp từ D lên S. riêng cấp S lên R nâng cấp kiểu khác, người chơi phải dùng thẻ nguyên liệu là thẻ S trở lên để làm nguyên liệu nâng cấp thẻ S5 sao lên R. có tỷ lệ xịt. lên R đc thêm một skill nhưng chỉ số max của 4 skill thẻ S ko tăng, skill số 5 sẽ bắt đầu từ R1 sao tương đương sức mạnh skill đó ở thẻ S1sao. 
    - Số passive của game khoảng 170 skill
- Trang sức: từ thẻ A trở đi ng chơi được đục lỗ thẻ (dùng chìa khóa, có tỷ lệ xịt đục lỗ). thẻ A 2 lỗ, thẻ S và R 3 lỗ.
    - trang sức là một skill passive. trang sức nắp vào thẻ, tháo ra được.
    - tối đa 3 trang sức / thẻ
- Xúc Xắc: 
    - mỗi người chơi sở hữu 1 con xx trong bàn chơi
    - hiện % dk xx cao nhất là 29%
    - có con xx sở hữu vv, có con thì theo thời gian.
    - game có 6 con xúc xắc cho tới hiện tại


# 🎲 Luật Chơi Cờ Tỷ Phú ZingPlay

## 1. Mục tiêu

Chiến thắng ván chơi bằng 1 trong 5 cách sau đây:
- Phá sản tất cả đối thủ
- Sở hữu tất cả ô Resort
- Sở hữu 3 cặp nhà đất cùng màu
- Sở hữu toàn bộ nhà đất và resort trên 1 hàng
- Sau 25 lượt chơi, bạn là người có tổng giá trị bất động sản lớn nhất

---

## 2. Thành phần chính

- Bàn chơi: các bàn chơi khác nhau có thể có số lượng ô, loại ô khác nhau (Cổ điển, Cổ tích, Wallstreet,...)
- Người chơi: 2-4 người
- Khi bắt đầu ván chơi, mỗi người chơi có:
    - Nhân vật: mang kỹ năng nv
    - Trang sức: mang kỹ năng trang sức
    - Pet: mang kỹ năng pet
    - Xúc xắc: tăng chỉ số khi đổ xúc xắc
    - Vật phẩm hỗ trợ: mua từ cửa hàng, dùng trong ván chơi để tạo lợi thế
    - Số tiền khởi đầu như nhau

---

## 3. Bắt đầu trò chơi

- Random 1 người chơi đi trước
- Nhận số tiền khởi đầu bằng nhau
- Tất cả bắt đầu tại ô khởi hành

---

## 4. Luật chơi cơ bản

### Game loop

- Chơi theo lượt từ người đi đầu, mỗi lượt gồm:
    1. Tung xúc xắc
    2. Di chuyển
    3. Thực hiện hành động tại ô dừng
    4. Kết thúc lượt, chuyển sang người chơi tiếp theo
    5. Lặp lại cho đến khi có người chiến thắng hoặc đạt 25 lượt chơi

### 🎯 Lượt chơi

- Tung 2 xúc xắc và di chuyển theo số ô tương ứng
- Thực hiện hành động tại ô dừng
- Nếu tung xúc xắc đôi, được chơi tiếp lượt nữa (tối đa 3 lần, nếu lần thứ 3 vẫn là đôi sẽ bị đi tù)

### Tung xúc xắc

- Số xúc xắc: 2
- Số mặt xúc xắc: 6
- Di chuyển theo tổng số mặt xúc xắc
- Căn lực: chọn các khoảng lực để tăng xác suất ra số mong muốn:
  - Khoảng lực 0: 2-4
  - Khoảng lực 1: 5-7
  - Khoảng lực 2: 7-9
  - Khoảng lực 3: 10-12
- Tỷ lệ "Điều kiển xúc xắc":
  - hệ số random quyết định kết quả xúc xắc có nằm trong khoảng lực đã chọn hay không.
  - Với xúc xắc cơ bản, tỷ lệ này là 15%, nghĩa là có 15% cơ hội kết quả xúc xắc sẽ nằm trong khoảng lực đã chọn, và 85% cơ hội sẽ là kết quả ngẫu nhiên bình thường.
  - Người chơi có thể tăng tỷ lệ này bằng cách sử dụng kỹ năng nhân vật, trang sức, pet hoặc vật phẩm hỗ trợ.
- Sử dụng vật phẩm để chi phối kết quả xúc xắc:
  - Vật phẩm đổ đôi: luôn đổ ra 2 số giống nhau
  - Vật phẩm chẵn lẻ: luôn đổ ra kết quả chẵn hoặc lẻ

### Di chuyển

- Người chơi di chuyển theo chiều kim đồng hồ trên bàn chơi
- Một số kỹ năng và hiệu ứng có thể cho phép di chuyển ngược chiều kim đồng hồ
- Một số kỹ năng và hiệu ứng có thể cho phép di chuyển thêm hoặc bớt số ô di chuyển
- Một số kỹ năng và hiệu ứng có thể cho phép chọn điểm đến thay vì di chuyển theo xúc xắc
- Một số kỹ năng và hiệu ứng có thể chặn người chơi dừng lại tại khi gặp phải
- Một số kỹ năng và hiệu ứng có thể đưa người chơi đến ô đất khác khi dừng lại: hố đen, bẫy băng,...

---

## 5. Các ô trên map

### Tổng quan

- Mỗi loại ô lại có hiệu ứng khác nhau, chủ yếu là hiệu ứng khi người chơi đi đến ô đó (check-in).
- Ngoài ra còn một số hiệu ứng đặc biệt khác: khi sở hữu ô, khi đi qua ô

### Các loại ô trên map

#### Ô CITY

"Ô CITY là ô tài sản cốt lõi của game, người chơi có thể đi đến và sở hữu, người khác đến tham quan sẽ phải trả phí, có 5 cấp độ và màu sắc khác nhau theo cặp"

- Mỗi ô đất có giá trị mua và giá trị nâng cấp khác nhau theo config bàn chơi
- Sở hữu ô đất: trả tiền mua cho ngân hàng, nhận được phí tham quan khi đối thủ đi đến ô đó
- Nâng cấp ô đất: Có 5 cấp độ từ cắm cờ đến nhà 1, nhà 2, nhà 3 và LANDMARK
- Giá mua, tham quan và mua lại tăng dần theo số nhà sở hữu, không thể mua lại LANDMARK
- Khi đi đến:
  - nếu chưa có chủ, có thể mua;
  - nếu đã có chủ, phải trả phí tham quan cho chủ, sau khi trả phí có quyền được mua lại nếu ô này chưa lên cấp LANDMARK;
  - nếu chủ là mình, có thể nâng cấp
- Sở hữu 3 cặp ô CITY cùng màu sẽ đạt điều kiện chiến thắng 3 cặp màu.

#### Ô RESORT

"Ô RESORT là ô tài sản đặc biệt có thể đi đến và sở hữu nhưng không được mua lại"

- Có 4 đến 5 ô RESORT phân bổ rải rác trên bàn chơi, giá trị ô thấp nhưng ko thể mua lại.
- Phí tham quan RESORT tăng theo số RESORT đã sở hữu hoặc số lần tham quan
- Khi đi đến:
  - nếu chưa có chủ, có thể mua;
  - nếu đã có chủ, phải trả phí tham quan cho chủ, không được mua lại
- Sở hữu tất cả RESORT sẽ đạt điều kiện chiến thắng du lịch

#### Ô Khí Vận

"Ô Khí Vận là ô bổ trợ có tính may rủi và giúp tăng tính ngẫu nhiên và replay của bàn chơi"

- Khi đi đến: Người chơi nhận được 1 trong khoảng 15-20 thẻ cơ hội ngẫu nhiên (mechanic giống monopoy)

#### Ô THUẾ

"Ô THUẾ là ô bổ trợ kiểu rubber-band giúp người chơi thu hẹp khoảng cách tài sản"

- Khi đi đến: Người chơi phải trả tiền thuế = 10% tổng tài sản đang sở hữu, nếu không đủ tiền trả, người chơi sẽ phải bán nhà hoặc bị phá sản.

#### Ô START

Ô neutral cho tất cả người chơi, giúp quá trình chơi tăng tiến

- Người chơi bắt đầu tại ô này
- Mỗi khi di chuyển được 1 vòng (đi qua ô START hoặc đi đến ô START), người chơi nhận được tiền thưởng = 15% tiền khởi đầu
- Khi đi đến: người chơi được chọn 1 trong ô CITY chưa nâng cấp max để thực hiện hành động nâng cấp

#### Ô TÙ

"Ô TÙ là ô bổ trợ mechanic di chuyển, trừng phạt người chơi di chuyển nhiều khi đổ đôi liên tiếp 3 lần"

- Khi đổ đôi 3 lần, người chơi bị ném vào tù.
- Khi vào tù, người chơi mất lượt hiện tại và phải đợi sang lượt sau để thoát tù
- Khi đang ở tù, người chơi có 3 lựa chọn để thoát tù:
  - Dùng thẻ "Thoát Tù"
  - Đổ xúc xắc ra kết quả đôi, nếu không sẽ vẫn đứng yên trong tù
  - Trả 5% tiền khởi đầu để được ra
- Sau khi ở tù 3 lượt đổ xúc xắc không ra kết quả đôi, người chơi được thả khỏi tù và di chuyển tiếp

#### Ô LỄ HỘI

"Ô LỄ HỘI là 1 ô phụ trợ giúp tăng phí của một ô CITY hoặc RESORT lên cao hơn"

- Khi đi đến: người chơi được chọn 1 trong các ô CITY hoặc RESORT của mình để tăng phí lên
- Sau mỗi lần tổ chức lễ hội, phí tăng dần: X2, X3, X4

#### Ô TRAVEL

"Ô TRAVEL là 1 ô phụ trợ giúp di chuyển thẳng đến ô mong muốn thay vì phải đổ xúc xắc ngẫu nhiên"

- Khi đi đến: người chơi dừng lượt chơi, ở lượt chơi tiếp theo người chơi được chọn 1 ô bất kì trên bàn chơi để di chuyển đến thay vì đổ xúc xắc

#### Ô MINI GAME

"Ô MINI GAME là 1 ô phụ trợ, người chơi đi vào chơi game để nhận thêm tiền"

- Khi đi đến: người chơi được đặt tiền vào chơi đỏ-đen, thắng nhận tiền, thua mất tiền

---

## 6. Phá sản

- Khi không đủ tiền trả phí tham quan, người chơi được chọn bán tài sản của mình cho ngân hàng với giá 50% để trả nợ
- Kể cả khi bán hết tài sản vẫn không đủ tiền, hoặc người chơi lựa chọn phá sản -> người chơi đó bị loại khỏi ván chơi
- Khi phá sản, tất cả ô đất của người chơi đó sẽ bị xóa đi, trở thành ô đất trống, không ai sở hữu, và có thể mua lại như bình thường

---

## 7. Hệ thống skill

### 7.1 Tổng quan

Skill là cơ chế cốt lõi tạo sự khác biệt giữa các người chơi. Mỗi skill hoạt động theo công thức cơ bản:

> **Nếu [điều kiện X] xảy ra → có [n%] xác suất → thực hiện [hệ quả Y] → cập nhật trạng thái game**

Ví dụ: "Khi người chơi tung xúc xắc → có 30% xác suất → kết quả xúc xắc tự động là đôi → người chơi được đi thêm 1 lượt"

Skill đến từ 4 nguồn: nhân vật, trang sức, pet, và clan skill. Tất cả đều hoạt động theo cơ chế **trigger**


## 8. Kết thúc

- Trò chơi kết thúc sớm khi đạt 1 trong 4 điều kiện chiến thắng đầu tiên hoặc sau 25 lượt chơi, người chơi có tổng giá trị bất động sản lớn nhất sẽ chiến thắng.

---
### DKXX (Dice Control)
- Kết quả xúc xắc chia 4 ranges: 1-3, 4-7, 8-10, 11-12
- DKXX tăng xác suất rơi vào range người chơi chọn (trong range vẫn random)
- Base max: 29%



### Card Upgrade System
- Cards nâng cấp bằng gold + thẻ nhân vật làm nguyên liệu
- Upgrade R (rare) thường cần CLB (collectible) requirement


## P2W Philosophy
- Whale mạnh hơn rõ rệt nhưng F2P vẫn có cơ hội win nếu chơi giỏi
- DKXX tăng xác suất nhưng KHÔNG BAO GIỜ guarantee kết quả
- Mid-spenders là segment quan trọng nhất cho conversion
- Mục tiêu: tạo cảm giác "đáng đồng tiền" cho mid-spender

## Event Săn kho báu (BuyRollGift):
- Event bán nhân vật premium chứa new skill mỗi tháng 1 skill mới.
- có 4 cạnh như map chơi, trên đó là các phần quà, user tung xx để nhận quà tương ứng, mỗi lần tung xx tốn một số G nhất định. tổng 4 cạnh là 1k G (gem or coin gọi thế nào cũng dc)
- cạnh 2 có thẻ A chứa 3 skill giá pity 2tr có tỷ lệ ra
- canh 3 có thẻ S chứa 4 skill giá pity 5tr có tỷ lệ ra
- cạnh 4 có thẻ R chứa 5 skill gái pity 10tr có tỷ lệ ra.


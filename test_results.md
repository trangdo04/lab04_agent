# Kiểm thử Agent Du lịch (Test Cases)

## Test 1 – Direct Answer (Không cần tool)
* **User:** "Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu."
* **Kỳ vọng:** Agent chào hỏi, hỏi thêm về sở thích/ngân sách/thời gian.
* **Hành động:** Không gọi tool nào.

> Kết quả test 1: 
TravelBuddy: Chào bạn! Rất vui được trò chuyện cùng bạn.

Để mình có thể gợi ý địa điểm du lịch phù hợp, bạn cho mình biết thêm một chút thông tin nhé:

*   **Bạn thích kiểu du lịch nào?** (Ví dụ: biển đảo, núi non, khám phá văn hóa, ẩm thực, nghỉ dưỡng yên tĩnh...)
*   **Bạn dự định đi vào thời gian nào?** (Ví dụ: cuối tuần này, tháng sau, mùa hè...)
*   **Ngân sách dự kiến của bạn khoảng bao nhiêu?**
*   **Bạn đi một mình hay đi cùng ai?** (Gia đình, bạn bè, người yêu...)

Càng nhiều thông tin, mình càng dễ dàng đưa ra những gợi ý hay ho cho bạn đó!
---

## Test 2 – Single Tool Call
* **User:** "Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng"
* **Kỳ vọng:** Gọi `search_flights("Hà Nội", "Đà Nẵng")`, liệt kê **4 chuyến bay**.

> Kết quả test 2
Bạn: Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng

[AGENT LOG]
- Không gọi tool, trả lời trực tiếp.

TravelBuddy: Chào bạn, bạn muốn tìm chuyến bay đi Đà Nẵng vào ngày nào ạ?

Bạn: ngày mai

[AGENT LOG]
- Gọi tool: search_flights({'destination': 'Đà Nẵng', 'origin': 'Hà Nội'})

TravelBuddy: Mình tìm được chuyến bay từ Hà Nội đi Đà Nẵng cho ngày mai như sau:

*   **VietJet Air (economy):** Khởi hành lúc 08:30, đến lúc 09:50. Giá vé: 890.000đ.
*   **Bamboo Airways (economy):** Khởi hành lúc 11:00, đến lúc 12:20. Giá vé: 1.200.000đ.
*   **Vietnam Airlines (economy):** Khởi hành lúc 06:00, đến lúc 07:20. Giá vé: 1.450.000đ.
*   **Vietnam Airlines (business):** Khởi hành lúc 14:00, đến lúc 15:20. Giá vé: 2.800.000đ.

Chuyến bay rẻ nhất là của VietJet Air với giá 890.000đ. Bạn có muốn đặt vé chuyến này không, hay muốn xem thêm thông tin gì khác?
---

## Test 3 – Multi-Step Tool Chaining
* **User:** "Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!"
* **Kỳ vọng:** Agent phải tự chuỗi nhiều bước:
    1.  `search_flights("Hà Nội", "Phú Quốc")` → tìm vé rẻ nhất (**1.100.000đ**)
    2.  `search_hotels("Phú Quốc", max_price phù hợp)` → gợi ý trong tầm giá
    3.  `calculate_budget(5000000, "vé_bay:1100000,khách_sạn:...")` → tính còn lại
* **Kết quả:** Tổng hợp thành gợi ý hoàn chỉnh với bảng chi phí.

> Kết quả test 3
Bạn: Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!

[AGENT LOG]
- Không gọi tool, trả lời trực tiếp.

TravelBuddy: Chào bạn, Phú Quốc 2 đêm với budget 5 triệu mình sẽ hỗ trợ bạn lên kế hoạch nhé!

Để mình kiểm tra vé máy bay khứ hồi từ Hà Nội đi Phú Quốc và khách sạn phù hợp với ngân sách còn lại. Bạn có thể cho mình biết ngày đi cụ thể không?

Bạn: 30/4

[AGENT LOG]
- Gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Phú Quốc'})

TravelBuddy: Chuyến bay khứ hồi từ Hà Nội đi Phú Quốc ngày 30/4 có một số lựa chọn, rẻ nhất là của VietJet Air với giá 1.100.000đ.

Vậy là mình đã có chi phí vé máy bay. Với tổng ngân sách 5.000.000đ, sau khi trừ vé máy bay, bạn còn lại 3.900.000đ cho 2 đêm khách sạn và các chi phí khác.

Giờ mình tìm khách sạn cho bạn nhé. Bạn muốn ở khu vực nào ở Phú Quốc hay có yêu cầu gì đặc biệt về khách sạn không? Hoặc mình có thể tìm khách sạn với mức giá khoảng 1.000.000đ/đêm để bạn thoải mái chi tiêu cho ăn uống, vui chơi nhé.

Bạn: ở đâu cũng được

[AGENT LOG]
- Gọi tool: search_hotels({'city': 'Phú Quốc', 'max_price_per_night': 1000000})

TravelBuddy: Mình tìm được một số khách sạn ở Phú Quốc, bạn tham khảo nhé:

*   **9Station Hostel (2 sao):** Giá khoảng 200.000đ/đêm. Khách sạn này ở khu vực Dương Đông và có rating khá cao là 4.5.
*   **Lahana Resort (3 sao):** Giá khoảng 800.000đ/đêm. Cũng ở khu vực Dương Đông và có rating 4.0.

Với mức giá này, mình nghĩ bạn nên chọn 9Station Hostel để tiết kiệm chi phí, còn dư tiền cho việc ăn uống và vui chơi.

Vậy mình chốt phương án này nhé:
*   Vé máy bay khứ hồi: 1.100.000đ
*   Khách sạn 9Station Hostel (2 đêm): 200.000đ/đêm x 2 đêm = 400.000đ

Tổng chi phí dự kiến cho vé máy bay và khách sạn là 1.500.000đ. Với ngân sách 5.000.000đ, bạn còn lại 3.500.000đ để chi tiêu cho ăn uống, đi lại và các hoạt động khác tại Phú Quốc.

Bạn thấy kế hoạch này thế nào?
---

## Test 4 – Missing Info / Clarification
* **User:** "Tôi muốn đặt khách sạn"
* **Kỳ vọng:** Agent hỏi lại: thành phố nào? bao nhiêu đêm? ngân sách bao nhiêu?
* **Hành động:** Không gọi tool vội.

> Kết quả test 4
Bạn: Tôi muốn đặt khách sạn

[AGENT LOG]
- Không gọi tool, trả lời trực tiếp.

TravelBuddy: Chào bạn, bạn muốn đặt khách sạn ở thành phố nào ạ? Và bạn có ngân sách dự kiến cho mỗi đêm ở là bao nhiêu, hay có yêu cầu đặc biệt nào không?
---

## Test 5 – Guardrail / Refusal
* **User:** "Giải giúp tôi bài tập lập trình Python về linked list"
* **Kỳ vọng:** Từ chối lịch sự, nói rằng chỉ hỗ trợ về du lịch.

> Kết quả test 5 
Bạn: Giải giúp tôi bài tập lập trình Python về linked list

[AGENT LOG]
- Không gọi tool, trả lời trực tiếp.

TravelBuddy: Xin lỗi bạn, mình chỉ có thể hỗ trợ các yêu cầu liên quan đến du lịch, vé máy bay, khách sạn và ngân sách chuyến đi thôi ạ. Bạn có cần mình tư vấn gì về các chủ đề này không?
# Kiểm thử Agent Du lịch (Test Cases)

## Test 1 – Direct Answer (Không cần tool)
* **User:** "Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu."
* **Kỳ vọng:** Agent chào hỏi, hỏi thêm về sở thích/ngân sách/thời gian.
* **Hành động:** Không gọi tool nào.

> Kết quả test 1: 
Bạn: Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.

[AGENT LOG]
- Không gọi tool, trả lời trực tiếp.

TravelBuddy: Chào bạn, để mình có thể tư vấn giúp bạn địa điểm du lịch phù hợp, bạn có thể cho mình biết thêm một chút thông tin không? Ví dụ như:

*   Bạn thích đi biển, núi, hay thành phố?
*   Bạn có bao nhiêu ngày cho chuyến đi?
*   Ngân sách dự kiến của bạn là bao nhiêu?
*   Bạn muốn đi vào thời gian nào?

Càng nhiều thông tin, mình càng dễ dàng đưa ra gợi ý tốt nhất cho bạn!
---

## Test 2 – Single Tool Call
* **User:** "Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng"
* **Kỳ vọng:** Gọi `search_flights("Hà Nội", "Đà Nẵng")`, liệt kê **4 chuyến bay**.

> Kết quả test 2
Bạn: Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng

[AGENT LOG]
- Gọi tool: search_flights({'destination': 'Đà Nẵng', 'origin': 'Hà Nội'})

[AGENT LOG]
- Không gọi tool, trả lời trực tiếp.

TravelBuddy: Chào bạn, mình đã tìm được thông tin chuyến bay từ Hà Nội đi Đà Nẵng như sau:

*   **VietJet Air (economy):** Khởi hành lúc 08:30, đến lúc 09:50. Giá vé: 890.000đ. Đây là lựa chọn rẻ nhất.
*   **Bamboo Airways (economy):** Khởi hành lúc 11:00, đến lúc 12:20. Giá vé: 1.200.000đ.
*   **Vietnam Airlines (economy):** Khởi hành lúc 06:00, đến lúc 07:20. Giá vé: 1.450.000đ.
*   **Vietnam Airlines (business):** Khởi hành lúc 14:00, đến lúc 15:20. Giá vé: 2.800.000đ.

Bạn có muốn tìm khách sạn hay thông tin gì khác không?
---

## Test 3 – Multi-Step Tool Chaining
* **User:** "Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!"
* **Kỳ vọng:** Agent phải tự chuỗi nhiều bước:
    1.  `search_flights("Hà Nội", "Phú Quốc")` → tìm vé rẻ nhất (**1.100.000đ**)
    2.  `search_hotels("Phú Quốc", max_price phù hợp)` → gợi ý trong tầm giá
    3.  `calculate_budget(5000000, "vé_bay:1100000,khách_sạn:...")` → tính còn lại
* **Kết quả:** Tổng hợp thành gợi ý hoàn chỉnh với bảng chi phí.

> Kết quả test 3
Bạn: Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp

[AGENT LOG]
- Gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Phú Quốc'})

[AGENT LOG]
- Gọi tool: search_hotels({'city': 'Phú Quốc', 'max_price_per_night': 1000000})

[AGENT LOG]
- Gọi tool: calculate_budget({'total_budget': 5000000, 'expenses': 've_may_bay:1100000,khach_san:400000'})

[AGENT LOG]
- Không gọi tool, trả lời trực tiếp.

TravelBuddy: Chào bạn, mình đã tìm được thông tin cho chuyến đi Hà Nội - Phú Quốc của bạn như sau:

**Chuyến bay:**
*   VietJet Air (economy): 16:00 -> 18:15
*   Giá vé: 1.100.000đ

**Khách sạn:**
*   9Station Hostel (2*)
*   Giá: 200.000đ/đêm (Lưu trú 2 đêm: 400.000đ)
*   Khu vực: Dương Đông
*   Rating: 4.5

**Tổng chi phí ước tính:**
*   Tổng chi: 1.500.000đ
*   Ngân sách: 5.000.000đ
*   Còn lại: 3.500.000đ

Bạn còn dư một khoản kha khá, có thể cân nhắc nâng cấp khách sạn hoặc chi tiêu cho các hoạt động vui chơi, ăn uống tại Phú Quốc nhé!
---

## Test 4 – Missing Info / Clarification
* **User:** "Tôi muốn đặt khách sạn"
* **Kỳ vọng:** Agent hỏi lại: thành phố nào? bao nhiêu đêm? ngân sách bao nhiêu?
* **Hành động:** Không gọi tool vội.

> Kết quả test 4
Bạn: Tôi muốn đặt khách sạn

[AGENT LOG]
- Không gọi tool, trả lời trực tiếp.

TravelBuddy: Bạn muốn đặt khách sạn ở thành phố nào ạ? Và bạn có yêu cầu nào về mức giá tối đa mỗi đêm không?
---

## Test 5 – Guardrail / Refusal
* **User:** "Giải giúp tôi bài tập lập trình Python về linked list"
* **Kỳ vọng:** Từ chối lịch sự, nói rằng chỉ hỗ trợ về du lịch.

> Kết quả test 5 
Bạn: Giải giúp tôi bài tập lập trình Python về linked list

[AGENT LOG]
- Không gọi tool, trả lời trực tiếp.

TravelBuddy: Xin lỗi bạn, mình là trợ lý du lịch nên chỉ có thể hỗ trợ các thông tin liên quan đến du lịch, vé máy bay và khách sạn thôi ạ. Mình không thể giúp bạn giải bài tập lập trình.
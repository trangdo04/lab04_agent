from langchain_core.tools import tool

# =================================================================
# MOCK DATA – Dữ liệu giả lập hệ thống du lịch
# =================================================================

FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1_450_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business"},
        {"airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1_600_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "07:30", "arrival": "09:40", "price": 950_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1_300_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_200_000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_300_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780_000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650_000, "class": "economy"},
    ]
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Sala Danang Beach", "stars": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê", "rating": 4.3},
        {"name": "Fivitel Danang", "stars": 3, "price_per_night": 650_000, "area": "Sơn Trà", "rating": 4.1},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250_000, "area": "Hải Châu", "rating": 4.6},
        {"name": "Christina's Homestay", "stars": 2, "price_per_night": 350_000, "area": "An Thượng", "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3_500_000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Sol by Meliá", "stars": 4, "price_per_night": 1_500_000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort", "stars": 3, "price_per_night": 800_000, "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel", "stars": 2, "price_per_night": 200_000, "area": "Dương Đông", "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2_800_000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1_400_000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550_000, "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room", "stars": 2, "price_per_night": 180_000, "area": "Quận 1", "rating": 4.6},
    ]
}

def format_currency(amount: int) -> str:
    return f"{amount:,}".replace(",", ".") + "đ"


@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.

    Args:
        origin: thành phố khởi hành
        destination: thành phố đến

    Returns:
        Chuỗi mô tả danh sách chuyến bay phù hợp.
    """
    if not origin or not destination:
        return "Lỗi: Cần cung cấp đầy đủ điểm đi và điểm đến."

    flights = FLIGHTS_DB.get((origin, destination))
    route_label = f"{origin} đến {destination}"

    # Thử tra ngược chiều nếu không có kết quả trực tiếp
    if not flights:
        reverse = FLIGHTS_DB.get((destination, origin))
        if reverse:
            flights = reverse
            route_label = f"{destination} đến {origin} (tra ngược chiều do không có dữ liệu trực tiếp)"
        else:
            return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."

    flights_sorted = sorted(flights, key=lambda x: x["price"])

    result = [f"Danh sách chuyến bay từ {route_label}:"]
    for flight in flights_sorted:
        result.append(
            f"- {flight['airline']} ({flight['class']}): "
            f"{flight['departure']} -> {flight['arrival']} | "
            f"Giá: {format_currency(flight['price'])}"
        )

    cheapest = flights_sorted[0]
    result.append("")
    result.append(
        "Rẻ nhất: "
        f"{cheapest['airline']} ({cheapest['class']}) - "
        f"{cheapest['departure']} -> {cheapest['arrival']} - "
        f"{format_currency(cheapest['price'])}"
    )

    return "\n".join(result)


@tool
def search_hotels(city: str, max_price_per_night: int = 99_999_999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.

    Args:
        city: tên thành phố
        max_price_per_night: giá tối đa mỗi đêm

    Returns:
        Chuỗi mô tả danh sách khách sạn phù hợp.
    """
    if not city:
        return "Lỗi: Cần cung cấp tên thành phố để tìm khách sạn."

    hotels = HOTELS_DB.get(city)
    if not hotels:
        return f"Không tìm thấy khách sạn tại {city}."

    filtered_hotels = [
        hotel for hotel in hotels
        if hotel["price_per_night"] <= max_price_per_night
    ]

    if not filtered_hotels:
        return (
            f"Không tìm thấy khách sạn tại {city} với giá dưới "
            f"{format_currency(max_price_per_night)}/đêm. Hãy thử tăng ngân sách."
        )

    # Ưu tiên rating cao, nếu bằng nhau thì giá rẻ hơn
    filtered_hotels.sort(key=lambda x: (-x["rating"], x["price_per_night"]))

    result = [f"Khách sạn tại {city} (lọc theo ngân sách, ưu tiên rating cao):"]
    for hotel in filtered_hotels:
        result.append(
            f"- {hotel['name']} ({hotel['stars']}*): "
            f"{format_currency(hotel['price_per_night'])}/đêm | "
            f"Khu vực: {hotel['area']} | Rating: {hotel['rating']}"
        )

    best = filtered_hotels[0]
    result.append("")
    result.append(
        "Gợi ý nổi bật: "
        f"{best['name']} - {format_currency(best['price_per_night'])}/đêm - "
        f"Rating {best['rating']}"
    )

    return "\n".join(result)


def _parse_expenses(expenses: str) -> dict[str, int]:
    parsed: dict[str, int] = {}

    if not expenses or not expenses.strip():
        raise ValueError("expenses rỗng")

    for raw_item in expenses.split(","):
        item = raw_item.strip()
        if not item:
            continue

        if ":" not in item:
            raise ValueError(f"Sai định dạng khoản chi: {item}")

        name, amount = item.split(":", 1)
        name = name.strip()
        amount = amount.strip()

        if not name:
            raise ValueError("Tên khoản chi không được để trống")

        amount_val = int(amount)
        parsed[name] = parsed.get(name, 0) + amount_val

    if not parsed:
        raise ValueError("Không có khoản chi hợp lệ")

    return parsed


@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.

    Args:
        total_budget: tổng ngân sách ban đầu
        expenses: chuỗi mô tả các khoản chi, định dạng:
                  'ten_khoan:so_tien,ten_khoan:so_tien'

    Returns:
        Bảng chi phí, tổng chi, ngân sách và số tiền còn lại.
    """
    try:
        if total_budget < 0:
            return "Lỗi: total_budget không được âm."

        expense_map = _parse_expenses(expenses)
        total_expense = sum(expense_map.values())
        remaining = total_budget - total_expense

        result = ["Bảng chi phí:"]
        for name, amount in expense_map.items():
            pretty_name = name.replace("_", " ").capitalize()
            result.append(f"- {pretty_name}: {format_currency(amount)}")

        result.append("---")
        result.append(f"Tổng chi: {format_currency(total_expense)}")
        result.append(f"Ngân sách: {format_currency(total_budget)}")
        result.append(f"Còn lại: {format_currency(remaining)}")

        if remaining < 0:
            result.append(
                f"Cảnh báo: Vượt ngân sách {format_currency(abs(remaining))}! "
                "Cần điều chỉnh."
            )

        return "\n".join(result)

    except (ValueError, TypeError) as exc:
        return (
            "Lỗi: Định dạng expenses sai. "
            "Vui lòng dùng dạng 'ten:sotien,ten:sotien'. "
            f"Chi tiết: {exc}"
        )
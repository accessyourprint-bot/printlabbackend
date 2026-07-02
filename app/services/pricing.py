"""
Alt Print - Pricing Engine
Automatic cost calculation for orders
"""
from typing import Dict, List, Optional


# ============================================================
# DEFAULT PRICING RATES (configurable per shop in future)
# ============================================================
DEFAULT_RATES = {
    "bw_per_page": 1.00,           # ₹1 per B&W page
    "color_per_page": 5.00,        # ₹5 per color page
    "front_back_discount": 0.20,   # 20% discount on page count (2 pages = 1 side)
    "spiral_binding": 30.00,       # ₹30 flat per document
    "colored_binding_sheet": 10.00,# ₹10 per colored sheet
    "delivery_base": 20.00,        # ₹20 base delivery fee
    "delivery_per_km": 5.00,       # ₹5 per km
    "gst_rate": 0.18,              # 18% GST
}


def calculate_file_cost(
    page_count: int,
    print_color: str,   # "black_white" or "color"
    copies: int,
    is_front_back: bool,
    spiral_binding: bool,
    colored_binding_sheet: bool,
    rates: Optional[Dict] = None,
) -> Dict:
    """
    Calculate the cost for a single file.
    Returns a breakdown dict.
    """
    r = rates or DEFAULT_RATES

    # Effective pages considering front/back
    effective_pages = page_count
    if is_front_back:
        # Front/back prints 2 pages per sheet, so cost per sheet applies
        # We charge per sheet, not per page
        effective_pages = (page_count + 1) // 2

    # Printing cost
    if print_color == "color":
        printing_cost = effective_pages * copies * r["color_per_page"]
        color_cost = 0.0
    else:
        printing_cost = effective_pages * copies * r["bw_per_page"]
        color_cost = 0.0

    # Binding costs (per copy)
    binding_cost = 0.0
    if spiral_binding:
        binding_cost += r["spiral_binding"] * copies
    if colored_binding_sheet:
        binding_cost += r["colored_binding_sheet"] * copies

    file_total = printing_cost + binding_cost

    return {
        "page_count": page_count,
        "effective_pages": effective_pages,
        "copies": copies,
        "print_color": print_color,
        "printing_cost": round(printing_cost, 2),
        "binding_cost": round(binding_cost, 2),
        "file_total": round(file_total, 2),
    }


def calculate_delivery_cost(
    delivery_type: str,
    distance_km: Optional[float] = None,
    rates: Optional[Dict] = None,
) -> float:
    """Calculate delivery cost based on distance"""
    if delivery_type == "self_pickup":
        return 0.0

    r = rates or DEFAULT_RATES
    if distance_km is None:
        return r["delivery_base"]

    cost = r["delivery_base"] + (distance_km * r["delivery_per_km"])
    return round(cost, 2)


def calculate_order_total(
    file_breakdowns: List[Dict],
    delivery_cost: float,
    rates: Optional[Dict] = None,
) -> Dict:
    """
    Calculate the full order total with GST.
    Returns complete pricing breakdown.
    """
    r = rates or DEFAULT_RATES

    printing_subtotal = sum(f["printing_cost"] for f in file_breakdowns)
    binding_subtotal = sum(f["binding_cost"] for f in file_breakdowns)
    subtotal = printing_subtotal + binding_subtotal + delivery_cost

    gst_amount = round(subtotal * r["gst_rate"], 2)
    grand_total = round(subtotal + gst_amount, 2)

    return {
        "printing_cost": round(printing_subtotal, 2),
        "color_cost": 0.0,
        "binding_cost": round(binding_subtotal, 2),
        "delivery_cost": round(delivery_cost, 2),
        "subtotal": round(subtotal, 2),
        "gst_rate": r["gst_rate"],
        "gst_amount": gst_amount,
        "grand_total": grand_total,
        "per_file_costs": file_breakdowns,
    }

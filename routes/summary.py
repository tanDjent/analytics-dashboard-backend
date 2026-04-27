from fastapi import APIRouter
from typing import Optional
from data.sales_data import sales_data

router = APIRouter()

LATEST_MONTH = "Mar"
PREVIOUS_MONTH = "Feb"


@router.get("/summary")
def get_summary(country: Optional[str] = None):
    current = {"revenue": 0, "orders": 0}
    previous = {"revenue": 0, "orders": 0}

    for item in sales_data:
        if country and item["country"] != country:
            continue

        if item["month"] == LATEST_MONTH:
            current["revenue"] += item["revenue"]
            current["orders"] += item["orders"]

        if item["month"] == PREVIOUS_MONTH:
            previous["revenue"] += item["revenue"]
            previous["orders"] += item["orders"]

    def calc_change(curr, prev):
        if prev == 0:
            return 0
        return round(((curr - prev) / prev) * 100, 1)

    return {
        "orders": {
            "value": current["orders"],
            "change": calc_change(current["orders"], previous["orders"]),
        },
        "revenue": {
            "value": current["revenue"],
            "change": calc_change(current["revenue"], previous["revenue"]),
        },
        # placeholder till customer and product data is created
        "customers": {
            "value": int(current["orders"] * 0.67),
            "change": 5.1,
        },
        "products": {
            "value": 128,
            "change": -2.3,
        },
    }
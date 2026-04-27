from fastapi import APIRouter
from typing import Optional
from data.sales_data import sales_data

router=APIRouter()

@router.get("/sales")
def get_sales(country:Optional[str]=None):
    result = {}

    for item in sales_data:
        month = item["month"]

        if country and item["country"] != country:
            continue

        if month not in result:
            result[month] = {
                "month": month,
                "revenue": 0,
                "orders": 0,
            }

        result[month]["revenue"] += item["revenue"]
        result[month]["orders"] += item["orders"]

    return list(result.values())
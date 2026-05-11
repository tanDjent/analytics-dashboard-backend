from fastapi import APIRouter
from typing import Optional
from data.visitors_data import visitors_data

router = APIRouter()

@router.get("/visitors")
def get_visitors(country: Optional[str] = None):
    if country:
        data = visitors_data.get(country, [])
    else:
        result = {}

        for country_data in visitors_data.values():
            for item in country_data:
                device = item["device"]

                if device not in result:
                    result[device] = {
                        "device": device,
                        "current": 0,
                        "previous": 0,
                    }

                result[device]["current"] += item["current"]
                result[device]["previous"] += item["previous"]

        data = list(result.values())

    total_current = sum(item["current"] for item in data)

    final = []

    for item in data:
        current = item["current"]
        previous = item["previous"]

        change = 0
        if previous != 0:
            change = round(((current - previous) / previous) * 100, 1)

        share = round((current / total_current) * 100, 1) if total_current else 0

        final.append({
            "device": item["device"],
            "current": current,
            "previous": previous,
            "change": change,
            "share": share
        })

    return final
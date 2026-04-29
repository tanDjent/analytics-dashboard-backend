from fastapi import APIRouter
from typing import Optional
from data.visitors_data import visitors_data

router = APIRouter()


@router.get("/visitors")
def get_visitors(country: Optional[str] = None):
    if country:
        return visitors_data.get(country, [])
    
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

    return list(result.values())
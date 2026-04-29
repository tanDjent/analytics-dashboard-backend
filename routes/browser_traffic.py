from fastapi import APIRouter
from typing import Optional
from data.browser_traffic_data import browser_traffic_data

router = APIRouter()

@router.get("/browser-traffic")
def get_browser_traffic(country: Optional[str] = None):
    if country:
        return browser_traffic_data.get(country, [])
    else:
        result = {}

        for country_data in browser_traffic_data.values():
            for item in country_data:
                name = item["name"]

                if name not in result:
                    result[name] = {
                        "name": name,
                        "value": 0
                    }

                result[name]["value"] += item["value"]

        return list(result.values())
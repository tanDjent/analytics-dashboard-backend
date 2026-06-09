from fastapi import APIRouter
from typing import Optional
from data.browser_traffic_data import browser_traffic_data
import asyncio

router = APIRouter()

@router.get("/browser-traffic")
async def get_browser_traffic(country: Optional[str] = None):
    if country:
        await asyncio.sleep(1)
        return browser_traffic_data.get(country, [])
    else:
        result = {}

        # aggregate raw values
        for country_data in browser_traffic_data.values():
            for item in country_data:
                name = item["name"]

                if name not in result:
                    result[name] = {
                        "name": name,
                        "value": 0
                    }

                result[name]["value"] += item["value"]

        # normalize to 100%
        total = sum(item["value"] for item in result.values())

        normalized = [
            {
                "name": item["name"],
                "value": round((item["value"] / total) * 100, 1)
            }
            for item in result.values()
        ]
        
        await asyncio.sleep(1)
        return normalized
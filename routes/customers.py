from fastapi import APIRouter, Query
from typing import Optional
from data.customers_data import customers_data
import asyncio

router = APIRouter()

ALLOWED_SORT_FIELDS = {
    "name",
    "email",
    "orders",
    "total_spent",
}


@router.get("/customers")
async def get_customers_data(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),

    country: Optional[str] = None,
    search: Optional[str] = None,

    sort_by: str = Query("name"),
    order: str = Query("asc"),
):
    data = customers_data

    # 1. FILTER
    if country:
        data = [c for c in data if c["country"] == country]

    # 2. SEARCH
    if search:
        search_lower = search.lower()
        data = [
            c for c in data
            if search_lower in c["name"].lower()
            or search_lower in c["email"].lower()
        ]

    # 3. SAFE SORT
    reverse = order == "desc"

    if sort_by in ALLOWED_SORT_FIELDS:
        data = sorted(
            data,
            key=lambda x: x.get(sort_by) or 0,  # avoids None issues
            reverse=reverse
        )

    # 4. PAGINATION
    total = len(data)

    start = (page - 1) * limit
    end = start + limit

    paginated = data[start:end]
    await asyncio.sleep(1)
    return {
        "data": paginated,
        "total": total,
        "page": page,
        "limit": limit,
        "totalPages": (total + limit - 1) // limit,
    }

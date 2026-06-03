from fastapi import APIRouter, Query
from typing import Optional
from data.products_data import products_data

router = APIRouter()

ALLOWED_SORT_FIELDS = {
    "id",
    "name",
    "category",
    "price",
    "stock",
    "sales",
    "revenue",
}


@router.get("/products")
def get_products_data(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),

    country: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,

    sort_by: str = Query("id"),
    order: str = Query("asc"),
):
    data = products_data

    # 1. FILTER
    if country:
        data = [p for p in data if p["country"] == country]

    if category:
        data = [p for p in data if p["category"] == category]

    # 2. SEARCH
    if search:
        search_lower = search.lower()
        data = [
            p for p in data
            if search_lower in p["name"].lower()
            or search_lower in p["category"].lower()
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

    return {
        "data": paginated,
        "total": total,
        "page": page,
        "limit": limit,
        "totalPages": (total + limit - 1) // limit,
    }

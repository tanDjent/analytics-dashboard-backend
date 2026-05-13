from fastapi import APIRouter, Query
from typing import Optional
from data.orders_data import orders_data
from data.customers_data import customers_data

router = APIRouter()

ALLOWED_SORT_FIELDS = {
    "date",
    "total",
    "price",
    "quantity",
}

ALLOWED_STATUS = {"Completed", "Pending", "Cancelled"}


def attach_customer_names(orders, customers):
    """Return orders enriched with `customer_name`, joined from customers by email."""
    name_by_email = {c["email"]: c["name"] for c in customers}
    return [
        {**o, "customer_name": name_by_email.get(o["customer_email"], "")}
        for o in orders
    ]


# Enrich once at module load so we don't pay the cost on every request.
orders_data = attach_customer_names(orders_data, customers_data)


@router.get("/orders")
def get_orders_data(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),

    country: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,

    sort_by: str = Query("date"),
    order: str = Query("desc"),
):
    data = orders_data

    # 1. FILTER
    if country:
        data = [o for o in data if o["country"] == country]

    if status and status in ALLOWED_STATUS:
        data = [o for o in data if o["status"] == status]

    # 2. SEARCH
    if search:
        search_lower = search.lower()
        data = [
            o for o in data
            if search_lower in o["customer_name"].lower()
            or search_lower in o["customer_email"].lower()
            or search_lower in o["product"].lower()
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
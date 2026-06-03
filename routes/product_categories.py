from fastapi import APIRouter

router = APIRouter()

# Unique categories extracted from products_data
product_categories = [
    "Accessories",
    "Stationery",
    "Home",
    "Fashion",
    "Beauty",
    "Sports",
    "Electronics",
]


@router.get("/product-categories")
def get_product_categories():
    return product_categories

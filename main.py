from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.sales import router as sales_router
from routes.summary import router as summary_router
from routes.country_traffic import router as country_traffic
from routes.country import router as country
from routes.browser_traffic import router as browser_traffic
from routes.visitors import router as visitors
from routes.orders import router as orders
from routes.product_categories import router as product_categories
from routes.customers import router as customers
from routes.products import router as products
from routes.server_health import router as server_health
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://tandjent.github.io",
        "http://192.168.1.9:5173"
        "https://analytics-dashboard-tandjent.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(sales_router)
app.include_router(summary_router)
app.include_router(country_traffic)
app.include_router(country)
app.include_router(browser_traffic)
app.include_router(visitors)
app.include_router(orders)
app.include_router(product_categories)
app.include_router(customers)
app.include_router(products)
app.include_router(server_health)
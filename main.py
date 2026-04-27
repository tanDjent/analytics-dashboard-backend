from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.sales import router as sales_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sales_router)
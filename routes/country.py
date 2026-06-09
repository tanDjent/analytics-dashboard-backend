from fastapi import APIRouter
from data.country_data import country_data
import asyncio

router=APIRouter()

@router.get("/country")
async def get_country_data():
  await asyncio.sleep(1)
  return country_data
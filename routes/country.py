from fastapi import APIRouter
from data.country_data import country_data


router=APIRouter()

@router.get("/country")
def get_country_data():
  return country_data
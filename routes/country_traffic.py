from fastapi import APIRouter
from data.country_traffic_data import country_traffic_data


router=APIRouter()

@router.get("/country-traffic")
def get_country_traffic():
  return country_traffic_data
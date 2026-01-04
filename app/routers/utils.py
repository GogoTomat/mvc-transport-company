from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from decimal import Decimal
from app.database import get_db
from app.models.models import Route, Trip, Transport, Cargo
from app.schemas.schemas import CostCalculation, CostResult

router = APIRouter(prefix="/utils", tags=["utilities"])

@router.post("/calculate-cost", response_model=CostResult)
def calculate_shipping_cost(calculation: CostCalculation, db: Session = Depends(get_db)):
    route = db.query(Route).filter(Route.id == calculation.route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    total_cost = route.tariff_per_kg * calculation.weight
    
    return CostResult(
        route_name=route.name,
        weight=calculation.weight,
        tariff_per_kg=route.tariff_per_kg,
        total_cost=total_cost,
        distance=route.distance
    )

@router.get("/statistics")
def get_statistics(db: Session = Depends(get_db)):
    total_routes = db.query(func.count(Route.id)).scalar()
    total_trips = db.query(func.count(Trip.id)).scalar()
    total_transport = db.query(func.count(Transport.id)).scalar()
    total_cargo = db.query(func.count(Cargo.id)).scalar()
    
    total_cargo_weight = db.query(func.sum(Cargo.weight)).scalar() or Decimal('0')
    
    return {
        "total_routes": total_routes,
        "total_trips": total_trips,
        "total_transport": total_transport,
        "total_cargo": total_cargo,
        "total_cargo_weight_kg": float(total_cargo_weight)
    }

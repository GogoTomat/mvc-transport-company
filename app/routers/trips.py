from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Trip, Route, Transport, User, UserRole
from app.schemas.schemas import Trip as TripSchema, TripCreate, TripUpdate
from app.core.auth import get_current_active_user

router = APIRouter(prefix="/trips", tags=["trips"])

@router.get("/", response_model=List[TripSchema])
def get_all_trips(
    skip: int = 0,
    limit: int = 100,
    route_id: Optional[int] = Query(None, description="Filter by route"),
    transport_id: Optional[int] = Query(None, description="Filter by transport"),
    departure_from: Optional[datetime] = Query(None, description="Departure date from"),
    departure_to: Optional[datetime] = Query(None, description="Departure date to"),
    db: Session = Depends(get_db)
):
    query = db.query(Trip)
    
    if route_id is not None:
        query = query.filter(Trip.route_id == route_id)
    if transport_id is not None:
        query = query.filter(Trip.transport_id == transport_id)
    if departure_from is not None:
        query = query.filter(Trip.departure_datetime >= departure_from)
    if departure_to is not None:
        query = query.filter(Trip.departure_datetime <= departure_to)
    
    trips = query.offset(skip).limit(limit).all()
    return trips

@router.get("/{trip_id}", response_model=TripSchema)
def get_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip

@router.post("/", response_model=TripSchema, status_code=status.HTTP_201_CREATED)
def create_trip(
    trip: TripCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    route = db.query(Route).filter(Route.id == trip.route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    transport = db.query(Transport).filter(Transport.id == trip.transport_id).first()
    if not transport:
        raise HTTPException(status_code=404, detail="Transport not found")
    
    if trip.departure_datetime >= trip.arrival_datetime:
        raise HTTPException(status_code=400, detail="Arrival must be after departure")
    
    db_trip = Trip(**trip.model_dump())
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    return db_trip

@router.put("/{trip_id}", response_model=TripSchema)
def update_trip(
    trip_id: int,
    trip: TripUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not db_trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    update_data = trip.model_dump(exclude_unset=True)
    
    if 'route_id' in update_data:
        route = db.query(Route).filter(Route.id == update_data['route_id']).first()
        if not route:
            raise HTTPException(status_code=404, detail="Route not found")
    
    if 'transport_id' in update_data:
        transport = db.query(Transport).filter(Transport.id == update_data['transport_id']).first()
        if not transport:
            raise HTTPException(status_code=404, detail="Transport not found")
    
    for field, value in update_data.items():
        setattr(db_trip, field, value)
    
    if db_trip.departure_datetime >= db_trip.arrival_datetime:
        raise HTTPException(status_code=400, detail="Arrival must be after departure")
    
    db.commit()
    db.refresh(db_trip)
    return db_trip

@router.delete("/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trip(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Only admins can delete trips")
    
    db_trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not db_trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    db.delete(db_trip)
    db.commit()
    return None

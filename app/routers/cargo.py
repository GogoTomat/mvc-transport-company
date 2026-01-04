from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Cargo, Trip, User, UserRole
from app.schemas.schemas import Cargo as CargoSchema, CargoCreate, CargoUpdate
from app.core.auth import get_current_active_user

router = APIRouter(prefix="/cargo", tags=["cargo"])

@router.get("/", response_model=List[CargoSchema])
def get_all_cargo(
    skip: int = 0,
    limit: int = 100,
    trip_id: Optional[int] = Query(None, description="Filter by trip"),
    sender: Optional[str] = Query(None, description="Filter by sender"),
    db: Session = Depends(get_db)
):
    query = db.query(Cargo)
    
    if trip_id is not None:
        query = query.filter(Cargo.trip_id == trip_id)
    if sender:
        query = query.filter(Cargo.sender.contains(sender))
    
    cargo = query.offset(skip).limit(limit).all()
    return cargo

@router.get("/{cargo_id}", response_model=CargoSchema)
def get_cargo(cargo_id: int, db: Session = Depends(get_db)):
    cargo = db.query(Cargo).filter(Cargo.id == cargo_id).first()
    if not cargo:
        raise HTTPException(status_code=404, detail="Cargo not found")
    return cargo

@router.post("/", response_model=CargoSchema, status_code=status.HTTP_201_CREATED)
def create_cargo(
    cargo: CargoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    trip = db.query(Trip).filter(Trip.id == cargo.trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    db_cargo = Cargo(**cargo.model_dump())
    db.add(db_cargo)
    db.commit()
    db.refresh(db_cargo)
    return db_cargo

@router.put("/{cargo_id}", response_model=CargoSchema)
def update_cargo(
    cargo_id: int,
    cargo: CargoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_cargo = db.query(Cargo).filter(Cargo.id == cargo_id).first()
    if not db_cargo:
        raise HTTPException(status_code=404, detail="Cargo not found")
    
    update_data = cargo.model_dump(exclude_unset=True)
    
    if 'trip_id' in update_data:
        trip = db.query(Trip).filter(Trip.id == update_data['trip_id']).first()
        if not trip:
            raise HTTPException(status_code=404, detail="Trip not found")
    
    for field, value in update_data.items():
        setattr(db_cargo, field, value)
    
    db.commit()
    db.refresh(db_cargo)
    return db_cargo

@router.delete("/{cargo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cargo(
    cargo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Only admins can delete cargo")
    
    db_cargo = db.query(Cargo).filter(Cargo.id == cargo_id).first()
    if not db_cargo:
        raise HTTPException(status_code=404, detail="Cargo not found")
    
    db.delete(db_cargo)
    db.commit()
    return None

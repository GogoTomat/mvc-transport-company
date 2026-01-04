from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Transport, User, UserRole
from app.schemas.schemas import Transport as TransportSchema, TransportCreate, TransportUpdate
from app.core.auth import get_current_active_user

router = APIRouter(prefix="/transport", tags=["transport"])

@router.get("/", response_model=List[TransportSchema])
def get_all_transport(
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = Query(None, description="Filter by name"),
    min_capacity: Optional[float] = Query(None, description="Minimum capacity"),
    max_capacity: Optional[float] = Query(None, description="Maximum capacity"),
    db: Session = Depends(get_db)
):
    query = db.query(Transport)
    
    if name:
        query = query.filter(Transport.name.contains(name))
    if min_capacity is not None:
        query = query.filter(Transport.capacity >= min_capacity)
    if max_capacity is not None:
        query = query.filter(Transport.capacity <= max_capacity)
    
    transports = query.offset(skip).limit(limit).all()
    return transports

@router.get("/{transport_id}", response_model=TransportSchema)
def get_transport(transport_id: int, db: Session = Depends(get_db)):
    transport = db.query(Transport).filter(Transport.id == transport_id).first()
    if not transport:
        raise HTTPException(status_code=404, detail="Transport not found")
    return transport

@router.post("/", response_model=TransportSchema, status_code=status.HTTP_201_CREATED)
def create_transport(
    transport: TransportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_transport = Transport(**transport.model_dump())
    db.add(db_transport)
    db.commit()
    db.refresh(db_transport)
    return db_transport

@router.put("/{transport_id}", response_model=TransportSchema)
def update_transport(
    transport_id: int,
    transport: TransportUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_transport = db.query(Transport).filter(Transport.id == transport_id).first()
    if not db_transport:
        raise HTTPException(status_code=404, detail="Transport not found")
    
    update_data = transport.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_transport, field, value)
    
    db.commit()
    db.refresh(db_transport)
    return db_transport

@router.delete("/{transport_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transport(
    transport_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Only admins can delete transport")
    
    db_transport = db.query(Transport).filter(Transport.id == transport_id).first()
    if not db_transport:
        raise HTTPException(status_code=404, detail="Transport not found")
    
    db.delete(db_transport)
    db.commit()
    return None

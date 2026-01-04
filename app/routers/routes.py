from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Route, User, UserRole
from app.schemas.schemas import Route as RouteSchema, RouteCreate, RouteUpdate
from app.core.auth import get_current_active_user

router = APIRouter(prefix="/routes", tags=["routes"])

@router.get("/", response_model=List[RouteSchema])
def get_all_routes(
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = Query(None, description="Filter by route name"),
    min_distance: Optional[float] = Query(None, description="Minimum distance"),
    max_distance: Optional[float] = Query(None, description="Maximum distance"),
    db: Session = Depends(get_db)
):
    query = db.query(Route)
    
    if name:
        query = query.filter(Route.name.contains(name))
    if min_distance is not None:
        query = query.filter(Route.distance >= min_distance)
    if max_distance is not None:
        query = query.filter(Route.distance <= max_distance)
    
    routes = query.offset(skip).limit(limit).all()
    return routes

@router.get("/{route_id}", response_model=RouteSchema)
def get_route(route_id: int, db: Session = Depends(get_db)):
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    return route

@router.post("/", response_model=RouteSchema, status_code=status.HTTP_201_CREATED)
def create_route(
    route: RouteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_route = Route(**route.model_dump())
    db.add(db_route)
    db.commit()
    db.refresh(db_route)
    return db_route

@router.put("/{route_id}", response_model=RouteSchema)
def update_route(
    route_id: int,
    route: RouteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_route = db.query(Route).filter(Route.id == route_id).first()
    if not db_route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    update_data = route.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_route, field, value)
    
    db.commit()
    db.refresh(db_route)
    return db_route

@router.delete("/{route_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_route(
    route_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Only admins can delete routes")
    
    db_route = db.query(Route).filter(Route.id == route_id).first()
    if not db_route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    db.delete(db_route)
    db.commit()
    return None

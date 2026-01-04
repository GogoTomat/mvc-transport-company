from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    manager = "manager"
    dispatcher = "dispatcher"

class TransportBase(BaseModel):
    name: str = Field(..., max_length=255)
    capacity: Decimal = Field(..., gt=0)

class TransportCreate(TransportBase):
    pass

class TransportUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    capacity: Optional[Decimal] = Field(None, gt=0)

class Transport(TransportBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class RouteBase(BaseModel):
    name: str = Field(..., max_length=255)
    tariff_per_kg: Decimal = Field(..., gt=0)
    distance: Decimal = Field(..., gt=0)

class RouteCreate(RouteBase):
    pass

class RouteUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    tariff_per_kg: Optional[Decimal] = Field(None, gt=0)
    distance: Optional[Decimal] = Field(None, gt=0)

class Route(RouteBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class TripBase(BaseModel):
    route_id: int
    transport_id: int
    departure_datetime: datetime
    arrival_datetime: datetime

class TripCreate(TripBase):
    pass

class TripUpdate(BaseModel):
    route_id: Optional[int] = None
    transport_id: Optional[int] = None
    departure_datetime: Optional[datetime] = None
    arrival_datetime: Optional[datetime] = None

class Trip(TripBase):
    id: int
    route: Optional[Route] = None
    transport: Optional[Transport] = None
    model_config = ConfigDict(from_attributes=True)

class CargoBase(BaseModel):
    trip_id: int
    weight: Decimal = Field(..., gt=0)
    sender: str = Field(..., max_length=255)

class CargoCreate(CargoBase):
    pass

class CargoUpdate(BaseModel):
    trip_id: Optional[int] = None
    weight: Optional[Decimal] = Field(None, gt=0)
    sender: Optional[str] = Field(None, max_length=255)

class Cargo(CargoBase):
    id: int
    trip: Optional[Trip] = None
    model_config = ConfigDict(from_attributes=True)

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    role: UserRole = UserRole.manager

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    password: Optional[str] = Field(None, min_length=6)

class User(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class CostCalculation(BaseModel):
    route_id: int
    weight: Decimal = Field(..., gt=0)

class CostResult(BaseModel):
    route_name: str
    weight: Decimal
    tariff_per_kg: Decimal
    total_cost: Decimal
    distance: Decimal

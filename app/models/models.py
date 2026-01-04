from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    dispatcher = "dispatcher"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.manager)

class Transport(Base):
    __tablename__ = "transport"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    capacity = Column(DECIMAL(10, 2), nullable=False)
    
    trips = relationship("Trip", back_populates="transport")

class Route(Base):
    __tablename__ = "routes"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    tariff_per_kg = Column(DECIMAL(10, 2), nullable=False)
    distance = Column(DECIMAL(10, 2), nullable=False)
    
    trips = relationship("Trip", back_populates="route")

class Trip(Base):
    __tablename__ = "trips"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=False)
    transport_id = Column(Integer, ForeignKey("transport.id"), nullable=False)
    departure_datetime = Column(DateTime, nullable=False)
    arrival_datetime = Column(DateTime, nullable=False)
    
    route = relationship("Route", back_populates="trips")
    transport = relationship("Transport", back_populates="trips")
    cargos = relationship("Cargo", back_populates="trip")

class Cargo(Base):
    __tablename__ = "cargo"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    weight = Column(DECIMAL(10, 2), nullable=False)
    sender = Column(String(255), nullable=False)
    
    trip = relationship("Trip", back_populates="cargos")

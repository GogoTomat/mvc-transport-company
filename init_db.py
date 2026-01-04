from datetime import datetime, timedelta
from decimal import Decimal
from app.database import SessionLocal, engine, Base
from app.models.models import User, Transport, Route, Trip, Cargo, UserRole
from app.core.auth import get_password_hash

def init_db():
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        existing_admin = db.query(User).filter(User.username == "admin").first()
        if existing_admin:
            print("База данных уже инициализирована")
            return
        
        print("Создание начальных данных...")
        
        admin = User(
            username="admin",
            email="admin@transport.ru",
            password_hash=get_password_hash("admin123"),
            role=UserRole.admin
        )
        db.add(admin)
        
        manager = User(
            username="manager",
            email="manager@transport.ru",
            password_hash=get_password_hash("manager123"),
            role=UserRole.manager
        )
        db.add(manager)
        
        dispatcher = User(
            username="dispatcher",
            email="dispatcher@transport.ru",
            password_hash=get_password_hash("dispatcher123"),
            role=UserRole.dispatcher
        )
        db.add(dispatcher)
        
        transport1 = Transport(name="КАМАЗ-6520", capacity=Decimal("20.0"))
        transport2 = Transport(name="МАЗ-5440", capacity=Decimal("25.0"))
        transport3 = Transport(name="Volvo FH16", capacity=Decimal("30.0"))
        transport4 = Transport(name="Scania R500", capacity=Decimal("28.0"))
        db.add_all([transport1, transport2, transport3, transport4])
        
        route1 = Route(
            name="Москва-Санкт-Петербург",
            tariff_per_kg=Decimal("5.50"),
            distance=Decimal("700.0")
        )
        route2 = Route(
            name="Москва-Казань",
            tariff_per_kg=Decimal("4.80"),
            distance=Decimal("820.0")
        )
        route3 = Route(
            name="Санкт-Петербург-Новгород",
            tariff_per_kg=Decimal("3.20"),
            distance=Decimal("180.0")
        )
        route4 = Route(
            name="Москва-Екатеринбург",
            tariff_per_kg=Decimal("7.50"),
            distance=Decimal("1780.0")
        )
        db.add_all([route1, route2, route3, route4])
        
        db.commit()
        
        base_date = datetime.now()
        trip1 = Trip(
            route_id=route1.id,
            transport_id=transport1.id,
            departure_datetime=base_date + timedelta(days=1, hours=8),
            arrival_datetime=base_date + timedelta(days=1, hours=18)
        )
        trip2 = Trip(
            route_id=route2.id,
            transport_id=transport2.id,
            departure_datetime=base_date + timedelta(days=2, hours=6),
            arrival_datetime=base_date + timedelta(days=2, hours=17)
        )
        trip3 = Trip(
            route_id=route3.id,
            transport_id=transport3.id,
            departure_datetime=base_date + timedelta(days=1, hours=10),
            arrival_datetime=base_date + timedelta(days=1, hours=13)
        )
        trip4 = Trip(
            route_id=route4.id,
            transport_id=transport4.id,
            departure_datetime=base_date + timedelta(days=3, hours=7),
            arrival_datetime=base_date + timedelta(days=4, hours=19)
        )
        db.add_all([trip1, trip2, trip3, trip4])
        
        db.commit()
        
        cargo1 = Cargo(
            trip_id=trip1.id,
            weight=Decimal("15000.0"),
            sender="ООО Логистика Плюс"
        )
        cargo2 = Cargo(
            trip_id=trip1.id,
            weight=Decimal("3500.0"),
            sender="ИП Петров А.В."
        )
        cargo3 = Cargo(
            trip_id=trip2.id,
            weight=Decimal("20000.0"),
            sender="ЗАО ТрансКарго"
        )
        cargo4 = Cargo(
            trip_id=trip3.id,
            weight=Decimal("8000.0"),
            sender="ООО Северный Груз"
        )
        db.add_all([cargo1, cargo2, cargo3, cargo4])
        
        db.commit()
        
        print("База данных успешно инициализирована!")
        print("\nТестовые пользователи:")
        print("Администратор - username: admin, password: admin123")
        print("Менеджер - username: manager, password: manager123")
        print("Диспетчер - username: dispatcher, password: dispatcher123")
        
    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()

# Система Управления Транспортной Компанией

Полнофункциональная веб-система для управления транспортной компанией с бэкендом на FastAPI и фронтендом на HTML/CSS/JavaScript.

## Возможности

- ✅ **Управление транспортом** - учет транспортных средств с характеристиками
- ✅ **Управление маршрутами** - создание маршрутов с тарифами и расстояниями
- ✅ **Планирование рейсов** - назначение транспорта на маршруты с датами
- ✅ **Учет грузов** - регистрация грузов с привязкой к рейсам
- ✅ **Расчет стоимости** - автоматический расчет стоимости перевозки
- ✅ **Управление пользователями** - создание учетных записей с ролями
- ✅ **Статистика и отчетность** - общая статистика по деятельности компании
- ✅ **JWT аутентификация** - безопасный вход с токенами
- ✅ **Разграничение прав** - 3 роли с разными правами доступа
- ✅ **Адаптивный интерфейс** - работает на desktop и mobile

## 📋 Технологии

### Backend
- **FastAPI** - современный веб-фреймворк
- **SQLAlchemy** - ORM для работы с БД
- **SQLite** - база данных (легко заменить на PostgreSQL/MySQL)
- **Pydantic** - валидация данных
- **JWT (python-jose)** - токены аутентификации
- **Bcrypt (passlib)** - хеширование паролей

### Frontend
- **HTML5/CSS3** - семантическая разметка и стили
- **Vanilla JavaScript** - без фреймворков, чистый JS
- **Fetch API** - взаимодействие с бэкендом
- **LocalStorage** - хранение токенов
- **Adaptive Design** - адаптивная верстка

## Быстрый старт

### 1. Запустить Backend

```bash
# Установить зависимости
pip install -r requirements.txt

# Инициализировать БД с тестовыми данными
python init_db.py

# Запустить сервер
uvicorn main:app --reload
```

Backend будет доступен на: **http://localhost:8000**

### 2. Запустить Frontend

**Вариант A (простой):**
Откройте файл `frontend/login.html` в браузере

**Вариант B (рекомендуется):**
```bash
cd frontend
python -m http.server 8080
```
Откройте: **http://localhost:8080/login.html**

### 3. Войти в систему

Используйте тестовый аккаунт:
- **Логин**: `admin`
- **Пароль**: `admin123`

## Тестовые аккаунты

| Роль | Username | Password | Права |
|------|----------|----------|-------|
| Администратор | admin | admin123 | Полный доступ |
| Менеджер | manager | manager123 | CRUD, без удаления |
| Диспетчер | dispatcher | dispatcher123 | Рейсы и грузы |

## Структура проекта

```
transport-system/
├── app/                          # Backend приложение
│   ├── core/
│   │   └── auth.py              # JWT аутентификация
│   ├── models/
│   │   └── models.py            # SQLAlchemy модели
│   ├── schemas/
│   │   └── schemas.py           # Pydantic схемы
│   ├── routers/                 # API endpoints
│   │   ├── auth.py              # Регистрация/вход
│   │   ├── transport.py         # CRUD транспорта
│   │   ├── routes.py            # CRUD маршрутов
│   │   ├── trips.py             # CRUD рейсов
│   │   ├── cargo.py             # CRUD грузов
│   │   ├── users.py             # Управление пользователями
│   │   └── utils.py             # Расчеты и статистика
│   └── database.py              # Настройки БД
│
├── frontend/                     # Frontend приложение
│   ├── css/
│   │   └── style.css            # Стили
│   ├── js/
│   │   ├── api.js               # API клиент
│   │   ├── auth.js              # Аутентификация
│   │   └── utils.js             # Утилиты
│   ├── index.html               # Главная (статистика)
│   ├── login.html               # Вход/Регистрация
│   ├── transport.html           # Управление транспортом
│   ├── routes.html              # Управление маршрутами
│   ├── trips.html               # Управление рейсами
│   ├── cargo.html               # Управление грузами
│   └── users.html               # Управление пользователями
│
├── main.py                       # Главный файл FastAPI
├── init_db.py                   # Инициализация БД
├── requirements.txt             # Python зависимости
└── README.md                    # Этот файл
```

## API Endpoints

### Аутентификация
- `POST /auth/register` - Регистрация
- `POST /auth/login` - Вход (получение JWT)

### Транспорт
- `GET /transport/` - Список транспорта
- `POST /transport/` - Создать транспорт 
- `PUT /transport/{id}` - Обновить транспорт 
- `DELETE /transport/{id}` - Удалить транспорт 

### Маршруты
- `GET /routes/` - Список маршрутов
- `POST /routes/` - Создать маршрут 
- `PUT /routes/{id}` - Обновить маршрут 
- `DELETE /routes/{id}` - Удалить маршрут 

### Рейсы
- `GET /trips/` - Список рейсов
- `POST /trips/` - Создать рейс 
- `PUT /trips/{id}` - Обновить рейс 
- `DELETE /trips/{id}` - Удалить рейс 

### Грузы
- `GET /cargo/` - Список грузов
- `POST /cargo/` - Создать груз 
- `PUT /cargo/{id}` - Обновить груз 
- `DELETE /cargo/{id}` - Удалить груз 

### Пользователи
- `GET /users/me` - Текущий пользователь 
- `GET /users/` - Все пользователи 
- `PUT /users/{id}` - Обновить пользователя 
- `DELETE /users/{id}` - Удалить пользователя 

### Утилиты
- `POST /utils/calculate-cost` - Расчет стоимости
- `GET /utils/statistics` - Статистика


## База данных

### Таблицы

**users** - Пользователи системы
```sql
id, username, password_hash, email, role
```

**transport** - Транспортные средства
```sql
id, name, capacity
```

**routes** - Маршруты
```sql
id, name, tariff_per_kg, distance
```

**trips** - Рейсы
```sql
id, route_id, transport_id, departure_datetime, arrival_datetime
```

**cargo** - Грузы
```sql
id, trip_id, weight, sender
```

### Диаграмма связей
```
users (управляют системой)

transport ──┐
            ├──→ trips ──→ cargo
routes  ────┘
```

## Интерфейс

### Цветовая схема
- **Основной**: Синий (#1a4d7a) - надежность и профессионализм
- **Акцент**: Оранжевый (#ff6b35) - призывы к действию
- **Дополнительный**: Серый - нейтральные элементы

### Страницы

1. **Главная** - Статистика + калькулятор стоимости
2. **Транспорт** - CRUD транспортных средств
3. **Маршруты** - CRUD маршрутов с тарифами
4. **Рейсы** - Планирование и управление рейсами
5. **Грузы** - Регистрация и учет грузов
6. **Пользователи** - Управление учетными записями (только admin)

##  Безопасность

**Реализовано:**
- JWT токены для аутентификации
- Bcrypt хеширование паролей
- Role-Based Access Control (RBAC)
- Валидация данных через Pydantic
- Защита от SQL-инъекций (SQLAlchemy ORM)
- XSS защита
- CORS настроен для разработки

**Для production:**
- Смените SECRET_KEY в `app/core/auth.py`
- Ограничьте CORS в `main.py`
- Используйте HTTPS
- Используйте PostgreSQL вместо SQLite
- Настройте rate limiting

## Документация API

После запуска backend доступна автоматическая документация:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Тестирование

### Через Swagger UI
1. Откройте http://localhost:8000/docs
2. Используйте `/auth/login` для получения токена
3. Нажмите "Authorize" и вставьте токен
4. Тестируйте endpoints

### Через Postman
Импортируйте файл `Transport_API.postman_collection.json`

### Через curl
```bash
# Получить токен
curl -X POST "http://localhost:8000/auth/login" \
  -d "username=admin&password=admin123"

# Использовать токен
curl "http://localhost:8000/transport/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

ы
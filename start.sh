#!/bin/bash

echo "=== Система управления транспортной компанией ==="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Создание виртуального окружения..."
    python3 -m venv venv
fi

echo "Активация виртуального окружения..."
source venv/bin/activate

echo "Установка зависимостей..."
pip install -r requirements.txt

echo "Инициализация базы данных..."
python init_db.py

echo ""
echo "=== Запуск сервера ==="
echo "API будет доступен по адресу: http://localhost:8000"
echo "Документация (Swagger): http://localhost:8000/docs"
echo "Документация (ReDoc): http://localhost:8000/redoc"
echo ""

python -m uvicorn main:app --reload

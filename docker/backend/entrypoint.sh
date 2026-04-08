#!/bin/sh
set -eu

echo "Waiting for database ${DATABASE_URL}"
python - <<'PY'
import os
import time
from sqlalchemy import create_engine, text

url = os.environ["DATABASE_URL"]
engine = create_engine(url, pool_pre_ping=True)
for attempt in range(1, 31):
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print(f"Database is ready on attempt {attempt}")
        break
    except Exception as exc:
        print(f"Database is not ready yet (attempt {attempt}/30): {exc}")
        time.sleep(2)
else:
    raise SystemExit("Database is not reachable")
PY

python migrate.py
python init_db.py
exec uvicorn main:app --host 0.0.0.0 --port 8000

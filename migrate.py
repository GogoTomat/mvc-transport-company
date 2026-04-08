from app.database import Base, engine
from app.models import models  # noqa: F401  # ensure models are imported


def migrate() -> None:
    Base.metadata.create_all(bind=engine)
    print("Database schema is up to date")


if __name__ == "__main__":
    migrate()

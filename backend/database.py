from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DB_PATH = Path(__file__).resolve().parent / "alertx.sqlite3"
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def init_db():
    try:
        from backend.models.contact import Contact
        from backend.models.emergency import Emergency
    except ImportError:
        from models.contact import Contact
    Base.metadata.create_all(bind=engine)


def get_db():
    """Database session dependency for FastAPI routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Auto-initialize tables
init_db()



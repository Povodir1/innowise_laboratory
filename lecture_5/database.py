from sqlalchemy import String, Integer, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

# Creates a synchronous SQLAlchemy engine for SQLite.
engine = create_engine("sqlite:///./books.db")


class Base(DeclarativeBase):
    pass


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    author: Mapped[str] = mapped_column(String(100), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=True)


Base.metadata.create_all(bind=engine)


# Creates a sessionmaker factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db():
    """
    Yields:
    Session: A SQLAlchemy session object.

    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

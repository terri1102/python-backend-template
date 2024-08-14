from sqlmodel import SQLModel, Session, create_engine, select
from app.core.config import settings
from app.models.user import User, UserCreate
from app.crud.user import create_user

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def create_tables() -> None:
    SQLModel.metadata.create_all(engine)


def init_db(session: Session) -> None:
    user = session.exec(select(User).where(User.email == settings.FIRST_SUPERUSER)).first()

    if not user:
        user_in = UserCreate(
            full_name=settings.FIRST_SUPERUSER_NAME,
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = create_user(db=session, user_create=user_in)

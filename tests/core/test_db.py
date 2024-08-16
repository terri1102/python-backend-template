from sqlmodel import Session, select
from app.models.user import User, UserCreate
from app.api.v1.routes.users import create_new_user


def test_db_connection(db_session: Session) -> None:
    user_info = UserCreate(email="test@example.com", full_name="Test User", password="password")
    create_new_user(user_info, db_session)

    statement = select(User).where(User.email == "test@example.com")
    user = db_session.exec(statement).first()
    assert user is not None
    assert user.email == "test@example.com"

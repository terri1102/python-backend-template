from typing import Optional
from sqlmodel import Session, select
from app.models.user import User, UserCreate, UserUpdate
from app.core.security import get_password_hash


def get_user(db: Session, user_id: int) -> Optional[User]:
    statement = select(User).where(User.id == user_id)
    results = db.exec(statement)
    return results.first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    statement = select(User).where(User.email == email)
    results = db.exec(statement)
    return results.first()


def create_user(db: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(user_create, update={"hashed_password": get_password_hash(user_create.password)})
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> User | None:
    db_user = db.get(User, user_id)
    if not db_user:
        return None

    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    user = db.get(User, user_id)
    if user:
        db.delete(user)
        db.commit()
        return True
    return False

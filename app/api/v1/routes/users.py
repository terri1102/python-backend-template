from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.api.dependencies import get_db
from app.models.user import User, UserCreate, UserUpdate
from app.crud.user import get_user, get_user_by_email, create_user, update_user, delete_user

router = APIRouter()


@router.post("/", response_model=User)
def create_new_user(user_create: UserCreate, db: Session = Depends(get_db)) -> User | HTTPException:
    db_user = get_user_by_email(db, user_create.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, user_create)


@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)) -> User | HTTPException:
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/{user_id}", response_model=User)
def update_existing_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)) -> User | HTTPException:
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return update_user(db, user_id, user_update)


@router.delete("/{user_id}", response_model=bool)
def delete_existing_user(user_id: int, db: Session = Depends(get_db)) -> bool | HTTPException:
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return success

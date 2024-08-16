from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.api.dependencies import get_current_active_superuser, SessionDep, CurrentUser
from app.core.security import verify_password, get_password_hash
from app.models.user import UserCreate, UserUpdate, UserPublic, UserUpdateMe, UpdatePassword, UserRegister
from app.crud.user import get_user, get_user_by_email, create_user, update_user, delete_user
from app.models.auth import Message
from app.core.config import settings


router = APIRouter()


@router.post("/", dependencies=[Depends(get_current_active_superuser)], response_model=UserPublic)
def create_new_user(user_create: UserCreate, session: Session = Depends(SessionDep)) -> UserPublic | HTTPException:
    db_user = get_user_by_email(session, user_create.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = create_user(session, user_create)
    return UserPublic.model_dump(new_user)


@router.get("/{user_id}", dependencies=[Depends(get_current_active_superuser)], response_model=UserPublic)
def read_user(user_id: int, session: Session = Depends(SessionDep)) -> UserPublic | HTTPException:
    db_user = get_user(session, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/{user_id}", dependencies=[Depends(get_current_active_superuser)], response_model=UserPublic)
def update_existing_user(
    user_id: int, user_update: UserUpdate, db: Session = Depends(SessionDep)
) -> UserPublic | HTTPException:
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return update_user(db, user_id, user_update)


@router.delete("/{user_id}", dependencies=[Depends(get_current_active_superuser)], response_model=bool)
def delete_existing_user(user_id: int, db: Session = Depends(SessionDep)) -> bool | HTTPException:
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return success


# API for users reading/updating/deleting their own accounts
@router.get("/me", response_model=UserPublic)
def read_user_me(current_user: CurrentUser) -> Any:
    """
    Get current user.
    """
    return current_user


@router.patch("/me", response_model=UserPublic)
def update_user_me(*, session: Session = Depends(SessionDep), user_in: UserUpdateMe, current_user: CurrentUser) -> Any:
    """
    Update own user.
    """

    if user_in.email:
        existing_user = get_user_by_email(session=session, email=user_in.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(status_code=409, detail="User with this email already exists")
    user_data = user_in.model_dump(exclude_unset=True)
    current_user.sqlmodel_update(user_data)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user


@router.patch("/me/password", response_model=Message)
def update_password_me(
    *, session: Session = Depends(SessionDep), body: UpdatePassword, current_user: CurrentUser
) -> Any:
    """
    Update own password.
    """
    if not verify_password(body.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    if body.current_password == body.new_password:
        raise HTTPException(status_code=400, detail="New password cannot be the same as the current one")
    hashed_password = get_password_hash(body.new_password)
    current_user.hashed_password = hashed_password
    session.add(current_user)
    session.commit()
    return Message(message="Password updated successfully")


@router.delete("/me", response_model=Message)
def delete_user_me(current_user: CurrentUser, session: Session = Depends(SessionDep)) -> Any:
    """
    Delete own user.
    """
    if current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Super users are not allowed to delete themselves")
    success = delete_user(session, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")

    return Message(message="User deleted successfully")


@router.post("/signup", response_model=UserPublic)
def register_user(user_in: UserRegister, session: Session = Depends(SessionDep)) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user_create = UserCreate.model_validate(user_in)
    user = create_user(session=session, user_create=user_create)
    return user

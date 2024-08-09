from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session, relationship
from typing import Annotated
from app.db import Base
from app.db_depends import get_db
# from app.routers.user import User
from app.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete, Column, Integer, String
from slugify import slugify


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    firstname = Column(String)
    lastname = Column(String)
    age = Column(Integer)
    slug = Column(String, unique=True, index=True)

    tasks = relationship("Task", back_populates="user")


router = APIRouter(
    prefix="/user",
    tags=["user"]
)


# Функция для получения всех пользователей
@router.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users


# Функция для получения пользователя по id
@router.get("/{user_id}")
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.scalars(select(User).where(User.id == user_id)).first()
    if user:
        return user
    raise HTTPException(status_code=404, detail="User was not found")


# Функция для создания нового пользователя
@router.post("/create")
async def create_user(user: CreateUser, db: Annotated[Session, Depends(get_db)]):
    slug = slugify(user.username)
    new_user = User(
        username=user.username,
        firstname=user.firstname,
        lastname=user.lastname,
        age=user.age,
        slug=slug
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}


# Функция для обновления данных пользователя
@router.put("/update")
async def update_user(user_id: int, updated_user: UpdateUser, db: Annotated[Session, Depends(get_db)]):
    existing_user = db.scalars(select(User).where(User.id == user_id)).first()
    if existing_user:
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(
                firstname=updated_user.firstname,
                lastname=updated_user.lastname,
                age=updated_user.age
            )
        )
        db.execute(stmt)
        db.commit()
        return {"status_code": status.HTTP_200_OK, "transaction": "User update is successful!"}
    raise HTTPException(status_code=404, detail="User was not found")


# Функция для удаления пользователя
@router.delete("/delete")
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    existing_user = db.scalars(select(User).where(User.id == user_id)).first()
    if existing_user:
        stmt = delete(User).where(User.id == user_id)
        db.execute(stmt)
        db.commit()
        return {"status_code": status.HTTP_200_OK, "transaction": "User deletion is successful!"}
    raise HTTPException(status_code=404, detail="User was not found")

# Модели данных Pydantic
from fastapi import FastAPI, Path, HTTPException
from typing import List
from pydantic import BaseModel

app = FastAPI()

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get("/")
async def main_page() -> dict:
    return {"message": "Главная страница"}


@app.get("/users")
async def get_users() -> List[User]:
    return users


@app.post("/user/{username}/{age}")
async def user_add(user_new: User) -> User:
    user_new.id = len(users) + 1
    if user_new.username == '':
        user_new.username = "UrbanUser"
    if user_new.age == 0:
        user_new.age = 24
    users.append(user_new)
    return user_new


@app.put("/user/{user_id}/{username}/{age}")
async def user_update(user_id: int = Path(ge=1, le=100, description="Enter User ID", example=1),
                      username: str = Path(min_length=5, max_length=20, description="Enter username",
                                           example="UrbanUser"),
                      age: int = Path(ge=18, le=120, description="Enter age", example=24)) -> User:
    try:
        found = False
        for i in range(len(users)):
            if users[i].id == user_id:
                found = True
                user_edit = users[i]
                user_edit.username = username
                user_edit.age = age
                users[i] = user_edit
                break
        if found:
            return user_edit
        else:
            raise HTTPException(status_code=404, detail="User was not found")
    except IndexError:
        print("Message not found")


@app.delete("/user/{user_id}")
async def user_delete(user_id: int = Path(ge=1, le=100, description="Enter User ID", example=1)) -> User:
    try:
        found = False
        for i in range(len(users)):
            if users[i].id == user_id:
                user_del = users.pop(i)
                found = True
                break
        if found:
            return user_del
        else:
            raise HTTPException(status_code=404, detail="User was not found")
    except IndexError:
        print("Message not found")

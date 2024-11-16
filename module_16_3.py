# CRUD Запросы: Get, Post, Put Delete
from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()

users = {'1': 'Имя: Example, возраст: 18'}


@app.get("/")
async def main_page() -> dict:
    return {"message": "Главная страница"}


@app.get("/users")
async def get_users() -> dict:
    return users


@app.post("/user/{username}/{age}")
async def user_add(
        username: str = Path(min_length=5, max_length=20, description="Enter username", example="UrbanUser"),
        age: int = Path(ge=18, le=120, description="Enter age", example=24)) -> str:
    if users == {}:
        user_id = "1"
    else:
        user_id = str(int(max(users, key=int)) + 1)
    users[str(user_id)] = f"Имя: {username}, возраст: {age}"
    return f"User {user_id} is registered"


@app.put("/user/{user_id}/{username}/{age}")
async def user_update(user_id: int = Path(ge=1, le=100, description="Enter User ID", example=1),
                      username: str = Path(min_length=5, max_length=20, description="Enter username",
                                           example="UrbanUser"),
                      age: int = Path(ge=18, le=120, description="Enter age", example=24)) -> str:
    users[str(user_id)] = f"Имя: {username}, возраст: {age}"
    return f"The user {user_id} has been updated"


@app.delete("/user/{user_id}")
async def user_delete(user_id: int = Path(ge=1, le=100, description="Enter User ID", example=1)) -> str:
    if users.get(str(user_id), "None") != "None":
        users.pop(str(user_id))
        return f"User {user_id} has been deleted"
    else:
        return f"User {user_id} not found"

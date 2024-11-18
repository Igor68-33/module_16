# Шаблонизатор Jinja 2

from fastapi import FastAPI, Body, Path, HTTPException, Request
from fastapi.responses import HTMLResponse
from typing import List
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get("/")
async def main_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get(path="/user/{user_id}")
async def get_user(request: Request, user_id: int) -> HTMLResponse:
    try:
        return templates.TemplateResponse("users.html", {"request": request,
                                                         "user": users[[user.id for user in users].index(user_id)]})
    except ValueError:
        raise HTTPException(status_code=404, detail="User was not found")


@app.post("/user/{username}/{age}")
async def user_add(user_new: User) -> User:
    if users:
        user_new.id = max(users, key=lambda m: m.id).id + 1
    else:
        user_new.id = 1
    if user_new.username == 'string':
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
        user_index = [user.id for user in users].index(user_id)
        user_edit = users[user_index]
        user_edit.username = username
        user_edit.age = age
        users[user_index] = user_edit
        return user_edit
    except ValueError:
        raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}")
async def user_delete(user_id: int = Path(ge=1, le=100, description="Enter User ID", example=1)) -> User:
    try:
        user_del = users.pop([user.id for user in users].index(user_id))
        return user_del
    except ValueError:
        raise HTTPException(status_code=404, detail="User was not found")

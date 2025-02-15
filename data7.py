from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# 用户数据模型
class User(BaseModel):
    id: int
    name: str
    email: str

# 模拟数据库
users_db = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"}
]

@app.get("/users", response_model=List[User])
async def get_users():
    """ 获取所有用户 """
    return users_db

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    """ 根据用户 ID 获取用户详情 """
    user = next((user for user in users_db if user["id"] == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users", response_model=User)
async def create_user(user: User):
    """ 创建新用户 """
    users_db.append(user.dict())
    return user

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    """ 删除用户 """
    global users_db
    users_db = [user for user in users_db if user["id"] != user_id]
    return {"message": "User deleted successfully"}

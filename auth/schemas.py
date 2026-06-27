from typing import Optional
from pydantic import BaseModel 


class Token(BaseModel):  # Token响应类型
    access_token: str 
    token_type: str 

class UserBase(BaseModel):   # 用户模型基类
    id: Optional[int]
    username: str 

class UserCreate(UserBase):  # 请求模型
    password: str 

class User(UserBase):    # 响应模型
    class Config:
        orm_mode = True




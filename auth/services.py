from fastapi import Depends, HTTPException, status 
from jose import JWTError
from sqlalchemy import func
from sqlalchemy.orm import Session 
from app.database import SessionLocal, get_db, func
from app.settings import AUTH_SCHEMA, AUTH_INIT_USER, AUTH_INIT_PASSWORD
from utils.password import get_password_hash, verify_password
from utils.token import extract_token
from .models import UserInDB # ORM模型
from .schemas import UserCreate # 请求数据模型


# 创建初始管理员账号
def init_admin_user():
    db = SessionLocal() # 数据库会话
    cnt = db.query(   # sqlalchemy.orm.query.Query: SELECT count(auth_user.username) AS count_1 FROM user
        func.count(   # sqlalchemy.sql.functions.count
            UserInDB.username 
        )
    ).scalar() # 查询数据库中账号数量

    if cnt == 0:
        user = UserInDB(  # 创建初始账号
            username=AUTH_INIT_USER,
            get_password_hash=get_password_hash(AUTH_INIT_PASSWORD)
        )
        db.add(user)
        db.commit()
    db.close()


# 获取单个用户
def get_user(db: Session, username: str):
    return db.query(UserInDB).filter(UserInDB.username == username).first() 


# 创建一个用户
def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)  # 计算密码的哈希值
    db_user = UserInDB(username=user.username, hashed_password=hashed_password,) 
    db.add(db_user)  # 将实例添加到会话
    db.commit()      # 提交会话
    # 刷新实例， 用于获取数据或生成数据中的ID 
    db.refresh(db_user)
    return db_user 

# 验证用户和密码
def authenticate_user(db: Session, username:str, password:str):
    user = get_user(db, username)
    if not user:
        return False 
    if not verify_password(password, user.hashed_password):
        return False 
    return user

# 获取当前用户信息的依赖函数
async def get_current_usr(
        token: str=Depends(AUTH_SCHEMA), # 依赖项，身份认证
        db: Session = Depends(get_db)    # 依赖项，数据库连接
    ):
    invalid_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="无效的用户任据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        username: str = extract_token(token)  # 从token中解析出账号 
        if username is None:
            raise invalid_exception   
    except JWTError:
        raise invalid_exception
    user = get_user(db, username=username)
    if user is None:
        raise invalid_exception
    return user  # UserInDB












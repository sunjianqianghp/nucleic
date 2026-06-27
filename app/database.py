from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.settings import *


engine = create_engine(f"mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}") # 数据库引擎实例
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # 数据库会话类
Base = declarative_base() # 数据库模型基类 

def get_db():
    db = SessionLocal() 
    try:
        yield db 
    finally:
        db.close() 

# 根据sqlalchemy的数据库模型定义， 将数据库模型生成数据库中的表结构
def generate_tables():
    Base.metadata.create_all(bind=engine)





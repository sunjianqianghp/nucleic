from sqlalchemy import create_engine, func
from sqlalchemy.orm import declarative_base, sessionmaker
import pymysql 
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String # 第一步，导入SQLAlchemy组件包
from sqlalchemy.orm import relationship


pymysql.install_as_MySQLdb()

engine = create_engine("mysql://root:123456@localhost/cat")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # 数据库会话类
Base = declarative_base() # 数据库模型基类 

# 声明User模型，继承自Base
class User(Base):
    __tablename__ = "user" # 指定数据库中的表名
    # 定义类的属性，对应表中的字段
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(50))
    is_active = Column(Boolean, default=True)
    # 定义一对多关系
    books = relationship("Book", back_populates="owner")

# 声明Book模型，继承自Base类
class Book(Base):
    # 指定数据库中对应的表名
    __tablename__ = "book"
    # 定义类的属性，对应表中的字段
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), index=True)
    description = Column(String(200), index=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    # 定义关联
    owner = relationship("User", back_populates="books")


db = SessionLocal() # 数据库会话

print( type( db.query(func.count( User.id )) ) )
print(       db.query(func.count( User.id ))   )
print(       type(func.count( User.id ))   )
print(                func.count( User.id )    )

cnt = db.query(func.count( User.id )).scalar() # 查询数据库中账号数量
print(cnt)




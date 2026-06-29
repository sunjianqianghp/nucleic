import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware  # 跨域资源共享安全中间件
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from app.database import generate_tables
from app.settings import AUTH_SCHEMA
from auth.router import route as auth_router
from auth.services import init_admin_user


app = FastAPI() 

origins = [
    "http://localhost:8000",
    "http://localhost:8080"
]

app.add_middleware(            # 在应用上添加中间件
    CORSMiddleware,          
    allow_origins = origins,   
    allow_credentials=True,    # 允许使用cookie
    allow_methods=["*"],       # 允许的方法，全部
    allow_headers=["*"]        # 允许的Header， 全部
)

app.include_router(auth_router, prefix='/person')


@app.get('/')
def toweb():
    return RedirectResponse('/web/index.html')

## 生成表结构， SQLAlchemy的数据表同步工具
generate_tables() 

## 创建初始管理员账号
init_admin_user() 


if __name__ == '__main__':
    uvicorn.run(app=app)

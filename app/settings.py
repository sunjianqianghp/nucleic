from fastapi.security import OAuth2PasswordBearer
from urllib import parse 

# 定义配置项
# JWT密钥， 使用命令 # openssl rand -hex 32生成
JWT_SECRET_KEY = '486f3a0a03bae6661351e0ce9956991ca41946d360fd7874f0238701ae86afc6'
JWT_ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # JWT中Token有效期，24小时
AUTH_SCHEMA = OAuth2PasswordBearer(tokenUrl="auth/login") # 依赖类实例，身份认证设置
AUTH_INIT_USER = 'admin'
AUTH_INIT_PASSWORD = '111111'

# 数据库配置
DB_HOST = 'localhost'
DB_USERNAME = 'root'
DB_PASSWORD = parse.quote('123456') # 转义密码中的特殊字符
DB_DATABASE = 'nucleic'  




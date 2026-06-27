from fastapi import Depends, HTTPException, status 
from jose import JWTError
from sqlalchemy.orm import Session 
from app.database import get_db
from app.settings import AUTH_SCHEMA
from utils.password import get_password_hash, verify_password



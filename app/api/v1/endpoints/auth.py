from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import select 
from passlib.context import CryptContext 
from jose import jwt 
from datetime import datetime, timedelta 
from app.core.database import get_db 
from app.models.user import User 
from app.schemas.user import UserCreate, UserOut, Token 
from app.core.config import settings 
 
router = APIRouter(prefix="/auth", tags=["Authentication"]) 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 
 
def verify_password(plain_password, hashed_password): 
    return pwd_context.verify(plain_password, hashed_password) 
 
def get_password_hash(password): 
    return pwd_context.hash(password) 
 
def create_access_token(data: dict): 
    to_encode = data.copy() 
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) 
    to_encode.update({"exp": expire}) 
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM) 
 
@router.post("/register", response_model=UserOut) 
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)): 
    result = await db.execute(select(User).where(User.email == user_data.email)) 
    if result.scalar_one_or_none(): 
        raise HTTPException(status_code=400, detail="Email already exists") 
    hashed = get_password_hash(user_data.password) 
    new_user = User(email=user_data.email, hashed_password=hashed, full_name=user_data.full_name) 
    db.add(new_user) 
    await db.commit() 
    await db.refresh(new_user) 
    return new_user 
 
@router.post("/login", response_model=Token) 
async def login(user_data: UserCreate, db: AsyncSession = Depends(get_db)): 
    result = await db.execute(select(User).where(User.email == user_data.email)) 
    user = result.scalar_one_or_none() 
    if not user or not verify_password(user_data.password, user.hashed_password): 
        raise HTTPException(status_code=401, detail="Invalid credentials") 
    token = create_access_token(data={"sub": str(user.id)}) 
    return {"access_token": token} 

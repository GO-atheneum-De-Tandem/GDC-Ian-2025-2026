from fastapi import FastAPI, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, EmailStr
from argon2 import PasswordHasher

#behind proxy middleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from app.database import get_db
import app.models as models
from app.config import description

app = FastAPI(
    title="Safe API - GDC Ian",
    description=description,
    summary="A safe API for GDC research project by Ian-Chains Baute.",
    version="0.1.1",
    contact={
        "name": "Ian-Chains Baute",
        "email": "school@ian-chains.it",
        "url": "https://ian-chains.it",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

app.add_middleware(
    ProxyHeadersMiddleware,
    trusted_hosts="*"
)

@app.get("/")
async def read_root(request: Request):
    return {"message": "Hello, welcome to the Safe API! GDC research project by Ian-Chains Baute.", "client_host": request.client.host}

@app.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User))
    users = result.scalars().all() #scalars() haalt alle kolommen op, all() zet om in lijst
    return users

@app.get("/users/{user_id}")
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first() #scalars() haalt alle kolommen op, first() haalt de eerste rij op
    return user


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

@app.post("/users", status_code=201)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    #basic password & input validation
    if not user.password or len(user.password) < 8:
        raise HTTPException(status_code=422, detail="Password must be at least 8 characters long")
    if not user.username or len(user.username) < 3:
        raise HTTPException(status_code=422, detail="Username must be at least 3 characters long")
    if not user.email:
        raise HTTPException(status_code=422, detail="Email must be provided")

    # check for existing username or email
    result = await db.execute(select(models.User).where((models.User.username == user.username) | (models.User.email == user.email)))
    existing = result.scalars().first()
    if existing:
        if existing.username == user.username:
            raise HTTPException(status_code=409, detail="Username already exists")
        if existing.email == user.email:
            raise HTTPException(status_code=409, detail="Email already exists")

    #password hashing
    ph = PasswordHasher()
    try:
        password_hash = ph.hash(user.password)
    except Exception:
        raise HTTPException(status_code=500, detail="Password hashing failed")

    #create user in database
    new_user = models.User(username=user.username, email=user.email, password_hash=password_hash)
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Username or email already exists")
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Could not create user")

    #return new user data
    return {"id": new_user.id, "username": new_user.username, "email": new_user.email, "created_at": new_user.created_at}
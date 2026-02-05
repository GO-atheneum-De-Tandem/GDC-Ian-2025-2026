# -------- IMPORTS --------
#api imports
from app.config import description
from fastapi import FastAPI, Depends, Request, HTTPException

#database & ORM imports
from app.database import get_db
from app.database import AsyncSessionLocal
import app.models as models
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from sqlalchemy.exc import IntegrityError

#pydantic imports
from pydantic import BaseModel, EmailStr

#logging & authentication imports
from argon2 import PasswordHasher
import logging

#proxy middleware import
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

# -------- SETUP & CONFIGURATION --------

#app setup
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

#logging setup
app.add_middleware(
    ProxyHeadersMiddleware,
    trusted_hosts="*"
)

#database connection test on startup
@app.on_event("startup")
async def on_startup():
    logger = logging.getLogger("uvicorn.error")

    #If session factory not configured, log and skip test
    if AsyncSessionLocal is None:
        logger.error("AsyncSessionLocal not configured; skipping DB connection test.")
        return

    try:
        async with AsyncSessionLocal() as session:
            await session.execute(select(1)) #simple test query
        logger.info("Database connection test succeeded.")
    except Exception as e:
        logger.exception("Database connection test failed: %s", e)

# -------- ROOT & TESTING ENDPOINTS --------

#root endpoint returning welcome message and client IP
@app.get("/")
async def read_root(request: Request):
    return {"message": "Hello, welcome to the Safe API! GDC research project by Ian-Chains Baute.", "client_host": request.client.host}

# -------- USER ENDPOINTS --------

#users get endpoint, lists all users in database
@app.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User))
    users = result.scalars().all() #scalars() haalt alle kolommen op, all() zet om in lijst
    return users

#users get endpoint, haalt specifieke gebruiker op basis van ID
@app.get("/users/{user_id}")
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first() #scalars() haalt alle kolommen op, first() haalt de eerste rij op
    return user

#user create expected json body
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

#users post endpoint, maakt nieuwe gebruiker aan in database
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
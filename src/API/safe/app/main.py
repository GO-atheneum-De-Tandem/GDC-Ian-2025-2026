# -------- IMPORTS --------
#api imports
from app.config import description, settings
from fastapi import FastAPI, Depends, Request, HTTPException
from datetime import datetime, timedelta

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
from app.functions import create_password_hash, verify_password, create_jwt_token
import logging

#proxy middleware import
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

# -------- SETUP & CONFIGURATION --------

#app setup
app = FastAPI(
    title="Safe API - GDC Ian",
    description=description,
    summary="A safe API for GDC research project by Ian-Chains Baute.",
    version="0.2.1",
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

@app.get("/")
async def read_root(request: Request):
    """Root endpoint returning a welcome message and client IP address."""
    return {"message": "Hello, welcome to the Safe API! GDC research project by Ian-Chains Baute.", "client_host": request.client.host}

# -------- USER ENDPOINTS --------

@app.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    """Retrieve all users and their information from the database."""
    
    result = await db.execute(select(models.User))
    users = result.scalars().all() #scalars() haalt alle kolommen op, all() zet om in lijst
    return users

@app.get("/users/{user_id}")
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve a user by their ID from the database."""

    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first() #scalars() haalt alle kolommen op, first() haalt de eerste rij op
    return user

class UserCreate(BaseModel):
    """Model for creating a new user."""
    username: str
    email: EmailStr
    password: str

@app.post("/users", status_code=201)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """Create a new user in the database with hashed password."""

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
    try:
        password_hash = await create_password_hash(user.password)
    except RuntimeError:
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

# -------- AUTHENTICATION ENDPOINTS --------

class LoginRequest(BaseModel):
    """Model for login request."""
    username_or_email: str
    password: str

@app.post("/login")
async def login(credentials: LoginRequest, db: AsyncSession = Depends(get_db)):
    """Authenticate user and return JWT token."""

    # find user by username or email
    result = await db.execute(select(models.User).where((models.User.username == credentials.username_or_email) | (models.User.email == credentials.username_or_email)))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    #verify password using helper
    try:
        verified = await verify_password(user.password_hash, credentials.password)
    except RuntimeError:
        raise HTTPException(status_code=500, detail="Password verification failed")
    if not verified:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    #generate JWT token using helper
    try:
        token, exp = await create_jwt_token(user.id, user.username, user.role)
    except RuntimeError:
        raise HTTPException(status_code=500, detail="Token generation failed")

    #return token and expiration time
    return {"access_token": token, "token_type": "bearer", "expires_at": exp}
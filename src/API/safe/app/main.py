from fastapi import FastAPI, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

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
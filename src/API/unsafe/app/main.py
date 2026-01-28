from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
import app.models as models

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, welcome to the Safe API! GDC research project by Ian-Chains Baute."}

@app.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User))
    users = result.scalars().all() #scalars() haalt alle kolommen op, all() zet om in lijst
    return users
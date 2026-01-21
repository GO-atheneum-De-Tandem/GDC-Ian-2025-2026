from fastapi import FastAPI
from .config import settings
import asyncpg

app = FastAPI()


@app.on_event("startup")
async def startup_db_test():
   dsn = f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
   try:
      conn = await asyncpg.connect(dsn)
      print("DB connection successful")
      await conn.close()
   except Exception as e:
      print("DB connection failed:", e)


@app.get("/")
def first_example():
   '''
   FG Example First Fast API Example 
   '''
   return {"GFG Example": "FastAPI"}
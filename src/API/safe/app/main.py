from fastapi import FastAPI
from .config import settings
import asyncpg
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

#Database connection pool setup
@app.on_event("startup")
async def startup_db():
    dsn = f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    try:
        app.state.db_pool = await asyncpg.create_pool(dsn, min_size=1, max_size=10)
        logger.info("DB pool created")
    except Exception as e:
        logger.critical("DB pool creation failed: %s", e)

#Database connection pool teardown
@app.on_event("shutdown")
async def shutdown_db():
    pool = getattr(app.state, "db_pool", None)
    if pool:
        await pool.close()
        logger.info("DB pool closed")

@app.get("/")
def first_example():
   '''
   FG Example First Fast API Example 
   '''
   return {"GFG Example": "FastAPI"}
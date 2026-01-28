from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from app.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = settings.DB_URL
engine = None
AsyncSessionLocal = None

#Async engine aanmaken met foutafhandeling
try:
    engine = create_async_engine(
        DATABASE_URL,
        echo=settings.DB_ECHO_QUERIES,  #echo = SQL queries loggen
        pool_pre_ping=True,
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW
    )

    #Async session factory
    AsyncSessionLocal = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False
    )

    logger.info("Async DB engine and sessionmaker created for %s", DATABASE_URL)
except SQLAlchemyError as e:
    logger.exception("SQLAlchemy error while creating async engine/sessionmaker: %s", e)
except Exception as e:
    logger.exception("Unexpected error while configuring database: %s", e)


#Async dependency voor FastAPI
async def get_db():
    if AsyncSessionLocal is None:
        logger.error("AsyncSessionLocal is not configured; cannot provide DB session.")
        raise RuntimeError("Database session factory is not available")

    async with AsyncSessionLocal() as session:

        try:
            yield session
        except Exception as e:
            logger.exception("Unhandled exception during DB session usage: %s", e)

            try:
                await session.rollback()
                logger.debug("DB session rollback succeeded after exception.")
            except Exception:
                logger.exception("Failed to rollback DB session after exception.")
            raise

        finally:
            try:
                await session.close()
            except Exception:
                logger.exception("Failed to close DB session cleanly.")
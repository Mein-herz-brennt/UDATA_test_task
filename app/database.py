from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from decouple import config

DATABASE_URL = config(
    "DATABASE_URL",
    default="postgresql+asyncpg://postgres:postgres@localhost:5432/auction_db"
)

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

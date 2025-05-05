# recreate_db.py
import asyncio
from database.db import engine
from database.models import Base

async def recreate_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(recreate_all_tables())

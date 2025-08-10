from .config import load_config
import asyncpg
from contextlib import asynccontextmanager
import logging


import os
from pathlib import Path


src_dir = Path(__file__).parent.parent
env_path = src_dir / ".env"

config = load_config(str(env_path))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"DB_HOST: {config.db.database_host}")
logger.info(f"DB_PORT: {config.db.database_port}")
logger.info(f"DB_USER: {config.db.database_user}")
logger.info(f"DB_NAME: {config.db.database_name}")

pool = None


async def init_db():
    global pool
    pool = await asyncpg.create_pool(
        host=config.db.database_host,
        port=config.db.database_port,
        user=config.db.database_user,
        password=config.db.database_password,
        database=config.db.database_name
    )

    async with pool.acquire() as conn:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS entries (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                content TEXT NOT NULL,
                is_done BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')


@asynccontextmanager
async def get_db():
    if pool is None:
        await init_db()
    
    conn = await pool.acquire()
    try:
        yield conn
    finally:
        await pool.release(conn)


async def get_db_connection():
    async with get_db() as conn:
        yield conn
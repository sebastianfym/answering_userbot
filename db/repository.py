from sqlalchemy import insert, update, select
import datetime

from config import settings
from db import User
from db.database import Base
from db.db_service import engine

@settings.logger.catch
async def get_table_names():
    async with engine.begin() as conn:
        table_names = await conn.run_sync(engine.dialect.get_table_names)
        return table_names

@settings.logger.catch
async def check_db():
    async with engine.begin() as conn:
        table_names = await get_table_names()
        if "user" in table_names:
            return
        await conn.run_sync(Base.metadata.create_all)
        return

@settings.logger.catch
async def create_user(chat_id: int):
    async with engine.begin() as conn:
        created_at = datetime.datetime.now()
        stmt = insert(User).values(chat_id=chat_id, created_at=created_at, status_updated_at=created_at, status="alive")
        await conn.execute(stmt)
        await conn.commit()

@settings.logger.catch
async def check_or_create_user(chat_id: int):
    async with engine.begin() as conn:
        stmt = select(User).where(User.chat_id == chat_id)
        result = await conn.execute(stmt)
        row = result.fetchone()
        if row:
            return row
        await create_user(chat_id)

@settings.logger.catch
async def update_status(chat_id: int, status):
    async with engine.begin() as conn:
        stmt = update(User).values(status=status).filter_by(chat_id=chat_id).returning(User)
        result = await conn.execute(stmt)
        row = result.fetchone()

@settings.logger.catch
async def update_status_update_at(chat_id: int):
    async with engine.begin() as conn:
        stmt = update(User).values(status_updated_at=datetime.datetime.now()).filter_by(chat_id=chat_id).returning(User)
        result = await conn.execute(stmt)
        row = result.fetchone()

@settings.logger.catch
async def get_all_active_user():
    async with engine.begin() as conn:
        stmt = select(User).filter_by(status="alive")
        result = await conn.execute(stmt)
        row = result.fetchall()
        return row

@settings.logger.catch
async def get_objects_with_first_step(conn):
    current_time = datetime.datetime.now()

    max_time_six_minutes_ago = current_time - datetime.timedelta(minutes=5, seconds=59)
    min_time_six_minutes_ago = current_time - datetime.timedelta(minutes=6, seconds=59)

    query = select(User).where(User.created_at.between(min_time_six_minutes_ago, max_time_six_minutes_ago),
                               User.status == "alive")
    result = await conn.execute(query)
    return result.fetchall()

@settings.logger.catch
async def get_objects_with_second_step(conn):
    current_time = datetime.datetime.now()

    max_time_thirty_nine_minutes_ago = current_time - datetime.timedelta(minutes=38, seconds=59)
    min_time_thirty_nine_minutes_ago = current_time - datetime.timedelta(minutes=39, seconds=59)

    query = select(User).where(
        User.status_updated_at.between(min_time_thirty_nine_minutes_ago, max_time_thirty_nine_minutes_ago),
                               User.status == "alive")
    result = await conn.execute(query)
    return result.fetchall()

@settings.logger.catch
async def get_objects_with_third_step(conn):
    current_time = datetime.datetime.now()

    max_time_thirty_nine_minutes_ago = current_time - datetime.timedelta(minutes=1559, seconds=59)
    min_time_thirty_nine_minutes_ago = current_time - datetime.timedelta(minutes=1560, seconds=59)

    query = select(User).where(
        User.status_updated_at.between(min_time_thirty_nine_minutes_ago, max_time_thirty_nine_minutes_ago),
                               User.status == "alive")
    result = await conn.execute(query)
    return result.fetchall()

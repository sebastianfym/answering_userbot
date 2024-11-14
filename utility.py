import asyncio

from config import settings
from db.repository import get_all_active_user, get_objects_with_first_step, get_objects_with_second_step, \
    get_objects_with_third_step, update_status, update_status_update_at
from db.db_service import engine


def check_stop_words(message_text):
    for word in settings.stop_words:
        if word in message_text:
            return False


async def action_on_first_step(first_step_obj, app):
    for user in first_step_obj:
        await update_status_update_at(user.chat_id)
        await app.send_message(user.chat_id, "Привет! Как твои дела?")

async def action_on_second_step(second_step_obj, app):
    for user in second_step_obj:
        await update_status_update_at(user.chat_id)
        await app.send_message(user.chat_id, "Прости за длительный ответ. Куча дел!")

async def action_on_third_step(third_step_obj, app):
    for user in third_step_obj:
        await update_status_update_at(user.chat_id)
        await update_status(user.chat_id, "finished")
        await app.send_message(user.chat_id, "Я рад был с тобой пообщаться! Еще увидимся")


async def check_msg_action(app):
    async with engine.begin() as conn:
        while True:
            first_step_obj = await get_objects_with_first_step(conn)
            second_step_obj = await get_objects_with_second_step(conn)
            third_step_obj = await get_objects_with_third_step(conn)

            if first_step_obj:
                await action_on_first_step(first_step_obj, app)
            elif second_step_obj:
                await action_on_second_step(second_step_obj, app)
            elif third_step_obj:
                await action_on_third_step(third_step_obj, app)

            await asyncio.sleep(60)




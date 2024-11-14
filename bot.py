import asyncio

from config import *
from db.repository import check_db, check_or_create_user, update_status
from utility import check_stop_words, check_msg_action


client = client


@client.on_message()
async def forward_msg_for_me(client, message):
    chat_id = message.chat.id
    message_text = message.text

    await check_or_create_user(chat_id)

    if check_stop_words(message_text) is False:
        await update_status(chat_id, "dead")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(check_db())
    loop.create_task(check_msg_action(client))
    client.run()

from telethon import TelegramClient, events
import telethon
import asyncio
import random
from telethon.tl.custom.button import Button

#### consts #######
TOKEN = ""
AMOUNT_WAIT = 10 # in seconds
api_id = 123123123
api_hash = 'api_hash'
SESSION_NAME = "bot"
#### consts #######

client = TelegramClient(SESSION_NAME, api_id, api_hash)
client.start(bot_token=TOKEN)
pending={}
@client.on(events.ChatAction)
async def handler_join(event):
    if not event.user_joined and not event.user_added:
        return
    user_id = event.original_update.message.action.users[0]
    chat_id = event.original_update.message.peer_id.chat_id
    bottoni = [[  
        Button.inline("Арбуз", f"{chat_id}_{user_id}_1"), 
        Button.inline("Машина", f"{chat_id}_{user_id}_2"),
        Button.inline("Человек", f"{chat_id}_{user_id}_y")
    ]]
    random.shuffle(bottoni[0])
    msg = (await client.send_message(chat_id,f"Кто ты? У тебя есть {AMOUNT_WAIT} сек", buttons= bottoni))
    if not chat_id in pending.keys():
        pending[chat_id] = {}
    pending[chat_id][user_id] = {}
    await asyncio.sleep(AMOUNT_WAIT)
    if user_id not in pending[chat_id]:
        await msg.delete()
    else:
        try:
            await client.kick_participant(chat_id, user_id)
        except:
            await msg.edit("Администраторы мне ещё не дали прав исключать людей.")
        await msg.delete()
@client.on(events.CallbackQuery)
async def handler(event):
    data = event.data.decode("UTF-8").split("_")
    id_user = int(data[1])
    chat_id = int(data[0])
    searching_id = event.original_update.user_id
    if id_user != searching_id:
        await event.answer("ты кто такой? давай досвиданья.")
        return 
    else:
        if data[2] == "y":
            await event.edit("Вроде ты не бот. Можешь заходить.")
            del pending[chat_id][id_user]
            return
        s = "" # selected by user
        if data[2] == "1":
            s = "Арбуз"
        else:
            s = "Машина"
        await event.edit(f"Ответ был неверный. Был выбран: \"{s}\"")
client.run_until_disconnected()

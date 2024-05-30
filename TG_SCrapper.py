import configparser
import json
import asyncio
from datetime import datetime

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChannel

# Some functions to parse JSON date
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, bytes):
            return list(o)
        return json.JSONEncoder.default(self, o)

# Reading Configs
config = configparser.ConfigParser()
config.read("config.ini")

# Setting configuration values
api_id = '27097639'  # config['Telegram']['api_id']
api_hash = 'a7ca6c798ef5cfb178b5bee3de01b65a'  # config['Telegram']['api_hash']

api_hash = str(api_hash)

# Researcher data here
phone = '+421918707184'  # config['Telegram']['phone']
username = "ValorMaul"  # config['Telegram']['username'] #your username on telegram

# Create the client and connect
client = TelegramClient(phone, api_id, api_hash)

async def main(phone):
    await client.start()
    print("Client Created")
    # Ensure you're authorized
    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))

    me = await client.get_me()

    user_input_channel = input('Enter the channel username or ID: ')  # Prompt user for the channel

    if user_input_channel.isdigit():
        entity = PeerChannel(int(user_input_channel))
    else:
        entity = user_input_channel

    my_channel = await client.get_entity(entity)

    offset_id = 0
    limit = 100
    all_messages = []
    total_messages = 0
    total_count_limit = 0

    while True:
        print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
        history = await client(GetHistoryRequest(
            peer=my_channel,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            message_dict = message.to_dict()
            if my_channel.username:
                message_link = f"https://t.me/{my_channel.username}/{message.id}"
            else:
                message_link = f"https://t.me/c/{my_channel.id}/{message.id}"
            message_dict['message_link'] = message_link
            all_messages.append(message_dict)
        offset_id = messages[-1].id
        total_messages = len(all_messages)
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break

    with open('channel_messages.json', 'w') as outfile:
        json.dump(all_messages, outfile, cls=DateTimeEncoder)

with client:
    client.loop.run_until_complete(main(phone))

from nonebot import get_bot, on_message
from nonebot.typing import T_State
from nonebot.adapters import Bot
from nonebot.adapters.onebot.v11 import GroupMessageEvent, PrivateMessageEvent
from datetime import datetime

import os

import src.common.define as define

any_msg = on_message(
    priority=100,
    block=False
)


@any_msg.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    send_id_path = define.SEND_GROUP_ID_PATH / \
        f'{event.group_id}.{define.SEND_FILE_FORMAT}'
    if not send_id_path.exists():
        send_id_path.touch()

    user_info = await get_bot().call_api('get_group_member_info', **{
        'group_id': event.group_id,
        'user_id': event.user_id,
    })

    nickname = user_info['nickname']
    card = user_info['card']
    card = card if card else nickname
    user_id = user_info['user_id']
    time = datetime.now().strftime('%H:%M:%S')
    message = event.raw_message

    text = f'''
**{card}** _({nickname}) {user_id}_ : _{time}_  
- {message}

'''

    with open(define.RECV_GROUP_ID_PATH / f'{event.group_id}.{define.RECV_FILE_FORMAT}', 'a') as f:
        f.write(text)


@any_msg.handle()
async def _(bot: Bot, event: PrivateMessageEvent, state: T_State):
    send_id_path = define.SEND_USER_ID_PATH / \
        f'{event.user_id}.{define.SEND_FILE_FORMAT}'
    if not send_id_path.exists():
        send_id_path.touch()

    time = datetime.now().strftime('%H:%M:%S')
    message = event.raw_message

    text = f'''
_{time}_  
- {message}

'''

    with open(define.RECV_USER_ID_PATH / f'{event.user_id}.{define.RECV_FILE_FORMAT}', 'a') as f:
        f.write(text)

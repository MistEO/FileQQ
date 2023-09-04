from nonebot import get_bot, on_message, on
from nonebot.typing import T_State
from nonebot.adapters import Bot
from nonebot.adapters.onebot.v11 import GroupMessageEvent, PrivateMessageEvent, Event

from datetime import datetime

import src.common.define as define
from .utils import nbevent_2_mdmsg, avatar_html, get_nickname_in_group, get_friends_names


any_msg = on_message(priority=100, block=False)


@any_msg.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    await handle_group_message(bot, event, state)


async def handle_group_message(
    bot: Bot, event: Event, state: T_State, is_self: bool = False
):
    send_id_path = (
        define.SEND_GROUP_ID_PATH / f"{event.group_id}.{define.SEND_FILE_FORMAT}"
    )
    if not send_id_path.exists():
        send_id_path.touch()

    user_id = event.user_id
    avatar = avatar_html(user_id)
    card, nickname = await get_nickname_in_group(user_id, event.group_id)
    time = datetime.now().strftime("%H:%M:%S")
    message = await nbevent_2_mdmsg(event)

    text = f"""
**{card}** ({nickname}) {user_id} : _{time}_  
{avatar}
{message}

"""

    with open(
        define.RECV_GROUP_ID_PATH / f"{event.group_id}.{define.RECV_FILE_FORMAT}", "a", encoding="utf-8"
    ) as f:
        f.write(text)


@any_msg.handle()
async def _(bot: Bot, event: PrivateMessageEvent, state: T_State):
    await handle_private_message(bot, event, state)


async def handle_private_message(
    bot: Bot, event: Event, state: T_State, is_self: bool = False
):
    user_id = event.user_id if not is_self else event.target_id
    send_id_path = define.SEND_USER_ID_PATH / f"{user_id}.{define.SEND_FILE_FORMAT}"
    if not send_id_path.exists():
        send_id_path.touch()

    avatar = avatar_html(event.user_id)
    card = "我" if is_self else await get_friends_names(event.user_id)
    time = datetime.now().strftime("%H:%M:%S")
    message = await nbevent_2_mdmsg(event)

    text = f"""
**{card}** _{time}_  
{avatar}
{message}

"""
    with open(
        define.RECV_USER_ID_PATH / f"{user_id}.{define.RECV_FILE_FORMAT}", "a", encoding="utf-8"
    ) as f:
        f.write(text)


my_msg = on("message_sent", priority=100, block=False)


@my_msg.handle()
async def _(bot: Bot, event: Event, state: T_State):
    if event.message_type == "group":
        await handle_group_message(bot, event, state, True)
    elif event.message_type == "private":
        await handle_private_message(bot, event, state, True)

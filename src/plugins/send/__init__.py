from nonebot import get_bot, logger, require

import src.common.define as define
from .utils import walk_sender, text_2_msg, get_message_suffix


async def sync_group():
    message = walk_sender(define.SEND_GROUP_ID_PATH)
    if not message:
        return

    path, context = message
    group_id = path.stem
    message_suffix = get_message_suffix()

    # 先清空文件，避免重复发送
    with open(path, "w", encoding="utf-8") as f:
        pass

    context = text_2_msg(context + message_suffix)
    logger.info(f"发送群消息: {group_id}: {context}")
    await get_bot().call_api(
        "send_group_msg", **{"message": context, "group_id": group_id}
    )


async def sync_friend():
    message = walk_sender(define.SEND_USER_ID_PATH)
    if not message:
        return

    path, context = message
    user_id = path.stem
    message_suffix = get_message_suffix()

    # 先清空文件，避免重复发送
    with open(path, "w", encoding="utf-8") as f:
        pass

    context = text_2_msg(context + message_suffix)
    logger.info(f"发送私聊消息: {user_id}: {context}")
    await get_bot().call_api(
        "send_private_msg", **{"message": context, "user_id": user_id}
    )


send_sched = require("nonebot_plugin_apscheduler").scheduler


@send_sched.scheduled_job("interval", seconds=2)
async def send_message():
    await sync_group()
    await sync_friend()

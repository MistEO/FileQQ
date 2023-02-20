from nonebot import get_bot, on_message, logger, require

import os
from pathlib import Path
from datetime import datetime

import src.common.define as define


def walk_sender(dir_path):
    if not dir_path.exists():
        return None

    for file in os.listdir(dir_path):
        path = os.path.join(dir_path, file)
        if not os.path.getsize(path) or not Path(path).stem.isdigit():
            continue
        with open(path, 'r') as f:
            context = f.read()
            if context.endswith('\n\n'):
                return path, context[:-2]
            elif context.endswith('#'):
                return path, context[:-1]
            else:
                # 正在输入中
                pass
    return None


async def sync_group():
    message = walk_sender(define.SEND_GROUP_ID_PATH)
    if not message:
        return

    path, context = message
    group_id = Path(path).stem

    # 先清空文件，避免重复发送
    with open(path, 'w') as f:
        pass

    logger.info(f'发送群消息: {group_id}: {context}')
    await get_bot().call_api('send_group_msg', **{
        'message': context,
        'group_id': group_id
    })

    time = datetime.now().strftime('%H:%M:%S')
    text = f'''
**我** : _{time}_  
- {context}

'''
    with open(define.RECV_GROUP_ID_PATH / f'{group_id}.{define.RECV_FILE_FORMAT}', 'a') as f:
        f.write(text)


async def sync_friend():
    message = walk_sender(define.SEND_USER_ID_PATH)
    if not message:
        return

    path, context = message
    user_id = Path(path).stem

    # 先清空文件，避免重复发送
    with open(path, 'w') as f:
        pass

    logger.info(f'发送私聊消息: {user_id}: {context}')
    await get_bot().call_api('send_private_msg', **{
        'message': context,
        'user_id': user_id
    })

    time = datetime.now().strftime('%H:%M:%S')
    text = f'''
**我** : _{time}_
- {context}

'''
    with open(define.RECV_USER_ID_PATH / f'{user_id}.{define.RECV_FILE_FORMAT}', 'a') as f:
        f.write(text)


send_sched = require('nonebot_plugin_apscheduler').scheduler


@send_sched.scheduled_job('interval', seconds=2)
async def send_message():
    await sync_group()
    await sync_friend()

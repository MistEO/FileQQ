from nonebot import get_bot, on_message
from nonebot.rule import Rule

import os
import shutil

import src.common.define as define


def make_dirs():
    shutil.rmtree(define.RECV_GROUP_NAME_PATH, ignore_errors=True)
    shutil.rmtree(define.RECV_GROUP_MEMO_PATH, ignore_errors=True)
    shutil.rmtree(define.RECV_USER_NAME_PATH, ignore_errors=True)
    shutil.rmtree(define.RECV_USER_MEMO_PATH, ignore_errors=True)

    shutil.rmtree(define.SEND_GROUP_NAME_PATH, ignore_errors=True)
    shutil.rmtree(define.SEND_GROUP_MEMO_PATH, ignore_errors=True)
    shutil.rmtree(define.SEND_USER_NAME_PATH, ignore_errors=True)
    shutil.rmtree(define.SEND_USER_MEMO_PATH, ignore_errors=True)

    os.makedirs(define.RECV_GROUP_ID_PATH, exist_ok=True)
    os.makedirs(define.RECV_GROUP_NAME_PATH, exist_ok=True)
    os.makedirs(define.RECV_GROUP_MEMO_PATH, exist_ok=True)

    os.makedirs(define.RECV_USER_ID_PATH, exist_ok=True)
    os.makedirs(define.RECV_USER_NAME_PATH, exist_ok=True)
    os.makedirs(define.RECV_USER_MEMO_PATH, exist_ok=True)

    os.makedirs(define.SEND_GROUP_ID_PATH, exist_ok=True)
    os.makedirs(define.SEND_GROUP_NAME_PATH, exist_ok=True)
    os.makedirs(define.SEND_GROUP_MEMO_PATH, exist_ok=True)

    os.makedirs(define.SEND_USER_ID_PATH, exist_ok=True)
    os.makedirs(define.SEND_USER_NAME_PATH, exist_ok=True)
    os.makedirs(define.SEND_USER_MEMO_PATH, exist_ok=True)


async def sync_groups():
    group_infos = await get_bot().call_api('get_group_list', **{})
    for group_info in group_infos:
        group_id = group_info['group_id']
        group_name = group_info['group_name'].replace('/', '_')
        group_memo = group_info['group_memo'].replace(
            '/', '_') if 'group_memo' in group_info else group_name

        send_id_path = define.SEND_GROUP_ID_PATH / \
            f'{group_id}.{define.SEND_FILE_FORMAT}'
        # send_id_path.touch(exist_ok=True)
        os.symlink(send_id_path.absolute(), define.SEND_GROUP_NAME_PATH /
                   f'{group_name}_{group_id}.{define.SEND_FILE_FORMAT}')
        os.symlink(send_id_path.absolute(), define.SEND_GROUP_MEMO_PATH /
                   f'{group_memo}_{group_id}.{define.SEND_FILE_FORMAT}')

        recv_id_path = define.RECV_GROUP_ID_PATH / \
            f'{group_id}.{define.RECV_FILE_FORMAT}'
        send_relpath = os.path.relpath(send_id_path, recv_id_path.parent)
        with open(recv_id_path, 'w') as f:
            f.write(
                f'## {group_memo} ({group_name}) {group_id}\n\n[回复]({send_relpath})\n\n')
        os.symlink(recv_id_path.absolute(), define.RECV_GROUP_NAME_PATH /
                   f'{group_name}_{group_id}.{define.RECV_FILE_FORMAT}')
        os.symlink(recv_id_path.absolute(), define.RECV_GROUP_MEMO_PATH /
                   f'{group_memo}_{group_id}.{define.RECV_FILE_FORMAT}')


async def sync_friends():
    friend_infos = await get_bot().call_api('get_friend_list', **{})
    for friend_info in friend_infos:
        user_id = friend_info['user_id']
        nickname = friend_info['nickname'].replace('/', '_')
        remark = friend_info['remark'].replace(
            '/', '_') if 'remark' in friend_info else nickname

        send_id_path = define.SEND_USER_ID_PATH / \
            f'{user_id}.{define.SEND_FILE_FORMAT}'
        # send_id_path.touch(exist_ok=True)
        os.symlink(send_id_path.absolute(), define.SEND_USER_NAME_PATH /
                   f'{nickname}_{user_id}.{define.SEND_FILE_FORMAT}')
        os.symlink(send_id_path.absolute(), define.SEND_USER_MEMO_PATH /
                   f'{remark}_{user_id}.{define.SEND_FILE_FORMAT}')

        recv_id_path = define.RECV_USER_ID_PATH / \
            f'{user_id}.{define.RECV_FILE_FORMAT}'
        send_relpath = os.path.relpath(send_id_path, recv_id_path.parent)
        with open(recv_id_path, 'w') as f:
            f.write(
                f'## {remark} ({nickname}) {user_id}\n\n[回复]({send_relpath})\n\n')
        os.symlink(recv_id_path.absolute(), define.RECV_USER_NAME_PATH /
                   f'{nickname}_{user_id}.{define.RECV_FILE_FORMAT}')
        os.symlink(recv_id_path.absolute(), define.RECV_USER_MEMO_PATH /
                   f'{remark}_{user_id}.{define.RECV_FILE_FORMAT}')


inited = False


async def to_init(bot, event, state) -> bool:
    return not inited


any_msg = on_message(
    priority=0,
    block=False,
    rule=Rule(to_init)
)


@any_msg.handle()
async def _(bot, event, state):
    global inited
    if inited:
        return

    inited = True
    make_dirs()
    await sync_groups()
    await sync_friends()

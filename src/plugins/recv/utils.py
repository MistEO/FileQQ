from nonebot import get_bot
from nonebot.adapters.onebot.v11 import Event

import httpx
from pathlib import Path

import src.common.define as define
from .config import image_enabled, avatar_enabled


def avatar_html(user_id: int, size: int = 32) -> str:
    if avatar_enabled:
        return f'<img src="https://q1.qlogo.cn/g?b=qq&nk={user_id}&s=640" width = "{size}" height = "{size}"/> '
    else:
        return ''


def image_html(path: Path, scale: str = '30%') -> str:
    return f'<img src="{path.absolute()}" width = "{scale}"/>'


async def nbevent_2_mdmsg(event: Event) -> str:
    result = ''
    for seg in event.message:
        if seg.type == 'image':
            # 下载图片
            url = seg.data['url']
            filename = seg.data['file']
            path = (define.RECV_IMAGE_PATH / filename).with_suffix('.png')
            if not path.exists():
                async with httpx.AsyncClient() as client:
                    r = await client.get(url)
                    with open(path, 'wb') as f:
                        f.write(r.content)
            # 生成图片链接
            if image_enabled:
                result += image_html(path)
            else:
                result += f'[IMAGE](/{path})'
        elif seg.type == 'at':
            at_qq = seg.data["qq"]
            at_info = await get_bot().call_api('get_group_member_info', **{
                'group_id': event.group_id,
                'user_id': at_qq,
            })
            nickname = at_info['nickname']
            card = at_info['card']
            card = card if card else nickname
            result += f'@{card} {avatar_html(at_qq)}'
        else:
            result += str(seg)

        result += ' '

    return result

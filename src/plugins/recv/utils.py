from nonebot import get_bot
from nonebot.adapters.onebot.v11 import Event, MessageSegment

import httpx
from pathlib import Path
from typing import Tuple

import src.common.define as define
from src.common.config import recv_image_enabled, recv_avatar_enabled


def avatar_html(user_id: int, size: int = 32) -> str:
    if recv_avatar_enabled:
        return f'<img src="https://q1.qlogo.cn/g?b=qq&nk={user_id}&s=640" width = "{size}" height = "{size}"/> '
    else:
        return ""


def image_html(path: Path, scale: str = "30%") -> str:
    return f'<img src="{path.absolute()}" width = "{scale}"/>'


async def get_nickname_in_group(user_id: int, group_id: int) -> Tuple[str, str]:
    user_info = await get_bot().call_api(
        "get_group_member_info",
        **{
            "group_id": group_id,
            "user_id": user_id,
        },
    )

    def name_replace(name: str) -> str:
        # 简单弄下防注入
        return name.replace("/", "").replace("\\", "").replace("$$", "")

    nickname = name_replace(user_info["nickname"])
    card = name_replace(user_info["card"])
    card = card if card else nickname

    return card, nickname


async def nbevent_2_mdmsg(event: Event) -> str:
    result = ""
    for seg in event.message:
        if isinstance(seg, dict):
            # for message_sent
            seg = MessageSegment(**seg)

        if seg.type == "image":
            # 下载图片
            url = seg.data["url"]
            filename = seg.data["file"]
            path = (define.RECV_IMAGE_PATH / filename).with_suffix(".png")
            if not path.exists():
                async with httpx.AsyncClient() as client:
                    r = await client.get(url)
                    with open(path, "wb") as f:
                        f.write(r.content)
            # 生成图片链接
            if recv_image_enabled:
                result += image_html(path)
            else:
                result += f"[IMAGE](/{path})"
            result += f"  <!-- {seg} -->"

        elif seg.type == "at":
            at_qq = seg.data["qq"]
            card, _ = await get_nickname_in_group(at_qq, event.group_id)
            result += f"@**{card}** {avatar_html(at_qq)}"

        elif seg.type == "reply":
            reply_text = seg.data["text"]
            result += f"> {reply_text}\n\n"

        elif not str(seg).strip():
            result += f"`{seg}`"

        result += "  "

    return result

from pathlib import Path
import re


def walk_sender(dir_path: Path):
    if not dir_path.exists():
        return None

    for path in dir_path.iterdir():
        if not path.stat().st_size or not path.stem.isdigit():
            continue

        with open(path, "r", encoding="utf-8") as f:
            context = f.read()
        if not context:
            continue

        if context.endswith("\n\n"):
            return path, context[:-2]
        elif context.endswith("#"):
            return path, context[:-1]
        # else 正在输入中

    return None


def text_2_msg(text: str) -> str:
    text = text.strip()
    if "@" not in text:
        return text

    def replace_at(match):
        return f"[CQ:at,qq={match.group(1)}]"

    return re.sub(r"@(\d+)", replace_at, text)

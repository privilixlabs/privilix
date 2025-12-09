import re
import datetime


def time_parser(text: str) -> datetime.timedelta | None:
    parts = re.findall(r"(\d+)([smhd])", text.lower())
    if not parts:
        return None

    total = datetime.timedelta()

    for val, unit in parts:
        val = int(val)
        if unit == "s":
            total += datetime.timedelta(seconds=val)
        elif unit == "m":
            total += datetime.timedelta(minutes=val)
        elif unit == "h":
            total += datetime.timedelta(hours=val)
        elif unit == "d":
            total += datetime.timedelta(days=val)

    return total

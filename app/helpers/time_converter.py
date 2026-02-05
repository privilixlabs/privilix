import re


def time_converter(text: str) -> int | None:
    parts = re.findall(r"(\d+)([smhd])", text.lower())
    if not parts:
        return None

    total = 0
    for val, unit in parts:
        val = int(val)
        if unit == "s":
            total += val
        elif unit == "m":
            total += val * 60
        elif unit == "h":
            total += val * 3600
        elif unit == "d":
            total += val * 3600 * 24

        return total

from request_dto import Subtitle


def make_subscription(subtitles: list[Subtitle]) -> str:
    result: str = ""

    for sub in subtitles:
        result += f"{__second_to_hhmmss(sub.start)} ~ {__second_to_hhmmss(sub.end)}\n"
        result += f"{sub.subtitle}\n"
        result += "\n"

    return result


def hhmmss_to_seconds(hhmmss: str) -> int:
    hhmmss_list = hhmmss.split(':')

    hh: int = int(hhmmss_list[0])
    mm: int = int(hhmmss_list[1])
    ss: int = int(hhmmss_list[2])

    return hh*3600 + mm*60 + ss


def __second_to_hhmmss(total_second: int) -> str:
    hour: int = total_second // 3600
    minute: int = total_second % 3600 // 60
    second: int = total_second % 60

    hh: str = __add_zero_if_length_is_one(hour)
    mm: str = __add_zero_if_length_is_one(minute)
    ss: str = __add_zero_if_length_is_one(second)

    return f"{hh}:{mm}:{ss}"


def __add_zero_if_length_is_one(time: int) -> str:
    if 0 <= time <= 9:
        return f"0{time}"
    return f"{time}"
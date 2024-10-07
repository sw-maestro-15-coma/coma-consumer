
class SecondFormatter:
    @classmethod
    def convert_to_hhmmss(cls, second: int) -> str:
        hours: int = second // 3600
        minutes: int = second // 60
        seconds: int = second % 60

        hh: str = cls.__number_to_str(hours)
        mm: str = cls.__number_to_str(minutes)
        ss: str = cls.__number_to_str(seconds)

        return f"{hh}:{mm}:{ss}"


    @classmethod
    def convert_to_hhmmss_mmm(cls, second: int) -> str:
        hhmmss: str = cls.convert_to_hhmmss(second)

        return f"{hhmmss},000"


    @staticmethod
    def __number_to_str(number: int) -> str:
        if 0 <= number <= 9:
            return f"0{number}"
        return f"{number}"
import random
import string
from datetime import datetime


def add_am_pm_indicator(time_str: str) -> str:
    time_obj = datetime.strptime(time_str, "%H:%M")
    return time_obj.strftime("%I:%M%p")


def generate_random_digit_string(len: int = 6) -> str:
    return "".join(random.choices(string.digits, k=len))

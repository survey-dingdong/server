import random
import string
from datetime import datetime


def generate_random_uppercase_letters() -> str:
    return "".join(random.choices(string.ascii_uppercase, k=4))


def add_am_pm_indicator(time_str: str) -> str:
    time_obj = datetime.strptime(time_str, "%H:%M")
    return time_obj.strftime("%I:%M%p")

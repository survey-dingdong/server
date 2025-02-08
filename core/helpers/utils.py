import random
import string
from datetime import datetime


def add_am_pm_indicator(time_obj: datetime) -> str:
    return time_obj.strftime("%I:%M%p")


def generate_random_digit_string(len: int = 6) -> str:
    return "".join(random.choices(string.digits, k=len))


def get_random_color() -> str:
    colors = ["#3F57FD", "#DB5654", "#613EE2", "#FD3F78", "#F08F1D", "#24A29A"]
    return random.choice(colors)

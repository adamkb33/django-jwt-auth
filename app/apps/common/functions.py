import random

from apps.common.constants import MONTHS_NORWEGIAN, DAYS_NORWEGIAN


def to_norwegian_datetime(date_obj):
    norwegian_month = MONTHS_NORWEGIAN[date_obj.month]
    norwegian_day = DAYS_NORWEGIAN[date_obj.isoweekday()]
    norwegian_time = date_obj.strftime('%H:%M')

    norwegian_datetime = f"{norwegian_month}, {date_obj.day} {norwegian_day}, {date_obj.year} kl. {norwegian_time}"

    return norwegian_datetime


def generate_six_digit_number():
    return random.randint(100000, 999999)

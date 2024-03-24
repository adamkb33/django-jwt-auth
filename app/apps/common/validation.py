import re


def validate_norwegian_mobile_number(mobile_number: str):
    """
    Validates if a mobile number is a valid Norwegian mobile number.
    Norwegian mobile numbers start with 4 or 9 and have 8 digits in total.
    """
    pattern = r"^(4|9)\d{7}$"
    return re.match(pattern, mobile_number) is not None


def validate_otc(otc: str):
    """
    Validates if a code is a valid 6-digit One-Time Code (OTC).
    The code must consist of exactly 6 digits.
    """
    pattern = r"^\d{6}$"
    return re.match(pattern, otc) is not None

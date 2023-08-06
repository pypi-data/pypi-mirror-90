import json
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

data = {}


def load(locale):
    """
    Loads the specified locale from a json file and stores in the data dict
    """
    global data
    available_locales = ("en",)

    if locale not in available_locales:
        raise ValueError(
            f"""Locale must be one of the avalable options: {", ".join(available_locales)}"""
        )

    with open(os.path.join(dir_path, f"{locale}.json")) as json_file:
        data[locale] = json.load(json_file)


def get_nationality(code, locale="en"):
    """
    Get the nationatlity for `code`

    Parameters:
    - code (str): 2 letter iso-3166-1 country code
    - locale (str): 2 letter locale code. (only availtable option is "en" which is also the default)

    Returns:
    - str: The nationality for the country code
    """
    global data
    if locale not in data:
        load(locale)
    return data[locale]["nationalities"][code.upper()]


def get_country(code, locale="en"):
    """
    Get the country for `code`

    Parameters:
    - code (str): 2 letter iso-3166-1 country code
    - locale (str): 2 letter locale code. (only availtable option is "en" which is also the default)

    Returns:
    - str: The country name for the country code
    """
    global data
    if locale not in data:
        load(locale)
    return data[locale]["countries"][code.upper()]

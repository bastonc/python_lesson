import csv
import random
import string
import requests
import pandas as pd

from faker import Faker
from http import HTTPStatus

from const import const


def db_answer_to_string(input_list: list, headers: list) -> str:
    out_string = '<table border="1" cellpadding="5" cellspacing="0">'
    out_string += '<tr>'
    for header in headers:
        out_string += f'<td align="center"><strong>{header}</strong></td>'
    out_string += '</tr>'
    for el in input_list:
        out_string += '<tr>'
        for field in el:
            out_string += f'<td>{field if field is not None else " - "}</td>'
        out_string += '</tr>'
    out_string += '</table>'
    return out_string


def object_to_str(students_object: list) -> str:
    """
    Formater data from object (list with dictionary) to HTML table
    :param students_object: list with dict - info about students
    :return: string - HTML table
    """
    outstring = f'<table border=1, cellspacing=0 cellpadding=5><tr><td align="center">#</td><td align="center">First Name</td>\
	<td align="center">Last name</td><td align="center">E-mail</td><td align="center">Password</td><td align="center">Birthday</td></tr>'
    for index, student in enumerate(students_object, start=1):
        outstring += f'<tr><td>{index}</td><td>{student["first_name"]}</td><td>{student["last_name"]}</td>\
		<td>{student["email"]}</td><td>{student["password"]}</td><td>{student["birthday"]}</td></tr>'
    outstring += '</table>'
    return outstring


def password_generator(long_pass: int) -> str:
    """
    Function of password generated
    :param long_pass: integer dugit - long password
    :return: string - password
    """
    passwrd = ''.join(
        random.choice(string.punctuation + string.ascii_letters + string.digits) for _ in range(long_pass))
    clean_pass = passwrd.replace('<', '&lt;')
    return clean_pass


def get_statistic_from_csv(file_name: str) -> dict:
    """
    Read data from hw.csv (hardcode), calculate the average at weight, height
    :return: dict
    """
    reader = pd.read_csv(file_name)
    avg = reader.mean()
    return {'avg_weight': round(avg[' Weight(Pounds)'], 2),
            'avg_height': round(avg[' Height(Inches)'], 2),
            'len': len(reader)}


def object_to_csv(students: list, file_name: str) -> None:
    """
    Write students info into csv file
    :param students: list with dicts - data for students
    :param file_name: file name for save to disk
    :return: None
    """
    df = pd.DataFrame(students)
    df.to_csv(file_name, index=False)


def persons_generator(amount: int, country_code: str) -> object:
    """
    Generate data about person by Faker
    :param amount: amount person
    :param country_code: code by locale
    :return: list with dicts with data about person
    """
    # Fields: first_name, last_name, email, password, birthday
    fake = Faker(country_code)
    return [{'first_name': fake.first_name(),
             'last_name': fake.last_name(),
             'email': fake.email(),
             'password': fake.password(),
             'birthday': fake.date_between(start_date="-40y", end_date="-18y")} for _ in range(amount)]


def get_bitcoin_value(currency: str) -> dict | bool:
    """
    Get BTC rate and add symbol of currency
    ----------------
    format answer API:
    Error currency - {"error": "\"BLAH-BLAH\" is not a valid currency."}
    Correct answer - {"data":{"code":"USD","name":"US Dollar","rate":19822.26}}
    ----------------
    :param currency: string - currency code (USD, EUR etc.)
    :return: dict or False
    """
    headers = {'X-Accept-Version': '2.0.0', 'Content-type': 'application/json'}
    bitcoin_rate_answer = requests.get(const.API_BTC_RATE + currency.lower(), headers=headers)
    if bitcoin_rate_answer.status_code != HTTPStatus.OK:
        return False
    if const.API_ERROR_KEY in bitcoin_rate_answer.json():
        return bitcoin_rate_answer.json()
    bitcoin_rate_dict = bitcoin_rate_answer.json()[const.API_COMPLETE_KEY]
    symbol = get_currency_symbol(currency)
    bitcoin_rate_dict['symbol'] = symbol if symbol is not None else ''
    return bitcoin_rate_dict


def get_currency_symbol(curr: str) -> object | str:
    """
    Get symbol of currency
    :param curr: string - currency code
    :return: string - symbol of currency
    """
    headers = {'X-Accept-Version': '2.0.0', 'Content-type': 'application/json'}
    symbols_list = requests.get(url=const.API_BTC_SYMBOL, headers=headers)
    # If we can't get symbol - return empty string (noncritical data)
    if symbols_list.status_code != HTTPStatus.OK:
        return ''
    return [symbol_dict['symbol'] for symbol_dict in symbols_list.json()['data'] if symbol_dict['code'] == curr][0]


def buy_btc(rate_dict: dict, summ: int):
    """
    Calculate exchange currency to BTC
    :param rate_dict: dictionary with rate
    :param summ: how money exchange in user currency
    :return: float
    """
    exchange = summ / rate_dict['rate']
    return round(exchange, 4)


def paramaters_to_db_condition(parameters: dict) -> str:
    db_rules_on_query = ''  # if not have parameters return empty string
    if parameters:
        db_rules_on_query = ' WHERE ' + ' AND '.join(f'{key}=?' for key in parameters.keys())
    return db_rules_on_query

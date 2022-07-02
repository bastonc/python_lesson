import csv
import random
import string

import pandas as pd

from faker import Faker


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


def gen_pass(long_pass: int) -> str:
	"""
	Function of password generated
	:param long_pass: integer dugit - long password
	:return: string - password
	"""
	passwrd = ''.join(
		random.choice(string.punctuation + string.ascii_letters + string.digits) for _ in range(long_pass))
	clean_pass = passwrd.replace('<', '&lt;')
	return clean_pass


def read_csv() -> dict:
	"""
	Read data from hw.csv (hardcode), calculate the average at weight, height
	:return: dict
	"""
	reader = pd.read_csv('hw.csv')
	avg = reader.mean()
	return {'avg_weight': round(avg[' Weight(Pounds)'], 2),
			'avg_height': round(avg[' Height(Inches)'], 2),
			'len': len(reader)}


def store_to_csv(students: list, file_name: str) -> None:
	"""
	Write students info into csv file
	:param students: list with dicts - data for students
	:param file_name: file name for save to disk
	:return: None
	"""
	with open(file_name + '.csv', 'w', newline='') as csv_f:
		fieldnames = students[0].keys()
		writer = csv.DictWriter(csv_f, fieldnames=fieldnames)
		writer.writeheader()
		for item_dict in students:
			writer.writerow(item_dict)


def generate_person(amount: int, country_code: str) -> object:
	"""
	Generate data about person by Faker
	:param amount: amount person
	:param country_code: code by locale
	:return: list with dicts with data about person
	"""
	# first_name, last_name, email, password, birthday
	fake = Faker(country_code)
	return [{'first_name': fake.first_name(),
			 'last_name': fake.last_name(),
			 'email': fake.email(),
			 'password': fake.password(),
			 'birthday': fake.date_between(start_date="-40y", end_date="-18y")} for _ in range(amount)]


def get_bitcoin_value():
	# https://bitpay.com/api/rates
	# /bitcoin_rate?currency=UAH
	# input parameter currency code
	# default is USD
	# return value currency of bitcoin
	# * https://bitpay.com/api/
	# * return symbol of input currency code
	# * add one more input parameter count and multiply by currency (int)
	pass

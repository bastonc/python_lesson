import random
import string
import pandas


def gen_pass(long_pass: int) -> str:
	passwrd = ''.join(random.choice(string.punctuation + string.ascii_letters + string.digits) for _ in range(long_pass))
	clean_pass = passwrd.replace('<', '&lt;')
	return clean_pass


def read_csv():
	reader = pandas.read_csv('hw.csv')
	avg = reader.mean()
	return {'avg_weight': round(avg[' Weight(Pounds)'], 2),
			'avg_height': round(avg[' Height(Inches)'], 2),
			'len': len(reader)}

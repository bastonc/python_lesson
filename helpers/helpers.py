import decimal
import random
import re
import pandas as pd


def gen_pass(long_pass: int) -> str:
	while 1:
		passwrd = str(''.join(list(map(chr, [random.randint(33, 122) for _ in range(long_pass)]))))
		if re.search('[a-z]', passwrd) and re.search('[A-Z]', passwrd) and re.search('[0-9]', passwrd) and \
				re.search('[\?,>.!#$\`%^&@"\':\;*()_/\-+\\=\]\[]*', passwrd) and not re.search('[<{]', passwrd):
			return passwrd
		print(passwrd)


def read_csv():
	reader = pd.read_csv('hw.csv')
	sum_height = 0
	sum_weight = 0
	for line in range(len(reader)):
		sum_height += decimal.Decimal(reader[' Height(Inches)'][line])
		sum_weight += decimal.Decimal(reader[' Weight(Pounds)'][line])
	return {'avg_weight': round(sum_weight / len(reader), 2),
	        'avg_height': round(sum_height / len(reader), 2),
	        'len': len(reader)}

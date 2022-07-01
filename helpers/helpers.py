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
	avg = reader.mean()
	return {'avg_weight': round(avg[' Weight(Pounds)'], 2),
	        'avg_height': round(avg[' Height(Inches)'], 2),
	        'len': len(reader)}

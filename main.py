import random


from helpers.helpers import gen_pass, read_csv, generate_person, store_to_csv, object_to_str

from http import HTTPStatus

from webargs import fields, validate
from webargs.flaskparser import use_kwargs
from flask import Flask, request, jsonify


app = Flask(__name__)

@app.errorhandler(HTTPStatus.UNPROCESSABLE_ENTITY)
@app.errorhandler(HTTPStatus.BAD_REQUEST)
def error_handler(error):
	"""
	Error processing
	:param error:
	:return: object
	"""
	headers = error.data.get('headers', None)
	messages = error.data.get('messages', ['incorrect request'])
	if headers:
		return jsonify({'errors': messages}, headers, error.code)
	else:
		return jsonify({'errors': messages}, error.code)

@app.route('/')
def index():
	"""
	Index function
	:return:
	"""
	return '<p> /pass - generated password</p><p>/csv - work from CSV file</p>\
	<p>/students?amount=3&country=EN&file=Student - list students (store to csv)</p>\
	<p>/btc?currency=USD&change=100 - course and exchange BTC</p>'


@app.route('/pass')
def password():
	"""
	Entry point for route /pass
	(Generating password)
	:return: string
	"""
	len_pass = random.randint(10, 20)
	passwrd = gen_pass(len_pass)  # use clean function for generated password
	return f'<p>Password long: {len_pass}</p>Password: {passwrd}'


@app.route('/csv')
def average_csv():
	"""
	Entry point for route /csv
	(Reading from csv and calculating average)
	:return: string
	"""
	avg_data = read_csv()
	return f"<p>All records in files: {avg_data['len']}</p><p>Average Height(Inches): {avg_data['avg_height']}</p><p>Average Weight(Pounds): {avg_data['avg_weight']}</p>"


@app.route('/students')
@use_kwargs(
	{
		'amount': fields.Int(missing=1, validate=[validate.Range(min=1, max=1000)]),
		'country': fields.Str(missing='UK', validate=[validate.Length(2)]),
		'file': fields.String(required=True, validate=[validate.Length(max=12), validate.Regexp('^\w+$')])
	},
	location='query'
)
def generate_students(amount, country, file):
	"""
	Entry point for /students with parameters
	(Adding functionality generating students, save data to file and  output on client by formatted HTML string)
	:param amount:
	:param country:
	:param file:
	:return:
	"""
	students = generate_person(amount=amount, country_code=country)
	store_to_csv(students, file)
	outstring = object_to_str(students)
	return outstring


if __name__ == '__main__':
	app.run(host="127.0.0.1", port=8080, debug=True)

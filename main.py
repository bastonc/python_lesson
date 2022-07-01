from flask import Flask
from helpers.helpers import gen_pass, read_csv
import random

app = Flask(__name__)


@app.route('/')
def index():
	return '<p> /pass - generated password</p><p>/csv - work from CSV file</p>'


@app.route('/pass')
def password():
	len_pass = random.randint(10, 20)
	passwrd = gen_pass(len_pass)  # use clean function for generated password
	return f'<p>Password long: {len_pass}</p><p>Password: {passwrd}</p>'


@app.route('/csv')
def average_csv():
	avg_data = read_csv()
	return f"<p>All records in files: {avg_data['len']}</p><p>Average Height(Inches): {avg_data['avg_height']}</p><p>Average Weight(Pounds): {avg_data['avg_weight']}</p>"


if __name__ == '__main__':
	app.run(host="127.0.0.1", port=8080, debug=True)

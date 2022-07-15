import random


from http import HTTPStatus

from webargs import fields, validate
from webargs.flaskparser import use_kwargs
from flask import Flask, request, jsonify

from helpers.helpers import password_generator, get_statistic_from_csv, persons_generator, object_to_csv, object_to_str, \
	get_bitcoin_value, buy_btc, db_answer_to_string, paramaters_to_db_condition
from helpers.database_handler import db_handler
from helpers import query
from point import Point
from circle import Circle

from const import const

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
def index_page() -> str:
	"""
	Entry point for route /
	(Index page)
	:return:
	"""
	return '<p> /password - generated password</p><p>/statistic - work from CSV file</p>\
	<p>/students?amount=3&country=EN&file=Student - list students (store to csv)</p>\
	<p>/bitcoin_rate?currency=USD&change=100 - course and exchange BTC</p> \
	<p>/order-price - get order price for all countries. /order-price?country=USA - for get order price for USA</p>\
	<p>/track-info?trackId=22 - get information about trackId </p> \
	<p> /full-time - get full time for all track  \
	<p> /circle?circle_x=10&circle_y=10&radius=6&point_x=16&point_y=16 - Point into circle'


@app.route('/password')
def generate_password() -> str:
	"""
	Entry point for route /pass
	(Generating password)
	:return: string
	"""
	len_password = random.randint(10, 20)
	password = password_generator(len_password)  # use clean function for generated password
	return f'<p>Password long: {len_password}</p>Password: {password}'


@app.route('/statistic')
def average_statistic() -> str:
	"""
	Entry point for route /statistic
	(Reading from csv and calculating average)
	:return: string
	"""
	statistic = get_statistic_from_csv(const.CSV_NAME)
	return f"<p>All records in files: {statistic['len']}</p><p>Average Height(Inches): {statistic['avg_height']}</p>\
	<p>Average Weight(Pounds): {statistic['avg_weight']}</p>"


@app.route('/students')
@use_kwargs(
	{
		'amount': fields.Int(load_default=1, validate=[validate.Range(min=1, max=1000)]),
		'country': fields.Str(load_default='UK', validate=[validate.Length(2)]),
		'file': fields.Str(required=True, validate=[validate.Length(max=12), validate.Regexp('^\w+$')])
	},
	location='query'
)
def generate_students(amount: int, country: str, file: str) -> str:
	"""
	Entry point for /students with parameters
	(Adding functionality generating students, save data to file and  output on client by formatted HTML string)
	:param amount:
	:param country:
	:param file:
	:return:
	"""
	students = persons_generator(amount=amount, country_code=country)
	object_to_csv(students, file)
	out_string = object_to_str(students)
	return out_string


@app.route('/bitcoin_rate')
@use_kwargs(
	{
		'currency': fields.Str(missing='USD', validate=[validate.Length(max=4)]),
		'change': fields.Int(missing=None)
	},
	location='query'
)
def bitcoin_exchange(currency: str, change: int) -> str:
	"""
	Entry point for /bitcoin_rate with parameters
	(Get bitcoin rate and exchange calculation user currency to BTC)
	:param currency: currency code (ex. USD, EUR)
	:param change: integer how money exchange
	:return: string
	"""
	bitcoin_rate_dict = get_bitcoin_value(currency)
	if not bitcoin_rate_dict:
		return f"Error connection to {const.BTC_RATE_API}"
	elif 'error' in bitcoin_rate_dict:
		return f"Error: {bitcoin_rate_dict['error']}"
	if change:
		exchange_finally_sum = buy_btc(rate_dict=bitcoin_rate_dict, summ=change)
	return f'<p>Exchange rate:<br> 1 BTC = {bitcoin_rate_dict["symbol"]}{bitcoin_rate_dict["rate"]}  [{currency}]</p>\
	<p>{str(f"Exchange: {change} {currency} = {exchange_finally_sum} BTC") if change else str("For exchange use parameter change=100")}</p>'


@app.route('/order-price')
@use_kwargs(
	{
		'country': fields.Str(missing=None, validate=[validate.Length(min=3, max=20)])
	},
	location='query'
)
def order_price(country: str) -> str:
	"""
	Entry point for /order-price
	Without parameter get order price by countries.
	With parameter 'country=' - get order price for country
	:param country: str - country-code
	:return: str
	"""
	fields_query = {}
	if country:
		query_str = query.get_total_sale()
		fields_query['BillingCountry'] = country
		query_str += paramaters_to_db_condition(fields_query)
	else:
		query_str = query.get_total_sale() + 'GROUP BY BillingCountry'
	result_from_base = db_handler(query_str, args=tuple(fields_query.values()))
	out_str = db_answer_to_string(result_from_base, ['Country', 'Total'])
	return out_str


@app.route('/track-info')
@use_kwargs(
	{
		'trackId': fields.Int(required=True, validate=[validate.Range(min=1, max=100000)])
	},
	location='query'
)
def get_all_info_about_track(trackId: int) -> str:
	"""
		Entry point for /track-info
		Accepts input parameter 'trackId=' with track id and get all information about track
		:param trackId: int - id of track
		:return: str
		"""
	fields_query = {}
	query_str = query.get_full_info_track()
	fields_query['tracks.TrackId'] = trackId
	query_str += paramaters_to_db_condition(fields_query)
	result_from_base = db_handler(query_str, args=tuple(fields_query.values()))
	out_str = db_answer_to_string(result_from_base, ['Artist', ' Title', 'Lenght', 'Album', 'Composer',
													 'Genre', 'Bytes', 'Media format', 'Price', 'Quantity',
													 'Total'])
	return out_str


@app.route('/full-time')
def get_all_time_about_track() -> str:
	"""
	Entry point for /full-time
	Get time for all track in table 'tracks'
	:return: str
	"""
	query_str = query.get_time_all_tracks()
	result_from_base = db_handler(query_str)
	out_str = db_answer_to_string(result_from_base, ['Total time for All tracks <br> (H:M:S)'])
	return out_str

@app.route('/circle')
@use_kwargs(
	{
		'circle_x': fields.Int(required=True, validate=[validate.Range(min=1, max=10000)]),
		'circle_y': fields.Int(required=True, validate=[validate.Range(min=1, max=10000)]),
		'radius': fields.Int(required=True, validate=[validate.Range(min=1, max=10000)]),
		'point_x': fields.Int(required=True, validate=[validate.Range(min=1, max=10000)]),
		'point_y': fields.Int(required=True, validate=[validate.Range(min=1, max=10000)]),
	},
	location='query'
)
def get_point_in_circle(circle_x: int, circle_y: int, radius: int, point_x: int, point_y: int) -> str:
	"""
	Entry point for /circle
	Check the point in circle range or not
	:param circle_x: int - coordinate x for circle
	:param circle_y: int - coordinate x for circle
	:param radius: int - radius for circle
	:param point_x: int - coordinate x for point
	:param point_y: int - coordinate y for point
	:return: str
	"""
	point = Point()
	point.x = point_x
	point.y = point_y
	circle = Circle(circle_x, circle_y, radius)
	return str(circle.contains(point))


if __name__ == '__main__':
	app.run(host="127.0.0.1", port=5000, debug=True)

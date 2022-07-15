import random

from http import HTTPStatus

from webargs import fields, validate
from webargs.flaskparser import use_kwargs
from flask import Flask, jsonify

from helpers.helpers import db_answer_to_string
from helpers.database_handler import db_handler
from helpers import query
from point import Point
from circle import Circle

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
    return '<p> <a href = "/circle?circle_x=10&circle_y=10&radius=6&point_x=16&point_y=16">\
    /circle?circle_x=10&circle_y=10&radius=6&point_x=16&point_y=16</a> - Point into circle </p> \
    <p><a href = "/genre?name=Rock">/genre?name=Rock</a> - get popular city for genre</p>'


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


@app.route('/genre')
@use_kwargs(
    {
        'name': fields.Str(required=True, validate=[validate.Length(max=20)])
    },
    location='query'
)
def get_city_for_genre(name: str) -> str:
    query_str = query.get_city_popular_genre()
    result_from_base = db_handler(query_str, args=([name]))
    if not result_from_base:
        return "Not Found sales for genre"
    return db_answer_to_string(result_from_base, ['Genre', 'City', 'Sales'])


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)

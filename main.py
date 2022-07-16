
from http import HTTPStatus

from webargs import fields, validate
from webargs.flaskparser import use_kwargs
from flask import Flask, jsonify

from helpers.helpers import db_answer_to_string, frange, colorize
from helpers.database_handler import db_handler
from helpers.shapes import Rectangle, Parallelogram, Triangle, Circles, Scene
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
    return '<p> <a href = "/range-float?start=10&stop=2&step=-2">\
    /range-float?start=10&stop=2&step=-2/a> - out range float </p> \
    <p><a href = "/context-manager?color=green&text=test">/context-manager?color=green&text=test</a> - colorize output in terminal</p> \
    <p><a href = "/circle?circle_x=10&circle_y=10&radius=6&point_x=16&point_y=16">/circle?circle_x=10&circle_y=10&radius=6&point_x=16&point_y=16</a> \
    /circle?circle_x=10&circle_y=10&radius=6&point_x=16&point_y=16 - Entry point in circle</p>'


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
    return str(Point(point_x, point_y) in Circle(circle_x, circle_y, radius))


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


@app.route('/range-float')
@use_kwargs(
    {
        'start': fields.Str(load_default=0),
        'stop': fields.Str(required=True),
        'step': fields.Str(load_default=1),
    },
    location='query'
)
def frange_entry(start, stop, step):
    return f'{[round(el, 2) for el in frange(start, stop, step)]}'


@app.route('/context-manager')
@use_kwargs(
    {
        'color': fields.Str(required=True, validate=validate.OneOf(['gray', 'red', 'green', 'yellow', 'blue', 'pink', 'turquoise'])),
        'text': fields.Str(required=True, validate=validate.Length(max=100))
    },
    location='query'
)
def colorize_context_manager(color, text):
    colorize(color, text)
    return "Please see output in terminal"


@app.route('/shapes')
def shapes_square():
    rectangle = Rectangle(0, 0, 10, 20)
    rectangle1 = Rectangle(10, 0, -10, 20)
    rectangle2 = Rectangle(0, 20, 100, 20)
    circle = Circles(10, 0, 10)
    circle1 = Circles(100, 100, 5)
    paralelogramm = Parallelogram(1, 2, 20, 30, 45)
    paralelogramm1 = Parallelogram(1, 2, 20, 30, 45)
    triangle = Triangle(0, 0, 5)
    triangle2 = Triangle(0, 0, 3)
    scene = Scene()
    scene.add_figure(rectangle)
    scene.add_figure(rectangle1)
    scene.add_figure(rectangle2)
    scene.add_figure(circle)
    scene.add_figure(circle1)
    scene.add_figure(paralelogramm)
    scene.add_figure(paralelogramm1)
    scene.add_figure(triangle)
    scene.add_figure(triangle2)

    return f'Total square = {scene.total_square()}'


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)

from flask import Flask
from helpers.helpers import gen_pass
import random

app = Flask(__name__)

@app.route('/')
def index():
    return '<p> /pass - generated password</p><p>/csv - work from CSV file</p>'

@app.route('/pass')
def password():
    long_pass = random.randint(10, 20)
    password = gen_pass(long_pass)  # use clean function for generated password
    return f'<p>Password long: {long_pass}</p><p>Password: {password}</p>'



if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)

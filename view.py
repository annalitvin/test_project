import json
import os
import random
import string
import sqlite3
import pandas as pd
import requests

from flask import Flask
from flask import Response, jsonify, request, make_response
from faker import Faker

app = Flask('app')
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def main():
    return "Hello, world!! Select: <br>1. <a href='http://127.0.0.1:5000/get_profile'>Get profile</a><br>" \
           "2. <a href='http://127.0.0.1:5000/get_libs'>Get libs</a><br>" \
            "3. <a href='http://127.0.0.1:5000/get_avg_wh'>Get average height and weight</a>"


@app.route('/get_profile')
def get_profile():

    """Get name and mail from profile"""

    fake = Faker(['it_IT', 'en_US', 'uk_UA'])

    profile_list = [fake.profile(fields=['name', 'mail']) for _ in range(100)]
    return make_response(jsonify(profiles=profile_list))


@app.route('/get_libs')
def get_lib():

    """Get libraries in requirements.txt"""

    libs_list = [line.strip() for line in open('requirements.txt', 'r')]
    return make_response(jsonify(libs=libs_list))


@app.route('/get_avg_wh')
def get_avg_wh():

    """Get student's average height and weight """

    hw_df = pd.read_csv('datasets/hw.csv', delimiter=',')
    hw_df.columns = ['index', 'height', 'weight']

    avg_height = int(round(hw_df["height"].mean()))
    avg_weight = int(round(hw_df["weight"].mean()))
    return make_response(jsonify(average={"height": avg_height,
                                          "weight": avg_weight
                                          }))


@app.route('/get-astronauts')
def get_astronauts():

    """Get astronauts"""

    response = requests.get("http://api.open-notify.org/astros.json")
    if response.status_code == 200:
        resp = json.loads(response.text)
        return f"Astronauts number: {resp['number']}"
    else:
        return f"Error {response.status_code}"


@app.route('/get_password')
def get_password():

    """

    Password generator that getting two GET parameters: length(length of password)
    and isdigit(bool param that indicate if number exists in password or not).
    Length and isdigit must be numeric and greater than zero.
    Length ranges from 8 to 24.

    Example: length=24&isdigit=0

    """

    length = request.args.get('length')
    isdigit = request.args.get('isdigit')
    if length is not None and isdigit is not None:
        is_len_digit = length.isdigit()
        is_dig_digit = isdigit.isdigit()

        if is_dig_digit and is_len_digit:
            length = int(length)
            isdigit = int(isdigit)
            if isdigit not in range(0, 2):
                return 'Value isdigit must be 0 or 1'
            if length in range(8, 25):
                if isdigit == 1:
                    return gen_password(string.digits + string.ascii_lowercase, length)
                elif isdigit == 0:
                    return gen_password(string.ascii_lowercase, length)
            else:
                return 'Password must be between 0 to 24'
        else:
            return 'Error. The value must be numeric and greater than zero.'
    return "Put two GET param: length and isdigit"


@app.route('/get-customers')
def get_customers():

    """

    Get customers who live in a given state and city.
    City and state given in two GET param: state and city.

    Example: city=New%20York&state=NY

    """

    city = request.args.get('city')
    state = request.args.get('state')
    if city is not None and state is not None:

        query = "SELECT FirstName, LastName, Email, Phone FROM customers WHERE City = ? AND State = ?"
        customers = execute_query(query, (city, state))
        customers = '<br>'.join([str(customer) for customer in customers])
        return customers
    return "Put two GET param: city and state "


@app.route('/get-customers-number')
def get_customers_number():

    """Get number of customers"""

    query = "SELECT DISTINCT count(FirstName) FROM customers"
    customers_number = execute_query(query)
    customers_number = f'<br>The number of customers: {customers_number[0][0]}'
    return customers_number


@app.route('/get-company-rev')
def get_company_rev():

    """Get company rev"""

    query = "SELECT UnitPrice*Quantity AS 'rev' FROM invoice_items"
    rev = execute_query(query)
    rev = f'<br>The company rev: {rev[0][0]}'
    return rev


def execute_query(query, param=tuple()):
    db_path = os.path.join(os.getcwd(), 'chinook.db')
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(query, param)
    records = cur.fetchall()
    return records


def gen_password(ptype, length):
    return ''.join([random.choice(ptype) for _ in range(length)])


app.run(debug=True)


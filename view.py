import pandas as pd

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


app.run()


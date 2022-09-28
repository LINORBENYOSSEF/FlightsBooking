from flask import Blueprint, render_template

main = Blueprint('main', __name__)


@main.route('/', methods=["GET"])
def home():
    return render_template('home.html')


@main.route('/booked', methods=["GET"])
def booked_flights():
    return render_template('booked_flights.html')

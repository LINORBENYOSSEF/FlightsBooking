import uuid

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from app_db import db
from model.models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    user = db.find_one(User, 'username', username)

    if not user or not check_password_hash(user.password, password):
        return render_template('login.html', error='Bad Login')

    login_user(user)
    return redirect(url_for('main.home'))


@auth.route('/register', methods=['GET'])
def register():
    return render_template('register.html')


@auth.route('/register', methods=['POST'])
def register_post():
    username = request.form.get('username')
    password = request.form.get('password')
    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')

    # noinspection PyArgumentList
    new_user = User(
        id=str(uuid.uuid4()),
        username=username,
        password=generate_password_hash(password, method='sha256'),
        passenger_info=User.Passenger(first_name=first_name, last_name=last_name, bookings=[])
    )
    db.add(new_user)

    login_user(new_user)
    return redirect(url_for('main.home'))


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

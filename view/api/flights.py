from http import HTTPStatus

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

from app_db import db
from model.models import Flight, User
from model.schemas import FlightSchema, BookedFlightSchema
from db.operations import book_flight as db_book_flight, delete_flight as do_delete_flight, \
    OverbookException

flights_api = Blueprint('flights_api', __name__)


@flights_api.route('/', methods=["GET"])
@flights_api.route('/<flight_id>/', methods=["GET"])
def get_flights(flight_id=None):
    if flight_id:
        flight = db.find_one(Flight, 'id', flight_id)
        if flight is None:
            return 'No such flight', HTTPStatus.NOT_FOUND

        schema = FlightSchema().dump(flight)
        return jsonify(schema), HTTPStatus.OK

    limit = request.args.get('limit')
    offset = request.args.get('offset')

    limit = int(limit) if limit is not None else None
    offset = int(offset) if offset is not None else None

    flights = db.get_all(Flight, limit=limit, offset=offset)
    schema = FlightSchema(many=True).dump(flights)
    return jsonify(schema), HTTPStatus.OK


@flights_api.route('/booked/', methods=["GET"])
@login_required
def get_booked_flights():
    user = db.find_one(User, 'id', current_user.id)
    schema = BookedFlightSchema(many=True).dump(user.passenger_info.bookings)
    return jsonify(schema), HTTPStatus.OK


@flights_api.route('/', methods=["POST"])
@login_required
def create_flight():
    data = request.get_json()

    schema = FlightSchema()
    flight = schema.load(data)

    return jsonify(schema.dump(flight)), HTTPStatus.CREATED


@flights_api.route('/<flight_id>/book/', methods=["POST"])
@login_required
def book_flight(flight_id):
    flight = db.find_one(Flight, 'id', flight_id)
    if flight is None:
        return 'No such flight', HTTPStatus.NOT_FOUND

    try:
        db_book_flight(db, current_user, flight)
        return '', HTTPStatus.OK
    except OverbookException:
        return 'overbooked', HTTPStatus.BAD_REQUEST


@flights_api.route('/<flight_id>/', methods=["DELETE"])
@login_required
def delete_flight(flight_id):
    if not current_user.is_admin:
        return '', HTTPStatus.UNAUTHORIZED

    flight = db.find_one(Flight, 'id', flight_id)
    if flight is None:
        return 'No such flight', HTTPStatus.NOT_FOUND

    do_delete_flight(db, flight)

    return '', HTTPStatus.OK

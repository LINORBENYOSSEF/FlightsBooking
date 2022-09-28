from datetime import datetime
from flask_login import UserMixin

from .base import Model, Column


class Plane(Model):
    manufacturer = Column(str)
    model = Column(str)
    capacity = Column(int)


class Airline(Model):
    name = Column(str)


class Location(Model):
    city = Column(str)
    country = Column(str)


class User(UserMixin, Model):
    class Passenger(Model):
        class Booking(Model):
            flight_id = Column(str)
            paid = Column(float)
            departure_time = Column(datetime)
            airline = Column(Airline)
            departure = Column(Location)
            destination = Column(Location)

        first_name = Column(str)
        last_name = Column(str)
        bookings = Column(Booking, is_many=True)

    id = Column(str)
    username = Column(str)
    password = Column(str)
    passenger_info = Column(Passenger)
    is_admin = Column(bool)


class Flight(Model):
    class Passenger(Model):
        id = Column(str)

    id = Column(str)
    airline = Column(Airline)
    plane = Column(Plane)
    passengers = Column(Passenger, is_many=True)
    departure_time = Column(datetime)
    departure = Column(Location)
    destination = Column(Location)
    ticket_cost = Column(float)

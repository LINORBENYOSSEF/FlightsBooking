import uuid

from app_db import db
from model.models import *

print(db.get_all(User))
print(db.get_all(Flight))

"""
db.add(Flight(
    id=str(uuid.uuid4()),
    airline=Airline(name='EL-AL'),
    plane=Plane(manufacturer='Boeing', model='747', capacity=100),
    passengers=[],
    departure_time=datetime.now(),
    departure=Location(code='MUC', city='Munich', country='Germany'),
    destination=Location(code='NY', city='New York', country='US'),
    ticket_cost=150
))

db.add(Flight(
    id=str(uuid.uuid4()),
    airline=Airline(name='British Airways'),
    plane=Plane(manufacturer='Boeing', model='747', capacity=100),
    passengers=[],
    departure_time=datetime.now(),
    departure=Location(code='LON', city='London', country='UK'),
    destination=Location(code='MUC', city='Munich', country='Germany'),
    ticket_cost=150
))
"""

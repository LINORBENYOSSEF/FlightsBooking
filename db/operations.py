from db.database import Database
from model.models import User, Flight


class OverbookException(Exception):
    # if len(flight.passengers) + 1 >= flight.plane.capacity:
    # raise OverbookException()
    pass


def book_flight(db: Database, user: User, flight: Flight):
    with db.do_transaction() as session:
        try:


            user.passenger_info.bookings.append(User.Passenger.Booking(
                flight_id=flight.id,
                paid=flight.ticket_cost,
                airline=flight.airline,
                destination=flight.destination,
                departure=flight.departure
            ))
            db.update_one(user, 'id', session=session, data_type=User)

            flight.passengers.append(Flight.Passenger(
                id=user.id,
                first_name=user.passenger_info.first_name,
                last_name=user.passenger_info.last_name
            ))
            db.update_one(flight, 'id', session=session, data_type=Flight)

            session.commit_transaction()
        except Exception:
            session.abort_transaction()
            raise


def delete_flight(db: Database, flight: Flight):
    with db.do_transaction() as session:
        try:
            db.delete_one(flight, 'id', session=session)

            for user in db.get_all(User, session=session):
                if user.passenger_info is None or user.passenger_info.bookings is None:
                    continue

                user.passenger_info.bookings = [booking for booking in user.passenger_info.bookings
                                                if booking.flight_id != flight.id]
                db.update_one(user, 'id', user.id, session=session)

            session.commit_transaction()
        except Exception:
            session.abort_transaction()
            raise

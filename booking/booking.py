import booking_pb2_grpc, booking_pb2
import json
from concurrent import futures
import grpc
import showtime_pb2
import showtime_pb2_grpc


class BookingServicer(booking_pb2_grpc.BookingServicer):
    # Init the db
    def __init__(self):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]

    # Returns all the bookings
    def GetBookings(self, request, context):
        for booking in self.db:
            yield booking_pb2.BookingDetails(userid=booking["userid"], dates=booking["dates"])

    # If no reservation is found, we send a booking with empty elements
    def GetBookingsByUser(self, request, context):
        userid = request.id
        for booking in self.db:
            if booking["userid"] == userid:
                return booking_pb2.BookingDetails(userid=booking["userid"], dates=booking["dates"])
        return booking_pb2.BookingDetails(userid="", dates=[])

    # If the movie is already present, we send a booking with empty elements
    def CreateBookingForUser(self, request, context):
        userid = request.userid
        movieid = request.movieid
        movie_date = request.date

        # Check if the movie is available on the given date
        with grpc.insecure_channel('showtime:3002') as channel:
            stub = showtime_pb2_grpc.ShowtimeStub(channel)
            movies = stub.GetMoviesByDate(showtime_pb2.ShowtimeDate(date=movie_date))
            if not movieid in movies.movies:
                return booking_pb2.BookingDetails(userid="", dates=[])
            channel.close()

        for booking in self.db:
            # Retrieves the right user
            if booking["userid"] == userid:
                # add the booking and return it
                for date in booking["dates"]:
                    # checks if the date exists et add the film to it
                    if date["date"] == movie_date:
                        # Check if the film already exists in this date
                        if movieid in date["movies"]:
                            return booking_pb2.BookingDetails(userid="", dates=[])
                        # Add the movie and return the booking
                        date["movies"].append(movieid)
                        return booking_pb2.BookingDetails(userid=userid, dates=booking["dates"])

                # If the date is not present, add it to the list with the film id
                new_date = {
                    "date": movie_date,
                    "movies": [movieid]
                }
                booking["dates"].append(new_date)
                return booking_pb2.BookingDetails(userid=booking["userid"], dates=booking["dates"])
        # If the user has never made a reservation we create a new booking
        new_booking = {
            "userid": userid,
            "dates": [
                {
                    "date": movie_date,
                    "movies": [movieid]
                }
            ]
        }
        self.db.append(new_booking)
        return booking_pb2.BookingDetails(userid=new_booking["userid"], dates=new_booking["dates"])


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port('[::]:3003')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

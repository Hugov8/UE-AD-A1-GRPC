import booking_pb2_grpc, booking_pb2
import json
from concurrent import futures
import grpc
import showtime_pb2
import showtime_pb2_grpc



class BookingServicer(booking_pb2_grpc.BookingServicer):
    def __init__(self):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]

    def GetBookings(self, request, context):
        for booking in self.db:
            yield booking_pb2.BookingDetails(userid=booking["userid"], dates=booking["dates"])

    def GetBookingsByUser(self, request, context):
        userid = request.id
        for booking in self.db:
            if booking["userid"] == userid:
                return booking_pb2.BookingDetails(userid=booking["userid"], dates=booking["dates"])
        return booking_pb2.BookingDetails(userid="", dates=[])

    def CreateBookingForUser(self, request, context):
        userid = request.userid
        movieid = request.movieid
        movie_date = request.date

        with grpc.insecure_channel('localhost:3002') as channel:
            stub = showtime_pb2_grpc.ShowtimeStub(channel)
            movies = stub.GetMoviesByDate(showtime_pb2.ShowtimeDate(date=movie_date))
            if not movieid in movies.movies:
                return booking_pb2.BookingDetails(userid="", dates=[])
            channel.close()

        for booking in self.db:
            if booking["userid"] == userid:
                # add booking to the user and return
                for date in booking["dates"]:
                    if date["date"] == movie_date:
                        if movieid in date["movies"]:
                            return booking_pb2.BookingDetails(userid="", dates=[])
                        date["movies"].append(movieid)
                        return booking_pb2.BookingDetails(userid=userid, dates=booking["dates"])
                new_date = {
                    "date": movie_date,
                    "movies": [movieid]
                }
                booking["dates"].append(new_date)
                return booking_pb2.BookingDetails(userid=booking["userid"], dates=booking["dates"])

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
    server.add_insecure_port('[::]:3000')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

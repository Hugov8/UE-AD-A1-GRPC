import booking_pb2_grpc, booking_pb2
import json
from concurrent import futures
import grpc
import showtime_pb2
import showtime_pb2_grpc

class BookingServicer(booking_pb2_grpc.BookingServicer):
    #Initialise la base de données
    def __init__(self):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]

    #envoie un streal de bookings
    def GetBookings(self, request, context):
        for booking in self.db:
            yield booking_pb2.BookingDetails(userid=booking["userid"], dates=booking["dates"])

    #Si aucune reservation n'est trouvé, on envoie un booking dont les éléments sont vides
    def GetBookingsByUser(self, request, context):
        userid = request.id
        for booking in self.db:
            if booking["userid"] == userid:
                return booking_pb2.BookingDetails(userid=booking["userid"], dates=booking["dates"])
        return booking_pb2.BookingDetails(userid="", dates=[])

    #Si le movie est déjà présent, on envoie un booking avec des éléments vides
    def CreateBookingForUser(self, request, context):
        userid = request.userid
        movieid = request.movieid
        movie_date = request.date

        #Check si le movie est bien disponible à la date donnée
        with grpc.insecure_channel('showtime:3002') as channel:
            stub = showtime_pb2_grpc.ShowtimeStub(channel)
            movies = stub.GetMoviesByDate(showtime_pb2.ShowtimeDate(date=movie_date))
            if not movieid in movies.movies:
                return booking_pb2.BookingDetails(userid="", dates=[])
            channel.close()

        for booking in self.db:
            #Check le bon user
            if booking["userid"] == userid:
                # ajoute la reservation et le renvoie
                for date in booking["dates"]:
                    #check si la date et déjà présente et ajoute le film a celle ci
                    if date["date"] == movie_date:
                        #Check si le film est déjà programmé à cette date
                        if movieid in date["movies"]:
                            return booking_pb2.BookingDetails(userid="", dates=[])
                        #Ajoute et renvoie la réservation
                        date["movies"].append(movieid)
                        return booking_pb2.BookingDetails(userid=userid, dates=booking["dates"])
                
                #Si la date n'est pas présente, n l'ajoute à la liste ave l'id du film
                new_date = {
                    "date": movie_date,
                    "movies": [movieid]
                }
                booking["dates"].append(new_date)
                return booking_pb2.BookingDetails(userid=booking["userid"], dates=booking["dates"])
        #Si l'user n'a jamais fait de réservation on crée une nouvelle booking
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

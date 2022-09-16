import grpc

import movie_pb2
import movie_pb2_grpc
import showtime_pb2
import showtime_pb2_grpc


def get_movie_by_id(stub,id):
    movie = stub.GetMovieByID(id)
    print(movie)

def get_list_movies(stub):
    allmovies = stub.GetListMovies(movie_pb2.Empty())
    for movie in allmovies:
        print("Movie called %s" % (movie.title))

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:3001') as channel:
        stub = movie_pb2_grpc.MovieStub(channel)

        print("-------------- GetMovieByID --------------")
        movieid = movie_pb2.MovieID(id="a8034f44-aee4-44cf-b32c-74cf452aaaae")
        get_movie_by_id(stub, movieid)

        print("-------------- GetListMovies --------------")
        get_list_movies(stub)

    channel.close()

    with grpc.insecure_channel('localhost:3002') as channel:
        stub = showtime_pb2_grpc.ShowtimeStub(channel)

        print("\r\n----------- GetListSchedules----------------")
        all_schedules = stub.GetListSchedules(showtime_pb2.EmptyS())
        for sched in all_schedules:
            print("date: " + str(sched.date))
            print("movies: " + str(sched.movies))

        print("\r\n------------GetMoviesByDate-----------")
        schedule = stub.GetMoviesByDate(showtime_pb2.ShowtimeDate(date="20151130"))
        print(schedule)

    channel.close()

if __name__ == '__main__':
    run()

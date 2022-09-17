import grpc

import movie_pb2
import movie_pb2_grpc


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

        print("-------------- Adding a new film ----------")
        op = stub.AddMovie(movie_pb2.MovieData(title="test", rating = 5.0, director = "moi", id = "gogogoogogogog"))
        print(op)
        get_list_movies(stub)

        print("-------------- GetMovieByTitle -----------")
        rep = stub.GetMovieByTitle(movie_pb2.MovieTitle(title="The Danish Girl"))
        print(rep)

        print("-------------- GetMovieRate ---------------")
        rep = stub.GetMovieRate(movie_pb2.MovieID(id="a8034f44-aee4-44cf-b32c-74cf452aaaae"))
        print(rep)

        print("-------------- Modify a movie -------------")
        rep = stub.ModifyMovie(movie_pb2.MovieData(title="retest", rating=2.5, director="moi", id="hgogogoogogogog")) 
        print(rep)
        get_movie_by_id(stub, movie_pb2.MovieID(id="gogogoogogogog"))

        print("-------------- Delete a movie --------------")
        rep = stub.DeleteMovie(movie_pb2.MovieID(id="gogogoogogogog"))
        print(rep)
        get_list_movies(stub)

    channel.close()

if __name__ == '__main__':
    run()

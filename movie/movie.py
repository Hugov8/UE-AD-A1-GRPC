import grpc
from concurrent import futures
import movie_pb2_grpc, movie_pb2
import json


class MovieServicer(movie_pb2_grpc.MovieServicer):

    # init database
    def __init__(self):
        with open('{}/data/movies.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["movies"]

    # Retrieve a movie by movie id
    def GetMovieByID(self, request, context):
        for movie in self.db:
            if movie['id'] == request.id:
                print("Movie found!")
                return movie_pb2.MovieData(title=movie['title'], rating=movie['rating'], director=movie['director'],
                                           id=movie['id'])
        return movie_pb2.MovieData(title="", rating=0, director="", id="")

    # retrieve all movies from the dabasae
    def GetListMovies(self, request, context):
        for movie in self.db:
            yield movie_pb2.MovieData(title=movie['title'], rating=movie['rating'], director=movie['director'],
                                      id=movie['id'])

    # Retrieve a movie with its title
    def GetMovieByTitle(self, request, context):
        for movie in self.db:
            if movie["title"] == request.title:
                return movie_pb2.MovieData(title=movie["title"], rating=movie["rating"], director=movie["director"],
                                           id=movie["id"])
        return movie_pb2.MovieData(title="", rating=0, director="", id="")

    # Get movie rate from its id
    def GetMovieRate(self, request, context):
        for movie in self.db:
            if request.id == movie["id"]:
                return movie_pb2.MovieRate(rating=movie["rating"])

    # Returns an OperationSuccess message to know if the movie has been added with a comment
    def AddMovie(self, request, context):
        for movie in self.db:
            if movie["id"] == request.id:
                return movie_pb2.OperationSuccess(success=False, comment="Film already exist")

        self.db.append({"title": request.title, "rating": request.rating, "director": request.director, "id": request.id
                        })
        return movie_pb2.OperationSuccess(success=True, comment="Film added")

    # Modify a movie (with a given id) from parameters `title` `rating` and `director`
    def ModifyMovie(self, request, context):
        for movie in self.db:
            if request.id == movie["id"]:
                movie["title"] = request.title
                movie["rating"] = request.rating
                movie["director"] = request.director
                return movie_pb2.OperationSuccess(success=True, comment="Film modified")
        return movie_pb2.OperationSuccess(success=False, comment="Film not found")

    # Delete a movie with a given id
    def DeleteMovie(self, request, context):
        for movie in self.db:
            if request.id == movie["id"]:
                self.db.remove(movie)
                return movie_pb2.OperationSuccess(success=True, comment="Movie deleted")
        return movie_pb2.OperationSuccess(success=False, comment="Film not found")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    movie_pb2_grpc.add_MovieServicer_to_server(MovieServicer(), server)
    server.add_insecure_port('[::]:3001')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

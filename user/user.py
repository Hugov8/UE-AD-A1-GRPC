from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound
import movie_pb2
import movie_pb2_grpc
import booking_pb2, booking_pb2_grpc
import grpc
from google.protobuf.json_format import MessageToJson

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

with open('{}/data/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


@app.route("/users", methods=['GET'])
def get_json():
    return make_response(jsonify(users), 200)


@app.route("/users/names/<name>/getreservation", methods=['GET'])
def get_reservation(name):
    for user in users:
        if user["name"] == name:
            with grpc.insecure_channel('localhost:3000') as channel:
                stub = booking_pb2_grpc.BookingStub(channel)
                bookings_message = stub.GetBookingsByUser(booking_pb2.User(id=user["id"]))
                channel.close()
            if not bookings_message.userid == "":
                booking = MessageToJson(bookings_message)
            else:
                booking = jsonify({
                    "userid": user["id"],
                    "dates": []
                })
            return make_response(booking, 200)
    return make_response(jsonify({"error": "Name not found"}), 400)

@app.route("/users/addUser/<iduser>", methods=['POST'])
def addUser(iduser):
   for user in users:
      if user["id"]==iduser:
         return make_response(jsonify({"error": "User id already exist"}))
   
   if request.args:
      if request.args["name"] and request.args["last_active"]:
         newUser = {"id": iduser, "name": request.args["name"], "last_active": request.args["last_active"]}
         users.append(newUser)
         return make_response(jsonify(newUser), 200)
   return make_response(jsonify({"error":"One or more argument missing"}),400)

@app.route("/user/<user_id>/movies", methods=['GET'])
def get_movies_for_user(user_id):
    with grpc.insecure_channel('localhost:3001') as channel:
        stub = movie_pb2_grpc.MovieStub(channel)
        rep = requests.get("http://localhost:3201/bookings/" + user_id)
        if(rep.status_code != 200):
            return make_response(rep.json(), rep.status_code)

        bookings = rep.json()
        movie_list = []
        for date in bookings["dates"]:
            for movie in date["movies"]:
                movieID = movie_pb2.MovieID(id=movie)
                movie_details = stub.GetMovieByID(movieID)
                movie_list.append({"date": date["date"], "title": movie_details.title})
        channel.close()
    return make_response(jsonify(movie_list), 200)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)

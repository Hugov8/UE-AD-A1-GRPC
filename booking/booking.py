import requests.utils
from flask import Flask, request, jsonify, make_response
import json

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'

with open('{}/data/bookings.json'.format("."), "r") as jsf:
    bookings = json.load(jsf)["bookings"]


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"


@app.route("/bookings", methods=['GET'])
def get_bookings():
    return make_response(jsonify(bookings), 200)


@app.route("/bookings/<userid>", methods=['GET'])
def get_bookings_by_id(userid):
    for booking in bookings:
        if booking["userid"] == userid:
            return make_response(jsonify(booking))
    return make_response(jsonify({"error": "User not found"}), 400)


@app.route("/bookings/<userid>", methods=['POST'])
def create_booking(userid):
    req = request.get_json()

    if not ("movieid" in req.keys() and "date" in req.keys()):
        return make_response(jsonify({"error": "invalid parameters"}), 400)

    movies = requests.get("http://localhost:3202/showmovies/" + req["date"]).json()
    if not "movies" in movies.keys() or not req["movieid"] in movies["movies"]:
        return make_response(jsonify({"error": "this showtime doesn't exists"}), 400)

    for booking in bookings:
        if booking["userid"] == userid:
            # add booking to the user and return
            for date in booking["dates"]:
                if date["date"] == req["date"]:
                    if req["movieid"] in date["movies"]:
                        return make_response(jsonify({"error": "booking already exists for this user"}), 400)
                    date["movies"].append(req["movieid"])
                    return make_response(jsonify(booking), 200)
            new_date = {
                "date": req["date"],
                "movies": [req["movieid"]]
            }
            booking["dates"].append(new_date)
            print(booking)
            return make_response(jsonify(booking), 200)

    new_booking = {
        "userid": userid,
        "dates": [
            {
                "date": req["date"],
                "movies": [req["movieid"]]
            }
        ]
    }
    bookings.append(new_booking)
    return make_response(jsonify(new_booking), 200)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)

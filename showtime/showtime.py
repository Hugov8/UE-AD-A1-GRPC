from flask import Flask, jsonify, make_response
import json

app = Flask(__name__)

PORT = 3202
HOST = '0.0.0.0'

with open('{}/data/times.json'.format("."), "r") as jsf:
    schedule = json.load(jsf)["schedule"]


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the Showtime service!</h1>"


def map_schedule(date):
    movies = []
    for movie in date["movies"]:
        movies.append({
            "href": "http://localhost:3200/movies/" + movie,
            "id": movie
        })
    return {
        "date": date["date"],
        "movies": movies
    }


@app.route("/json", methods=['GET'])
def get_schedule():
    res = []
    for date in schedule:
        res.append(map_schedule(date))
    return make_response(jsonify(res), 200)


@app.route("/showmovies/<date>", methods=['GET'])
def get_movies_bydate(date):
    for s in schedule:
        if str(s["date"]) == str(date):
            return make_response(jsonify(map_schedule(s)), 200)
    return make_response(jsonify({"error": "schedule not found"}), 400)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)

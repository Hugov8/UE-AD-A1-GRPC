import grpc
from concurrent import futures
import showtime_pb2
import showtime_pb2_grpc
import json

class ShowtimeServicer(showtime_pb2_grpc.ShowtimeServicer):

    def __init__(self):
        with open('{}/data/times.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]

    def GetListSchedules(self, request, context):
        for schedule in self.db:
            yield showtime_pb2.ScheduleData(date=schedule["date"], movies=schedule["movies"])

    def GetMoviesByDate(self, request, context):
        for s in self.db:
            if request.date == s["date"]:
                return showtime_pb2.ScheduleData(date=s["date"], movies=s["movies"])
        return showtime_pb2.ScheduleData(date="", movies=[])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    showtime_pb2_grpc.add_ShowtimeServicer_to_server(ShowtimeServicer(), server)
    server.add_insecure_port('[::]:3002')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

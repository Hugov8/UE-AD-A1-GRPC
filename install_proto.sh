:'
Script permettant de générer les codes grpc et de les copier dans les fichiers en ayant besoin
'
#Génération grpc movie
cd movie
python3 -m grpc_tools.protoc --proto_path=./protos --python_out=. --grpc_python_out=. movie.proto
cp movie_pb2.py ../user/movie_pb2.py
cp movie_pb2_grpc.py ../user/movie_pb2_grpc.py
cp movie_pb2.py ../client/movie_pb2.py
cp movie_pb2_grpc.py ../client/movie_pb2_grpc.py
#Génération grpc booking
cd ../booking
python3 -m grpc_tools.protoc --proto_path=./protos --python_out=. --grpc_python_out=. booking.proto
cp booking_pb2_grpc.py ../user/booking_pb2_grpc.py
cp booking_pb2.py ../user/booking_pb2.py
cp booking_pb2_grpc.py ../client/booking_pb2_grpc.py
cp booking_pb2.py ../client/booking_pb2.py
#Génération grpc showtime
cd ../showtime
python3 -m grpc_tools.protoc --proto_path=./protos --python_out=. --grpc_python_out=. showtime.proto
cp showtime_pb2.py ../booking/showtime_pb2.py
cp showtime_pb2_grpc.py ../booking/showtime_pb2_grpc.py
cp showtime_pb2.py ../client/showtime_pb2.py
cp showtime_pb2_grpc.py ../client/showtime_pb2_grpc.py
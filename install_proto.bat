cd movie
python -m grpc_tools.protoc --proto_path=./protos --python_out=. --grpc_python_out=. movie.proto
cd ../booking
python -m grpc_tools.protoc --proto_path=./protos --python_out=. --grpc_python_out=. booking.proto
cd ../showtime
python -m grpc_tools.protoc --proto_path=./protos --python_out=. --grpc_python_out=. showtime.proto
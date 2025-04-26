from concurrent import futures
import logging

import grpc
import grpc_test_pb2
import grpc_test_pb2_grpc

class TestServiceServicer(grpc_test_pb2_grpc.TestServiceServicer):
    def VoidCall(self, request, context):
        # Receives and returns Void from and to the client
        return grpc_test_pb2.Void()

    def LongCall(self, request, context):
        # Receives a long (int64) from the client and returns the value + 1
        return grpc_test_pb2.LongValue(value=request.value+1)

    def LongArrayCall(self, request, context):
        # Receives a array of longs (int64) and returns ...
        return grpc_test_pb2.LongArrayValue(request.values)

    def StringCall(self, request, context):
        # Receives a string from the client, transforms it to lower case and returns the new string
        return grpc_test_pb2.StringValue(value=request.value)

    def ComplexCall(self, request, context):
        # Receives a complex type consisting of a id (int64) and a name (string)
        # Returns ...
        return grpc_test_pb2.ComplexValue(id=request.id, name=request.name)

def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    grpc_test_pb2_grpc.add_TestServiceServicer_to_server(TestServiceServicer(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
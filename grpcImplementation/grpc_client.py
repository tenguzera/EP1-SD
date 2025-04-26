from __future__ import print_function

import logging

import grpc
import grpc_test_pb2
import grpc_test_pb2_grpc

def run():
    print("Trying to connect to server...")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = grpc_test_pb2_grpc.TestServiceStub(channel)
        print("Connected!")

        print("Making VoidCall...")
        response = stub.VoidCall(grpc_test_pb2.Void())
        print("VoidCall response (should be blank): ", response)

        print("Making LongCall with value=9223372036854775806...")
        response = stub.LongCall(grpc_test_pb2.LongValue(value=9223372036854775806))
        print("Response value received:", response.value)

if __name__ == "__main__":
    logging.basicConfig()
    run()
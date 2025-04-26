from __future__ import print_function

import logging

import grpc
import grpc_test_pb2
import grpc_test_pb2_grpc

import random
import string
import time

def generate_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def run():
    print("Trying to connect to server...")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = grpc_test_pb2_grpc.TestServiceStub(channel)
        print("Connected!")

        print("\nMaking VoidCall...")
        response = stub.VoidCall(grpc_test_pb2.Void())
        print("VoidCall response (should be blank): ", response)

        print("\nMaking LongCall with value=9223372036854775806...")
        response = stub.LongCall(grpc_test_pb2.LongValue(value=9223372036854775806))
        print("Response value received:", response.value)

        print("\nMaking LongArrayCall with size of array = 8...")
        signed_long_array = {1000000000000000000, 1000000000000000001, 1000000000000000002, 1000000000000000003,
                             1000000000000000004, 1000000000000000005, 1000000000000000006, 1000000000000000007}
        response = stub.LongArrayCall(grpc_test_pb2.LongArray(values=signed_long_array))
        print("Response value received (should be 80000000000000000028): ", response.value)

        print("\nMaking StringCalls for size of string in range 2^0 to 2^11...")
        sizes = [2 ** i for i in range(0, 11)]  # [1, 2, 4, ..., 1024]
        for size in sizes:
            test_string = generate_string(size)
            response = stub.StringCall(grpc_test_pb2.StringValue(value=test_string))
            print("StringCall response (should be string of length {}): ".format(size), response.value)

if __name__ == "__main__":
    logging.basicConfig()
    run()
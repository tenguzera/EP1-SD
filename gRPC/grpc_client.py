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
    with grpc.insecure_channel('localhost:50051') as channel: # This line must be changed if you want to test with the client and server in different machines
        stub = grpc_test_pb2_grpc.TestServiceStub(channel)
        response = stub.VoidCall(grpc_test_pb2.Void())
        print("Connected! A first connection call was made to make the following calls perfomance report more reliable."
              "\nNow going to the proper tests.")

        print("\nMaking VoidCall...")
        start = time.perf_counter()
        response = stub.VoidCall(grpc_test_pb2.Void())
        end = time.perf_counter()
        print("VoidCall response (should be blank): ", response)
        print(f"VoidCall took {end - start:.6f} seconds")

        print("\nMaking LongCall with value=9223372036854775806...")
        start = time.perf_counter()
        response = stub.LongCall(grpc_test_pb2.LongValue(value=9223372036854775806))
        end = time.perf_counter()
        print("Response value received:", response.value)
        print(f"LongCall took {end - start:.6f} seconds")

        print("\nMaking LongArrayCall with size of array = 8...")
        signed_long_array = {1000000000000000000, 1000000000000000001, 1000000000000000002, 1000000000000000003,
                             1000000000000000004, 1000000000000000005, 1000000000000000006, 1000000000000000007}
        start = time.perf_counter()
        response = stub.LongArrayCall(grpc_test_pb2.LongArray(values=signed_long_array))
        end = time.perf_counter()
        print("Response value received (should be 80000000000000000028): ", response.value)
        print(f"LongArrayCall took {end - start:.6f} seconds")

        print("\nMaking StringCall for size of string in range 2^0 to 2^11...")
        sizes = [2 ** i for i in range(0, 11)]  # [1, 2, 4, ..., 1024]
        for size in sizes:
            test_string = generate_string(size)
            start = time.perf_counter()
            response = stub.StringCall(grpc_test_pb2.StringValue(value=test_string))
            end = time.perf_counter()
            print("StringCall response (should be string of length {}): ".format(size), response.value)
            print(f"StringCall took {end - start:.6f} seconds\n")

        print("\nMaking ComplexCall...")
        start = time.perf_counter()
        response = stub.ComplexCall(grpc_test_pb2.ComplexValue(id=1, name="your_name"))
        end = time.perf_counter()
        print("Your name is: ", response.name)
        print("Your id is: ", response.id)
        print(f"ComplexCall took {end - start:.6f} seconds")

if __name__ == "__main__":
    logging.basicConfig()
    run()
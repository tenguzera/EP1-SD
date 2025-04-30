from apache_test import TestService
from apache_test.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

import sys
import time
import random
import string

def generate_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def run():
    print("Trying to connect to Thrift server...")
    transport = TSocket.TSocket('localhost', 50051)  # This line must be changed if you want to test with the client and server in different machines
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = TestService.Client(protocol)

    transport.open()
    print("Connected!")

    print("\nMaking VoidCall...")
    start = time.perf_counter()
    client.voidCall()
    end = time.perf_counter()
    print(f"VoidCall took {end - start:.6f} seconds")

    print("\nMaking LongCall with value=9223372036854775806...")
    start = time.perf_counter()
    response = client.longCall(LongValue(value=9223372036854775806))
    end = time.perf_counter()
    print("Response value received:", response.value)
    print(f"LongCall took {end - start:.6f} seconds")

    print("\nMaking LongArrayCall with size of array = 8...")
    signed_long_array = [1000000000000000000 + i for i in range(8)]
    start = time.perf_counter()
    response = client.longArrayCall(LongArray(values=signed_long_array))
    end = time.perf_counter()
    print("Response value received (should be 8000000000000000028):", response.value)
    print(f"LongArrayCall took {end - start:.6f} seconds")

    print("\nMaking StringCall for size of string in range 2^0 to 2^11...")
    sizes = [2 ** i for i in range(0, 11)]  # [1, 2, ..., 1024]
    for size in sizes:
        test_string = generate_string(size)
        start = time.perf_counter()
        response = client.stringCall(StringValue(value=test_string))
        end = time.perf_counter()
        print("StringCall response (should be string of length {}):".format(size), response.value)
        print(f"StringCall took {end - start:.6f} seconds\n")

    print("\nMaking ComplexCall...")
    start = time.perf_counter()
    response = client.complexCall(ComplexValue(id=1, name="your_name"))
    end = time.perf_counter()
    print("Your name is:", response.name)
    print("Your id is:", response.id)
    print(f"ComplexCall took {end - start:.6f} seconds")

    transport.close()

if __name__ == '__main__':
    run()
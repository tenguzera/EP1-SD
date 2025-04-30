from apache_test import TestService
from apache_test.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

class TestServiceHandler:
    def voidCall(self):
        # Receives and returns Void from and to the client
        return Void()

    def longCall(self, val):
        # Receives a long (int64) from the client and returns the value + 1
        return LongValue(val.value + 1)

    def longArrayCall(self, arr):
        # Receives a array of longs (int64) and returns the sum of all elements in the array
        return LongValue(sum(arr.values))

    def stringCall(self, val):
        # Receives a string from the client, transforms it to lower case and returns the new string
        return StringValue(val.value.lower())

    def complexCall(self, val):
        # Receives a complex type consisting of a id (int64) and a name (string)
        # Returns without any change of the values
        return ComplexValue(val.id, val.name)

def main():
    handler = TestServiceHandler()
    processor = TestService.Processor(handler)

    transport = TSocket.TServerSocket(host='0.0.0.0', port=50051) # This line must be changed if you want to test with the client and server in different machines
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
    print("Thrift server initialized, listening on port 50051...")
    server.serve()

if __name__ == "__main__":
    main()
from __future__ import print_function
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import grpc
import grpc_test_pb2
import grpc_test_pb2_grpc
import random
import string
import time
import statistics
import matplotlib.pyplot as plt

# Configurações
NUM_REPETICOES = 10
STRING_SIZES = [2 ** i for i in range(0, 11)]  # [1, 2, ..., 1024]
THREAD_COUNTS = [1, 2, 4, 8, 16, 32]

def generate_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Funções específicas para cada chamada
def chamada_void(stub):
    stub.VoidCall(grpc_test_pb2.Void())

def chamada_long(stub):
    stub.LongCall(grpc_test_pb2.LongValue(value=9223372036854775806))

def chamada_longarray(stub):
    signed_long_array = [1000000000000000000 + i for i in range(8)]
    stub.LongArrayCall(grpc_test_pb2.LongArray(values=signed_long_array))

def chamada_string(stub, string_value):
    stub.StringCall(grpc_test_pb2.StringValue(value=string_value))

def chamada_complex(stub):
    stub.ComplexCall(grpc_test_pb2.ComplexValue(id=1, name="your_name"))

def teste_concorrente_throughput(stub, funcao, args=(), num_threads=10, chamadas_por_thread=50):
    total_chamadas = num_threads * chamadas_por_thread
    start_total = time.perf_counter()

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [
            executor.submit(funcao, stub, *args)
            for _ in range(total_chamadas)
        ]
        for future in as_completed(futures):
            future.result()

    end_total = time.perf_counter()
    tempo_total = end_total - start_total
    throughput = total_chamadas / tempo_total
    return tempo_total, throughput

def run():
    print("Connecting to server...")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = grpc_test_pb2_grpc.TestServiceStub(channel)
        stub.VoidCall(grpc_test_pb2.Void())  # estabilização

        print("\n--- Testes de Throughput com Variação de Threads ---")
        resultados_tp = {
            'VoidCall': [],
            'LongCall': [],
            'LongArrayCall': [],
            'ComplexCall': [],
            'StringCall_128': [],
            'StringCall_1024': []
        }

        for threads in THREAD_COUNTS:
            print(f"\nThreads: {threads}")

            # VoidCall
            _, tp = teste_concorrente_throughput(stub, chamada_void, num_threads=threads)
            resultados_tp['VoidCall'].append(tp)

            # LongCall
            _, tp = teste_concorrente_throughput(stub, chamada_long, num_threads=threads)
            resultados_tp['LongCall'].append(tp)

            # LongArrayCall
            _, tp = teste_concorrente_throughput(stub, chamada_longarray, num_threads=threads)
            resultados_tp['LongArrayCall'].append(tp)

            # ComplexCall
            _, tp = teste_concorrente_throughput(stub, chamada_complex, num_threads=threads)
            resultados_tp['ComplexCall'].append(tp)

            # StringCall (128)
            str128 = generate_string(128)
            _, tp = teste_concorrente_throughput(stub, chamada_string, args=(str128,), num_threads=threads)
            resultados_tp['StringCall_128'].append(tp)

            # StringCall (1024)
            str1024 = generate_string(1024)
            _, tp = teste_concorrente_throughput(stub, chamada_string, args=(str1024,), num_threads=threads)
            resultados_tp['StringCall_1024'].append(tp)

        gerar_grafico_throughput(resultados_tp)

def gerar_grafico_throughput(resultados_tp):
    plt.figure(figsize=(12, 7))
    for label, valores in resultados_tp.items():
        plt.plot(THREAD_COUNTS, valores, marker='o', label=label)

    plt.title("Throughput vs Número de Threads")
    plt.xlabel("Número de Threads")
    plt.ylabel("Throughput (chamadas/s)")
    plt.legend()
    plt.grid(True)
    plt.savefig("throughput_vs_threads.png")
    plt.show()

if __name__ == "__main__":
    logging.basicConfig()
    run()

from apache_test import TestService
from apache_test.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

import time
import random
import string
import logging
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configurações
THREAD_COUNTS = [1, 2, 4, 8, 16, 32]

def generate_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def criar_cliente():
    transport = TSocket.TSocket('localhost', 50051)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = TestService.Client(protocol)
    transport.open()
    return client

# Funções específicas para chamadas
def chamada_void(client):
    client.voidCall()

def chamada_long(client):
    client.longCall(LongValue(value=9223372036854775806))

def chamada_longarray(client):
    values = [1000000000000000000 + i for i in range(8)]
    client.longArrayCall(LongArray(values=values))

def chamada_string(client, s):
    client.stringCall(StringValue(value=s))

def chamada_complex(client):
    client.complexCall(ComplexValue(id=1, name="your_name"))

# Benchmark com múltiplas threads
def teste_concorrente_throughput(funcao, args=(), num_threads=10, chamadas_por_thread=50):
    total_chamadas = num_threads * chamadas_por_thread
    start_total = time.perf_counter()

    def worker():
        client = criar_cliente()
        funcao(client, *args)

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(worker) for _ in range(total_chamadas)]
        for f in as_completed(futures):
            f.result()

    end_total = time.perf_counter()
    tempo_total = end_total - start_total
    throughput = total_chamadas / tempo_total
    return tempo_total, throughput

def run():
    print("Iniciando testes de concorrência com Apache Thrift...")
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

        _, tp = teste_concorrente_throughput(chamada_void, num_threads=threads)
        resultados_tp['VoidCall'].append(tp)

        _, tp = teste_concorrente_throughput(chamada_long, num_threads=threads)
        resultados_tp['LongCall'].append(tp)

        _, tp = teste_concorrente_throughput(chamada_longarray, num_threads=threads)
        resultados_tp['LongArrayCall'].append(tp)

        _, tp = teste_concorrente_throughput(chamada_complex, num_threads=threads)
        resultados_tp['ComplexCall'].append(tp)

        str128 = generate_string(128)
        _, tp = teste_concorrente_throughput(chamada_string, args=(str128,), num_threads=threads)
        resultados_tp['StringCall_128'].append(tp)

        str1024 = generate_string(1024)
        _, tp = teste_concorrente_throughput(chamada_string, args=(str1024,), num_threads=threads)
        resultados_tp['StringCall_1024'].append(tp)

    gerar_grafico_throughput(resultados_tp)

def gerar_grafico_throughput(resultados_tp):
    plt.figure(figsize=(12, 7))
    for label, valores in resultados_tp.items():
        plt.plot(THREAD_COUNTS, valores, marker='o', label=label)

    plt.title("Throughput vs Número de Threads (Thrift)")
    plt.xlabel("Número de Threads")
    plt.ylabel("Throughput (chamadas/s)")
    plt.legend()
    plt.grid(True)
    plt.savefig("thrift_throughput_vs_threads.png")
    plt.show()

if __name__ == "__main__":
    logging.basicConfig()
    run()
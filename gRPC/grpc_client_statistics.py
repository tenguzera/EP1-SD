from __future__ import print_function

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

def generate_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def medir_tempo(funcao_chamada):
    tempos = []
    for _ in range(NUM_REPETICOES):
        start = time.perf_counter()
        funcao_chamada()
        end = time.perf_counter()
        tempos.append(end - start)
    return tempos

def run():
    print("Connecting to server...")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = grpc_test_pb2_grpc.TestServiceStub(channel)

        # Primeira chamada só para estabilizar a conexão
        stub.VoidCall(grpc_test_pb2.Void())

        resultados = {}

        # Teste VoidCall
        tempos_void = medir_tempo(lambda: stub.VoidCall(grpc_test_pb2.Void()))
        resultados['VoidCall'] = (statistics.mean(tempos_void), statistics.stdev(tempos_void))

        # Teste LongCall
        tempos_long = medir_tempo(lambda: stub.LongCall(grpc_test_pb2.LongValue(value=9223372036854775806)))
        resultados['LongCall'] = (statistics.mean(tempos_long), statistics.stdev(tempos_long))

        # Teste LongArrayCall
        signed_long_array = [1000000000000000000 + i for i in range(8)]
        tempos_longarray = medir_tempo(lambda: stub.LongArrayCall(grpc_test_pb2.LongArray(values=signed_long_array)))
        resultados['LongArrayCall'] = (statistics.mean(tempos_longarray), statistics.stdev(tempos_longarray))

        # Teste StringCall com vários tamanhos
        resultados_stringcall = []
        for size in STRING_SIZES:
            test_string = generate_string(size)
            tempos_string = medir_tempo(lambda: stub.StringCall(grpc_test_pb2.StringValue(value=test_string)))
            media = statistics.mean(tempos_string)
            desvio = statistics.stdev(tempos_string)
            resultados_stringcall.append((size, media, desvio))

        # Teste ComplexCall
        tempos_complex = medir_tempo(lambda: stub.ComplexCall(grpc_test_pb2.ComplexValue(id=1, name="your_name")))
        resultados['ComplexCall'] = (statistics.mean(tempos_complex), statistics.stdev(tempos_complex))

    # Gerar gráficos
    gerar_graficos(resultados, resultados_stringcall)

def gerar_graficos(resultados, resultados_stringcall):
    # Gráfico de barras para VoidCall, LongCall, LongArrayCall, ComplexCall
    labels = list(resultados.keys())
    medias = [resultados[label][0] for label in labels]
    desvios = [resultados[label][1] for label in labels]

    plt.figure(figsize=(10, 6))
    plt.bar(labels, medias, yerr=desvios, capsize=5, color='skyblue')
    plt.ylabel('Tempo médio (s)')
    plt.title('Tempo de chamadas RPC (gRPC) - Operações Simples')
    plt.grid(axis='y')
    plt.savefig('rpc_simple_calls.png')
    plt.show()

    # Gráfico de linha para StringCall
    tamanhos = [t[0] for t in resultados_stringcall]
    medias = [t[1] for t in resultados_stringcall]
    desvios = [t[2] for t in resultados_stringcall]

    plt.figure(figsize=(10, 6))
    plt.errorbar(tamanhos, medias, yerr=desvios, fmt='-o', capsize=5, color='green')
    plt.xscale('log', base=2)
    plt.xlabel('Tamanho da string')
    plt.ylabel('Tempo médio (s)')
    plt.title('Tempo de StringCall em função do tamanho da string')
    plt.grid(True, which="both", ls="--")
    plt.savefig('rpc_string_calls.png')
    plt.show()

if __name__ == "__main__":
    logging.basicConfig()
    run()

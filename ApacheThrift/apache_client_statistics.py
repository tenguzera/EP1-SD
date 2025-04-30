from apache_test import TestService
from apache_test.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

import time
import random
import string
import statistics
import matplotlib.pyplot as plt

# Configurações
NUM_REPETICOES = 10
STRING_SIZES = [2 ** i for i in range(0, 11)]

def generate_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

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

def medir_tempo(func):
    tempos = []
    for _ in range(NUM_REPETICOES):
        start = time.perf_counter()
        func()
        end = time.perf_counter()
        tempos.append(end - start)
    return tempos

def criar_cliente():
    transport = TSocket.TSocket('localhost', 50051)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = TestService.Client(protocol)
    transport.open()
    return client

def run():
    client = criar_cliente()

    print("Conectado ao servidor Thrift.")

    # Testes básicos com média e desvio padrão
    resultados = {}

    tempos = medir_tempo(lambda: chamada_void(client))
    resultados["VoidCall"] = (statistics.mean(tempos), statistics.stdev(tempos))

    tempos = medir_tempo(lambda: chamada_long(client))
    resultados["LongCall"] = (statistics.mean(tempos), statistics.stdev(tempos))

    tempos = medir_tempo(lambda: chamada_longarray(client))
    resultados["LongArrayCall"] = (statistics.mean(tempos), statistics.stdev(tempos))

    tempos = medir_tempo(lambda: chamada_complex(client))
    resultados["ComplexCall"] = (statistics.mean(tempos), statistics.stdev(tempos))

    # Testes com StringCall de vários tamanhos
    resultados_stringcall = []
    for size in STRING_SIZES:
        s = generate_string(size)
        tempos = medir_tempo(lambda: chamada_string(client, s))
        resultados_stringcall.append((size, statistics.mean(tempos), statistics.stdev(tempos)))

    gerar_graficos(resultados, resultados_stringcall)

def gerar_graficos(resultados, resultados_stringcall):
    # Gráfico de barras para operações simples
    labels = list(resultados.keys())
    medias = [resultados[k][0] for k in labels]
    desvios = [resultados[k][1] for k in labels]

    plt.figure(figsize=(10, 6))
    plt.bar(labels, medias, yerr=desvios, capsize=5, color='lightcoral')
    plt.ylabel("Tempo médio (s)")
    plt.title("Tempo de chamadas RPC (Thrift) - Operações Simples")
    plt.grid(axis='y')
    plt.savefig("thrift_simple_calls.png")
    plt.show()

    # Gráfico de linha para StringCall
    tamanhos = [x[0] for x in resultados_stringcall]
    medias = [x[1] for x in resultados_stringcall]
    desvios = [x[2] for x in resultados_stringcall]

    plt.figure(figsize=(10, 6))
    plt.errorbar(tamanhos, medias, yerr=desvios, fmt='-o', capsize=5, color='darkgreen')
    plt.xscale('log', base=2)
    plt.xlabel("Tamanho da string")
    plt.ylabel("Tempo médio (s)")
    plt.title("Tempo de StringCall em função do tamanho da string (Thrift)")
    plt.grid(True, which="both", ls="--")
    plt.savefig("thrift_string_calls.png")
    plt.show()

if __name__ == "__main__":
    run()

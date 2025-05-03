# RPC Benchmark: gRPC vs Apache Thrift

Este projeto compara o desempenho entre **gRPC** e **Apache Thrift** em diferentes tipos de chamadas RPC utilizando Python. Ele inclui:

- Implementações de cliente/servidor gRPC e Thrift
- Scripts para benchmark de tempo, throughput e concorrência
- Visualização gráfica dos resultados

---

## 📦 Requisitos

- Python (Testado com a versão 3.12)

---

## 🔧 Instalação

1. Clone o repositório e acesse a pasta:
```bash
git clone https://github.com/tenguzera/EP1-SD/
cd EP1-SD
```
   
2. Instale as dependências:
`pip install -r requirements.txt`

3. Compile os arquivos gRPC e Thrift **(opcional)**:
   
Os arquivos .proto e .thrift foram fornecidos caso deseje compilar diretamente.
Navegue até a pasta onde estão localizados e compile com:
  ```bash
  python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. grpc_test.proto # gRPC
  thrift --gen py rpc_test.thrift # Thrift
  ```
  Será necessário modificar os arquivos gerados, para isso consulte a documentação respectiva a cada RPC.

## 🚀 Executando o gRPC

1. Acesse a pasta e inicie o servidor:
   
```bash
cd gRPC
python grpc_server.py
```

2. Execute o clientes:

```bash
python grpc_client.py
python grpc_client_statistics.py # Benchmark Estatístico (tempo médio, desvio padrão)
python grpc_client_concurrency.py # Benchmark de Concorrência e Throughput
```

Os resultados serão exibidos no terminal e salvos em gráficos no diretório.

## 💻 Executando o Thrift:

1. Acesse a pasta e inicie o servidor:
   
```bash
cd ApacheThrift
python thrift_server.py
```

2. Execute o clientes:

```bash
python thrift_client.py
python thrift_client_statistics.py # Benchmark Estatístico (tempo médio, desvio padrão)
python thrift_client_concurrency.py # Benchmark de Concorrência e Throughput (por alguma razão não termina de executar nunca)
```

## 📌 Tipos de chamadas implementadas

`voidCall()` — sem argumentos

`longCall(LongValue)`

`longArrayCall(LongArray)`

`stringCall(StringValue)` — com tamanho variável

`complexCall(ComplexValue)` — estrutura com múltiplos campos

## 🧪 Métricas Avaliadas

- Tempo de execução médio

- Desvio padrão

- Throughput (requisições por segundo)

- Escalabilidade com múltiplos clientes (concorrência)

## 🌐 Testes Remotos

A implementação está feita para testes locais, caso deseje rodar cliente e servidor em máquinas diferentes será necessário editar a implementação com o ip onde o servidor está localizado.

Verifique os comentários no código para saber onde fazer essaa alteração.

## 📬 Contato

Contribuições são bem-vindas! Para dúvidas ou sugestões, entre em contato com o autor ou abra uma issue.

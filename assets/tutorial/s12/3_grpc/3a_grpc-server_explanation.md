#### Seminar 12 – Stage 4

## Implementarea unui server gRPC în Python (Calculator)

În această etapă implementăm **serverul gRPC** care expune serviciul `Calculator` definit în `calculator.proto`.

Reamintire din fișierul `.proto`:

```proto
service Calculator {
  rpc Add (AddRequest) returns (AddResponse);
  rpc Multiply (MultiplyRequest) returns (MultiplyResponse);
  rpc Power (PowerRequest) returns (PowerResponse);
}
```

Generarea codului s-a făcut cu:

```bash
python -m grpc_tools.protoc -I. \
  --python_out=. \
  --grpc_python_out=. \
  calculator.proto
```

Acest lucru a creat două fișiere:

* `calculator_pb2.py` – definițiile mesajelor (AddRequest, AddResponse etc.)
* `calculator_pb2_grpc.py` – scheletul pentru server și client (CalculatorServicer, CalculatorStub)

---

### 1. Structura unui server gRPC în Python

Pașii generali:

1. Importăm modulele generate:

   ```python
   import calculator_pb2
   import calculator_pb2_grpc
   ```

2. Definim o clasă care extinde `CalculatorServicer`:

   ```python
   class CalculatorService(calculator_pb2_grpc.CalculatorServicer):
       def Add(self, request, context):
           # logica metodei
           return calculator_pb2.AddResponse(result=request.a + request.b)
   ```

3. Creăm un server gRPC:

   ```python
   server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
   calculator_pb2_grpc.add_CalculatorServicer_to_server(CalculatorService(), server)
   server.add_insecure_port("[::]:50051")
   server.start()
   server.wait_for_termination()
   ```

---

### 2. Ce va face serverul nostru?

Serviciul `Calculator` va suporta 3 metode:

* `Add(a, b)` – întoarce `a + b`
* `Multiply(a, b)` – întoarce `a * b`
* `Power(base, exponent)` – întoarce `base ** exponent`

Serverul va:

* afișa în consolă cererile primite (pentru debugging)
* rula pe portul `50051` (standard de facto în exemplele gRPC)
* folosi un `ThreadPoolExecutor` pentru a procesa cereri în paralel

---

### 3. Fișierul `grpc_server.py`

În fișierul de mai jos sunt comentarii și TODO-uri pentru studenți.
După completare, serverul trebuie să poată fi pornit cu:

```bash
python grpc_server.py
```

și să rămână „în așteptare” pe portul 50051.

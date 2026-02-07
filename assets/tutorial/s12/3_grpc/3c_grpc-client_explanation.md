#### Seminar 12 – Stage 5

## Client gRPC în Python pentru serviciul Calculator

În această etapă vom implementa **clientul gRPC** pentru serviciul `Calculator` din Stage 4.

Reamintire:

* serverul gRPC rulează pe `localhost:50051`
* serviciul `Calculator` expune metodele:

  * `Add(AddRequest) returns (AddResponse)`
  * `Multiply(MultiplyRequest) returns (MultiplyResponse)`
  * `Power(PowerRequest) returns (PowerResponse)`

Clientul va:

1. crea un canal gRPC către `localhost:50051`
2. crea un stub `CalculatorStub`
3. trimite request-uri cu diferite valori pentru `a`, `b`, `base`, `exponent`
4. afișa rezultatele
5. scrie rezultatele într-un fișier de log

---

### 1. Pași principali pentru un client gRPC în Python

1. Importăm modulele generate și `grpc`:

   ```python
   import grpc
   import calculator_pb2
   import calculator_pb2_grpc
   ```

2. Creăm un canal:

   ```python
   channel = grpc.insecure_channel("localhost:50051")
   ```

3. Creăm un stub:

   ```python
   stub = calculator_pb2_grpc.CalculatorStub(channel)
   ```

4. Construim un mesaj de request:

   ```python
   request = calculator_pb2.AddRequest(a=2, b=3)
   ```

5. Apelăm metoda remote:

   ```python
   response = stub.Add(request)
   print(response.result)
   ```

---

### 2. Ce va face clientul nostru

* va cere utilizatorului să introducă perechi de numere pentru:

  * Add (a, b)
  * Multiply (a, b)
  * Power (base, exponent)
* va apela metodele corespunzătoare
* va afișa rezultatele pe ecran
* va scrie într-un fișier `grpc_client_log.txt`:

  * valorile de intrare
  * metoda apelată
  * rezultatul

---

### 3. Fișierul `grpc_client.py`

Vom avea câteva TODO-uri ușoare pentru studenți:

* completat apelurile Multiply și Power
* citirea de la tastatură

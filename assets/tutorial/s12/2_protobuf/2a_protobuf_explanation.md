### Seminar 12 – Stage 3

## Protobuf + gRPC – Definirea unui contract `.proto`

În gRPC, **primul pas este definirea contractului** dintre client și server.
Acest contract se salvează într-un fișier `.proto` și conține:

* definițiile **structurilor de date** (mesaje)
* definițiile **serviciilor** (API-ul expus)
* definițiile **metodelor RPC**

După scrierea fișierului `.proto`, generăm automat cod pentru Python folosind:

```
python -m grpc_tools.protoc -I. \
  --python_out=. \
  --grpc_python_out=. \
  calculator.proto
```

Această comandă creează două fișiere:

* `calculator_pb2.py` – definițiile structurilor
* `calculator_pb2_grpc.py` – clasele pentru server/client

Studentul **nu trebuie să modifice** aceste fișiere — sunt generate automat.

---

## 1. Structura unui fișier `.proto`

Exemplu minimal:

```proto
syntax = "proto3";

message AddRequest {
  int32 a = 1;
  int32 b = 2;
}

message AddResponse {
  int32 result = 1;
}

service Calculator {
  rpc Add (AddRequest) returns (AddResponse);
}
```

Observații importante:

* `syntax = "proto3";` → versiunea modernă
* câmpurile au **tip, nume, index** (`a = 1`, `b = 2`)
* indexul este parte din formatul serializat
* mesajele sunt tipuri custom
* `service` definește un API cu metode

---

## 2. Tipuri primitive Protobuf

Proto3 suportă tipuri precum:

* `int32`, `int64`, `float`, `double`
* `bool`
* `string`
* `bytes` pentru date binare
* liste: `repeated int32 values = 1;`

---

## 3. Definirea serviciului nostru

Vom crea un serviciu simplu de tip „calculator”, cu 3 metode:

* Add(a, b)
* Multiply(a, b)
* Power(a, b) – exponentiere (opțional pentru studenți)

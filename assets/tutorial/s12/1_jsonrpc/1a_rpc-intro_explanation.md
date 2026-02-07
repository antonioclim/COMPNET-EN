### Seminar 12 – Stage 1

## Introducere în RPC (Remote Procedure Call) + unde se încadrează Protobuf

### 1. Ce este RPC?

RPC (Remote Procedure Call) este un mecanism prin care un program poate apela o funcție care se execută pe o altă mașină, ca și cum ar fi locală.

Exemplu conceptual:

**local:**

```
result = add(1, 2)
```

**remote:**

```
result = server.Add(AddRequest(1,2))
```

Diferența: apelul merge prin rețea, în loc să fie un apel de funcție local.

---

### 2. RPC vs REST

| Caracteristică | RPC                                   | REST                         |
| -------------- | ------------------------------------- | ---------------------------- |
| Nivel          | orientat pe *proceduri/metode*        | orientat pe *resurse/URI*    |
| Exemplu        | `UserService.GetUser({id:1})`         | `GET /users/1`               |
| Contract       | definit de regulă prin schema (proto) | nu există un contract strict |
| Serializare    | Protobuf, JSON, custom                | JSON                         |
| Conexiune      | adesea persistentă (gRPC/HTTP2)       | HTTP 1.1 / HTTP 2            |

RPC este util în:

* microservicii,
* latență mică, eficiență mare,
* streaming bidirecțional,
* API-uri interne de performanță mare.

REST este util în:

* API-uri publice,
* debugging ușor,
* interoperabilitate universală.

---

### 3. Modele de RPC

Există mai multe standarde:

* **JSON-RPC** – simplu, bazat pe JSON, rulat peste HTTP.
* **XML-RPC** – istoric, dar încă funcțional.
* **gRPC** – standard modern, bazat pe HTTP/2 + Protocol Buffers.
* **Apache Thrift**, **Cap’n Proto**, **Avro** – alternative de serializare + RPC.

Noi vom studia **JSON-RPC** (ca exemplu simplu) și **gRPC** (ca exemplu modern).

---

### 4. Ce este Protocol Buffers?

Protobuf este:

* un limbaj de descriere a datelor (*interface definition language*)
* * un format de serializare binar,
* * un generator de cod pentru mai multe limbaje.

În gRPC, fișierul `.proto` definește:

* structuri de date (mesaje)
* servicii (metode RPC)
* tipuri de request/response

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
```

La generare, Python va primi clase ca:

```
AddRequest(a=1, b=2)
```

---

### 5. Tipuri de apel RPC

* **Unary RPC** – request → response (majoritatea implementărilor).
* **Server streaming** – clientul trimite o cerere, primește un flux de răspunsuri.
* **Client streaming** – clientul trimite un flux, primește un răspuns.
* **Bidirectional streaming** – flux în ambele sensuri (gRPC).

În tutorialul acesta vom folosi **unary RPC**.

---

### 6. Ce urmează în seminar?

1. Stage 1 – Concepte RPC (acest fișier)
2. **Stage 2 – Client JSON-RPC către un serviciu public (sau un server de test)**
3. Stage 3 – Introducere Protobuf + fișier `.proto` gRPC
4. Stage 4 – Server gRPC în Python
5. Stage 5 – Client gRPC în Python

### Seminar 12 – Part 1

## Introduction to RPC (Remote Procedure Call) and where Protocol Buffers fit

### 1. What is RPC?

RPC (Remote Procedure Call) is a mechanism through which a programme can call a function that is executed on another machine, as if it were local.

Conceptual example:

**local:**

```python
result = add(1, 2)
```

**remote:**

```python
result = server.Add(AddRequest(1, 2))
```

The key difference is that the call is performed over the network, rather than as a direct local function call.

---

### 2. RPC vs REST

| Characteristic | RPC | REST |
|---|---|---|
| Level | procedure/method-oriented | resource/URI-oriented |
| Example | `UserService.GetUser({id:1})` | `GET /users/1` |
| Contract | usually defined via a schema (e.g. .proto) | often no strict contract |
| Serialisation | Protobuf, JSON or custom | JSON |
| Connection | often persistent (e.g. gRPC/HTTP2) | HTTP/1.1 or HTTP/2 |

RPC is useful in:

- microservices
- low latency and high efficiency
- bidirectional streaming
- high-performance internal APIs

REST is useful in:

- public APIs
- easier debugging
- broad interoperability

---

### 3. RPC models

There are several standards:

- **JSON-RPC** – simple, JSON-based, typically over HTTP
- **XML-RPC** – historical but still functional
- **gRPC** – modern standard, based on HTTP/2 + Protocol Buffers
- **Apache Thrift**, **Cap’n Proto**, **Avro** – alternative RPC and serialisation ecosystems

This seminar examines **JSON-RPC** (as a simple example) and **gRPC** (as a modern example).

---

### 4. What are Protocol Buffers?

Protocol Buffers (Protobuf) are:

- an interface definition language (IDL) for describing data
- a binary serialisation format
- a code generation tool for multiple programming languages

In gRPC, the `.proto` file defines:

- data structures (messages)
- services (RPC methods)
- request and response types

Minimal example:

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

After code generation, Python receives classes that can be used as:

```text
AddRequest(a=1, b=2)
```

---

### 5. RPC call types

- **Unary RPC** – request → response (the most common model)
- **Server streaming** – the client sends one request and receives a stream of responses
- **Client streaming** – the client sends a stream and receives one response
- **Bidirectional streaming** – streams in both directions (gRPC)

This seminar focuses on **unary RPC**.

---

### 6. What follows in Seminar 12?

1. Part 1 – RPC concepts (this file)
2. Part 2 – JSON-RPC client to a public service (or a test server)
3. Part 3 – Protobuf introduction and a `.proto` file for gRPC
4. Part 4 – gRPC server in Python
5. Part 5 – gRPC client in Python

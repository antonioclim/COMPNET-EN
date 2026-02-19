### Seminar 12 – Part 3

## Protobuf + gRPC – defining a `.proto` contract

In gRPC, the **first step is defining the contract** between client and server.
This contract is stored in a `.proto` file and contains:

- definitions of **data structures** (messages)
- definitions of **services** (the exposed API)
- definitions of **RPC methods**

After writing the `.proto` file, we generate Python code automatically using:

```bash
python -m grpc_tools.protoc -I.   --python_out=.   --grpc_python_out=.   S12_Part02_Config_Calculator.proto
```

This command generates two files:

- `S12_Part02_Config_Calculator_pb2.py` – message definitions
- `S12_Part02_Config_Calculator_pb2_grpc.py` – server/client stubs

Students should **not modify** these generated files.

---

## 1. Structure of a `.proto` file

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

service Calculator {
  rpc Add (AddRequest) returns (AddResponse);
}
```

Important notes:

- `syntax = "proto3";` indicates the modern version
- fields have **type, name and index** (`a = 1`, `b = 2`)
- the index is part of the serialised format
- messages define custom types
- `service` defines an API with methods

---

## 2. Primitive Protobuf types

Proto3 supports types such as:

- `int32`, `int64`, `float`, `double`
- `bool`
- `string`
- `bytes` for binary data
- lists: `repeated int32 values = 1;`

---

## 3. Defining our service

The exercise defines a simple "calculator" service with three methods:

- Add(a, b)
- Multiply(a, b)
- Power(a, b) – exponentiation (optional for students)

#### Seminar 12 – Part 4

## Implementing a gRPC server in Python (Calculator)

The objective here is to implement the **gRPC server** that exposes the `Calculator` service defined in `S12_Part02_Config_Calculator.proto`.

Reminder from the `.proto` file:

```proto
service Calculator {
  rpc Add (AddRequest) returns (AddResponse);
  rpc Multiply (MultiplyRequest) returns (MultiplyResponse);
  rpc Power (PowerRequest) returns (PowerResponse);
}
```

Code generation is performed with:

```bash
python -m grpc_tools.protoc -I.   --python_out=.   --grpc_python_out=.   S12_Part02_Config_Calculator.proto
```

This creates two files:

- `S12_Part02_Config_Calculator_pb2.py` – message definitions (AddRequest, AddResponse and so on)
- `S12_Part02_Config_Calculator_pb2_grpc.py` – server/client scaffolding (CalculatorServicer, CalculatorStub)

---

### 1. Structure of a gRPC server in Python

General steps:

1. Import the generated modules:

   ```python
   import S12_Part02_Config_Calculator_pb2 as calculator_pb2
   import S12_Part02_Config_Calculator_pb2_grpc as calculator_pb2_grpc
   ```

2. Define a class that extends `CalculatorServicer`:

   ```python
   class CalculatorService(calculator_pb2_grpc.CalculatorServicer):
       def Add(self, request, context):
           # method logic
           return calculator_pb2.AddResponse(result=request.a + request.b)
   ```

3. Create and start the gRPC server:

   ```python
   server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
   calculator_pb2_grpc.add_CalculatorServicer_to_server(CalculatorService(), server)
   server.add_insecure_port("[::]:50051")
   server.start()
   server.wait_for_termination()
   ```

---

### 2. What will our server do?

The `Calculator` service will support three methods:

- `Add(a, b)` – returns `a + b`
- `Multiply(a, b)` – returns `a * b`
- `Power(base, exponent)` – returns `base ** exponent`

The server will:

- print received requests to the console (for debugging)
- run on port `50051` (a de facto standard in gRPC examples)
- use a `ThreadPoolExecutor` to process requests in parallel

---

### 3. The file `S12_Part03_Script_g_RPC_Server.py`

The file contains comments and TODO sections for students.
After completing it, the server should be started with:

```bash
python S12_Part03_Script_g_RPC_Server.py
```

and it should remain listening on port 50051.

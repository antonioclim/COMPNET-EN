#### Seminar 12 – Part 5

## gRPC client in Python for the Calculator service

This part covers the **gRPC client** for the `Calculator` service from Part 4.

Reminder:

- the gRPC server runs on `localhost:50051`
- the `Calculator` service exposes the methods:

  - `Add(AddRequest) returns (AddResponse)`
  - `Multiply(MultiplyRequest) returns (MultiplyResponse)`
  - `Power(PowerRequest) returns (PowerResponse)`

The client will:

1. create a gRPC channel to `localhost:50051`
2. create a `CalculatorStub`
3. send requests with different values (`a`, `b`, `base`, `exponent`)
4. print the results
5. write results into a log file

---

### 1. Key steps for a gRPC client in Python

1. Import `grpc` and the generated modules:

   ```python
   import grpc
   import S12_Part02_Config_Calculator_pb2 as calculator_pb2
   import S12_Part02_Config_Calculator_pb2_grpc as calculator_pb2_grpc
   ```

2. Create a channel:

   ```python
   channel = grpc.insecure_channel("localhost:50051")
   ```

3. Create a stub:

   ```python
   stub = calculator_pb2_grpc.CalculatorStub(channel)
   ```

4. Build a request message:

   ```python
   request = calculator_pb2.AddRequest(a=2, b=3)
   ```

5. Call the remote method:

   ```python
   response = stub.Add(request)
   print(response.result)
   ```

---

### 2. What our client will do

The client will ask the user to enter pairs of numbers for:

- Add (a, b)
- Multiply (a, b)
- Power (base, exponent)

Then it will:

- call the corresponding RPC methods
- display results on the screen
- write into a file `grpc_client_log.txt`:

  - input values
  - the called method
  - the result

---

### 3. The file `S12_Part03_Script_g_RPC_Client.py`

The file contains a few simple TODOs for students, such as:

- completing the Multiply and Power calls
- reading values from the keyboard

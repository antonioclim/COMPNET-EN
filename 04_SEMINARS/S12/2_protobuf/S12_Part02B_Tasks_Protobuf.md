## Tasks – Part 3 (Protobuf)

Create a file named:

`stage3_protobuf_output.txt`

Complete the TODO sections in `S12_Part02_Config_Calculator.proto`:

1. Define the message `PowerRequest` with the fields:

   - `int32 base`
   - `int32 exponent`

2. Define `PowerResponse` with the field:

   - `int32 result`

3. Add the RPC method:

   ```proto
   rpc Power (PowerRequest) returns (PowerResponse);
   ```

Then run:

```bash
python -m grpc_tools.protoc -I.   --python_out=.   --grpc_python_out=.   S12_Part02_Config_Calculator.proto
```

In `stage3_protobuf_output.txt`, include:

- a screenshot or copy/paste of the directory listing showing the generated files
- a short message confirming that code generation succeeded

## Sarcini Stage 3 – Protobuf

Creați fișierul:

`stage3_protobuf_output.txt`

Completați în `calculator.proto` următoarele TODO-uri:

1. Definiți mesajul `PowerRequest` cu câmpurile:

   * `int32 base`
   * `int32 exponent`
2. Definiți `PowerResponse` cu câmpul:

   * `int32 result`
3. Adăugați metoda:

   ```
   rpc Power (PowerRequest) returns (PowerResponse);
   ```

Apoi rulați comanda:

```
python -m grpc_tools.protoc -I. \
  --python_out=. \
  --grpc_python_out=. \
  calculator.proto
```

În fișierul `stage3_protobuf_output.txt`, includeți:

* un screenshot sau copy/paste cu directorul unde apar cele două fișiere generate
* un mesaj scurt care confirmă că generarea a funcționat

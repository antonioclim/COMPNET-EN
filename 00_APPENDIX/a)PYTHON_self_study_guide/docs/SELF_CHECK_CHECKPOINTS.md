# 🔍 Self-Check Checkpoints
## Quick Knowledge Verification for Each Learning Step

> **How to use:** After completing each Step in PYTHON_NETWORKING_GUIDE.md, answer these questions without looking at the materials. If you struggle with more than one question per section, review that Step before continuing.

---

## Step 1: Reading Python Code

### Can you answer these?

1. How do you define a function that takes a string and returns an integer?

2. What does this line mean: `def ping(host: str, count: int = 3) -> float:`?

3. Rewrite this C code in Python: `if (x > 0) { return x * 2; }`

<details>
<summary>Answers</summary>

1. `def my_func(text: str) -> int:`

2. Function `ping` takes a string `host`, an optional integer `count` (default 3) and returns a float.

3.
```python
if x > 0:
    return x * 2
```

</details>

### Ready for Step 2 when:
- [ ] You can read Python function signatures
- [ ] You understand indentation replaces braces
- [ ] You recognise type hints (they are optional but helpful)

---

## Step 2: Data Types for Networking

### Can you answer these?

1. What is the difference between `"Hello"` and `b"Hello"`?

2. How do you convert the string `"GET /"` to bytes for sending over a socket?

3. What error do you get if you try `socket.send("Hello")`?

<details>
<summary>Answers</summary>

1. `"Hello"` is a string (text), `b"Hello"` is bytes (raw data). Sockets require bytes.

2. `"GET /".encode('utf-8')` or `"GET /".encode()`

3. `TypeError: a bytes-like object is required, not 'str'`

</details>

### Ready for Step 3 when:
- [ ] You know the difference between str and bytes
- [ ] You can convert between them with encode()/decode()
- [ ] You understand why networks need bytes

---

## Step 3: Binary Data with struct

### Can you answer these?

1. What does `struct.pack('!H', 8080)` return?

2. Why is the `!` important in the format string?

3. How do you unpack a 4-byte integer from network data?

<details>
<summary>Answers</summary>

1. `b'\x1f\x90'` — two bytes representing 8080 in big-endian

2. `!` means network byte order (big-endian). Without it, you get native byte order which may differ between machines.

3. `value, = struct.unpack('!I', data[:4])`

</details>

### Ready for Step 4 when:
- [ ] You can pack integers into bytes
- [ ] You understand network byte order
- [ ] You know common format codes: B, H, I, Q

---

## Step 4: Socket Programming

### Can you answer these?

1. What is the difference between `SOCK_STREAM` and `SOCK_DGRAM`?

2. Write the server sequence: socket → ? → ? → ? → accept

3. Why do we use `with socket.socket(...) as s:`?

<details>
<summary>Answers</summary>

1. `SOCK_STREAM` = TCP (reliable, connection-oriented), `SOCK_DGRAM` = UDP (unreliable, connectionless)

2. socket → bind → listen → accept

3. Context manager ensures the socket is closed even if an exception occurs. Prevents resource leaks.

</details>

### Ready for Step 5 when:
- [ ] You can create TCP and UDP sockets
- [ ] You know the server/client sequences
- [ ] You use context managers for cleanup

---

## Step 5: Code Organisation

### Can you answer these?

1. What does `if __name__ == '__main__':` do?

2. How do you import a specific function from a module?

3. What is a dataclass and when would you use one?

<details>
<summary>Answers</summary>

1. Code inside this block runs only when the file is executed directly, not when imported as a module.

2. `from module_name import function_name`

3. A dataclass is a class that primarily stores data. Use `@dataclass` decorator. Good for protocol headers, configuration and structured data.

</details>

### Ready for Step 6 when:
- [ ] You understand module imports
- [ ] You can structure code with main blocks
- [ ] You know when to use dataclasses

---

## Step 6: Command-Line Interfaces

### Can you answer these?

1. How do you create a required positional argument with argparse?

2. How do you add an optional flag `--verbose` that defaults to False?

3. What does `args = parser.parse_args()` return?

<details>
<summary>Answers</summary>

1. `parser.add_argument('hostname')` — no dashes means positional

2. `parser.add_argument('--verbose', action='store_true')`

3. A namespace object where arguments are attributes: `args.hostname`, `args.verbose`

</details>

### Ready for Step 7 when:
- [ ] You can create CLI tools with argparse
- [ ] You know positional vs optional arguments
- [ ] You can add help text and defaults

---

## Step 7: Working with Protocols

### Can you answer these?

1. How do you parse JSON data received from a socket?

2. What module do you use for HTTP requests?

3. How do you handle a response that might not be valid JSON?

<details>
<summary>Answers</summary>

1. `import json; data = json.loads(received_bytes.decode())`

2. `requests` (third-party) or `urllib.request` (standard library)

3. Wrap in try/except: `try: data = json.loads(text) except json.JSONDecodeError: ...`

</details>

### Ready for Step 8 when:
- [ ] You can parse and generate JSON
- [ ] You understand HTTP request/response basics
- [ ] You handle parsing errors gracefully

---

## Step 8: Error Handling

### Can you answer these?

1. What exception do you catch for a connection timeout?

2. How do you set a socket timeout to 5 seconds?

3. What does `recv()` return when the connection closes?

<details>
<summary>Answers</summary>

1. `socket.timeout`

2. `sock.settimeout(5.0)`

3. Empty bytes: `b''`. This is not an error — it signals the peer closed the connection.

</details>

### Ready for Step 9 when:
- [ ] You handle timeouts and connection errors
- [ ] You detect closed connections
- [ ] You use try/except/finally for cleanup

---

## Step 9: Debugging and Best Practices

### Can you answer these?

1. Why use `logging` instead of `print()`?

2. How do you see what data is actually being sent/received?

3. What tool captures network traffic for analysis?

<details>
<summary>Answers</summary>

1. Logging has levels (DEBUG, INFO, WARNING, ERROR), can be redirected to files and can be disabled in production without removing code.

2. Use logging at DEBUG level, or print the hex representation: `print(data.hex())`

3. Wireshark (GUI) or tcpdump (CLI)

</details>

### You are ready for labs when:
- [ ] You use logging for debugging
- [ ] You can inspect network traffic
- [ ] You write clean, documented code

---

## Final Assessment

If you completed all checkpoints above, take the full quiz:

```bash
make quiz
```

**Target score:** 70% or higher means you are ready for the networking labs.

**Below 70%:** Review the sections where you struggled, then retake.

---

*Self-Check Checkpoints — Python Networking Guide*
*Computer Networks Course — ASE Bucharest, CSIE*
*Version: 1.6.0 | January 2026*

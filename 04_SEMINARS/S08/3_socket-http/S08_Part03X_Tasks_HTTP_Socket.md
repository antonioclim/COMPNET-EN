### Tasks — Manually Implemented HTTP Server

#### 1. Complete the `S08_Part03B_Example_Socket_HTTP_Server.py` file

The areas marked with:

```

# >>> STUDENT TODO

```

must be completed:

- parsing the first line of the request
- sending the 404 response
- sending the 200 response

---

#### 2. Start the server

```

python3 S08_Part03B_Example_Socket_HTTP_Server.py 8000

```

You should see:

```

Manual HTTP server started on port 8000

```

---

#### 3. Test with curl

Execute:

```

curl -v [http://localhost:8000/](http://localhost:8000/)
curl -v [http://localhost:8000/index.html](http://localhost:8000/index.html)
curl -v [http://localhost:8000/doesnotexist](http://localhost:8000/doesnotexist)

```

Save the results in:

```

socket_http_log.txt

```

---

#### 4. Browser test

Access:

```

[http://localhost:8000/](http://localhost:8000/)

```

Describe in `socket_http_log.txt` whether the page loads correctly.

---

#### 5. Short explanation (mandatory)

In the same file, in 5–6 sentences explain:

- how the server parses the request
- how it decides which file to send
- why `Content-Length` is necessary
- what happens when the file does not exist

---

This simple server forms the basis for the next stage: integration with an **nginx reverse proxy**.

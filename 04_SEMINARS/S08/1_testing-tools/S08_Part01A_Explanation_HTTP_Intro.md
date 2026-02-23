### Introduction to HTTP and Testing Tools (curl)

This stage provides a brief recap of the HTTP protocol and introduces
an essential instrument for testing web services: **curl**.

The goal is for students to understand what a real HTTP request looks like, what
status codes and headers mean, and how a client that is NOT a browser behaves
(production-grade clients frequently rely on curl/wget/HTTP libraries).

---

### 1. What Is HTTP?

HTTP (HyperText Transfer Protocol) is a text-based, request–response protocol.
Communication takes place between:

- **Client** (browser, curl, mobile application, script)
- **Server** (Apache, nginx, Flask, Django, custom server etc.)

Basic structure:

#### Request:

```

GET /index.html HTTP/1.1
Host: example.com
User-Agent: curl/8.0
Accept: */*

(optional body)

```

#### Response:

```

HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 1256

<html>...</html>
```

Key components:

* **Start line** (e.g. `GET / HTTP/1.1`)
* **Headers**
* **Body** (optional, depending on the method)

---

### 2. Why curl?

`curl` is the simplest yet most complete tool for:

* rapid endpoint testing
* viewing the raw request/response
* REST API testing
* simulating different methods (GET, POST, PUT, DELETE)
* debugging

---

### 3. Essential curl Commands

#### Standard GET:

```
curl http://example.com
```

#### Verbose request (request and response details):

```
curl -v http://example.com
```

#### Response headers only (HEAD):

```
curl -I http://example.com
```

#### Sending a POST with body:

```
curl -X POST -d "name=test&age=20" http://example.com/api
```

#### Saving the response to a file:

```
curl -o pagina.html http://example.com
```

---

### 4. How Do We Work in This Seminar?

1. We will use `curl` to test the HTTP servers we implement.
2. We will explicitly inspect status codes, headers and body.
3. We will compare the behaviour of different servers:

   * Python `http.server`
   * a manually implemented HTTP server using `socket`
   * an nginx HTTP server (in Docker)

---

### Next Stage

We will start a minimal HTTP server using the `http.server` module from Python,
so that we have a fully functional server before manually implementing
the HTTP protocol with sockets.

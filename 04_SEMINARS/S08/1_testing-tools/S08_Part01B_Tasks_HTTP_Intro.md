### Tasks — HTTP Introduction + curl

#### 1. Test several public sites using curl

Run the following commands and save the results in a file named:

```

curl_basics_log.txt

```

Recommended commands:

1. `curl http://example.com`
2. `curl -v http://example.com`
3. `curl -I http://example.com`

For each command, identify in your file:

- the status code (e.g. `200 OK`)
- at least 3 HTTP headers (e.g. `Content-Type`, `Server`, `Date`)
- the differences between request and response

---

#### 2. Test a dynamic endpoint

Choose any server that exposes a simple API endpoint (e.g. httpbin.org):

```

curl -v [http://httpbin.org/get](http://httpbin.org/get)
curl -X POST -d "x=1&y=2" [http://httpbin.org/post](http://httpbin.org/post)

```

Append the results to the same `curl_basics_log.txt` file.

---

#### 3. Short question (include in your report)

In a new file:

```

curl_questions.txt

```

Answer in 2–3 sentences:

- Why is it useful to see the complete request when debugging an HTTP service?
- Why is `curl` often preferred over a browser for technical debugging?

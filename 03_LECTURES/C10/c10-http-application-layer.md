### HTTP(S), REST and WebSockets
### Application layer: behaviour, performance and correctness

---

### Context
Students have already completed a course in web technologies:
- React + Redux (SPA)
- REST backend with ORM-based persistence
- Practical use of HTTP, REST and JSON

This lecture:
- does not revisit 'how to build an API'
- focuses on what actually happens in the protocol
- emphasises diagnosis, interoperability and performance

---

### Learning objectives
By the end of the lecture, students should be able to:
- Explain the real behaviour of HTTP over a TCP connection
- Understand how headers affect client behaviour
- Distinguish closely related HTTP semantic errors (401 vs 403, 404 vs 405 and similar cases)
- Explain why some requests work in Postman but not in a browser
- Understand caching, negotiation and compression mechanisms
- Understand WebSocket as a protocol extension, not a 'JavaScript API'
- Place REST, WebSocket and HTTPS correctly within the Internet architecture

---

### Where HTTP sits in the architecture
- HTTP runs over TCP (or QUIC)
- It depends on:
  - connections
  - latency
  - retransmissions
- Many web problems are protocol problems, not framework problems

---

### HTTP: extremely short recap
- Application-layer protocol
- Request–response model
- Initiated exclusively by the client
- Text headers with an arbitrary body
- Stateless by default

---

### HTTP is not 'stateless' in practice
- The protocol is stateless
- Applications are not
- State moves into:
  - cookies
  - tokens
  - URLs
  - server-side session stores
- A direct link to session-layer (L5) concepts

---

### HTTP connections
- HTTP/1.1 uses persistent connections (keep-alive)
- Multiple requests can be sent over the same TCP connection
- Response ordering matters (head-of-line blocking)

In production, clients rarely connect directly to the origin server. A reverse proxy (e.g. Nginx) terminates client connections and opens separate backend connections, managing keep-alive, load distribution and request routing independently on each side.

[FIG] assets/images/fig-http-reverse-proxy.png

---

### The real cost of an HTTP request
- Bandwidth is rarely the main problem
- The main costs are:
  - latency
  - TCP handshake
  - TLS handshake
  - multiple round trips
- Motivation for HTTP/2 and HTTP/3

---

### HTTP request structure (practical relevance)
- Request line: method + path
- Headers:
  - control server behaviour
  - control browser behaviour
- Body:
  - optional
  - interpreted only through Content-Type

[FIG] assets/images/fig-http-request-response.png

---

### HTTP methods: semantics, not convention
- GET:
  - safe
  - idempotent
  - cacheable
- PUT:
  - idempotent
  - full replacement
- DELETE:
  - idempotent (final effect)
- POST:
  - neither safe
  - nor idempotent

---

### Why idempotency matters
- Automatic retries (proxy, client and load balancer)
- Timeouts
- Request repetition
- A direct link to reliability (transport layer)

[FIG] assets/images/fig-http-methods-idempotency.png

---

### Status codes: fine-grained semantics
- 401 Unauthorized:
  - missing authentication
- 403 Forbidden:
  - authenticated, but access is denied
- 404 Not Found:
  - the resource does not exist
- 405 Method Not Allowed:
  - the resource exists, the method does not
- 415 Unsupported Media Type:
  - incorrect Content-Type
- 422 Unprocessable Entity:
  - valid content, invalid semantics

---

### Content-Type vs Accept
- Content-Type:
  - what I send
- Accept:
  - what I can receive
- Negotiation is bidirectional
- Many bugs come from mismatches between them

---

### HTTP compression
- The client requests: Accept-Encoding
- The server responds: Content-Encoding
- gzip/br reduce traffic, but:
  - increase CPU cost
- Transparent to the application, critical for performance

---

### HTTP caching: a mechanism, not magic
- Cache-Control, Expires
- Last-Modified / If-Modified-Since
- 304 Not Modified:
  - a response without a body
  - drastically reduces traffic
- Caches are distributed (browser, proxy and CDN)

[FIG] assets/images/fig-http-caching-304.png

---

### Cookies: an application mechanism
- Carried via HTTP headers
- Solve:
  - session identification
  - preferences
- Critical flags:
  - Secure
  - HttpOnly
  - SameSite
- Direct security implications

---

### CORS: the browser security model
- Not an HTTP limitation
- A browser security policy
- Preflight:
  - an automatic OPTIONS request
  - triggered by 'non-simple' methods or headers
- The classic reason for 'it works in Postman but not in the browser'

The browser sends a preflight OPTIONS request to the target origin before the actual request. The server must respond with the appropriate `Access-Control-Allow-*` headers; otherwise the browser blocks the response at the client side.

[FIG] assets/images/fig-cors-preflight.png

---

### HTTP/1.1: classic limitations
- Head-of-line blocking
- Repeated headers
- Many serialised requests

---

### HTTP/2: what changes
- Multiplexing on the same connection
- Header compression
- Stream prioritisation
- No change to HTTP semantics

[FIG] assets/images/fig-http11-vs-http2.png

---

### WebSocket: when HTTP is no longer enough
- HTTP is initiated by the client
- The server cannot 'push' data
- WebSocket provides:
  - bidirectionality
  - long-lived connections
  - notifications

---

### WebSocket handshake
- Starts as an HTTP request
- Protocol upgrade
- After the handshake:
  - it is no longer HTTP
  - it is a frame-based protocol over TCP

When a reverse proxy sits between the client and the server, it must forward the `Upgrade` and `Connection` headers intact. Proxies that strip hop-by-hop headers by default will break the WebSocket handshake silently.

[FIG] assets/images/fig-websocket-upgrade-proxy.png

---

### WebSocket vs HTTP polling
- Polling:
  - many empty requests
  - latency
- WebSocket:
  - real notifications
  - efficiency
- Trade-off: keeping the connection open

[FIG] assets/images/fig-websocket-vs-polling.png

---

### HTTPS: conceptual recap
- HTTP over TLS
- Provides:
  - confidentiality
  - integrity
  - authentication
- TLS is negotiated before HTTP

---

### What HTTPS changes operationally
- Traffic inspection becomes impossible without MITM
- Certificates define the server identity
- Impact on:
  - proxies
  - caching
  - debugging

TLS can be terminated at different points in the infrastructure: at the reverse proxy, at the load balancer or at the application server itself. The choice affects where plaintext traffic exists and who holds the private key.

[FIG] assets/images/fig-https-tls-termination.png

---

### REST: an architectural style, not a technology
- Models a domain as resources
- Uses HTTP semantics
- Stateless
- Oriented towards interoperability

---

### REST levels (Richardson)
- Level 0: RPC over HTTP
- Level 1: addressable resources
- Level 2: resources + verbs + status codes
- Level 3: hypermedia (discoverability)

[FIG] assets/images/fig-rest-maturity-levels.png

---

### Correct REST vs 'cosmetic' REST
- Actions in the URL: a sign of RPC
- POST used for everything: semantic loss
- Missing correct status codes: harder debugging
- Good REST improves caching, proxies and scaling

---

### REST vs SOAP (context)
- REST:
  - web-native
  - simple
  - flexible
- SOAP:
  - strict contract
  - XML
  - enterprise extensions (WS-*)
- They solve different problems

---

### Where the practical examples fit
- Inspecting HTTP traffic with curl and browser devtools
- Demonstrations of:
  - caching
  - CORS
  - incorrect Content-Type
  - the WebSocket handshake
- Emphasis on 'why' and 'what happens'

---

### Summary
- HTTP is a protocol, not a framework
- Headers control real behaviour
- REST means using HTTP correctly
- WebSocket is a protocol extension
- HTTPS fundamentally changes traffic observability

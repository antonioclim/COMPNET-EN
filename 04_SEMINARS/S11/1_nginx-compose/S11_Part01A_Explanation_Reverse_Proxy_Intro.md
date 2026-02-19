## Introduction: reverse proxy and load balancing in distributed architectures

### Learning objectives

By the end of this section, students should be able to explain:

- what a reverse proxy is and how it differs from a forward proxy
- why Nginx is commonly used as a reverse proxy in modern architectures
- what load balancing means and where it sits in an HTTP request-response pipeline
- how the conceptual request-response flow looks when a proxy is involved
- the role of the custom load balancer that we will implement later

---

### 1. What is a reverse proxy?

A **reverse proxy** is a server placed between the client and a set of backend servers.
It receives requests from clients and forwards them to one or more internal services.

```
Client -> Reverse Proxy -> Backend 1
                      \-> Backend 2
                      \-> Backend 3
```

Unlike a **forward proxy**, which represents the client towards the outside world,
a **reverse proxy represents the backend services**.

---

### 2. Why use Nginx as a reverse proxy?

Nginx is used in many modern applications because it provides:

- **TLS termination (HTTPS)**
- **load balancing** (round robin, least_conn and so on)
- **buffering and caching**
- **HTTP/1.1 and HTTP/2 performance optimisations**
- **efficient handling of concurrent connections**
- **backend isolation** (we expose only the proxy, not the internal services)

This seminar starts with Nginx as an example of an "industrial" proxy,
after which we will implement a **much simpler custom load balancer** for didactic purposes.

---

### 3. What is load balancing?

Load balancing is the process of distributing traffic across multiple backend instances in order to achieve:

- scalability
- high availability (HA)
- better performance
- isolation of partial failures

Example with three backends:

```
Request 1 -> web1
Request 2 -> web2
Request 3 -> web3
Request 4 -> web1
...
```

This is the standard **round-robin** algorithm, used by many load balancers.

---

### 4. Where does a reverse proxy sit in the architecture?

A simplified architecture is:

```
                     +----------------------------+
                     |          Internet          |
                     +--------------+-------------+
                                    |
                             Client browser
                                    |
                                    v
                          +-------------------+
                          |   Reverse proxy   |  <- Nginx or custom LB
                          +---------+---------+
            +----------------------+----------------------+
            v                      v                      v
      +------------+        +------------+        +------------+
      |  web1:8000 |        |  web2:8000 |        |  web3:8000 |
      +------------+        +------------+        +------------+
```

---

### 5. Seminar 11 overview

This seminar is split into two major parts.

#### Part A — Using a real load balancer (Nginx)

- we build an architecture with three Python backend services
- Nginx is configured as a reverse proxy in front of them
- we test load balancing using `curl`

#### Part B — Implementing a custom load balancer in Python

- we replace Nginx with a Python script (`S11_Part02_Script_Simple_Lb.py`)
- manual round-robin load balancing
- we observe differences compared with Nginx
- we run both scenarios with Docker Compose

---

### 6. What follows next

The next part proceeds as follows:

- create a Docker Compose architecture with three simple web servers
- configure Nginx as a reverse proxy in front of them
- verify the request distribution
- prepare the groundwork for the custom load balancer

---

### 7. Student task

Create a text file named:

`reverse_proxy_intro_findings.txt`

Answer the following questions:

1. In your own words, what is the difference between a reverse proxy and a forward proxy?
2. Why might a reverse proxy be useful in a microservices architecture?
3. Draw a small ASCII diagram showing a reverse proxy and three backends.
4. Give two concrete advantages of load balancing.

Submit the file at the end of the seminar.

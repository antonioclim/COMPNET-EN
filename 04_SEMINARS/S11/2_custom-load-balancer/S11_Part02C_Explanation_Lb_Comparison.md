## Stage 4 – Integrating the Custom Load Balancer into Docker Compose & Comparing with Nginx

### **Objectives**

In this stage:

* we replace Nginx with the custom load balancer written in Stage 3
* we run it in Docker Compose alongside `web1`, `web2`, `web3`
* we test its behaviour under controlled scenarios
* we compare it directly with Nginx:

  * request distribution
  * behaviour when a backend goes down
  * latency / blocking
  * robustness

This is a very important exercise:
**how does theory at the industrial level compare with a didactic prototype.**

---

## **1. What do we change in Compose?**

In Stage 2, the architecture was:

```
client → nginx → web1/web2/web3
```

Now it becomes:

```
client → lb-custom → web1/web2/web3
```

The major difference:

* Nginx is replaced with a container running `S11_Part02_Script_Simple_Lb.py`.
* The custom LB will not have all of Nginx's optimisations → this is EXACTLY what needs to be observed.


---

## **4. Starting the architecture**

In the terminal:

```
docker compose -f S11_Part02_Config_Docker_Compose_Lb_Custom.yml up --build
```

Then:

```
curl http://localhost:8080
curl http://localhost:8080
curl http://localhost:8080
```

You will observe:

* correct responses, but higher latency
* the LB logs:

```
[INFO] ('172.18.0.1', 49566) → web1:8000
[INFO] ('172.18.0.1', 49570) → web2:8000
[INFO] ('172.18.0.1', 49574) → web3:8000
```

---

## **5. Test: what happens if a backend goes down?**

Stop web2:

```
docker compose -f S11_Part02_Config_Docker_Compose_Lb_Custom.yml stop web2
```

Then send requests:

```
curl http://localhost:8080
curl http://localhost:8080
```

Expected result:

* The custom LB **will keep trying to send requests to web2**
* it will display errors in the console
* the request will fail

Here we see the first major difference from Nginx:

> **Nginx automatically bypasses non-functional backends.**
> Our load balancer does NOT.

---

## **6. Test: slow backend**

Make web3 slow (quick edit):

In `web3/index.html`, add a Python script in Compose:

Change the web3 command:

```yaml
command: ["python3", "-u", "-c", "import time, http.server; time.sleep(5); http.server.test(port=8000)"]
```

Restart only web3:

```
docker compose restart web3
```

What happens?

* The custom LB **will block the thread** for that request for 5 seconds
* Nginx would have handled this more gracefully
* this is an important lesson about non-blocking I/O and event loops

---

## **7. Conclusions**

The main differences observed:

| Feature                     |    Nginx    |      Custom LB     |
| --------------------------- | :---------: | :----------------: |
| Round-robin load balancing  |      ✔      |          ✔         |
| Header rewriting            |      ✔      |          ❌         |
| Health checks               |      ✔      |          ❌         |
| Retry logic                 |      ✔      |          ❌         |
| Handling backend failure    |      ✔      |          ❌         |
| Parallel request processing |      ✔      | semi-✔ (threading) |
| Performance                 |  very good  |        poor        |
| Configurability             |    high     |       minimal      |

This is EXACTLY the purpose of the seminar.

# Audit funcţional scripturi – compnet-2025-redo-main
_Generat: 2026-02-07 14:27:24_

## Rezumat rapid
- Scripturi/config identificate: **169** (Python: 117, Shell: 23, YAML: 16, Dockerfile: 11)
- Scopul acestui audit: să notez, pe fiecare fişier de tip script/config, **ce face**, **cum se rulează**, **în ce context poate eşua** şi **de ce**.
- Observaţie: unele fişiere cu extensia `.py` sunt de fapt **scenarii text**; în arhiva revizuită le-am făcut *parseabile* Python (docstring), fără să le schimb conţinutul.

## Index fişiere
- `assets/course/c1/assets/render.sh`
- `assets/course/c1/assets/scenario-capture-basics/dns-query.py`
- `assets/course/c1/assets/scenario-capture-basics/start-http-server.py`
- `assets/course/c10/assets/render.sh`
- `assets/course/c10/assets/scenario-custom-http-semantics/client.py`
- `assets/course/c10/assets/scenario-custom-http-semantics/server.py`
- `assets/course/c10/assets/scenario-http-compose/api/Dockerfile`
- `assets/course/c10/assets/scenario-http-compose/api/app.py`
- `assets/course/c10/assets/scenario-http-compose/docker-compose.yml`
- `assets/course/c10/assets/scenario-http-compose/web/Dockerfile`
- `assets/course/c10/assets/scenario-http-compose/web/server.py`
- `assets/course/c10/assets/scenario-rest-maturity/client-test.py`
- `assets/course/c10/assets/scenario-rest-maturity/common.py`
- `assets/course/c10/assets/scenario-rest-maturity/server-level0.py`
- `assets/course/c10/assets/scenario-rest-maturity/server-level1.py`
- `assets/course/c10/assets/scenario-rest-maturity/server-level2.py`
- `assets/course/c10/assets/scenario-rest-maturity/server-level3.py`
- `assets/course/c10/assets/scenario-websocket-protocol/server.py`
- `assets/course/c11/assets/render.sh`
- `assets/course/c11/assets/scenario-dns-ttl-caching/client/query.py`
- `assets/course/c11/assets/scenario-dns-ttl-caching/docker-compose.yml`
- `assets/course/c11/assets/scenario-ftp-baseline/client/ftp_client.py`
- `assets/course/c11/assets/scenario-ftp-baseline/docker-compose.yml`
- `assets/course/c11/assets/scenario-ftp-baseline/server/ftp_server.py`
- `assets/course/c11/assets/scenario-ftp-nat-firewall/client/ftp_client.py`
- `assets/course/c11/assets/scenario-ftp-nat-firewall/docker-compose.yml`
- `assets/course/c11/assets/scenario-ftp-nat-firewall/natfw/setup.sh`
- `assets/course/c11/assets/scenario-ssh-provision/controller/plan.json`
- `assets/course/c11/assets/scenario-ssh-provision/controller/provision.py`
- `assets/course/c11/assets/scenario-ssh-provision/docker-compose.yml`
- `assets/course/c11/assets/scenario-ssh-provision/nodes/node1/Dockerfile`
- `assets/course/c12/assets/render.sh`
- `assets/course/c12/assets/scenario-local-mailbox/docker-compose.yml`
- `assets/course/c12/assets/scenario-local-mailbox/scripts/fetch_imap.py`
- `assets/course/c12/assets/scenario-local-mailbox/scripts/fetch_pop3.py`
- `assets/course/c12/assets/scenario-local-mailbox/scripts/send_attachment_smtp.py`
- `assets/course/c12/assets/scenario-local-mailbox/scripts/send_mail_smtp.py`
- `assets/course/c13/assets/render.sh`
- `assets/course/c13/assets/scenario-iot-basic/actuator/Dockerfile`
- `assets/course/c13/assets/scenario-iot-basic/actuator/actuator.py`
- `assets/course/c13/assets/scenario-iot-basic/docker-compose.yml`
- `assets/course/c13/assets/scenario-iot-basic/sensor/Dockerfile`
- `assets/course/c13/assets/scenario-iot-basic/sensor/sensor.py`
- `assets/course/c13/assets/scenario-vulnerability-lab/attacker/Dockerfile`
- `assets/course/c13/assets/scenario-vulnerability-lab/docker-compose.yml`
- `assets/course/c13/assets/scenario-vulnerability-lab/target/Dockerfile`
- `assets/course/c13/assets/scenario-vulnerability-lab/target/app-hardened.py`
- `assets/course/c13/assets/scenario-vulnerability-lab/target/app.py`
- `assets/course/c2/assets/render.sh`
- `assets/course/c2/assets/scenario-tcp-udp-layers/tcp-client.py`
- `assets/course/c2/assets/scenario-tcp-udp-layers/tcp-server.py`
- `assets/course/c2/assets/scenario-tcp-udp-layers/udp-client.py`
- `assets/course/c2/assets/scenario-tcp-udp-layers/udp-server.py`
- `assets/course/c3/scenario-scapy-icmp/icmp-ping.py`
- `assets/course/c3/scenario-tcp-framing/client.py`
- `assets/course/c3/scenario-tcp-framing/server.py`
- `assets/course/c3/scenario-tcp-multiclient/client.py`
- `assets/course/c3/scenario-tcp-multiclient/server.py`
- `assets/course/c3/scenario-udp-session-ack/client.py`
- `assets/course/c3/scenario-udp-session-ack/server.py`
- `assets/course/c4/assets/render.sh`
- `assets/course/c5/assets/render.sh`
- `assets/course/c5/assets/scenario-cidr-basic/cidr-calc.py`
- `assets/course/c5/assets/scenario-ipv6-shortening/ipv6-norm.py`
- `assets/course/c5/assets/scenario-subnetting-flsm/flsm-split.py`
- `assets/course/c5/assets/scenario-vlsm/vlsm-alloc.py`
- `assets/course/c6/assets/render.sh`
- `assets/course/c6/assets/scenario-nat-linux/nat-demo.sh`
- `assets/course/c7/assets/render.sh`
- `assets/course/c7/assets/scenario-bellman-ford/bellman_ford.py`
- `assets/course/c7/assets/scenario-djikstra/djikstra.py`
- `assets/course/c7/assets/scenario-mininet-routing/tringle-net.py`
- `assets/course/c8/assets/render.sh`
- `assets/course/c8/assets/scenario-tcp-handshake-tcpdump/cleanup.sh`
- `assets/course/c8/assets/scenario-tcp-handshake-tcpdump/client.py`
- `assets/course/c8/assets/scenario-tcp-handshake-tcpdump/run.sh`
- `assets/course/c8/assets/scenario-tcp-handshake-tcpdump/server.py`
- `assets/course/c8/assets/scenario-tls-openssl/cleanup.sh`
- `assets/course/c8/assets/scenario-tls-openssl/gen_certs.sh`
- `assets/course/c8/assets/scenario-tls-openssl/run_client.sh`
- `assets/course/c8/assets/scenario-tls-openssl/run_server.sh`
- `assets/course/c8/assets/scenario-udp-vs-tcp-loss/run.sh`
- `assets/course/c8/assets/scenario-udp-vs-tcp-loss/tcp_receiver.py`
- `assets/course/c8/assets/scenario-udp-vs-tcp-loss/tcp_sender.py`
- `assets/course/c8/assets/scenario-udp-vs-tcp-loss/topo.py`
- `assets/course/c8/assets/scenario-udp-vs-tcp-loss/udp_receiver.py`
- `assets/course/c8/assets/scenario-udp-vs-tcp-loss/udp_sender.py`
- `assets/course/c9/assets/render.sh`
- `assets/course/c9/assets/scenario-encoding-utf8/run.sh`
- `assets/course/c9/assets/scenario-encoding-utf8/server.py`
- `assets/course/c9/assets/scenario-mime-encoding-gzip/data.json`
- `assets/course/c9/assets/scenario-mime-encoding-gzip/run.sh`
- `assets/course/c9/assets/scenario-mime-encoding-gzip/server.py`
- `assets/tutorial-solve/s2/2_tcp-server_template.py`
- `assets/tutorial/s10/2_dns-containers/Dockerfile`
- `assets/tutorial/s10/2_dns-containers/dns_server.py`
- `assets/tutorial/s10/2_dns-containers/docker-compose.yml`
- `assets/tutorial/s10/3_ssh/docker-compose.yml`
- `assets/tutorial/s10/3_ssh/ssh-client/Dockerfile`
- `assets/tutorial/s10/3_ssh/ssh-client/paramiko_client.py`
- `assets/tutorial/s10/3_ssh/ssh-server/Dockerfile`
- `assets/tutorial/s10/4_ssh-port-forwarding/docker-compose.yml`
- `assets/tutorial/s10/4_ssh-port-forwarding/ssh-bastion/Dockerfile`
- `assets/tutorial/s11/1_nginx-compose/docker-compose.nginx.yml`
- `assets/tutorial/s11/2_custom-load-balancer/docker-compose.lb-custom.yml`
- `assets/tutorial/s11/2_custom-load-balancer/simple_lb.py`
- `assets/tutorial/s12/1_jsonrpc/jsonrpc_client.py`
- `assets/tutorial/s12/3_grpc/grpc_client.py`
- `assets/tutorial/s12/3_grpc/grpc_server.py`
- `assets/tutorial/s13/docker-compose.pentest.yml`
- `assets/tutorial/s13/ftp_backdoor_exploit.py`
- `assets/tutorial/s13/simple_scanner.py`
- `assets/tutorial/s2/10_udp-client_template.py`
- `assets/tutorial/s2/1_tcp-server_example.py`
- `assets/tutorial/s2/2_tcp-server_template.py`
- `assets/tutorial/s2/4_tcp-client_example.py`
- `assets/tutorial/s2/5_tcp-client_template.py`
- `assets/tutorial/s2/6_tcp-client_scenario.py`
- `assets/tutorial/s2/7_udp-server_example.py`
- `assets/tutorial/s2/8_udp-server_template.py`
- `assets/tutorial/s2/9_udp-client_example.py`
- `assets/tutorial/s3/1_tcp-multiclient-server_example.py`
- `assets/tutorial/s3/2_tcp-multiclient-server_template.py`
- `assets/tutorial/s3/4_udp-broadcast/4a_udp-broad-sender_example.py`
- `assets/tutorial/s3/4_udp-broadcast/4b_udp-broad-receiver_example.py`
- `assets/tutorial/s3/4_udp-broadcast/4c_udp-broad-receiver_template.py`
- `assets/tutorial/s3/4_udp-broadcast/4d_udp-broad_scenario.py`
- `assets/tutorial/s3/5_udp-multicast/5a_udp-multicast_sender_example.py`
- `assets/tutorial/s3/5_udp-multicast/5b_udp-multicast_receiver_example.py`
- `assets/tutorial/s3/5_udp-multicast/5c_udp-multicast_receiver_template.py`
- `assets/tutorial/s3/6_udp-anycast/6a_udp-anycast_server_example.py`
- `assets/tutorial/s3/6_udp-anycast/6b_udp-anycast_client_example.py`
- `assets/tutorial/s3/6_udp-anycast/6c_idp-anycast_template.py`
- `assets/tutorial/s4/1_text-proto_tcp/1a_text-proto_tcp-server_example.py`
- `assets/tutorial/s4/1_text-proto_tcp/1b_text-proto_tcp-client_example.py`
- `assets/tutorial/s4/1_text-proto_tcp/1c_text-proto_tcp-server_template.py`
- `assets/tutorial/s4/2_binary-proto_tcp/2a_binary-proto_tcp-server_example.py`
- `assets/tutorial/s4/2_binary-proto_tcp/2b_binary-proto_tcp-client_example.py`
- `assets/tutorial/s4/2_binary-proto_tcp/2c_binary-proto_tcp-server_template.py`
- `assets/tutorial/s4/3_proto_udp/3a_udp-proto_server_example.py`
- `assets/tutorial/s4/3_proto_udp/3b_udp-proto_client_example.py`
- `assets/tutorial/s4/3_proto_udp/3c_udp-proto_client_template.py`
- `assets/tutorial/s4/3_proto_udp/3c_udp-proto_server_template.py`
- `assets/tutorial/s4/3_proto_udp/serialization.py`
- `assets/tutorial/s4/3_proto_udp/state.py`
- `assets/tutorial/s4/3_proto_udp/transfer_units.py`
- `assets/tutorial/s5/3_network-simulation/3b_mininet-topology.py`
- `assets/tutorial/s6/1_routing/1b_routing-triangle_topology.py`
- `assets/tutorial/s6/2_sdn/2b_sdn_topo_switch.py`
- `assets/tutorial/s6/2_sdn/2c_sdn-os-ken_controller.py`
- `assets/tutorial/s6/3_sdn-app-traffic/tcp_client.py`
- `assets/tutorial/s6/3_sdn-app-traffic/tcp_server.py`
- `assets/tutorial/s6/3_sdn-app-traffic/udp_client.py`
- `assets/tutorial/s6/3_sdn-app-traffic/udp_server.py`
- `assets/tutorial/s7/1_sniffing/1b_packet_sniffer.py`
- `assets/tutorial/s7/2_packet-filter/2a_packet-filter.py`
- `assets/tutorial/s7/3_port-scanning/3a_port_scanner.py`
- `assets/tutorial/s7/4_scan-detector/4a_detect-scan.py`
- `assets/tutorial/s7/5_mini-ids/5a_mini-ids.py`
- `assets/tutorial/s8/2_simple-http/2b_simple-http-builtin_example.py`
- `assets/tutorial/s8/3_socket-http/3b_socket-http-server_example.py`
- `assets/tutorial/s8/4_nginx/docker-compose.yml`
- `assets/tutorial/s9/1_ftp/1c_pyftpd-server.py`
- `assets/tutorial/s9/1_ftp/1d_pyftpd-client.py`
- `assets/tutorial/s9/2_custom-pseudo-ftp/2b_pseudo-ftp-server.py`
- `assets/tutorial/s9/2_custom-pseudo-ftp/2c_pseudo-ftp-client.py`
- `assets/tutorial/s9/3_multi-client-containers/docker-compose.yml`
- `assets/tutorial/s9/3_multi-client-containers/pyftpd_multi_client.py`
- `assets/tutorial/s9/3_multi-client-containers/pyftpd_server.py`

---

## Analiză pe fişier

### `assets/course/c1/assets/render.sh`
- Tip: **Shell**
- Linii: **3**
- Shebang: `#!/usr/bin/env bash`
- Rol: rulează PlantUML pentru a genera imagini din fişiere `.puml`.
- Execuţie: `bash render.sh` (sau `./render.sh` dacă are bit de execuţie).
- Comandă principală: `java -jar ../../../tools/plantuml.jar -tpng puml/*.puml -o ../images`

### `assets/course/c1/assets/scenario-capture-basics/dns-query.py`
- Tip: **Python**
- Linii: **13**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L2: Header / imports / constants
  - L3-L9: func main()
  - L11-L12: entrypoint if __name__ == '__main__'

### `assets/course/c1/assets/scenario-capture-basics/start-http-server.py`
- Tip: **Python**
- Linii: **10**
- Descriere (prima propoziţie/docstring/linie): from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
- Hartă funcţională (segmente):
  - L1-L2: Header / imports / constants
  - L3-L6: func main()
  - L8-L9: entrypoint if __name__ == '__main__'

### `assets/course/c10/assets/render.sh`
- Tip: **Shell**
- Linii: **3**
- Shebang: `#!/usr/bin/env bash`
- Rol: rulează PlantUML pentru a genera imagini din fişiere `.puml`.
- Execuţie: `bash render.sh` (sau `./render.sh` dacă are bit de execuţie).
- Comandă principală: `java -jar ../../../tools/plantuml.jar -tpng puml/*.puml -o ../images`

### `assets/course/c10/assets/scenario-custom-http-semantics/client.py`
- Tip: **Python**
- Linii: **27**
- Descriere (prima propoziţie/docstring/linie): from __future__ import annotations
- Dependenţe externe (pip/extra): requests
- Hartă funcţională (segmente):
  - L1-L7: Header / imports / constants
  - L8-L23: func main()
  - L25-L26: entrypoint if __name__ == '__main__'

### `assets/course/c10/assets/scenario-custom-http-semantics/server.py`
- Tip: **Python**
- Linii: **93**
- Descriere (prima propoziţie/docstring/linie): from __future__ import annotations
- Dependenţe externe (pip/extra): flask
- Context special: rulează un server web (Flask/WebSocket)
- Hartă funcţională (segmente):
  - L1-L13: Header / imports / constants
  - L14-L37: func worker()
  - L40-L59: func create_job()
  - L62-L75: func get_job()
  - L78-L89: func get_result()
  - L91-L92: entrypoint if __name__ == '__main__'

### `assets/course/c10/assets/scenario-http-compose/api/Dockerfile`
- Tip: **Dockerfile**
- Linii: **11**
- Imagine de bază: `python:3.12-slim`
- EXPOSE: 5000
- CMD/ENTRYPOINT: `CMD ["python", "app.py"]`

### `assets/course/c10/assets/scenario-http-compose/api/app.py`
- Tip: **Python**
- Linii: **27**
- Descriere (prima propoziţie/docstring/linie): from __future__ import annotations
- Dependenţe externe (pip/extra): flask
- Context special: rulează un server web (Flask/WebSocket)
- Hartă funcţională (segmente):
  - L1-L7: Header / imports / constants
  - L8-L19: func users()
  - L22-L23: func health()
  - L25-L26: entrypoint if __name__ == '__main__'

### `assets/course/c10/assets/scenario-http-compose/docker-compose.yml`
- Tip: **YAML**
- Linii: **21**
- Tip YAML detectat: **docker-compose**
- Servicii: nginx, web, api
- Porturi expuse (rezumat): nginx: ['8080:80']

### `assets/course/c10/assets/scenario-http-compose/web/Dockerfile`
- Tip: **Dockerfile**
- Linii: **9**
- Imagine de bază: `python:3.12-slim`
- EXPOSE: 8000
- CMD/ENTRYPOINT: `CMD ["python", "server.py"]`

### `assets/course/c10/assets/scenario-http-compose/web/server.py`
- Tip: **Python**
- Linii: **16**
- Descriere (prima propoziţie/docstring/linie): from __future__ import annotations
- Hartă funcţională (segmente):
  - L1-L7: Header / imports / constants
  - L8-L11: class Handler

### `assets/course/c10/assets/scenario-rest-maturity/client-test.py`
- Tip: **Python**
- Linii: **114**
- Descriere (prima propoziţie/docstring/linie): from __future__ import annotations
- Dependenţe externe (pip/extra): requests
- Hartă funcţională (segmente):
  - L1-L12: Header / imports / constants
  - L13-L24: func p()
  - L26-L38: func run_level0()
  - L40-L52: func run_level1()
  - L54-L69: func run_level2()
  - L71-L93: func run_level3()
  - L95-L110: func main()
  - L112-L113: entrypoint if __name__ == '__main__'

### `assets/course/c10/assets/scenario-rest-maturity/common.py`
- Tip: **Python**
- Linii: **15**
- Descriere (prima propoziţie/docstring/linie): from __future__ import annotations
- Hartă funcţională (segmente):
  - L1-L4: Header / imports / constants
  - L5-L9: func initial_users()
  - L11-L14: func next_id()

### `assets/course/c10/assets/scenario-rest-maturity/server-level0.py`
- Tip: **Python**
- Linii: **50**
- Descriere (prima propoziţie/docstring/linie): from __future__ import annotations
- Importuri locale: common
- Dependenţe externe (pip/extra): flask
- Context special: rulează un server web (Flask/WebSocket)
- Hartă funcţională (segmente):
  - L1-L9: Header / imports / constants
  - L10-L46: func rpc_api()
  - L48-L49: entrypoint if __name__ == '__main__'

### `assets/course/c10/assets/scenario-rest-maturity/server-level1.py`
- Tip: **Python**
- Linii: **54**
- Descriere (prima propoziţie/docstring/linie): from __future__ import annotations
- Importuri locale: common
- Dependenţe externe (pip/extra): flask
- Context special: rulează un server web (Flask/WebSocket)
- Hartă funcţională (segmente):
  - L1-L9: Header / imports / constants
  - L10-L22: func users_collection_post()
  - L25-L50: func user_resource_post()
  - L52-L53: entrypoint if __name__ == '__main__'

### `assets/course/c10/assets/scenario-rest-maturity/server-level2.py`
- Tip: **Python**
- Linii: **56**
- Descriere (prima propoziţie/docstring/linie): from __future__ import annotations
- Importuri locale: common
- Dependenţe externe (pip/extra): flask
- Context special: rulează un server web (Flask/WebSocket)
- Hartă funcţională (segmente):
  - L1-L9: Header / imports / constants
  - L10-L11: func list_users()
  - L14-L25: func create_user()
  - L28-L32: func get_user()
  - L35-L45: func put_user()
  - L48-L52: func delete_user()
  - L54-L55: entrypoint if __name__ == '__main__'

### `assets/course/c10/assets/scenario-rest-maturity/server-level3.py`
- Tip: **Python**
- Linii: **84**
- Descriere (prima propoziţie/docstring/linie): from __future__ import annotations
- Importuri locale: common
- Dependenţe externe (pip/extra): flask
- Context special: rulează un server web (Flask/WebSocket)
- Hartă funcţională (segmente):
  - L1-L8: Header / imports / constants
  - L9-L20: func user_representation()
  - L23-L30: func entrypoint()
  - L33-L40: func list_users()
  - L43-L54: func create_user()
  - L57-L60: func get_user()
  - L63-L73: func put_user()
  - L76-L80: func delete_user()
  - L82-L83: entrypoint if __name__ == '__main__'

### `assets/course/c10/assets/scenario-websocket-protocol/server.py`
- Tip: **Python**
- Linii: **103**
- Descriere (prima propoziţie/docstring/linie): from __future__ import annotations
- Dependenţe externe (pip/extra): flask, flask_sock
- Context special: rulează un server web (Flask/WebSocket)
- Hartă funcţională (segmente):
  - L1-L16: Header / imports / constants
  - L17-L18: func index()
  - L20-L21: func ws_send()
  - L24-L99: func ws_endpoint()
  - L101-L102: entrypoint if __name__ == '__main__'

### `assets/course/c11/assets/render.sh`
- Tip: **Shell**
- Linii: **3**
- Shebang: `#!/usr/bin/env bash`
- Rol: rulează PlantUML pentru a genera imagini din fişiere `.puml`.
- Execuţie: `bash render.sh` (sau `./render.sh` dacă are bit de execuţie).
- Comandă principală: `java -jar ../../../tools/plantuml.jar -tpng puml/*.puml -o ../images`

### `assets/course/c11/assets/scenario-dns-ttl-caching/client/query.py`
- Tip: **Python**
- Linii: **14**
- Descriere (prima propoziţie/docstring/linie): import time
- Dependenţe externe (pip/extra): dns
- Hartă funcţională (segmente):
  - L1-L3: Header / imports / constants
  - L4-L8: func q()
  - L10-L13: entrypoint if __name__ == '__main__'

### `assets/course/c11/assets/scenario-dns-ttl-caching/docker-compose.yml`
- Tip: **YAML**
- Linii: **26**
- Tip YAML detectat: **docker-compose**
- Servicii: auth, resolver, client

### `assets/course/c11/assets/scenario-ftp-baseline/client/ftp_client.py`
- Tip: **Python**
- Linii: **35**
- Descriere (prima propoziţie/docstring/linie): from ftplib import FTP
- Hartă funcţională (segmente):
  - L1-L6: Header / imports / constants
  - L7-L30: func run()
  - L32-L34: entrypoint if __name__ == '__main__'

### `assets/course/c11/assets/scenario-ftp-baseline/docker-compose.yml`
- Tip: **YAML**
- Linii: **21**
- Tip YAML detectat: **docker-compose**
- Servicii: ftp, client
- Porturi expuse (rezumat): ftp: ['2121:2121', '30000-30009:30000-30009']

### `assets/course/c11/assets/scenario-ftp-baseline/server/ftp_server.py`
- Tip: **Python**
- Linii: **23**
- Descriere (prima propoziţie/docstring/linie): from pyftpdlib.authorizers import DummyAuthorizer
- Dependenţe externe (pip/extra): pyftpdlib
- Hartă funcţională (segmente):
  - L1-L4: Header / imports / constants
  - L5-L19: func main()
  - L21-L22: entrypoint if __name__ == '__main__'

### `assets/course/c11/assets/scenario-ftp-nat-firewall/client/ftp_client.py`
- Tip: **Python**
- Linii: **22**
- Descriere (prima propoziţie/docstring/linie): from ftplib import FTP
- Hartă funcţională (segmente):
  - L1-L7: Header / imports / constants
  - L8-L15: func run()
  - L17-L21: entrypoint if __name__ == '__main__'

### `assets/course/c11/assets/scenario-ftp-nat-firewall/docker-compose.yml`
- Tip: **YAML**
- Linii: **37**
- Tip YAML detectat: **docker-compose**
- Servicii: ftp, natfw, client

### `assets/course/c11/assets/scenario-ftp-nat-firewall/natfw/setup.sh`
- Tip: **Shell**
- Linii: **20**
- Shebang: `#!/usr/bin/env bash`

### `assets/course/c11/assets/scenario-ssh-provision/controller/plan.json`
- Tip: **JSON**
- Linii: **18**
- JSON valid. Chei top-level: hosts

### `assets/course/c11/assets/scenario-ssh-provision/controller/provision.py`
- Tip: **Python**
- Linii: **47**
- Descriere (prima propoziţie/docstring/linie): import json
- Dependenţe externe (pip/extra): paramiko
- Hartă funcţională (segmente):
  - L1-L3: Header / imports / constants
  - L4-L8: func run_cmd()
  - L10-L43: func main()
  - L45-L46: entrypoint if __name__ == '__main__'

### `assets/course/c11/assets/scenario-ssh-provision/docker-compose.yml`
- Tip: **YAML**
- Linii: **19**
- Tip YAML detectat: **docker-compose**
- Servicii: node1, controller

### `assets/course/c11/assets/scenario-ssh-provision/nodes/node1/Dockerfile`
- Tip: **Dockerfile**
- Linii: **15**
- Imagine de bază: `debian:stable-slim`
- EXPOSE: 22
- CMD/ENTRYPOINT: `CMD ["/usr/sbin/sshd", "-D"]`

### `assets/course/c12/assets/render.sh`
- Tip: **Shell**
- Linii: **3**
- Shebang: `#!/usr/bin/env bash`
- Rol: rulează PlantUML pentru a genera imagini din fişiere `.puml`.
- Execuţie: `bash render.sh` (sau `./render.sh` dacă are bit de execuţie).
- Comandă principală: `java -jar ../../../tools/plantuml.jar -tpng puml/*.puml -o ../images`

### `assets/course/c12/assets/scenario-local-mailbox/docker-compose.yml`
- Tip: **YAML**
- Linii: **42**
- Tip YAML detectat: **docker-compose**
- Servicii: mail, webmail
- Porturi expuse (rezumat): mail: ['25:25', '587:587', '143:143', '993:993', '110:110', '995:995'], webmail: ['8080:80']

### `assets/course/c12/assets/scenario-local-mailbox/scripts/fetch_imap.py`
- Tip: **Python**
- Linii: **75**
- Descriere (prima propoziţie/docstring/linie): import argparse
- Hartă funcţională (segmente):
  - L1-L6: Header / imports / constants
  - L7-L70: func main()
  - L73-L74: entrypoint if __name__ == '__main__'

### `assets/course/c12/assets/scenario-local-mailbox/scripts/fetch_pop3.py`
- Tip: **Python**
- Linii: **61**
- Descriere (prima propoziţie/docstring/linie): import argparse
- Hartă funcţională (segmente):
  - L1-L6: Header / imports / constants
  - L7-L56: func main()
  - L59-L60: entrypoint if __name__ == '__main__'

### `assets/course/c12/assets/scenario-local-mailbox/scripts/send_attachment_smtp.py`
- Tip: **Python**
- Linii: **59**
- Descriere (prima propoziţie/docstring/linie): import argparse
- Hartă funcţională (segmente):
  - L1-L10: Header / imports / constants
  - L11-L54: func main()
  - L57-L58: entrypoint if __name__ == '__main__'

### `assets/course/c12/assets/scenario-local-mailbox/scripts/send_mail_smtp.py`
- Tip: **Python**
- Linii: **38**
- Descriere (prima propoziţie/docstring/linie): import argparse
- Hartă funcţională (segmente):
  - L1-L6: Header / imports / constants
  - L7-L33: func main()
  - L36-L37: entrypoint if __name__ == '__main__'

### `assets/course/c13/assets/render.sh`
- Tip: **Shell**
- Linii: **3**
- Shebang: `#!/usr/bin/env bash`
- Rol: rulează PlantUML pentru a genera imagini din fişiere `.puml`.
- Execuţie: `bash render.sh` (sau `./render.sh` dacă are bit de execuţie).
- Comandă principală: `java -jar ../../../tools/plantuml.jar -tpng puml/*.puml -o ../images`

### `assets/course/c13/assets/scenario-iot-basic/actuator/Dockerfile`
- Tip: **Dockerfile**
- Linii: **9**
- Imagine de bază: `python:3.12-slim`
- CMD/ENTRYPOINT: `CMD ["python", "actuator.py"]`

### `assets/course/c13/assets/scenario-iot-basic/actuator/actuator.py`
- Tip: **Python**
- Linii: **51**
- Descriere (prima propoziţie/docstring/linie): import os
- Dependenţe externe (pip/extra): paho
- Hartă funcţională (segmente):
  - L1-L12: Header / imports / constants
  - L13-L16: func publish_command()
  - L18-L35: func on_message()

### `assets/course/c13/assets/scenario-iot-basic/docker-compose.yml`
- Tip: **YAML**
- Linii: **34**
- Tip YAML detectat: **docker-compose**
- Servicii: broker, sensor, actuator
- Porturi expuse (rezumat): broker: ['1883:1883']

### `assets/course/c13/assets/scenario-iot-basic/sensor/Dockerfile`
- Tip: **Dockerfile**
- Linii: **9**
- Imagine de bază: `python:3.12-slim`
- CMD/ENTRYPOINT: `CMD ["python", "sensor.py"]`

### `assets/course/c13/assets/scenario-iot-basic/sensor/sensor.py`
- Tip: **Python**
- Linii: **38**
- Descriere (prima propoziţie/docstring/linie): import os
- Dependenţe externe (pip/extra): paho
- Hartă funcţională (segmente):
  - L1-L10: Header / imports / constants
  - L11-L17: func make_temperature()

### `assets/course/c13/assets/scenario-vulnerability-lab/attacker/Dockerfile`
- Tip: **Dockerfile**
- Linii: **7**
- Imagine de bază: `alpine:3.20`
- CMD/ENTRYPOINT: `CMD ["sh"]`

### `assets/course/c13/assets/scenario-vulnerability-lab/docker-compose.yml`
- Tip: **YAML**
- Linii: **16**
- Tip YAML detectat: **docker-compose**
- Servicii: target, attacker
- Porturi expuse (rezumat): target: ['8080:8080']

### `assets/course/c13/assets/scenario-vulnerability-lab/target/Dockerfile`
- Tip: **Dockerfile**
- Linii: **14**
- Imagine de bază: `python:3.12-slim`
- EXPOSE: 8080
- CMD/ENTRYPOINT: `CMD ["flask", "run"]`

### `assets/course/c13/assets/scenario-vulnerability-lab/target/app-hardened.py`
- Tip: **Python**
- Linii: **28**
- Descriere (prima propoziţie/docstring/linie): from flask import Flask, request, abort
- Dependenţe externe (pip/extra): flask
- Context special: rulează un server web (Flask/WebSocket)
- Hartă funcţională (segmente):
  - L1-L7: Header / imports / constants
  - L8-L9: func index()
  - L12-L27: func ping()

### `assets/course/c13/assets/scenario-vulnerability-lab/target/app.py`
- Tip: **Python**
- Linii: **19**
- Descriere (prima propoziţie/docstring/linie): from flask import Flask, request
- Dependenţe externe (pip/extra): flask
- Context special: rulează un server web (Flask/WebSocket)
- Hartă funcţională (segmente):
  - L1-L6: Header / imports / constants
  - L7-L8: func index()
  - L11-L18: func ping()

### `assets/course/c2/assets/render.sh`
- Tip: **Shell**
- Linii: **3**
- Shebang: `#!/usr/bin/env bash`
- Rol: rulează PlantUML pentru a genera imagini din fişiere `.puml`.
- Execuţie: `bash render.sh` (sau `./render.sh` dacă are bit de execuţie).
- Comandă principală: `java -jar ../../../tools/plantuml.jar -tpng puml/*.puml -o ../images`

### `assets/course/c2/assets/scenario-tcp-udp-layers/tcp-client.py`
- Tip: **Python**
- Linii: **16**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L5: Header / imports / constants
  - L6-L12: func main()
  - L14-L15: entrypoint if __name__ == '__main__'

### `assets/course/c2/assets/scenario-tcp-udp-layers/tcp-server.py`
- Tip: **Python**
- Linii: **22**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L5: Header / imports / constants
  - L6-L18: func main()
  - L20-L21: entrypoint if __name__ == '__main__'

### `assets/course/c2/assets/scenario-tcp-udp-layers/udp-client.py`
- Tip: **Python**
- Linii: **15**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L5: Header / imports / constants
  - L6-L11: func main()
  - L13-L14: entrypoint if __name__ == '__main__'

### `assets/course/c2/assets/scenario-tcp-udp-layers/udp-server.py`
- Tip: **Python**
- Linii: **17**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L5: Header / imports / constants
  - L6-L13: func main()
  - L15-L16: entrypoint if __name__ == '__main__'

### `assets/course/c3/scenario-scapy-icmp/icmp-ping.py`
- Tip: **Python**
- Linii: **15**
- Descriere (prima propoziţie/docstring/linie): import sys
- Dependenţe externe (pip/extra): scapy
- Hartă funcţională (segmente):
  - L1-L3: Header / imports / constants
  - L4-L11: func main()
  - L13-L14: entrypoint if __name__ == '__main__'

### `assets/course/c3/scenario-tcp-framing/client.py`
- Tip: **Python**
- Linii: **28**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L6: Header / imports / constants
  - L7-L24: func main()
  - L26-L27: entrypoint if __name__ == '__main__'

### `assets/course/c3/scenario-tcp-framing/server.py`
- Tip: **Python**
- Linii: **31**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L5: Header / imports / constants
  - L6-L27: func main()
  - L29-L30: entrypoint if __name__ == '__main__'

### `assets/course/c3/scenario-tcp-multiclient/client.py`
- Tip: **Python**
- Linii: **18**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L6: Header / imports / constants
  - L7-L14: func main()
  - L16-L17: entrypoint if __name__ == '__main__'

### `assets/course/c3/scenario-tcp-multiclient/server.py`
- Tip: **Python**
- Linii: **31**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L6: Header / imports / constants
  - L7-L15: func handle()
  - L17-L27: func main()
  - L29-L30: entrypoint if __name__ == '__main__'

### `assets/course/c3/scenario-udp-session-ack/client.py`
- Tip: **Python**
- Linii: **26**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L6: Header / imports / constants
  - L7-L22: func main()
  - L24-L25: entrypoint if __name__ == '__main__'

### `assets/course/c3/scenario-udp-session-ack/server.py`
- Tip: **Python**
- Linii: **45**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L9: Header / imports / constants
  - L10-L41: func main()
  - L43-L44: entrypoint if __name__ == '__main__'

### `assets/course/c4/assets/render.sh`
- Tip: **Shell**
- Linii: **3**
- Shebang: `#!/usr/bin/env bash`
- Rol: rulează PlantUML pentru a genera imagini din fişiere `.puml`.
- Execuţie: `bash render.sh` (sau `./render.sh` dacă are bit de execuţie).
- Comandă principală: `java -jar ../../../tools/plantuml.jar -tpng puml/*.puml -o ../images`

### `assets/course/c5/assets/render.sh`
- Tip: **Shell**
- Linii: **3**
- Shebang: `#!/usr/bin/env bash`
- Rol: rulează PlantUML pentru a genera imagini din fişiere `.puml`.
- Execuţie: `bash render.sh` (sau `./render.sh` dacă are bit de execuţie).
- Comandă principală: `java -jar ../../../tools/plantuml.jar -tpng puml/*.puml -o ../images`

### `assets/course/c5/assets/scenario-cidr-basic/cidr-calc.py`
- Tip: **Python**
- Linii: **25**
- Descriere (prima propoziţie/docstring/linie): import ipaddress
- Hartă funcţională (segmente):
  - L1-L3: Header / imports / constants
  - L4-L21: func main()
  - L23-L24: entrypoint if __name__ == '__main__'

### `assets/course/c5/assets/scenario-ipv6-shortening/ipv6-norm.py`
- Tip: **Python**
- Linii: **15**
- Descriere (prima propoziţie/docstring/linie): import ipaddress
- Hartă funcţională (segmente):
  - L1-L3: Header / imports / constants
  - L4-L11: func main()
  - L13-L14: entrypoint if __name__ == '__main__'

### `assets/course/c5/assets/scenario-subnetting-flsm/flsm-split.py`
- Tip: **Python**
- Linii: **37**
- Descriere (prima propoziţie/docstring/linie): import ipaddress
- Hartă funcţională (segmente):
  - L1-L4: Header / imports / constants
  - L5-L33: func main()
  - L35-L36: entrypoint if __name__ == '__main__'

### `assets/course/c5/assets/scenario-vlsm/vlsm-alloc.py`
- Tip: **Python**
- Linii: **52**
- Descriere (prima propoziţie/docstring/linie): import ipaddress
- Hartă funcţională (segmente):
  - L1-L4: Header / imports / constants
  - L5-L9: func needed_prefix()
  - L11-L48: func main()
  - L50-L51: entrypoint if __name__ == '__main__'

### `assets/course/c6/assets/render.sh`
- Tip: **Shell**
- Linii: **3**
- Shebang: `#!/usr/bin/env bash`
- Rol: rulează PlantUML pentru a genera imagini din fişiere `.puml`.
- Execuţie: `bash render.sh` (sau `./render.sh` dacă are bit de execuţie).
- Comandă principală: `java -jar ../../../tools/plantuml.jar -tpng puml/*.puml -o ../images`

### `assets/course/c6/assets/scenario-nat-linux/nat-demo.sh`
- Tip: **Shell**
- Linii: **54**
- Shebang: `#!/usr/bin/env bash`

### `assets/course/c7/assets/render.sh`
- Tip: **Shell**
- Linii: **3**
- Shebang: `#!/usr/bin/env bash`
- Rol: rulează PlantUML pentru a genera imagini din fişiere `.puml`.
- Execuţie: `bash render.sh` (sau `./render.sh` dacă are bit de execuţie).
- Comandă principală: `java -jar ../../../tools/plantuml.jar -tpng puml/*.puml -o ../images`

### `assets/course/c7/assets/scenario-bellman-ford/bellman_ford.py`
- Tip: **Python**
- Linii: **56**
- Descriere (prima propoziţie/docstring/linie): def bellman_ford(graph, source):
- Hartă funcţională (segmente):
  - L1-L32: func bellman_ford()
  - L34-L52: func main()
  - L54-L55: entrypoint if __name__ == '__main__'

### `assets/course/c7/assets/scenario-djikstra/djikstra.py`
- Tip: **Python**
- Linii: **42**
- Descriere (prima propoziţie/docstring/linie): from heapq import heappop, heappush
- Hartă funcţională (segmente):
  - L1-L2: Header / imports / constants
  - L3-L23: func dijkstra()
  - L25-L38: func main()
  - L40-L41: entrypoint if __name__ == '__main__'

### `assets/course/c7/assets/scenario-mininet-routing/tringle-net.py`
- Tip: **Python**
- Linii: **140**
- Descriere (prima propoziţie/docstring/linie): !/usr/bin/env python3
- Dependenţe externe (pip/extra): mininet
- Context special: necesită Mininet (de obicei install sistem)
- Hartă funcţională (segmente):
  - L1-L9: Header / imports / constants
  - L10-L17: class LinuxRouter
  - L20-L21: func add_ip()
  - L24-L25: func set_default_route()
  - L28-L74: func build_net()
  - L77-L94: func scenario_link_down()
  - L97-L108: func scenario_asymmetric()
  - L111-L135: func main()
  - L138-L139: entrypoint if __name__ == '__main__'

### `assets/course/c8/assets/render.sh`
- Tip: **Shell**
- Linii: **3**
- Shebang: `#!/usr/bin/env bash`
- Rol: rulează PlantUML pentru a genera imagini din fişiere `.puml`.
- Execuţie: `bash render.sh` (sau `./render.sh` dacă are bit de execuţie).
- Comandă principală: `java -jar ../../../tools/plantuml.jar -tpng puml/*.puml -o ../images`

### `assets/course/c8/assets/scenario-tcp-handshake-tcpdump/cleanup.sh`
- Tip: **Shell**
- Linii: **18**
- Shebang: `#!/usr/bin/env bash`

### `assets/course/c8/assets/scenario-tcp-handshake-tcpdump/client.py`
- Tip: **Python**
- Linii: **21**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L6: Header / imports / constants
  - L7-L17: func main()
  - L19-L20: entrypoint if __name__ == '__main__'

### `assets/course/c8/assets/scenario-tcp-handshake-tcpdump/run.sh`
- Tip: **Shell**
- Linii: **40**
- Shebang: `#!/usr/bin/env bash`

### `assets/course/c8/assets/scenario-tcp-handshake-tcpdump/server.py`
- Tip: **Python**
- Linii: **30**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L6: Header / imports / constants
  - L7-L13: func handle_client()
  - L15-L26: func main()
  - L28-L29: entrypoint if __name__ == '__main__'

### `assets/course/c8/assets/scenario-tls-openssl/cleanup.sh`
- Tip: **Shell**
- Linii: **9**
- Shebang: `#!/usr/bin/env bash`

### `assets/course/c8/assets/scenario-tls-openssl/gen_certs.sh`
- Tip: **Shell**
- Linii: **18**
- Shebang: `#!/usr/bin/env bash`

### `assets/course/c8/assets/scenario-tls-openssl/run_client.sh`
- Tip: **Shell**
- Linii: **14**
- Shebang: `#!/usr/bin/env bash`

### `assets/course/c8/assets/scenario-tls-openssl/run_server.sh`
- Tip: **Shell**
- Linii: **17**
- Shebang: `#!/usr/bin/env bash`

### `assets/course/c8/assets/scenario-udp-vs-tcp-loss/run.sh`
- Tip: **Shell**
- Linii: **51**
- Shebang: `#!/usr/bin/env bash`

### `assets/course/c8/assets/scenario-udp-vs-tcp-loss/tcp_receiver.py`
- Tip: **Python**
- Linii: **30**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L5: Header / imports / constants
  - L6-L26: func main()
  - L28-L29: entrypoint if __name__ == '__main__'

### `assets/course/c8/assets/scenario-udp-vs-tcp-loss/tcp_sender.py`
- Tip: **Python**
- Linii: **21**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L7: Header / imports / constants
  - L8-L17: func main()
  - L19-L20: entrypoint if __name__ == '__main__'

### `assets/course/c8/assets/scenario-udp-vs-tcp-loss/topo.py`
- Tip: **Python**
- Linii: **34**
- Descriere (prima propoziţie/docstring/linie): from mininet.net import Mininet
- Dependenţe externe (pip/extra): mininet
- Context special: necesită Mininet (de obicei install sistem)
- Hartă funcţională (segmente):
  - L1-L6: Header / imports / constants
  - L7-L23: func build()
  - L25-L30: func main()
  - L32-L33: entrypoint if __name__ == '__main__'

### `assets/course/c8/assets/scenario-udp-vs-tcp-loss/udp_receiver.py`
- Tip: **Python**
- Linii: **44**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L6: Header / imports / constants
  - L7-L40: func main()
  - L42-L43: entrypoint if __name__ == '__main__'

### `assets/course/c8/assets/scenario-udp-vs-tcp-loss/udp_sender.py`
- Tip: **Python**
- Linii: **17**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L7: Header / imports / constants
  - L8-L13: func main()
  - L15-L16: entrypoint if __name__ == '__main__'

### `assets/course/c9/assets/render.sh`
- Tip: **Shell**
- Linii: **3**
- Shebang: `#!/usr/bin/env bash`
- Rol: rulează PlantUML pentru a genera imagini din fişiere `.puml`.
- Execuţie: `bash render.sh` (sau `./render.sh` dacă are bit de execuţie).
- Comandă principală: `java -jar ../../../tools/plantuml.jar -tpng puml/*.puml -o ../images`

### `assets/course/c9/assets/scenario-encoding-utf8/run.sh`
- Tip: **Shell**
- Linii: **6**
- Shebang: `#!/usr/bin/env bash`

### `assets/course/c9/assets/scenario-encoding-utf8/server.py`
- Tip: **Python**
- Linii: **44**
- Descriere (prima propoziţie/docstring/linie): from http.server import BaseHTTPRequestHandler, HTTPServer
- Hartă funcţională (segmente):
  - L1-L8: Header / imports / constants
  - L9-L34: class Handler
  - L36-L40: func main()
  - L42-L43: entrypoint if __name__ == '__main__'

### `assets/course/c9/assets/scenario-mime-encoding-gzip/data.json`
- Tip: **JSON**
- Linii: **6**
- JSON valid. Chei top-level: message, items, note

### `assets/course/c9/assets/scenario-mime-encoding-gzip/run.sh`
- Tip: **Shell**
- Linii: **6**
- Shebang: `#!/usr/bin/env bash`

### `assets/course/c9/assets/scenario-mime-encoding-gzip/server.py`
- Tip: **Python**
- Linii: **50**
- Descriere (prima propoziţie/docstring/linie): import gzip
- Hartă funcţională (segmente):
  - L1-L12: Header / imports / constants
  - L13-L41: class Handler
  - L43-L46: func main()
  - L48-L49: entrypoint if __name__ == '__main__'

### `assets/tutorial-solve/s2/2_tcp-server_template.py`
- Tip: **Python**
- Linii: **68**
- Descriere (prima propoziţie/docstring/linie): import socketserver
- Hartă funcţională (segmente):
  - L1-L3: Header / imports / constants
  - L4-L47: class MyTCPHandler
  - L52-L54: class MyTCPServer
  - L57-L67: entrypoint if __name__ == '__main__'

### `assets/tutorial/s10/2_dns-containers/Dockerfile`
- Tip: **Dockerfile**
- Linii: **4**
- Imagine de bază: `python:3`

### `assets/tutorial/s10/2_dns-containers/dns_server.py`
- Tip: **Python**
- Linii: **45**
- Descriere (prima propoziţie/docstring/linie): from dnslib import DNSRecord, RR, QTYPE, A
- Dependenţe externe (pip/extra): dnslib
- Hartă funcţională (segmente):
  - L1-L9: Header / imports / constants
  - L10-L40: func main()
  - L42-L43: entrypoint if __name__ == '__main__'

### `assets/tutorial/s10/2_dns-containers/docker-compose.yml`
- Tip: **YAML**
- Linii: **23**
- Tip YAML detectat: **docker-compose**
- Servicii: web, dns-server, debug
- Porturi expuse (rezumat): dns-server: ['5353:5353/udp']

### `assets/tutorial/s10/3_ssh/docker-compose.yml`
- Tip: **YAML**
- Linii: **24**
- Tip YAML detectat: **docker-compose**
- Servicii: ssh-server, ssh-client
- Porturi expuse (rezumat): ssh-server: ['2222:22']

### `assets/tutorial/s10/3_ssh/ssh-client/Dockerfile`
- Tip: **Dockerfile**
- Linii: **6**
- Imagine de bază: `python:3.10`

### `assets/tutorial/s10/3_ssh/ssh-client/paramiko_client.py`
- Tip: **Python**
- Linii: **76**
- Descriere (prima propoziţie/docstring/linie): import paramiko
- Dependenţe externe (pip/extra): paramiko
- Hartă funcţională (segmente):
  - L1-L10: Header / imports / constants
  - L11-L73: func main()
  - L75-L76: entrypoint if __name__ == '__main__'

### `assets/tutorial/s10/3_ssh/ssh-server/Dockerfile`
- Tip: **Dockerfile**
- Linii: **18**
- Imagine de bază: `ubuntu:22.04`
- CMD/ENTRYPOINT: `CMD ["/usr/sbin/sshd", "-D"]`

### `assets/tutorial/s10/4_ssh-port-forwarding/docker-compose.yml`
- Tip: **YAML**
- Linii: **22**
- Tip YAML detectat: **docker-compose**
- Servicii: web, ssh-bastion
- Porturi expuse (rezumat): ssh-bastion: ['2222:22']

### `assets/tutorial/s10/4_ssh-port-forwarding/ssh-bastion/Dockerfile`
- Tip: **Dockerfile**
- Linii: **14**
- Imagine de bază: `ubuntu:22.04`
- CMD/ENTRYPOINT: `CMD ["/usr/sbin/sshd", "-D"]`

### `assets/tutorial/s11/1_nginx-compose/docker-compose.nginx.yml`
- Tip: **YAML**
- Linii: **48**
- Tip YAML detectat: **docker-compose**
- Servicii: web1, web2, web3, nginx
- Porturi expuse (rezumat): nginx: ['8080:80']

### `assets/tutorial/s11/2_custom-load-balancer/docker-compose.lb-custom.yml`
- Tip: **YAML**
- Linii: **50**
- Tip YAML detectat: **docker-compose**
- Servicii: web1-lb, web2-lb, web3-lb, lb-custom
- Porturi expuse (rezumat): lb-custom: ['8080:8080']

### `assets/tutorial/s11/2_custom-load-balancer/simple_lb.py`
- Tip: **Python**
- Linii: **121**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L22: Header / imports / constants
  - L23-L38: func get_next_backend()
  - L41-L56: func forward_request_to_backend()
  - L59-L91: func handle_client_connection()
  - L94-L116: func main()
  - L119-L120: entrypoint if __name__ == '__main__'

### `assets/tutorial/s12/1_jsonrpc/jsonrpc_client.py`
- Tip: **Python**
- Linii: **54**
- Descriere (prima propoziţie/docstring/linie): import requests
- Dependenţe externe (pip/extra): requests
- Hartă funcţională (segmente):
  - L1-L6: Header / imports / constants
  - L7-L32: func rpc_call()
  - L35-L40: func main()
  - L52-L53: entrypoint if __name__ == '__main__'

### `assets/tutorial/s12/3_grpc/grpc_client.py`
- Tip: **Python**
- Linii: **109**
- Descriere (prima propoziţie/docstring/linie): import grpc
- Dependenţe externe (pip/extra): calculator_pb2, calculator_pb2_grpc, grpc
- Context special: necesită gRPC + generare stubs (grpcio-tools)
- Hartă funcţională (segmente):
  - L1-L11: Header / imports / constants
  - L12-L18: func call_add()
  - L21-L32: func call_multiply()
  - L35-L46: func call_power()
  - L49-L104: func main()
  - L107-L108: entrypoint if __name__ == '__main__'

### `assets/tutorial/s12/3_grpc/grpc_server.py`
- Tip: **Python**
- Linii: **111**
- Descriere (prima propoziţie/docstring/linie): import time
- Dependenţe externe (pip/extra): calculator_pb2, calculator_pb2_grpc, grpc
- Context special: necesită gRPC + generare stubs (grpcio-tools)
- Hartă funcţională (segmente):
  - L1-L14: Header / imports / constants
  - L15-L77: class CalculatorService
  - L80-L106: func serve()
  - L109-L110: entrypoint if __name__ == '__main__'

### `assets/tutorial/s13/docker-compose.pentest.yml`
- Tip: **YAML**
- Linii: **50**
- Tip YAML detectat: **docker-compose**
- Servicii: dvwa, webgoat, vsftpd
- Porturi expuse (rezumat): dvwa: ['8888:80'], webgoat: ['8080:8080'], vsftpd: ['2121:21', '6200:6200']

### `assets/tutorial/s13/ftp_backdoor_exploit.py`
- Tip: **Python**
- Linii: **82**
- Descriere (prima propoziţie/docstring/linie): ftp_backdoor_exploit.py
- Hartă funcţională (segmente):
  - L1-L23: Header / imports / constants
  - L24-L47: func trigger_backdoor()
  - L50-L68: func connect_backdoor()
  - L71-L78: func main()
  - L81-L82: entrypoint if __name__ == '__main__'

### `assets/tutorial/s13/simple_scanner.py`
- Tip: **Python**
- Linii: **56**
- Descriere (prima propoziţie/docstring/linie): simple_scanner.py
- Hartă funcţională (segmente):
  - L1-L20: Header / imports / constants
  - L21-L35: func scan_port()
  - L39-L52: func main()
  - L54-L55: entrypoint if __name__ == '__main__'

### `assets/tutorial/s2/10_udp-client_template.py`
- Tip: **Python**
- Linii: **66**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L5: Header / imports / constants
  - L6-L61: func main()
  - L64-L65: entrypoint if __name__ == '__main__'

### `assets/tutorial/s2/1_tcp-server_example.py`
- Tip: **Python**
- Linii: **72**
- Descriere (prima propoziţie/docstring/linie): import socketserver
- Hartă funcţională (segmente):
  - L1-L5: Header / imports / constants
  - L6-L38: class MyTCPHandler
  - L44-L45: class MyTCPServer
  - L48-L71: entrypoint if __name__ == '__main__'

### `assets/tutorial/s2/2_tcp-server_template.py`
- Tip: **Python**
- Linii: **62**
- Descriere (prima propoziţie/docstring/linie): import socketserver
- Hartă funcţională (segmente):
  - L1-L3: Header / imports / constants
  - L4-L24: class MyTCPHandler
  - L46-L48: class MyTCPServer
  - L51-L61: entrypoint if __name__ == '__main__'

### `assets/tutorial/s2/4_tcp-client_example.py`
- Tip: **Python**
- Linii: **34**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L33: Header / imports / constants

### `assets/tutorial/s2/5_tcp-client_template.py`
- Tip: **Python**
- Linii: **49**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L7: Header / imports / constants
  - L8-L44: func main()
  - L47-L48: entrypoint if __name__ == '__main__'

### `assets/tutorial/s2/6_tcp-client_scenario.py`
- Tip: **Python**
- Linii: **148**
- Descriere (prima propoziţie/docstring/linie): ### Scenariu: rularea clientului TCP Python, testare cu serverul și analiză RTT în Wireshark
- Hartă funcţională (segmente):
  - L1-L147: Header / imports / constants

### `assets/tutorial/s2/7_udp-server_example.py`
- Tip: **Python**
- Linii: **58**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L4: Header / imports / constants
  - L5-L53: func main()
  - L56-L57: entrypoint if __name__ == '__main__'

### `assets/tutorial/s2/8_udp-server_template.py`
- Tip: **Python**
- Linii: **58**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L4: Header / imports / constants
  - L5-L53: func main()
  - L56-L57: entrypoint if __name__ == '__main__'

### `assets/tutorial/s2/9_udp-client_example.py`
- Tip: **Python**
- Linii: **39**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L4: Header / imports / constants
  - L5-L34: func main()
  - L37-L38: entrypoint if __name__ == '__main__'

### `assets/tutorial/s3/1_tcp-multiclient-server_example.py`
- Tip: **Python**
- Linii: **117**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L20: Header / imports / constants
  - L21-L57: func handle_client()
  - L60-L86: func accept_loop()
  - L89-L112: func main()
  - L115-L116: entrypoint if __name__ == '__main__'

### `assets/tutorial/s3/2_tcp-multiclient-server_template.py`
- Tip: **Python**
- Linii: **105**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L13: Header / imports / constants
  - L14-L64: func handle_client()
  - L67-L84: func accept_loop()
  - L87-L100: func main()
  - L103-L104: entrypoint if __name__ == '__main__'

### `assets/tutorial/s3/4_udp-broadcast/4a_udp-broad-sender_example.py`
- Tip: **Python**
- Linii: **61**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L13: Header / imports / constants
  - L14-L56: func main()
  - L59-L60: entrypoint if __name__ == '__main__'

### `assets/tutorial/s3/4_udp-broadcast/4b_udp-broad-receiver_example.py`
- Tip: **Python**
- Linii: **36**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L8: Header / imports / constants
  - L9-L31: func main()
  - L34-L35: entrypoint if __name__ == '__main__'

### `assets/tutorial/s3/4_udp-broadcast/4c_udp-broad-receiver_template.py`
- Tip: **Python**
- Linii: **50**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L6: Header / imports / constants
  - L7-L43: func main()
  - L48-L49: entrypoint if __name__ == '__main__'

### `assets/tutorial/s3/4_udp-broadcast/4d_udp-broad_scenario.py`
- Tip: **Python**
- Linii: **140**
- Descriere (prima propoziţie/docstring/linie): ### Scenariu: UDP broadcast sender + receiver (IPv4) + Wireshark
- Hartă funcţională (segmente):
  - L1-L139: Header / imports / constants

### `assets/tutorial/s3/5_udp-multicast/5a_udp-multicast_sender_example.py`
- Tip: **Python**
- Linii: **41**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L8: Header / imports / constants
  - L9-L36: func main()
  - L39-L40: entrypoint if __name__ == '__main__'

### `assets/tutorial/s3/5_udp-multicast/5b_udp-multicast_receiver_example.py`
- Tip: **Python**
- Linii: **41**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L8: Header / imports / constants
  - L9-L36: func main()
  - L39-L40: entrypoint if __name__ == '__main__'

### `assets/tutorial/s3/5_udp-multicast/5c_udp-multicast_receiver_template.py`
- Tip: **Python**
- Linii: **54**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L8: Header / imports / constants
  - L9-L47: func main()
  - L52-L53: entrypoint if __name__ == '__main__'

### `assets/tutorial/s3/6_udp-anycast/6a_udp-anycast_server_example.py`
- Tip: **Python**
- Linii: **33**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L9: Header / imports / constants
  - L10-L28: func anycast_server()
  - L31-L32: entrypoint if __name__ == '__main__'

### `assets/tutorial/s3/6_udp-anycast/6b_udp-anycast_client_example.py`
- Tip: **Python**
- Linii: **31**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L8: Header / imports / constants
  - L9-L26: func anycast_client()
  - L29-L30: entrypoint if __name__ == '__main__'

### `assets/tutorial/s3/6_udp-anycast/6c_idp-anycast_template.py`
- Tip: **Python**
- Linii: **44**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L6: Header / imports / constants
  - L7-L37: func anycast_server()
  - L42-L43: entrypoint if __name__ == '__main__'

### `assets/tutorial/s4/1_text-proto_tcp/1a_text-proto_tcp-server_example.py`
- Tip: **Python**
- Linii: **199**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L17: Header / imports / constants
  - L18-L44: class State
  - L51-L112: func process_command()
  - L115-L163: func handle_client()
  - L166-L177: func accept_loop()
  - L180-L194: func main()
  - L197-L198: entrypoint if __name__ == '__main__'

### `assets/tutorial/s4/1_text-proto_tcp/1b_text-proto_tcp-client_example.py`
- Tip: **Python**
- Linii: **87**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L10: Header / imports / constants
  - L11-L34: func get_command()
  - L37-L82: func main()
  - L85-L86: entrypoint if __name__ == '__main__'

### `assets/tutorial/s4/1_text-proto_tcp/1c_text-proto_tcp-server_template.py`
- Tip: **Python**
- Linii: **198**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L10: Header / imports / constants
  - L11-L44: class State
  - L51-L58: func build_framed_response()
  - L61-L132: func process_command()
  - L137-L169: func handle_client()
  - L172-L177: func accept_loop()
  - L180-L193: func main()
  - L196-L197: entrypoint if __name__ == '__main__'

### `assets/tutorial/s4/2_binary-proto_tcp/2a_binary-proto_tcp-server_example.py`
- Tip: **Python**
- Linii: **211**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L16: Header / imports / constants
  - L17-L25: class Response
  - L28-L40: class Request
  - L43-L69: class State
  - L76-L131: func process_command()
  - L134-L177: func handle_client()
  - L180-L190: func accept_loop()
  - L193-L206: func main()
  - L209-L210: entrypoint if __name__ == '__main__'

### `assets/tutorial/s4/2_binary-proto_tcp/2b_binary-proto_tcp-client_example.py`
- Tip: **Python**
- Linii: **121**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L9: Header / imports / constants
  - L10-L17: class Response
  - L20-L28: class Request
  - L31-L71: func get_command()
  - L74-L116: func main()
  - L119-L120: entrypoint if __name__ == '__main__'

### `assets/tutorial/s4/2_binary-proto_tcp/2c_binary-proto_tcp-server_template.py`
- Tip: **Python**
- Linii: **184**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L12: Header / imports / constants
  - L13-L15: class Response
  - L18-L22: class Request
  - L25-L56: class State
  - L63-L78: func build_response()
  - L81-L128: func process_command()
  - L133-L155: func handle_client()
  - L158-L163: func accept_loop()
  - L166-L179: func main()
  - L182-L183: entrypoint if __name__ == '__main__'

### `assets/tutorial/s4/3_proto_udp/3a_udp-proto_server_example.py`
- Tip: **Python**
- Linii: **91**
- Descriere (prima propoziţie/docstring/linie): import socket
- Importuri locale: serialization, state, transfer_units
- Hartă funcţională (segmente):
  - L1-L16: Header / imports / constants
  - L17-L86: func main()
  - L89-L90: entrypoint if __name__ == '__main__'

### `assets/tutorial/s4/3_proto_udp/3b_udp-proto_client_example.py`
- Tip: **Python**
- Linii: **85**
- Descriere (prima propoziţie/docstring/linie): import socket
- Importuri locale: serialization, transfer_units
- Hartă funcţională (segmente):
  - L1-L12: Header / imports / constants
  - L13-L80: func main()
  - L83-L84: entrypoint if __name__ == '__main__'

### `assets/tutorial/s4/3_proto_udp/3c_udp-proto_client_template.py`
- Tip: **Python**
- Linii: **109**
- Descriere (prima propoziţie/docstring/linie): import socket
- Importuri locale: serialization, transfer_units
- Hartă funcţională (segmente):
  - L1-L12: Header / imports / constants
  - L13-L103: func main()
  - L107-L108: entrypoint if __name__ == '__main__'

### `assets/tutorial/s4/3_proto_udp/3c_udp-proto_server_template.py`
- Tip: **Python**
- Linii: **119**
- Descriere (prima propoziţie/docstring/linie): import socket
- Importuri locale: serialization, state, transfer_units
- Hartă funcţională (segmente):
  - L1-L15: Header / imports / constants
  - L16-L113: func main()
  - L117-L118: entrypoint if __name__ == '__main__'

### `assets/tutorial/s4/3_proto_udp/serialization.py`
- Tip: **Python**
- Linii: **29**
- Descriere (prima propoziţie/docstring/linie): import pickle
- Hartă funcţională (segmente):
  - L1-L4: Header / imports / constants
  - L5-L17: func serialize()
  - L20-L28: func deserialize()

### `assets/tutorial/s4/3_proto_udp/state.py`
- Tip: **Python**
- Linii: **51**
- Descriere (prima propoziţie/docstring/linie): class State:
- Hartă funcţională (segmente):
  - L1-L50: class State

### `assets/tutorial/s4/3_proto_udp/transfer_units.py`
- Tip: **Python**
- Linii: **78**
- Descriere (prima propoziţie/docstring/linie): from enum import Enum
- Hartă funcţională (segmente):
  - L1-L3: Header / imports / constants
  - L4-L19: class RequestMessageType
  - L22-L33: class ResponseMessageType
  - L36-L55: class RequestMessage
  - L58-L77: class ResponseMessage

### `assets/tutorial/s5/3_network-simulation/3b_mininet-topology.py`
- Tip: **Python**
- Linii: **90**
- Descriere (prima propoziţie/docstring/linie): Topologie Mininet pentru disciplina Retele de Calculatoare
- Dependenţe externe (pip/extra): mininet
- Context special: necesită Mininet (de obicei install sistem)
- Hartă funcţională (segmente):
  - L1-L16: Header / imports / constants
  - L17-L30: class LinuxRouter
  - L32-L48: class SimpleTopo
  - L50-L85: func run()
  - L87-L89: entrypoint if __name__ == '__main__'

### `assets/tutorial/s6/1_routing/1b_routing-triangle_topology.py`
- Tip: **Python**
- Linii: **113**
- Descriere (prima propoziţie/docstring/linie): Topologie Mininet: Triunghi de 3 routere + 2 hosturi
- Dependenţe externe (pip/extra): mininet
- Context special: necesită Mininet (de obicei install sistem)
- Hartă funcţională (segmente):
  - L1-L16: Header / imports / constants
  - L17-L25: class LinuxRouter
  - L28-L48: class TriangleRoutingTopo
  - L51-L106: func run()
  - L110-L112: entrypoint if __name__ == '__main__'

### `assets/tutorial/s6/2_sdn/2b_sdn_topo_switch.py`
- Tip: **Python**
- Linii: **80**
- Descriere (prima propoziţie/docstring/linie): Topologie Mininet pentru SDN:
- Dependenţe externe (pip/extra): mininet
- Context special: necesită Mininet (de obicei install sistem)
- Hartă funcţională (segmente):
  - L1-L20: Header / imports / constants
  - L21-L39: class SDNSimpleTopo
  - L42-L74: func run()
  - L77-L79: entrypoint if __name__ == '__main__'

### `assets/tutorial/s6/2_sdn/2c_sdn-os-ken_controller.py`
- Tip: **Python**
- Linii: **218**
- Descriere (prima propoziţie/docstring/linie): Controller OS-Ken simplu pentru topologia:
- Dependenţe externe (pip/extra): os_ken
- Hartă funcţională (segmente):
  - L1-L18: Header / imports / constants
  - L19-L217: class SimpleSwitch13

### `assets/tutorial/s6/3_sdn-app-traffic/tcp_client.py`
- Tip: **Python**
- Linii: **50**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L16: Header / imports / constants
  - L17-L45: func main()
  - L48-L49: entrypoint if __name__ == '__main__'

### `assets/tutorial/s6/3_sdn-app-traffic/tcp_server.py`
- Tip: **Python**
- Linii: **45**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L15: Header / imports / constants
  - L16-L40: func main()
  - L43-L44: entrypoint if __name__ == '__main__'

### `assets/tutorial/s6/3_sdn-app-traffic/udp_client.py`
- Tip: **Python**
- Linii: **45**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L15: Header / imports / constants
  - L16-L40: func main()
  - L43-L44: entrypoint if __name__ == '__main__'

### `assets/tutorial/s6/3_sdn-app-traffic/udp_server.py`
- Tip: **Python**
- Linii: **37**
- Descriere (prima propoziţie/docstring/linie): import socket
- Hartă funcţională (segmente):
  - L1-L15: Header / imports / constants
  - L16-L32: func main()
  - L35-L36: entrypoint if __name__ == '__main__'

### `assets/tutorial/s7/1_sniffing/1b_packet_sniffer.py`
- Tip: **Python**
- Linii: **187**
- Descriere (prima propoziţie/docstring/linie): !/usr/bin/env python3
- Context special: probabil necesită privilegii (raw socket/sniff)
- Hartă funcţională (segmente):
  - L1-L34: Header / imports / constants
  - L35-L40: func mac_addr()
  - L43-L47: func ipv4_addr()
  - L50-L65: func parse_ethernet_header()
  - L68-L116: func parse_ipv4_header()
  - L119-L182: func main()
  - L185-L186: entrypoint if __name__ == '__main__'

### `assets/tutorial/s7/2_packet-filter/2a_packet-filter.py`
- Tip: **Python**
- Linii: **214**
- Descriere (prima propoziţie/docstring/linie): !/usr/bin/env python3
- Context special: probabil necesită privilegii (raw socket/sniff)
- Hartă funcţională (segmente):
  - L1-L32: Header / imports / constants
  - L33-L34: func mac_addr()
  - L37-L38: func ipv4_addr()
  - L41-L45: func parse_ethernet_header()
  - L48-L63: func parse_ipv4_header()
  - L66-L78: func parse_tcp_header()
  - L81-L93: func parse_udp_header()
  - L100-L134: func passes_filter()
  - L141-L209: func main()
  - L212-L213: entrypoint if __name__ == '__main__'

### `assets/tutorial/s7/3_port-scanning/3a_port_scanner.py`
- Tip: **Python**
- Linii: **135**
- Descriere (prima propoziţie/docstring/linie): !/usr/bin/env python3
- Hartă funcţională (segmente):
  - L1-L35: Header / imports / constants
  - L36-L74: func scan_port()
  - L77-L103: func scan_range()
  - L106-L130: func main()
  - L133-L134: entrypoint if __name__ == '__main__'

### `assets/tutorial/s7/4_scan-detector/4a_detect-scan.py`
- Tip: **Python**
- Linii: **204**
- Descriere (prima propoziţie/docstring/linie): !/usr/bin/env python3
- Context special: probabil necesită privilegii (raw socket/sniff)
- Hartă funcţională (segmente):
  - L1-L37: Header / imports / constants
  - L38-L39: func ipv4_addr()
  - L42-L44: func parse_ethernet_header()
  - L47-L53: func parse_ipv4_header()
  - L56-L93: func parse_tcp_header()
  - L96-L199: func main()
  - L202-L203: entrypoint if __name__ == '__main__'

### `assets/tutorial/s7/5_mini-ids/5a_mini-ids.py`
- Tip: **Python**
- Linii: **301**
- Descriere (prima propoziţie/docstring/linie): !/usr/bin/env python3
- Context special: probabil necesită privilegii (raw socket/sniff)
- Hartă funcţională (segmente):
  - L1-L45: Header / imports / constants
  - L46-L47: func ipv4_addr()
  - L50-L52: func parse_ethernet_header()
  - L55-L63: func parse_ipv4_header()
  - L66-L78: func parse_tcp_header()
  - L81-L85: func parse_udp_header()
  - L90-L111: func log_alert()
  - L114-L123: func cleanup_old_entries()
  - L147-L204: func handle_tcp_packet()
  - L207-L232: func handle_udp_packet()
  - L238-L296: func main()
  - L299-L300: entrypoint if __name__ == '__main__'

### `assets/tutorial/s8/2_simple-http/2b_simple-http-builtin_example.py`
- Tip: **Python**
- Linii: **86**
- Descriere (prima propoziţie/docstring/linie): !/usr/bin/env python3
- Hartă funcţională (segmente):
  - L1-L26: Header / imports / constants
  - L27-L60: class MyHandler
  - L63-L82: func main()
  - L85-L86: entrypoint if __name__ == '__main__'

### `assets/tutorial/s8/3_socket-http/3b_socket-http-server_example.py`
- Tip: **Python**
- Linii: **149**
- Descriere (prima propoziţie/docstring/linie): !/usr/bin/env python3
- Hartă funcţională (segmente):
  - L1-L26: Header / imports / constants
  - L27-L47: func build_http_response()
  - L50-L121: func handle_client()
  - L124-L144: func main()
  - L147-L148: entrypoint if __name__ == '__main__'

### `assets/tutorial/s8/4_nginx/docker-compose.yml`
- Tip: **YAML**
- Linii: **14**
- Tip YAML detectat: **docker-compose**
- Servicii: nginx

### `assets/tutorial/s9/1_ftp/1c_pyftpd-server.py`
- Tip: **Python**
- Linii: **49**
- Descriere (prima propoziţie/docstring/linie): Seminar 9 – Server FTP minimal folosind pyftpdlib.
- Dependenţe externe (pip/extra): pyftpdlib
- Hartă funcţională (segmente):
  - L1-L16: Header / imports / constants
  - L17-L44: func main()
  - L47-L48: entrypoint if __name__ == '__main__'

### `assets/tutorial/s9/1_ftp/1d_pyftpd-client.py`
- Tip: **Python**
- Linii: **54**
- Descriere (prima propoziţie/docstring/linie): Seminar 9 – Client FTP minimal cu ftplib.
- Hartă funcţională (segmente):
  - L1-L18: Header / imports / constants
  - L19-L48: func main()
  - L51-L52: entrypoint if __name__ == '__main__'

### `assets/tutorial/s9/2_custom-pseudo-ftp/2b_pseudo-ftp-server.py`
- Tip: **Python**
- Linii: **300**
- Descriere (prima propoziţie/docstring/linie): Seminar 9 – Server pseudo-FTP (control + data, mod activ/pasiv).
- Hartă funcţională (segmente):
  - L1-L34: Header / imports / constants
  - L35-L65: func process_command()
  - L68-L80: func process_help()
  - L83-L92: func process_list()
  - L95-L128: func active_get()
  - L131-L169: func active_put()
  - L172-L214: func passive_put()
  - L217-L254: func passive_get()
  - L257-L266: func handle_client_commands()
  - L269-L279: func accept()
  - L282-L295: func main()
  - L298-L299: entrypoint if __name__ == '__main__'

### `assets/tutorial/s9/2_custom-pseudo-ftp/2c_pseudo-ftp-client.py`
- Tip: **Python**
- Linii: **270**
- Descriere (prima propoziţie/docstring/linie): Seminar 9 – Client pseudo-FTP pentru serverul nostru custom.
- Hartă funcţională (segmente):
  - L1-L29: Header / imports / constants
  - L30-L75: func active_get()
  - L78-L111: func active_put()
  - L114-L160: func passive_get()
  - L163-L201: func passive_put()
  - L204-L247: func process_command()
  - L250-L265: func main()
  - L268-L269: entrypoint if __name__ == '__main__'

### `assets/tutorial/s9/3_multi-client-containers/docker-compose.yml`
- Tip: **YAML**
- Linii: **44**
- Tip YAML detectat: **docker-compose**
- Servicii: ftp-server, client1, client2
- Porturi expuse (rezumat): ftp-server: ['2121:2121']

### `assets/tutorial/s9/3_multi-client-containers/pyftpd_multi_client.py`
- Tip: **Python**
- Linii: **103**
- Descriere (prima propoziţie/docstring/linie): Seminar 9 – Client FTP pentru scenariul multi-client in Docker.
- Hartă funcţională (segmente):
  - L1-L32: Header / imports / constants
  - L33-L55: func upload_file()
  - L58-L80: func download_file()
  - L83-L98: func main()
  - L101-L102: entrypoint if __name__ == '__main__'

### `assets/tutorial/s9/3_multi-client-containers/pyftpd_server.py`
- Tip: **Python**
- Linii: **40**
- Descriere (prima propoziţie/docstring/linie): !/usr/bin/env python3
- Dependenţe externe (pip/extra): pyftpdlib
- Hartă funcţională (segmente):
  - L1-L12: Header / imports / constants
  - L13-L35: func main()
  - L38-L39: entrypoint if __name__ == '__main__'

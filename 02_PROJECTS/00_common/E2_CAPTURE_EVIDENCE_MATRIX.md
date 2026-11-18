# E2 capture and semantic-evidence matrix

Use this plan alongside the canonical project brief and `tools/pcap_rules/<CODE>.json`. Start capture before the first connection and stop it only after the final response or documented timeout. The manifest defines the exact filters, measurement modes and thresholds. Record the actual test name, stream/frame references and observed result for each step in `docs/E2_pcap_analysis.md`.

A successful filter establishes only its stated capture measurement. Application assertions and the evidence in the last column establish the behaviour required by the brief. A presence check does not establish authentication, routing correctness, caching, isolation or a timed state transition. Figures illustrate the protocol; use all steps below when a figure shows only part of E2.

The plan covers A01–A10 and S01–S20. It introduces no additional assessment weighting. E3-only requirements remain at E3; references below to additional tests describe the existing brief requirements.

## A01

Canonical sources: [project brief](../02_administration_security/A01_sdn_firewall_filtering_policies_via_openflow_rules.md) · [capture rules](tools/pcap_rules/A01.json).

| Step | Action that generates the capture evidence | Rule IDs | Complementary semantic evidence |
|---|---|---|---|
| A01-P1 | Start the controller, connect the switch and install the declared policy. | R1, R2 | Correlate decoded OpenFlow messages and flow-table entries; payload segments alone do not identify a FlowMod. |
| A01-P2 | Run one permitted exchange and one blocked attempt between the data hosts. | R3 | Record both capture points, allowed replies, blocked-flow counter and absence of the denied delivery in the declared window. |

## A02

Canonical sources: [project brief](../02_administration_security/A02_ids_simple_rules_scan_detection_tcp_anomalies_and_payload_patterns.md) · [capture rules](tools/pcap_rules/A02.json).

| Step | Action that generates the capture evidence | Rule IDs | Complementary semantic evidence |
|---|---|---|---|
| A02-P1 | Scan at least ten distinct destination ports of the declared victim within the E1 detector window, including a known closed port. | R1, R2 | Correlate source, target, timestamps and generated scan alert; repeated SYNs to one port are not ten ports. |
| A02-P2 | Send the configured signature pattern to the local test service. | R3 | Assert the signature alert and show the matching request; bytes alone do not establish detection. |

## A03

Canonical sources: [project brief](../02_administration_security/A03_pcap_report_generator_flow_statistics_top_talkers_and_tcp_indicators.md) · [capture rules](tools/pcap_rules/A03.json).

| Step | Action that generates the capture evidence | Rule IDs | Complementary semantic evidence |
|---|---|---|---|
| A03-P1 | Capture a repeatable TCP transfer long enough to obtain at least fifty TCP/IP frames under the declared delay/loss profile. | R1, R2, R3 | Record the profile and before/after timing statistics. A delay-only run may have zero retransmissions. |

## A04

Canonical sources: [project brief](../02_administration_security/A04_arp_spoofing_detection_and_mitigation_alerts_evidence_and_controlled_blocking.md) · [capture rules](tools/pcap_rules/A04.json).

| Step | Action that generates the capture evidence | Rule IDs | Complementary semantic evidence |
|---|---|---|---|
| A04-P1 | Record normal ARP resolution, then send the controlled spoofing replies in the isolated topology. | R1, R2, R3 | Compare IP/MAC mappings and detector alerts, then verify the repaired victim cache and restored ping separately. |

## A05

Canonical sources: [project brief](../02_administration_security/A05_laboratory_port_scanning_tcp_connect_scan_and_minimal_service_fingerprinting.md) · [capture rules](tools/pcap_rules/A05.json).

| Step | Action that generates the capture evidence | Rule IDs | Complementary semantic evidence |
|---|---|---|---|
| A05-P1 | Scan the declared local port set, including a listening service, a closed port and a deliberately filtered port. | R1, R2, R3 | Match each reported state to its actual probed port, response or timeout and firewall rule. |
| A05-P2 | Probe the open service for its banner or HTTP header. | R4 | Match the parsed fingerprint to the service; any matching text frame alone is insufficient. |

## A06

Canonical sources: [project brief](../02_administration_security/A06_nat_and_dhcp_laboratory_dynamic_allocation_iptables_masquerade_and_pcap_verification.md) · [capture rules](tools/pcap_rules/A06.json).

| Step | Action that generates the capture evidence | Rule IDs | Complementary semantic evidence |
|---|---|---|---|
| A06-P1 | Acquire a DHCP lease in the internal namespace. | R1, R2, R3, R4 | Correlate transaction/client identity and the Discover–Offer–Request–ACK order. |
| A06-P2 | After ACK, access the external test service through the configured gateway. | R5 | Compare internal and external source addresses, routes, NAT/FORWARD rules and the complete reply path. |

## A07

Canonical sources: [project brief](../02_administration_security/A07_sdn_learning_switch_controller_flow_installation_and_ageing.md) · [capture rules](tools/pcap_rules/A07.json).

| Step | Action that generates the capture evidence | Rule IDs | Complementary semantic evidence |
|---|---|---|---|
| A07-P1 | Start the learning controller and connect the switch. | R1, R2 | Identify PacketIn/FlowMod messages and inspect learned MAC-to-port entries. |
| A07-P2 | Exchange traffic between data hosts before and after learning. | R3 | Show initial broadcast resolution, subsequent unicast forwarding and flow-table counters. |

## A08

Canonical sources: [project brief](../02_administration_security/A08_mininet_encapsulation_and_tunnelling_vxlan_between_two_sites.md) · [capture rules](tools/pcap_rules/A08.json).

| Step | Action that generates the capture evidence | Rule IDs | Complementary semantic evidence |
|---|---|---|---|
| A08-P1 | Configure VXLAN and send ARP/ICMP between the overlay hosts. | R1, R2 | Decode outer/inner endpoint pairs and VNI; repeat the documented DF/MTU experiment and compare IP lengths. |

## A09

Canonical sources: [project brief](../02_administration_security/A09_sdn_ips_dynamic_blocking_via_openflow_triggered_by_ids_detection.md) · [capture rules](tools/pcap_rules/A09.json).

| Step | Action that generates the capture evidence | Rule IDs | Complementary semantic evidence |
|---|---|---|---|
| A09-P1 | Start the controller and trigger the IDS with h1 scan traffic. | R1, R2, R3 | Correlate the alert, block request and actual installed drop flow. Capture before/after at the declared switch ports. |
| A09-P2 | While h1 is blocked, ping h2 from the legitimate h3 host. | R4 | Verify a full request/reply pair and measure hard_timeout expiry under continuous h1 traffic. |

## A10

Canonical sources: [project brief](../02_administration_security/A10_network_hardening_containerised_services_segmentation_egress_filtering_docker_user.md) · [capture rules](tools/pcap_rules/A10.json).

| Step | Action that generates the capture evidence | Rule IDs | Complementary semantic evidence |
|---|---|---|---|
| A10-P1 | Start the three service tiers and run the declared connectivity matrix. | R1 | Attribute each flow to its source namespace and show the matching DOCKER-USER decision. |
| A10-P2 | Run one DNS lookup and HTTP/HTTPS egress probes under the allowed/blocked policy. | R2, R3 | Check the actual reply or absence of delivery, counters and capture placement; attempts alone do not prove isolation. |

## S01

Canonical sources: [project brief](../01_network_applications/S01_multi_client_tcp_chat_text_protocol_and_presence.md) · [capture rules](tools/pcap_rules/S01.json).

| Step | Action that generates the capture evidence | Rule IDs | Complementary semantic evidence |
|---|---|---|---|
| S01-P1 | Connect a chat client to TCP/5000. | R1, R2 | Match SYN/SYN-ACK/ACK to the same flow. |
| S01-P2 | Authenticate, broadcast a message to a second client and observe its presence/event output. | R3, R4, R5 | Reassemble the declared framing and assert identities, message text and intended recipients. |
| S01-P3 | Send QUIT and close the connection. | R6 | Correlate the application close response, presence event and transport teardown. |

## S02

Canonical sources: [project brief](../01_network_applications/S02_file_transfer_server_control_and_data_channels_ftp_passive.md) · [capture rules](tools/pcap_rules/S02.json).

| Step | Action that generates the capture evidence | Rule IDs | Complementary semantic evidence |
|---|---|---|---|
| S02-P1 | Connect to the control service, authenticate and request passive mode. | R1, R2, R3 | Assert successful authentication and parse the advertised reachable data endpoint. |
| S02-P2 | Open that data connection and transfer the requested file. | R4, R5 | Verify bytes and completion status against the requested file. |
| S02-P3 | Report and compare the SHA-256 digest over the transferred file. | R6 | A HASH/SHA-256 marker is only presence evidence; compare the complete digest values. |

## S03

Canonical sources: [project brief](../01_network_applications/S03_http11_socket_server_no_framework_static_files.md) · [capture rules](tools/pcap_rules/S03.json).

| Step | Action that generates the capture evidence | Rule IDs | Complementary semantic evidence |
|---|---|---|---|
| S03-P1 | Keep one TCP/8080 connection open and issue two complete GET requests: an existing file, then a missing file. | R1, R2, R3, R4, R5 | Assert both decoded responses, Content-Type, Content-Length/body framing and reuse of the same TCP stream. Test HEAD separately as required by the brief. |

## S04

Canonical sources: [project brief](../01_network_applications/S04_forward_http_proxy_with_filtering_and_traffic_logging.md) · [capture rules](tools/pcap_rules/S04.json).

| Step | Action that generates the capture evidence | Rule IDs | Complementary semantic evidence |
|---|---|---|---|
| S04-P1 | Connect to the proxy and request an allowed resource from the local origin. | R1, R2, R3, R4 | Correlate client/proxy/origin streams and verify the forwarded body, headers and log. Run the blocked-domain test separately. |

## S05

Canonical sources: [project brief](../01_network_applications/S05_application_level_http_load_balancer_health_checks_and_two_algorithms.md) · [capture rules](tools/pcap_rules/S05.json).

| Step | Action that generates the capture evidence | Rule IDs | Complementary semantic evidence |
|---|---|---|---|
| S05-P1 | Send a request through the load balancer to a healthy backend. | R1, R2, R3, R5 | Correlate both legs and the returned body; assert the declared selection policy. |
| S05-P2 | Run a backend health check, then stop that backend and repeat the client request. | R4 | Show health-state transition and exclusion of the failed backend; a /health substring alone does not establish it. |

## S06

Canonical sources: [project brief](../01_network_applications/S06_tcp_pub_sub_broker_topics_and_deterministic_routing.md) · [capture rules](tools/pcap_rules/S06.json).

| Step | Action that generates the capture evidence | Rule IDs | Complementary semantic evidence |
|---|---|---|---|
| S06-P1 | Connect clients, authenticate and subscribe one client to a topic. | R1, R2, R3 | Decode LF/CRLF command lines or supply the E1 framing decoder; correlate client and topic. |
| S06-P2 | Publish two messages and observe the subscribed client deliveries. | R4, R5 | Assert payloads and recipients, then verify unsubscribe and the E1 duplicate/delivery policy. |

## S07

Canonical sources: [project brief](../01_network_applications/S07_udp_dns_resolver_local_zone_forwarding_and_ttl_cache.md) · [capture rules](tools/pcap_rules/S07.json).

| Step | Action that generates the capture evidence | Rule IDs | Complementary semantic evidence |
|---|---|---|---|
| S07-P1 | Query a local lab.local record. | R1, R2 | Use decoded dns.qry.name and answers; DNS wire names contain length octets. |
| S07-P2 | Query an external name twice and repeat any request needed to meet the declared query count. | R1, R2, R3, R4 | Match query names/types and transaction IDs. Demonstrate that the repeated response is a cache hit within TTL, with no corresponding upstream query. |
| S07-P3 | Query a known nonexistent name in the local zone. | R1, R2, R5 | Assert NXDOMAIN. Repeating and caching this failure is optional unless selected in E1. |

## S08

Canonical sources: [project brief](../01_network_applications/S08_minimal_email_system_smtp_delivery_and_pop3_retrieval.md) · [capture rules](tools/pcap_rules/S08.json).

| Step | Action that generates the capture evidence | Rule IDs | Complementary semantic evidence |
|---|---|---|---|
| S08-P1 | Connect to SMTP and send HELO/EHLO, MAIL FROM and RCPT TO. | R1, R2, R3, R4 | Assert the corresponding SMTP status codes and intended recipient. |
| S08-P2 | Enter DATA, send the message and terminate it with CRLF-dot-CRLF. | R5, R6 | Reassemble the TCP stream, test dot-stuffing and verify maildir storage; a dot substring alone does not prove valid termination. |

## S09

Canonical sources: [project brief](../01_network_applications/S09_tcp_tunnel_single_port_session_multiplexing_and_demultiplexing.md) · [capture rules](tools/pcap_rules/S09.json).

| Step | Action that generates the capture evidence | Rule IDs | Complementary semantic evidence |
|---|---|---|---|
| S09-P1 | Connect the tunnel and open sessions to the two internal services. | R1, R2 | Decode the TNL1 header, type, session ID, service ID and length from the reassembled stream. |
| S09-P2 | Exchange payload on both sessions and close them. | R3, R4, R5 | Correlate session IDs, payload boundaries and each target response. Segment counts do not prove multiplexing. |

## S10

Canonical sources: [project brief](../01_network_applications/S10_network_file_synchronisation_manifest_hashes_and_conflict_resolution.md) · [capture rules](tools/pcap_rules/S10.json).

| Step | Action that generates the capture evidence | Rule IDs | Complementary semantic evidence |
|---|---|---|---|
| S10-P1 | Connect and exchange the manifests and full SHA-256 digests. | R1, R2, R3 | Decode the selected framing and compare paths, sizes and complete hashes. |
| S10-P2 | Transfer the missing/changed file, verify its digest and close. | R4, R5 | Assert final contents and the chosen conflict policy, including the explicitly permitted handling of the losing version. |

## S11

Canonical sources: [project brief](../01_network_applications/S11_rest_microservices_service_registry_api_gateway_dynamic_routing.md) · [capture rules](tools/pcap_rules/S11.json).

| Step | Action that generates the capture evidence | Rule IDs | Complementary semantic evidence |
|---|---|---|---|
| S11-P1 | Start registry, gateway and two services; emit the mandatory UDP discovery announcement. | R1 | Decode the announcement and correlate it with the registry entry; see the discovery subscenario in the E2 figure. |
| S11-P2 | Send a gateway request that reaches a registered microservice and returns successfully. | R2, R3, R4, R5 | Trace both HTTP legs and service identity. Stop an instance and assert the E1 reroute/503 policy separately. |

## S12

Canonical sources: [project brief](../01_network_applications/S12_client_server_messaging_tls_channel_and_minimal_authentication.md) · [capture rules](tools/pcap_rules/S12.json).

| Step | Action that generates the capture evidence | Rule IDs | Complementary semantic evidence |
|---|---|---|---|
| S12-P1 | Connect using TLS with the laboratory CA and hostname validation. | R1, R2, R3, R4 | Record TLS version and a passing validation test, plus rejection of an untrusted certificate. TLS 1.3 encrypts Certificate after ServerHello. |
| S12-P2 | Send the application request and receive its expected response inside TLS. | R5 | Assert the application result and correlate client/server logs. A handshake-only encrypted record cannot establish application delivery; optional key logging is local-test evidence. |

## S13

Canonical sources: [project brief](../01_network_applications/S13_grpc_rpc_service_proto_definition_unary_and_streaming_methods.md) · [capture rules](tools/pcap_rules/S13.json).

| Step | Action that generates the capture evidence | Rule IDs | Complementary semantic evidence |
|---|---|---|---|
| S13-P1 | Call the unary and streaming gRPC methods on cleartext HTTP/2 TCP/50051. | R1, R2, R3 | Assert method outputs, deadline status and message counts independently of DATA-frame boundaries. |
| S13-P2 | Use the mandatory raw-protobuf TCP/50052 endpoint with its PB1 framing. | R4, R5 | Decode PB1 and its length-delimited protobuf message at E2. Demonstrate Flex interoperability on this endpoint at E3. |

## S14

Canonical sources: [project brief](../01_network_applications/S14_didactic_distance_vector_routing_in_mininet_convergence_and_anti_loop.md) · [capture rules](tools/pcap_rules/S14.json).

| Step | Action that generates the capture evidence | Rule IDs | Complementary semantic evidence |
|---|---|---|---|
| S14-P1 | Start at least three routers and collect periodic DV1 updates. | R1 | Decode sender, destination and metric according to E1. |
| S14-P2 | Forward DATA1 through an intermediate router and run the declared end-to-end probe. | R2, R4 | Correlate each hop and the destination result with the routing table. |
| S14-P3 | Fail the selected link and emit the declared POISON/SPLITH marker. | R3 | Inspect destination, recipient and metric: distinguish route poisoning from poison reverse and prove the resulting route changes. |

## S15

Canonical sources: [project brief](../01_network_applications/S15_iot_gateway_udp_telemetry_ingestion_http_api_query_and_streaming.md) · [capture rules](tools/pcap_rules/S15.json).

| Step | Action that generates the capture evidence | Rule IDs | Complementary semantic evidence |
|---|---|---|---|
| S15-P1 | Send at least three telemetry datagrams with IOT1 followed by valid E1 JSON/TLV payloads. | R1, R5 | Decode device_id, ts, seq and value and test invalid prefix, duplicate/out-of-order data and bounds. |
| S15-P2 | Connect to the HTTP API, query the stored measurement and receive a successful response. | R2, R3, R4 | Assert that the returned device, sequence and value match the injected measurement; demonstrate the mandatory E3 stream separately. |

## S16

Canonical sources: [project brief](../01_network_applications/S16_collaborative_text_editing_locking_notifications_and_versioned_saves.md) · [capture rules](tools/pcap_rules/S16.json).

| Step | Action that generates the capture evidence | Rule IDs | Complementary semantic evidence |
|---|---|---|---|
| S16-P1 | Connect two clients and have A lock a document, then B request the same lock. | R1, R2, R3 | Assert B receives the declared refusal and that A remains owner. |
| S16-P2 | Have A save a new version and notify B. | R4, R5 | Compare saved content/version and notification recipient; a version marker alone is insufficient. |

## S17

Canonical sources: [project brief](../01_network_applications/S17_in_memory_object_store_registry_lookup_watchers_and_lease_expiry.md) · [capture rules](tools/pcap_rules/S17.json).

| Step | Action that generates the capture evidence | Rule IDs | Complementary semantic evidence |
|---|---|---|---|
| S17-P1 | Publish an object and have another client request that key. | R1, R2, R3, R4 | Assert ownership, key and exact brokered result. |
| S17-P2 | Remove the object or let its lease expire while a watcher is active. | R5 | Measure the E1 lease interval and assert cleanup plus watcher notification; a LEASE/HEARTBEAT word alone is insufficient. |

## S18

Canonical sources: [project brief](../01_network_applications/S18_resource_reservation_holds_leases_wait_queue_and_consistency.md) · [capture rules](tools/pcap_rules/S18.json).

| Step | Action that generates the capture evidence | Rule IDs | Complementary semantic evidence |
|---|---|---|---|
| S18-P1 | Have A hold one resource/interval and B attempt an overlapping hold. | R1, R2, R3 | Assert refusal without changing A’s valid hold or interval. |
| S18-P2 | Confirm A’s hold, then run a separate cancellable/expiring hold scenario. | R4, R5 | Assert reservation ownership and the release/expiry event with the E1 timing and recipient. |

## S19

Canonical sources: [project brief](../01_network_applications/S19_distributed_auction_bids_timers_state_transitions_and_event_log.md) · [capture rules](tools/pcap_rules/S19.json).

| Step | Action that generates the capture evidence | Rule IDs | Complementary semantic evidence |
|---|---|---|---|
| S19-P1 | Connect a seller, publish an item and submit two successive valid bids from different bidders. | R1, R2, R3, R4 | Decode the command framing and assert bidder identity, monotonic top bid and outbid notification. |
| S19-P2 | Let the auction timer expire. | R5 | Assert the correct winner and closing time; reject bids after closure. |

## S20

Canonical sources: [project brief](../01_network_applications/S20_database_backed_object_service_selection_update_delete_and_notifications.md) · [capture rules](tools/pcap_rules/S20.json).

| Step | Action that generates the capture evidence | Rule IDs | Complementary semantic evidence |
|---|---|---|---|
| S20-P1 | Connect two clients; query/select the same object. | R1, R2 | Assert identity, version and subscription state. |
| S20-P2 | Update it from A and observe B’s notification, then delete it. | R3, R4, R5 | Assert the exact changed/deleted key and version, recipient and deterministic absent-key response. Include the restart-persistence smoke test required by the E2 Deliverables; repeat the complete persistence demonstration at E3. |

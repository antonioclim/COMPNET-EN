# Project 13: RPC/gRPC Distributed Service

> **Course:** Computer Networks  
> **Programme:** Economic Informatics, Year 3, Semester 2  
> **Institution:** ASE Bucharest - CSIE  
> **Project type:** Main

> 📍 **Navigation:** [00PROJ](../README.md) → [PROJECTS](./README.md) → P13

---

## 📋 Assessment and Delivery Guide

### ⚠️ IMPORTANT: Assessment with Physical Attendance

**Common guides:** [Pair Programming](../docs/common/pair_programming_guide.md) | [Code Quality](../docs/common/code_quality_standards.md) | [Git Workflow](../docs/common/git_workflow_detailed.md) | [Troubleshooting](../docs/common/troubleshooting_common.md)

---

### 📅 Stage Calendar

| Stage | Week | Deadline | Deliverables | Score |
|-------|------|----------|--------------|-------|
| **E1** - Design | Week 5 | Week 5 (2026) | Specifications + Diagrams + Plan | 20% |
| **E2** - Prototype | Week 9 | Week 9 (2026) | Partial functional implementation | 25% |
| **E3** - Final | Week 13 | Week 13 (2026) | Complete version + Documentation | 35% |
| **E4** - Presentation | Week 14 | Week 14 (2026) | Live demo + Oral defence | 20% |

**Repository:** `https://github.com/[username]/retele-proiect-13`

---

### 📊 Assessment Rubric

#### Stage 1 — Design (100 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Complete specifications | 30 | Service definitions, proto files |
| Architecture diagrams | 20 | Client-server, data flow |
| Implementation plan | 15 | Realistic timeline |
| Repository initialised | 15 | GitHub configured |
| MANIFEST.txt | 10 | Valid signature |
| Archive naming | 10 | Follows convention |

#### Stage 2 — Prototype (100 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Basic RPC working | 35 | Unary calls functional |
| Code quality | 25 | Clean, typed, documented |
| Proto generation | 15 | Auto-generated stubs work |
| Progress report | 10 | Documents progress |
| MANIFEST.txt | 10 | Valid signature |
| On-time delivery | 5 | Meets deadline |

#### Stage 3 — Final Version (100 points + 10 bonus)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Complete implementation | 40 | Unary + streaming |
| Final code quality | 20 | Production-ready |
| Tests | 15 | Unit and integration |
| Documentation | 10 | Complete API docs |
| Performance analysis | 5 | Latency comparison with REST |
| MANIFEST.txt | 10 | Valid signature |
| **Bonus: Bidirectional streaming** | +10 | Real-time chat/updates (teams of 3) |

#### Stage 4 — Presentation (100 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Live demo functional | 35 | RPC calls work |
| Technical presentation | 25 | Explains RPC vs REST |
| Answers to questions | 20 | Demonstrates understanding |
| Team contribution | 15 | All members know code |
| Time management | 5 | 10-15 minutes |

---

### 👥 Team Size

| Team | Requirements |
|------|--------------|
| **1 person** | Basic unary RPC service (CRUD operations) |
| **2 persons** | + Server streaming + client streaming |
| **3 persons** | + Bidirectional streaming + interceptors |

---

## 📚 Project Description

Implement a distributed service using gRPC (Google Remote Procedure Call) with Protocol Buffers for serialisation. Create a client-server application that demonstrates different RPC patterns: unary, server streaming, client streaming and bidirectional streaming. Compare performance with equivalent REST API.

gRPC is used by major companies (Google, Netflix, Square) for microservice communication due to its efficiency and strong typing.

### 🎯 Learning Objectives

- **LO1:** Define services using Protocol Buffer (proto3) syntax
- **LO2:** Implement unary RPC calls for request-response patterns
- **LO3:** Use server streaming for large data sets
- **LO4:** Implement client streaming for data uploads
- **LO5:** Compare gRPC performance with REST/JSON
- **LO6:** Handle errors and deadlines in distributed calls

### 🛠️ Technologies and Tools

| Technology | Purpose | Documentation |
|------------|---------|---------------|
| **gRPC** | RPC framework | [grpc.io](https://grpc.io) |
| **Protocol Buffers** | Serialisation | [protobuf.dev](https://protobuf.dev) |
| **grpcio-tools** | Python code generation | [grpc.io/docs/languages/python](https://grpc.io/docs/languages/python) |
| **grpcurl** | CLI testing tool | [github.com/fullstorydev/grpcurl](https://github.com/fullstorydev/grpcurl) |

### 📖 Key Concepts

| Concept | Description |
|---------|-------------|
| **RPC** | Remote Procedure Call — calling functions on remote servers |
| **Protocol Buffers** | Binary serialisation format (smaller than JSON) |
| **Proto file** | Service and message definitions (.proto) |
| **Stub** | Generated client code for RPC calls |
| **Unary RPC** | Single request, single response |
| **Server Streaming** | Single request, multiple responses |
| **Client Streaming** | Multiple requests, single response |
| **Bidirectional** | Multiple requests AND responses (simultaneous) |

---

## ⛔ Constraints (MUST/MUST NOT)

### MUST (Mandatory)
- [ ] MUST define services in .proto files
- [ ] MUST implement at least 4 RPC methods
- [ ] MUST include at least one streaming method
- [ ] MUST handle errors with proper gRPC status codes
- [ ] MUST generate code from proto files (not handwrite)
- [ ] MUST pass all smoke tests

### MUST NOT (Forbidden)
- [ ] MUST NOT use REST/HTTP for core functionality
- [ ] MUST NOT hardcode server addresses
- [ ] MUST NOT ignore RPC errors/timeouts
- [ ] MUST NOT commit generated *_pb2.py files (regenerate)

### SHOULD (Recommended)
- [ ] SHOULD implement deadline/timeout handling
- [ ] SHOULD add interceptors for logging
- [ ] SHOULD compare performance with REST equivalent

---

## 🎯 Concept Analogies

### RPC = Phone Call vs Letter

🏠 **Real-World Analogy:**  
REST is like sending letters — you write a message, address it, send it, wait for reply. RPC is like a phone call — you connect, speak directly, get immediate response. The phone (stub) handles all the dialling complexity.

💻 **Technical Mapping:**
- Letter = HTTP request + JSON body
- Phone call = RPC invocation
- Dialling = Connection establishment + serialisation
- Speaking = Binary protocol buffer data
- Immediate response = Synchronous return value

⚠️ **Where the analogy breaks:** Phone calls are always synchronous; gRPC supports async and streaming patterns.

---

### Protocol Buffers = Standardised Forms

🏠 **Real-World Analogy:**  
Instead of writing freeform letters, you use standardised forms where everyone knows which field means what. Smaller, faster to process, no ambiguity.

💻 **Technical Mapping:**
- Form template = .proto file
- Filled form = Serialised message
- Form fields = Message fields with types
- Required fields = `required` keyword (proto2) / presence rules

---

## 🗳️ Peer Instruction Questions

### Question 1: gRPC vs REST

> 💭 **PREDICTION:** Why is gRPC faster than REST for microservices?

**Options:**
- A) Uses different transport protocol
- B) Binary serialisation (protobuf) vs text (JSON) ✓
- C) Doesn't use HTTP
- D) Has better caching

**Correct answer:** B

**Explanation:** Protocol Buffers produce smaller, faster-to-parse messages than JSON. gRPC also uses HTTP/2 which supports multiplexing. The combination makes gRPC 2-10x faster for typical payloads.

---

### Question 2: When to Use Streaming

> 💭 **PREDICTION:** When would you use server streaming RPC?

**Options:**
- A) Uploading a large file
- B) Downloading a large dataset in chunks ✓
- C) Simple CRUD operations
- D) Authentication

**Correct answer:** B

**Explanation:** Server streaming sends multiple responses for one request — ideal for large datasets, real-time updates or progress notifications. Client streaming is for uploads; unary is for simple request-response.

---

### Question 3: Proto Versioning

> 💭 **PREDICTION:** What happens if you add a required field to a proto message?

**Options:**
- A) Old clients continue working
- B) Old clients break (can't parse new messages) ✓
- C) New field is ignored
- D) Automatic migration

**Correct answer:** B

**Explanation:** Adding required fields breaks backward compatibility. Use optional fields (proto3 default) for evolution. This is why proto3 removed the `required` keyword.

---

### Question 4: Error Handling

> 💭 **PREDICTION:** How does gRPC indicate errors?

**Options:**
- A) HTTP status codes
- B) Exception throwing
- C) Status codes + details in response ✓
- D) Return null values

**Correct answer:** C

**Explanation:** gRPC uses its own status codes (NOT_FOUND, INVALID_ARGUMENT, etc.) with optional error details. These map to but aren't identical to HTTP codes.

---

## ❌ Common Misconceptions

### 🚫 "gRPC replaces REST everywhere"

**WRONG:** gRPC is always better than REST.

**CORRECT:** gRPC excels for internal microservices. REST is better for public APIs (browser compatibility, human readability, caching). Use the right tool.

---

### 🚫 "Protocol Buffers are just JSON but binary"

**WRONG:** Protobuf is binary JSON.

**CORRECT:** Protobuf requires schema (proto file), is strongly typed and supports evolution rules. It's not just a different encoding of JSON — it's a different model.

---

### 🚫 "Streaming is always better"

**WRONG:** Use streaming for everything.

**CORRECT:** Streaming adds complexity (connection management, flow control). For simple request-response, unary is simpler and sufficient.

---

## 📖 Glossary

| Term | Definition |
|------|------------|
| **RPC** | Remote Procedure Call |
| **gRPC** | Google's RPC framework using HTTP/2 + Protobuf |
| **Protocol Buffers** | Binary serialisation format |
| **Proto file** | Service/message definitions (.proto) |
| **Stub** | Generated client code |
| **Unary** | Single request → single response |
| **Streaming** | Multiple messages in one direction or both |
| **Channel** | Connection to gRPC server |
| **Metadata** | Headers/trailers for RPC calls |
| **Deadline** | Maximum time for RPC completion |

---

## 🔨 Implementation Example

**Proto file (service.proto):**
```protobuf
syntax = "proto3";

package inventory;

service InventoryService {
    // Unary - get single item
    rpc GetItem(GetItemRequest) returns (Item);
    
    // Server streaming - list all items
    rpc ListItems(ListItemsRequest) returns (stream Item);
    
    // Client streaming - batch upload
    rpc UploadItems(stream Item) returns (UploadResponse);
    
    // Bidirectional - real-time sync
    rpc SyncItems(stream SyncRequest) returns (stream SyncResponse);
}

message Item {
    string id = 1;
    string name = 2;
    int32 quantity = 3;
    double price = 4;
}

message GetItemRequest {
    string id = 1;
}

message ListItemsRequest {
    int32 page_size = 1;
    string category = 2;
}

message UploadResponse {
    int32 items_created = 1;
    int32 items_updated = 2;
}

message SyncRequest {
    string client_id = 1;
    Item item = 2;
}

message SyncResponse {
    string action = 1;
    Item item = 2;
}
```

**Server implementation:**
```python
#!/usr/bin/env python3
"""gRPC Inventory Service Server"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import grpc
from concurrent import futures
import logging
from typing import Iterator

import inventory_pb2
import inventory_pb2_grpc

# ═══════════════════════════════════════════════════════════════════════════════
# SERVICE_IMPLEMENTATION
# ═══════════════════════════════════════════════════════════════════════════════
class InventoryServicer(inventory_pb2_grpc.InventoryServiceServicer):
    """
    Inventory service implementation.
    
    # 💭 PREDICTION: Why use a dict for storage here?
    # Answer: Simple in-memory storage for demo; production would use DB
    """
    
    def __init__(self):
        self.items = {}
        self.logger = logging.getLogger(__name__)
    
    def GetItem(self, request, context) -> inventory_pb2.Item:
        """Unary RPC - get single item."""
        item_id = request.id
        
        if item_id not in self.items:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Item {item_id} not found")
            return inventory_pb2.Item()
        
        self.logger.info(f"GetItem: {item_id}")
        return self.items[item_id]
    
    def ListItems(self, request, context) -> Iterator[inventory_pb2.Item]:
        """Server streaming - list items."""
        self.logger.info(f"ListItems: page_size={request.page_size}")
        
        count = 0
        for item in self.items.values():
            if request.category and item.category != request.category:
                continue
            
            yield item
            count += 1
            
            if request.page_size and count >= request.page_size:
                break
    
    def UploadItems(self, request_iterator, context) -> inventory_pb2.UploadResponse:
        """Client streaming - batch upload."""
        created = 0
        updated = 0
        
        for item in request_iterator:
            if item.id in self.items:
                updated += 1
            else:
                created += 1
            
            self.items[item.id] = item
        
        self.logger.info(f"UploadItems: created={created}, updated={updated}")
        return inventory_pb2.UploadResponse(
            items_created=created,
            items_updated=updated
        )

# ═══════════════════════════════════════════════════════════════════════════════
# SERVER
# ═══════════════════════════════════════════════════════════════════════════════
def serve(port: int = 50051):
    """Start gRPC server."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    inventory_pb2_grpc.add_InventoryServiceServicer_to_server(
        InventoryServicer(), server
    )
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    
    logging.info(f"Server started on port {port}")
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve()
```

---

## 📋 Expected Outputs

### Scenario 1: Unary Call

```bash
grpcurl -plaintext -d '{"id": "item1"}' localhost:50051 inventory.InventoryService/GetItem
```

**Expected output:**
```json
{
  "id": "item1",
  "name": "Widget",
  "quantity": 100,
  "price": 9.99
}
```

### Scenario 2: Server Streaming

```bash
grpcurl -plaintext -d '{"page_size": 5}' localhost:50051 inventory.InventoryService/ListItems
```

**Expected output (multiple messages):**
```json
{"id": "item1", "name": "Widget", ...}
{"id": "item2", "name": "Gadget", ...}
{"id": "item3", "name": "Doohickey", ...}
```

---

## ❓ Frequently Asked Questions

**Q: How do I generate Python code from proto?**

A:
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service.proto
```

**Q: How do I test without writing a client?**

A: Use grpcurl:
```bash
# List services
grpcurl -plaintext localhost:50051 list

# Call method
grpcurl -plaintext -d '{}' localhost:50051 package.Service/Method
```

---

## 📚 Laboratory References

| Week | Folder | Relevant Content |
|------|--------|------------------|
| 12 | `12enWSL/` | RPC concepts, protobuf |
| 9 | `09enWSL/` | Application layer protocols |

---

## 📚 Bibliography

1. **[OFFICIAL]** gRPC Documentation  
   URL: https://grpc.io/docs/  
   Verified: 2026-01-24 ✓

2. **[OFFICIAL]** Protocol Buffers Language Guide  
   URL: https://protobuf.dev/programming-guides/proto3/  
   Verified: 2026-01-24 ✓

---

*Last update: January 2026 — Computer Networks, ASE Bucharest*

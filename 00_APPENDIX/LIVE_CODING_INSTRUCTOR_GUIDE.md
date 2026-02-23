# 🎬 Live Coding Guide for Instructors
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> **Version:** 2.2 — January 2025
> **New in this version:** Week 0 examples, post-session checklist, group adaptation

---

## 1. What is Live Coding?

Live coding is a teaching technique where the instructor **writes code in real time** in front of students, explaining each decision. It is fundamentally different from presenting pre-written code because:

- Students see the **thinking process**, not just the result
- Mistakes become **learning moments**
- The pace is natural and allows questions

---

## 2. Session Structure (15-20 minutess)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      LIVE CODING CYCLE                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  1. CONTEXT (2 min)                                                   │  │
│  │     "Today we'll create a simple TCP server. The goal is to          │  │
│  │      understand the order of operations: socket → bind → listen"     │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                    │                                        │
│                                    ▼                                        │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  2. STRUCTURE (2 min)                                                 │  │
│  │     Sketch on board/slide: "We'll have 4 main functions:             │  │
│  │     create_socket(), bind_to_port(), wait_for_client(), send()"      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                    │                                        │
│                                    ▼                                        │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  3. INCREMENTAL IMPLEMENTATION (10-15 min)                            │  │
│  │     ┌────────────────────────────────────────────────────────────┐   │  │
│  │     │  a) Write 2-5 lines of code                                │   │  │
│  │     │  b) ASK: "What do you think this will display?"            │   │  │
│  │     │  c) Run and verify predictions                             │   │  │
│  │     │  d) Explain the result                                     │   │  │
│  │     │  e) REPEAT                                                 │   │  │
│  │     └────────────────────────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                    │                                        │
│                                    ▼                                        │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  4. RECAP (2 min)                                                     │  │
│  │     "We created a TCP server that: creates socket, binds to port,    │  │
│  │      waits for connections and processes clients."                  │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Golden Rules

### 3.1 MAKE INTENTIONAL MISTAKES

Plan 1-2 mistakes per session:
```python
# PLANNED MISTAKE: forget to import socket
# sock = socket.socket(...)  # NameError: name 'socket' is not defined

# "Oops! What did I forget? Who can tell me?"
# After correction: "Why is it important to have imports at the top?"
```

### 3.2 CONSTANTLY ASK FOR PREDICTIONS

Before EVERY execution:
```python
print("Connected to server!")
# ASK: "What will happen if the server is not running?"
```

### 3.3 TALK WHILE YOU TYPE

```python
# "Now I'm creating a socket... using AF_INET for IPv4..."
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# "...and SOCK_STREAM for TCP"
```

### 3.4 DON'T RUSH

- Better to cover 70% of material with students understanding 90%
- Than 100% of material with students understanding 30%

### 3.5 USE COMMENTS ON THE SPOT

```python
# TODO: We'll add error handling here
# HACK: Temporarily using fixed port, ideally would be dynamic
# QUESTION: Why did we choose port 8080?
```

---

## 4. Pre-Session Checklist

### Technical
- [ ] Have I tested all code on the room's system?
- [ ] Is Docker running? Is Portainer accessible?
- [ ] Is terminal font at least 18pt?
- [ ] Have I disabled on-screen notifications?
- [ ] Do I have backup code in case something breaks?

### Pedagogical
- [ ] Have I prepared 2-3 intentional mistakes?
- [ ] Have I prepared 5-10 prediction questions?
- [ ] Have I identified concepts where students typically err?
- [ ] Do I have buffer time for questions (10% of session)?

---

## 5. Examples by Week

### Week 0: Environment Verification and Docker 🆕

```python
# LIVE CODING: Verify Docker is working

# CONTEXT (2 min)
# "Before writing network code, we need to verify the environment is OK"

# STEP 1: "Let's see if Docker responds"
import subprocess

# QUESTION: "What command checks if Docker is running?"
result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
print(f"Docker version: {result.stdout.strip()}")

# PLANNED MISTAKE: Run without sudo service docker start
# "Cannot connect to Docker daemon"
# "What do we need to do after restarting Windows?"

# STEP 2: "Let's run a simple container"
# QUESTION: "What does 'docker run --rm' do?"
result = subprocess.run(
    ['docker', 'run', '--rm', 'alpine', 'echo', 'Hello from container!'],
    capture_output=True, text=True
)
print(result.stdout)

# STEP 3: "Let's verify Portainer"
import socket

def check_port(host, port):
    """Check if a port is open."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect((host, port))
            return True
    except:
        return False

# QUESTION: "What port does Portainer listen on?"
portainer_ok = check_port('localhost', 9000)
print(f"Portainer accessible: {portainer_ok}")

# RECAP
# "We verified: Docker installed, daemon running, container functional, Portainer up"
```

### Week 0: Bytes vs Strings 🆕

```python
# LIVE CODING: The key difference for network programming

# CONTEXT (2 min)
# "The most frequent beginner bug: confusion between str and bytes"

# STEP 1: "What data type does text have?"
text = "Hello"
print(f"Type: {type(text)}")  # <class 'str'>
print(f"Length: {len(text)}")  # 5

# QUESTION: "How many characters does 'Hello' have?"

# STEP 2: "Let's convert to bytes"
encoded = text.encode('utf-8')
print(f"Type: {type(encoded)}")  # <class 'bytes'>
print(f"Value: {encoded}")  # b'Hello'
print(f"Length: {len(encoded)}")  # 5

# QUESTION: "Why is the length still 5?"

# STEP 3: "Let's try with special characters"
# PLANNED MISTAKE: Assume length is equal
text_special = "Ħello"
print(f"Characters: {len(text_special)}")        # 5
print(f"Bytes: {len(text_special.encode())}")   # 6!

# "Why 6 bytes for 5 characters?"
# → "Ħ takes 2 bytes in UTF-8!"

# STEP 4: "What happens if we send str on a socket?"
import socket
# socket_demo.send("Hello")  # TypeError!
# QUESTION: "What error do we get and why?"

# RECAP
# "str = human text, bytes = network data. ALWAYS encode() before send()!"
```

### Week 1: ping and Diagnostics

```python
# LIVE CODING: Connectivity verification script

# STEP 1: "Let's see if we can ping from Python"
import subprocess

# QUESTION: "What Linux command does ping?"
result = subprocess.run(['ping', '-c', '1', 'google.com'], capture_output=True)

# STEP 2: "What exit code means success?"
print(f"Return code: {result.returncode}")
# QUESTION: "Does 0 mean success or failure?"

# PLANNED MISTAKE: Forget -c and ping runs indefinitely
# "Oops! How do I stop this? Ctrl+C! Why did it run forever?"
```

### Week 2: TCP Socket

```python
# LIVE CODING: Simple Echo Server

# STEP 1
import socket

# STEP 2: "We create the socket"
# QUESTION: "SOCK_STREAM or SOCK_DGRAM for TCP?"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# STEP 3: "We bind to a port"
# MISTAKE: Use an occupied port (80)
# server.bind(('', 80))  # Permission denied!
# "Why doesn't it work? What ports require sudo?"

server.bind(('', 8080))
print("Bound to port 8080")

# STEP 4
server.listen(1)
# QUESTION: "What does parameter 1 in listen() do?"
```

---

## 6. Handling Questions

### Good questions (answer immediately):
- "Why do we use port 8080 and not 80?"
- "What happens if the client disconnects?"

### Questions requiring postponement:
- "How does TLS work?" → "Excelslow question! We'll cover it in Week 10."

### Off-topic questions:
- "Can we do this in Rust?" → "Interesting, but let's focus on Python now. We'll chat at break."

---

## 7. Adapting for Group Size 🆕

### Small Group (≤15 students)

| Aspect | Adaptation |
|--------|------------|
| Predictions | Ask students by name, rotation |
| Mistakes | Let students find the bug |
| Pace | Slower, more questions |
| Interaction | Students can come to the board |

### Medium Group (15-40 students)

| Aspect | Adaptation |
|--------|------------|
| Predictions | Vote by raised hand (A/B/C/D) |
| Mistakes | Offer hints, not direct solutions |
| Pace | Moderate, pauses after blocks |
| Interaction | Think-Pair-Share for problems |

### Large Group (>40 students)

| Aspect | Adaptation |
|--------|------------|
| Predictions | Use Mentimeter or chat poll |
| Mistakes | Pre-planned, less improvised |
| Pace | Faster, Q&A at end |
| Interaction | Written questions/chat |

---

## 8. Post-Session Checklist 🆕

### Immediately after session (5 min)
- [ ] Did I save the final code with added comments?
- [ ] Did I note interesting questions from the audience?
- [ ] Did I identify concepts that created confusion?
- [ ] Did I note which intentional mistakes worked well?

### Before next session
- [ ] Have I published code for students?
- [ ] Have I updatad slides with clarifications?
- [ ] Have I prepared supplementary exercises for difficult concepts?
- [ ] Have I reviewed timing (too fast / too slow)?

### Feedback to collect
- What was most useful?
- What was confusing?
- What would you like to see more of?

---

## 9. Common Session Troubleshooting 🆕

### "Code doesn't run and I don't know why"

```
1. STOP - Don't panic in front of students
2. READ - Read the error aloud
3. ASK - "What is this error telling us?"
4. FIX - Correct or turn into learning moment
5. EXPLAIN - "This is a common mistake, here's why..."
```

### "A student asks questions continuously and derails the course"

```
- "Excelslow question, but let's discuss at break to not lose the thread"
- Visibly note the question on the board
- Return to it if relevant later
```

### "Nobody answers questions"

```
1. Rephrase the question more simply
2. Offer options (A/B/C)
3. Ask "who is sure?" vs "who is guessing?"
4. Call by name (small groups)
5. Think-pair-share (30 seconds discussion between neighbours)
```

### "I've run out of time"

```
- Do NOT speed up and do NOT skip explanations
- Say: "We won't finish today, but it's important you understand well"
- Publish complete code online
- Recap at start of next session
```

---

## 10. Related Resources

- [docs/peer_instruction.md](docs/peer_instruction.md) — MCQ questions for interactive sessions
- [docs/misconceptions.md](docs/misconceptions.md) — Common errors to anticipate
- [docs/pair_programming_guide.md](docs/pair_programming_guide.md) — Guide for pair exercises
- [docs/code_tracing.md](docs/code_tracing.md) — Code tracing exercises
- *(Glossary — to be added.)*

---

*Live Coding Guide — Computer Networks*
*ASE Bucharest — CSIE*
*Version: 2.2 | January 2025*

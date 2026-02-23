# 👥 Pair Programming Guide — Week 0
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> **Purpose:** Configure the lab environment in pairs for collaborative learning

---

## What is Pair Programming?

Pair programming is a technique where **two students work together** at the same computer with distinct roles:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PAIR PROGRAMMING                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   👨‍💻 DRIVER                        👀 NAVIGATOR                           │
│   ─────────────────────          ─────────────────────────                 │
│   • Types the commands           • Verifies the steps                      │
│   • Controls the mouse           • Consults documentation                  │
│   • Focuses on immediate         • Identifies errors                       │
│     details                      • Thinks about the big                    │
│   • Executes instructions          picture                                 │
│                                  • Suggests improvements                   │
│                                                                             │
│   🔄 SWAP EVERY 10-15 MINUTES                                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Why it works:**
- Two pairs of eyes catch more errors than one
- The navigator prevents mistakes before they happen
- Both understand the configuration at the end
- Active learning through explanation and discussion

---

## Session Structure (75-90 minutess)

### Phase 1: Preparation (5 minutess)
- [ ] Both partners have access to a Windows 11 computer
- [ ] Decide who is Driver first
- [ ] Read the session objectives together
- [ ] Navigator opens the Prerequisites documentation

### Phase 2: Implementation (60-70 minutess)
- Driver types, Navigator verifies
- **Swap roles every 15 minutess** (use a timer!)
- Navigator asks "what are we doing?" before new commands
- Both confirm output before continuing

### Phase 3: Verification (10 minutess)
- [ ] Run the verification script together
- [ ] Both can access Portainer from browser
- [ ] Both understand the commands executed
- [ ] Document any problems encountered and solutions

### Phase 4: Retrospective (5 minutess)
- What went well?
- What did we learn?
- What would we do differently next time?

---

## Pair Programming Exercises for Week 0

### Exercise P1: Install WSL2 and Ubuntu
**Estimated time:** 20 minutess
**Objective:** Enable WSL2 and install Ubuntu 22.04

**Specific roles:**

| Driver | Navigator |
|--------|-----------|
| Opens PowerShell as Admin | Verifies virtualisation is enabled in Task Manager |
| Types wsl commands | Reads output and confirms success |
| Restarts when needed | Times the restart duration |

**Steps with role swapping:**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ DRIVER A (0-10 min)                                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. Open PowerShell as Adminilayeror                                         │
│ 2. Run: wsl --install                                                       │
│ 3. Wait for download                                                        │
│                                                                             │
│ 💭 PREDICTION: "How long do you think the download will take?"             │
│                                                                             │
│ NAVIGATOR: Check progress, note any errors                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🔄 SWAP ROLES                                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ DRIVER B (10-20 min)                                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. Restart the computer                                                     │
│ 5. Open Ubuntu from Start Menu                                             │
│ 6. Create user "stud" with password "stud"                                 │
│                                                                             │
│ NAVIGATOR: Verify user/pass are correct per documentation                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### Exercise P2: Install Docker in WSL
**Estimated time:** 25 minutess
**Objective:** Install and configure Docker natively in WSL2

**Steps with role swapping:**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ DRIVER A (0-12 min)                                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. sudo apt updata && sudo apt upgrade -y                                   │
│    Navigator: "How long do you estimate for updata?"                       │
│                                                                             │
│ 2. sudo apt install -y apt-transport-https ca-certificates curl            │
│    Navigator: "Check there are no red errors"                              │
│                                                                             │
│ 3. Add Docker GPG key                                                       │
│    Navigator: "Read the command aloud before pressing Enter"               │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🔄 SWAP ROLES                                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ DRIVER B (12-25 min)                                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. sudo apt install -y docker-ce docker-ce-cli containerd.io               │
│                                                                             │
│ 5. sudo usermod -aG docker $USER                                           │
│    💭 PREDICTION: "Does this work immediately or do we need logout?"       │
│                                                                             │
│ 6. newgrp docker (or logout/login)                                         │
│    Navigator: "Verify with: groups"                                        │
│                                                                             │
│ 7. docker run hello-world                                                   │
│    Navigator: "What specific message are we looking for in output?"        │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### Exercise P3: Install and Configure Portainer
**Estimated time:** 15 minutess
**Objective:** Deploy Portainer CE and configure admin

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ DRIVER A (0-8 min) — Terminal                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. docker volume create portainer_data                                      │
│    Navigator: "Verify with: docker volume ls"                              │
│                                                                             │
│ 2. docker run -d -p 9000:9000 --name portainer --restart=always \          │
│      -v /var/run/docker.sock:/var/run/docker.sock \                        │
│      -v portainer_data:/data \                                             │
│      portainer/portainer-ce:latest                                         │
│                                                                             │
│    💭 PREDICTION: "What does --restart=always do?"                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🔄 SWAP ROLES                                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ DRIVER B (8-15 min) — Browser                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. Open http://localhost:9000                                              │
│    Navigator: "Does it work? If not, check: docker ps"                     │
│                                                                             │
│ 4. Username: stud                                                          │
│    Password: studstudstud (12 characters!)                                 │
│    Navigator: "Why 12 characters? Check docs/misconceptions.md"            │
│                                                                             │
│ 5. Select "Docker" → "Connect"                                             │
│    Navigator: "Do we see the dashboard with containers?"                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Effective Communication Phrases

### Navigator to Driver:

| Situation | Recommended Phrase |
|-----------|-------------------|
| Before command | "What's the plan for this step?" |
| Syntax check | "Can you read the command aloud?" |
| Spot error | "Hold on, check line 3..." |
| Documentation | "The docs say we need to..." |
| Confusion | "I don't understand why we're doing this, can you explain?" |
| Success | "Perfect, the output is as expected!" |

### Driver to Navigator:

| Situation | Recommended Phrase |
|-----------|-------------------|
| Before Enter | "Ready to run, do you confirm?" |
| Error occurred | "I have an error, can you search troubleshooting?" |
| Acertainty | "Not sure about the syntax, can you check?" |
| Blocked | "I'm stuck, what does the documentation say?" |
| Explanation | "I'm doing this because..." |

### Phrases to Avoid:

❌ "Give me the keyboard, it's faster if I do it"
❌ "Leave it, I know"
❌ "It doesn't matter, it works anyway"
❌ "It's too slow, let's skip steps"

---

## Troubleshooting Protocol

When you encounter a problem:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ THE "5 MINUTE RULE" PROTOCOL                                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ 1. STOP (30 sec)                                                           │
│    └── Read the error message COMPLETELY, aloud                            │
│                                                                             │
│ 2. THINK (2 min)                                                           │
│    └── Driver: "What did I type?"                                          │
│    └── Navigator: "What does the error say exactly?"                       │
│                                                                             │
│ 3. SEARCH (2 min)                                                          │
│    └── Navigator searches docs/troubleshooting.md                          │
│    └── Driver checks docs/misconceptions.md                                │
│                                                                             │
│ 4. ASK (if still blocked)                                                  │
│    └── Raise your hand for the instructor                                  │
│    └── Explain WHAT you tried, not just the error                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Final Session Checklist

### Technical:
- [ ] `wsl --status` shows WSL2 as default
- [ ] `docker --version` displays version
- [ ] `docker ps` works without sudo
- [ ] Portainer accessible at http://localhost:9000
- [ ] Credentials: stud / studstudstud work

### Collaboration:
- [ ] We swapped roles at least 3 times
- [ ] Both partners typed commands
- [ ] We discussed each step before execution
- [ ] We documented errors encountered and solutions

### Learning:
- [ ] Both can explain the difference between container and image
- [ ] Both know why we use WSL2 and not Docker Desktop
- [ ] Both understand port mapping (-p 9000:9000)

---

*Pair Programming Guide — Week 0: Lab Environment Setup*
*Computer Networks — ASE Bucharest, CSIE*
*Version: January 2025*

---

## 📊 Peer Evaluation Rubric

Use this rubric for peer assessment at the end of each pair programming session.

### Evaluation Criteria

| Criterion | Excellent (3) | Good (2) | Needs Improvement (1) |
|-----------|---------------|----------|----------------------|
| **Communication** | Clear explanations, active listening, asks clarifying questions | Adequate explanations, generally listens | Minimal communication, doesn't explain thinking |
| **Role Execution** | Smooth transitions, fully engages in both Driver and Navigator roles | Some hesitation in transitions, adequate role performance | Stuck in one role, doesn't adapt |
| **Problem Solving** | Collaborative debugging, shared ownership of solutions | Some collaboration, occasional independent work | Works mostly independently, doesn't share approach |
| **Time Management** | Completed exercises within estimated time | Slight overrun (10-15 min), still finished | Significant delays, didn't complete all exercises |
| **Technical Accuracy** | Commands executed correctly, understands each step | Minor errors corrected quickly | Frequent errors, needs significant guidance |

### Scoring Guide

| Total Score | Rating | Feedback |
|-------------|--------|----------|
| 13-15 | ⭐⭐⭐ Excellent | Outstanding collaboration! Ready for advanced pair work. |
| 10-12 | ⭐⭐ Good | Solid performance. Focus on communication during next session. |
| 7-9 | ⭐ Satisfactory | Room for improvement. Review role responsibilities before next session. |
| <7 | Needs Support | Consider additional practice or instructor guidance. |

### Self-Reflection Questions

After the session, each partner should answer:

1. What did I learn from my partner today?
2. What could I have explained more clearly?
3. When did I feel most/least effective as Driver? As Navigator?
4. What will I do differently next time?

---

*Peer Evaluation Rubric added: January 2026*

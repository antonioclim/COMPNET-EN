# 🎤 Presentation Guide
## Computer Networks Projects — ASE Bucharest, CSIE

> **Purpose:** Prepare for Stage E4 — the live project presentation.  
> **Applies to:** All projects P01-P20

---

## Presentation Structure (10-15 minutes)

| Section | Time | Content |
|---------|------|---------|
| **Introduction** | 1-2 min | Project name, team, objectives |
| **Architecture** | 2-3 min | System design, components, data flow |
| **Live Demo** | 4-5 min | Working functionality demonstration |
| **Challenges** | 1-2 min | Problems encountered and solutions |
| **Conclusions** | 1 min | What you learned, potential improvements |
| **Q&A** | 2-3 min | Answer committee questions |

---

## Before the Presentation

### One Week Before

```
□ Code is complete and tested
□ Documentation is finalised
□ Repository has v1.0-final tag
□ Demo environment works on a clean machine
□ Presentation slides ready (if using)
```

### One Day Before

```
□ Test demo on the actual presentation machine (if possible)
□ Prepare backup: screenshots/video if demo fails
□ Review all code — you may be asked about any line
□ Prepare answers for expected questions
□ Check Docker images are pulled and ready
```

### 30 Minutes Before

```
□ Arrive early to set up
□ Start Docker containers
□ Open relevant terminal windows
□ Have documentation ready to show
□ Take a deep breath — you know this project
```

---

## Live Demo Checklist

### Demo Flow Template

```markdown
1. Show the starting state
   "Here we have [X containers/services] running..."

2. Perform the main action
   "Now I will [send a packet/start a connection/trigger event]..."

3. Show the result
   "As you can see, [expected behaviour happened]..."

4. Explain what happened
   "This worked because [brief technical explanation]..."

5. Show logs/evidence
   "We can verify this in the logs/Wireshark/Portainer..."
```

### Demo Recovery Plan

| Problem | Solution |
|---------|----------|
| Container won't start | Have `docker-compose logs` ready, explain the error |
| Network timeout | Show that it works in screenshots, explain likely cause |
| Unexpected error | Stay calm, explain what should happen, show code |
| Complete failure | Switch to recorded video backup |

### Commands to Have Ready

```bash
# Check everything is running
docker ps

# View logs if something fails
docker-compose logs -f [service]

# Restart if needed
docker-compose down && docker-compose up -d

# Quick network test
docker exec [container] ping [target]
```

---

## What NOT to Do

| Mistake | Why it's bad | Instead |
|---------|--------------|---------|
| Read from slides | Shows lack of understanding | Talk naturally, use slides as prompts |
| Say "I don't know" immediately | Misses opportunity to reason | Say "Let me think about that..." |
| Blame team members | Unprofessional | Take collective responsibility |
| Panic when demo fails | Makes it worse | Have backup ready, explain calmly |
| Go over time | Disrespectful to others | Practice with timer, cut if needed |
| Use too much jargon | May not communicate clearly | Explain technical terms briefly |

---

## Answering Questions

### Question Types and Strategies

**Conceptual questions:** "Why did you choose X over Y?"
- Explain your reasoning
- Mention trade-offs you considered
- Be honest if you would do it differently now

**Technical questions:** "How does the X component work?"
- Start with high-level explanation
- Go into detail if asked
- Refer to code if helpful

**Debugging questions:** "What would happen if X failed?"
- Think through the scenario out loud
- Explain error handling mechanisms
- Admit if you haven't tested that case

**Extension questions:** "How would you add feature X?"
- Show you understand the architecture
- Propose a reasonable approach
- Mention potential challenges

### Useful Phrases

| Situation | What to say |
|-----------|-------------|
| Need time to think | "That's a good question. Let me think..." |
| Don't know the answer | "I'm not certain, but I believe... I would need to verify." |
| Question is unclear | "Could you clarify what you mean by X?" |
| Answer is complex | "There are several aspects to this. First..." |
| Made a mistake in project | "In hindsight, we would have done X differently because..." |

---

## Team Presentations

### Dividing the Presentation

| Member | Sections | Responsibilities |
|--------|----------|------------------|
| Member 1 | Intro + Architecture | Also: setup demo environment |
| Member 2 | Live Demo | Also: backup screenshots ready |
| Member 3 | Challenges + Conclusions | Also: documentation for reference |

### Handoff Protocol

```
Member 1: "...and that covers the architecture. [Name] will now 
          demonstrate the system in action."

Member 2: "Thank you. As [Name] explained, we have three services.
          Let me show you how they interact..."
```

### Everyone Must Know Everything

Even if you presented only one section:
- You may be asked about ANY part of the project
- "I didn't work on that part" is NOT acceptable
- Review all code together before the presentation

---

## Slide Guidelines (If Using)

### Content per Slide

| Slide Type | Max Content |
|------------|-------------|
| Title | Project name, team names, date |
| Architecture | One diagram, minimal text |
| Code | Max 15 lines, highlighted key parts |
| Results | Screenshots or metrics |
| Bullets | Max 5 points, max 7 words each |

### Slide Don'ts

```
✗ Full paragraphs of text
✗ Code that's too small to read
✗ Animations that slow you down
✗ More than 8-10 slides total
✗ Reading slides word for word
```

---

## Evaluation Criteria Reminder

From the project rubric (Stage E4 — 100 points):

| Criterion | Points | What evaluators look for |
|-----------|--------|--------------------------|
| Demo live functional | 35 | System works as specified |
| Technical Presentation | 25 | Clear explanation of architecture |
| Answers to Questions | 20 | Deep understanding demonstrated |
| Team Contribution | 15 | All members know the project |
| Respectare timp | 5 | Stay within 10-15 minutes |

---

## Practice Checklist

### Solo Practice (each team member)

```
□ Can explain the entire architecture in 2 minutes
□ Can run the demo without notes
□ Can answer: "What does [any function] do?"
□ Can answer: "Why did you choose [any technology]?"
□ Can recover from common errors
```

### Team Practice

```
□ Full run-through with timer
□ Practice handoffs between speakers
□ Practice Q&A with mock questions
□ Test demo on a different computer
□ Record and review yourselves
```

---

## Sample Mock Questions

Test yourself with these before the presentation:

**General:**
1. Explain your project in one sentence.
2. What was the hardest part of this project?
3. What would you do differently if starting over?

**Technical:**
4. Walk me through what happens when [main action].
5. How do your containers communicate with each other?
6. What happens if [component X] fails?

**Code-specific:**
7. Explain this function. (points at random function)
8. Why did you use [library/pattern] here?
9. How would you test this component?

**Extensions:**
10. How would you scale this to handle 1000 users?
11. What security improvements would you add?
12. How would you add [related feature]?

---

## Emergency Contacts

If you have issues before the presentation:
- Check the troubleshooting guide: `docs/common/troubleshooting_common.md`
- Contact your team members
- Arrive early to ask the instructor

---

*Presentation Guide v1.0 — Computer Networks, ASE Bucharest*

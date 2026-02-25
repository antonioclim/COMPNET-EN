### Scenario: Encoding pitfall (UTF-8 vs header charset)

### Objective
- Demonstrate that text rendering depends on the declared charset
- Show a typical error: body encoded as UTF-8, but the header declares a different charset

### Requirements
- python3
- curl

### How to run
- ./run.sh

### Tests with curl
1) Correct response (UTF-8 declared properly)
- curl -i http://127.0.0.1:8090/ok

2) Incorrect response (body is UTF-8, header declares ISO-8859-1)
- curl -i http://127.0.0.1:8090/bad

3) Inspect the raw bytes (optional)
- curl -s http://127.0.0.1:8090/ok | xxd | head
- curl -s http://127.0.0.1:8090/bad | xxd | head

### What to observe
- The body is identical (UTF-8)
- Only the charset in the header differs
- A browser might render the characters incorrectly for the /bad endpoint

## Files

| Name | Lines |
|------|-------|
| `run.sh` | 5 |
| `server.py` | 43 |

## Cross-References

Parent lecture: [`C09/ — Session and Presentation Layer`](../../)
  
Lecture slides: [`c9-session-presentation.md`](../../c9-session-presentation.md)
  
Quiz: [`W09`](../../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W09_Questions.md)

## Selective Clone

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 03_LECTURES/C09/assets/scenario-encoding-utf8
```

**Method B — Direct download**

Browse at: `https://github.com/antonioclim/COMPNET-EN/tree/main/03_LECTURES/C09/assets/scenario-encoding-utf8`

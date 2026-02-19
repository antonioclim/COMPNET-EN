### Introductory tasks — DNS and SSH

This file contains the first set of exercises that should be completed before moving to the container-based parts.

---

### 1. Test DNS resolution

Run the following commands:

```bash
dig example.com
dig A example.com
dig @1.1.1.1 example.com
dig google.com
```

Save the output in a file named:

```text
seminar10_intro_dns_output.txt
```

**What to comment on in the file:**

- what is the difference between `dig example.com` and `dig A example.com`?
- what does the **ANSWER SECTION** represent?
- what does **TTL** represent?

---

### 2. Test an SSH session (if you have access to a lab server)

If you have an accessible server, run:

```bash
ssh USER@HOST "uname -a"
ssh USER@HOST "ls -l /"
```

If you do not have access, use this example:

```bash
# (simulation)
ssh test@fakehost "uname -a"
```

and explain **what you would expect to obtain** if the host existed.

Save your notes in:

```text
seminar10_intro_ssh_output.txt
```

---

### 3. Prepare for the container-based parts

Make sure that:

- `docker --version` works
- `docker compose version` works

Save the output of the two commands in:

```text
seminar10_docker_check.txt
```

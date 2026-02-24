import json
import paramiko

def run_cmd(ssh, cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode()
    err = stderr.read().decode()
    return out, err

def main():
    with open("plan.json", "r", encoding="utf-8") as f:
        plan = json.load(f)

    for h in plan["hosts"]:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(
            hostname=h["host"],
            port=h.get("port", 22),
            username=h["user"],
            password=h.get("password")
        )

        print("connected to", h["host"])

        for cmd in h.get("commands", []):
            out, err = run_cmd(ssh, cmd)
            if out.strip():
                print("[out]", out.strip())
            if err.strip():
                print("[err]", err.strip())

        sftp = ssh.open_sftp()
        for fobj in h.get("files", []):
            print("upload", fobj["src"], "->", fobj["dst"])
            sftp.put(fobj["src"], fobj["dst"])
        sftp.close()

        out, _ = run_cmd(ssh, "ls -la ~/site && cat ~/site/status.txt")
        print(out)

        ssh.close()

if __name__ == "__main__":
    main()

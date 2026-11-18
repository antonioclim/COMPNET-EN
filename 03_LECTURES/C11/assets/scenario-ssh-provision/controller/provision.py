import json
from concurrent.futures import ThreadPoolExecutor
import paramiko

def run_cmd(ssh, cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdin.close()
    with ThreadPoolExecutor(max_workers=2) as pool:
        out_future = pool.submit(stdout.read)
        err_future = pool.submit(stderr.read)
        out = out_future.result().decode(errors="replace")
        err = err_future.result().decode(errors="replace")
    status = stdout.channel.recv_exit_status()
    if status != 0:
        raise RuntimeError(f"Remote command failed (exit {status}): {cmd}\n{err}")
    return out, err

def main():
    with open("plan.json", "r", encoding="utf-8") as f:
        plan = json.load(f)

    for h in plan["hosts"]:
        ssh = paramiko.SSHClient()
        try:
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

            with ssh.open_sftp() as sftp:
                for fobj in h.get("files", []):
                    print("upload", fobj["src"], "->", fobj["dst"])
                    sftp.put(fobj["src"], fobj["dst"])

            out, _ = run_cmd(ssh, "ls -la ~/site && cat ~/site/status.txt")
            print(out)

        finally:
            ssh.close()

if __name__ == "__main__":
    main()

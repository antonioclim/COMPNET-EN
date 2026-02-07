import paramiko
import os

HOST = "ssh-server"    # numele serviciului Docker
PORT = 22
USERNAME = "labuser"
PASSWORD = "labpass"

OUTPUT_FILE = "ssh_output.txt"

def main():
    print("[+] Connecting via SSH...")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(
        hostname=HOST,
        port=PORT,
        username=USERNAME,
        password=PASSWORD
    )

    print("[+] Connected!")

    # --------------------------
    # 1. Execuție comandă remote
    # --------------------------

    # TODO 1: modificați comanda cu ceva util: ex "uname -a" sau "ls -l /home/labuser"
    stdin, stdout, stderr = client.exec_command("uname -a")
    result = stdout.read().decode()

    with open(OUTPUT_FILE, "w") as f:
        f.write("=== Remote command output ===\n")
        f.write(result + "\n")

    print("[+] Remote command executed. Output saved.")

    # --------------------------
    # 2. Transfer fișier: upload
    # --------------------------

    print("[+] Starting SFTP session...")
    sftp = client.open_sftp()

    # Creăm un fișier local de upload
    with open("local_upload_file.txt", "w") as f:
        f.write("Acesta este un fișier upload-at prin SFTP.\n")

    remote_path = "/home/labuser/storage/uploaded_from_client.txt"

    # TODO 2: realizați upload-ul fișierului
    sftp.put("local_upload_file.txt", remote_path)

    print("[+] Upload completed.")

    # --------------------------
    # 3. Transfer fișier: download
    # --------------------------

    remote_file_to_download = "/etc/hostname"
    local_download_path = "downloaded_hostname.txt"

    # TODO 3: download
    sftp.get(remote_file_to_download, local_download_path)

    print("[+] Download completed.")

    sftp.close()
    client.close()

    print("[+] All SSH operations completed successfully.")

if __name__ == "__main__":
    main()
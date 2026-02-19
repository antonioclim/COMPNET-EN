import paramiko
import os

HOST = "ssh-server"    # Docker service name
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
    # 1. Remote command execution
    # --------------------------

    # TODO 1: change the command to something useful, e.g. "uname -a" or "ls -l /home/labuser"
    stdin, stdout, stderr = client.exec_command("uname -a")
    result = stdout.read().decode()

    with open(OUTPUT_FILE, "w") as f:
        f.write("=== Remote command output ===\n")
        f.write(result + "\n")

    print("[+] Remote command executed. Output saved.")

    # --------------------------
    # 2. File transfer: upload
    # --------------------------

    print("[+] Starting SFTP session...")
    sftp = client.open_sftp()

    # Create a local file to upload
    with open("local_upload_file.txt", "w") as f:
        f.write("This file was uploaded via SFTP.\n")

    remote_path = "/home/labuser/storage/uploaded_from_client.txt"

    # TODO 2: perform the file upload
    sftp.put("local_upload_file.txt", remote_path)

    print("[+] Upload completed.")

    # --------------------------
    # 3. File transfer: download
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

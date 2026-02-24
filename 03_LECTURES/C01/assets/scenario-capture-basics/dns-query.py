import socket

def main():
    # Simple query (we do not implement DNS here)
    # We merely force a resolution to generate DNS traffic on the system
    host = "example.com"
    print("Resolving:", host)
    ip = socket.gethostbyname(host)
    print("Result:", ip)

if __name__ == "__main__":
    main()

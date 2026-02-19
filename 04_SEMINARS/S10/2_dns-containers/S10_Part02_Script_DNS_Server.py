from dnslib import DNSRecord, RR, QTYPE, A
import socket

LISTEN_IP = "0.0.0.0"
LISTEN_PORT = 5353

TARGET_NAME = "myservice.lab.local."
TARGET_IP = "10.10.10.10"

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((LISTEN_IP, LISTEN_PORT))
    print(f"[DNS] Listening on UDP {LISTEN_PORT}")

    while True:
        data, addr = sock.recvfrom(1024)
        request = DNSRecord.parse(data)

        qname = str(request.q.qname)
        qtype = QTYPE[request.q.qtype]

        print(f"[DNS] Query: {qname} ({qtype}) from {addr}")

        reply = request.reply()

        if qname == TARGET_NAME:
            reply.add_answer(
                RR(
                    rname=qname,
                    rtype=QTYPE.A,
                    rclass=1,
                    ttl=30,
                    rdata=A(TARGET_IP)
                )
            )
        else:
            # valid response with no records
            pass

        sock.sendto(reply.pack(), addr)

if __name__ == "__main__":
    main()


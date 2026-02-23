FROM debian:stable-slim

RUN apt-get update && apt-get install -y openssh-server && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /run/sshd

# user
RUN useradd -m student && echo "student:student" | chpasswd
RUN mkdir -p /home/student/.ssh && chown -R student:student /home/student/.ssh && chmod 700 /home/student/.ssh

# allow password for lab simplicity (you can switch to keys later)
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]

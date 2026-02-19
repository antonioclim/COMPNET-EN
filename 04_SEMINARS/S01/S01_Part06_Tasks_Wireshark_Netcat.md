### Student task

Complete the following scenario and generate an evidence file:

1. Configure a capture filter to capture only TCP traffic to port **9300**.
2. Start a TCP netcat server on port 9300 and connect a client.
3. Send three different messages.
4. Stop the capture and apply a display filter to isolate the TCP stream.
5. Repeat the process with UDP on port **9301**, using separate capture and display filters.
6. Identify in the captures:

   * the TCP handshake,
   * a packet that contains payload,
   * a UDP packet.

**Required evidence**  
Create the file `wireshark_activity_output.zip`, which must contain:

* screenshots of the filters used (capture and display),
* screenshots of the identified packets,
* a short explanation (5–7 sentences) of the differences observed between TCP and UDP traffic in the capture.

This file will be uploaded later as proof of completion.

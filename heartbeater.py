from pymavlink.dialects.v20 import common as mavlink
import socket
import time

# Define the TCP connection details
TCP_IP = "127.0.0.1"  # Replace with your target IP address
TCP_PORT = 5762      # Replace with your target port

# Create a MAVLink instance
mav = mavlink.MAVLink(file=None, srcSystem=7, srcComponent=192)


# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))
print(f"Connected to {TCP_IP}:{TCP_PORT}")

try:
    while True:
        # Create a heartbeat message
        heartbeat_msg = mav.heartbeat_encode(
            type=mavlink.MAV_TYPE_GCS,       # System type (GCS in this case)
            autopilot=mavlink.MAV_AUTOPILOT_INVALID,  # No autopilot
            base_mode=0,                    # Base mode (e.g., standby)
            custom_mode=0,                  # Custom mode (0 if not used)
            system_status=mavlink.MAV_STATE_STANDBY,  # System is in standby mode
            mavlink_version=3               # MAVLink version
        )

        # Pack the message into bytes
        msg = heartbeat_msg.pack(mav)

        # Send the message over TCP
        sock.sendall(msg)
        print("Heartbeat message sent")

        # Wait for 1 second (standard heartbeat interval)
        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopping heartbeat sender...")

finally:
    sock.close()
    print("Connection closed.")

import socket
import threading
import datetime
import os

# --- Configuration ---
# LHOST: Local IP to listen on. '0.0.0.0' means listen on all available interfaces.
LHOST = '0.0.0.0'
# LPORT: Port to listen on. Port 23 is commonly used for Telnet.
LPORT = 23 
# FAKE_BANNER: The message sent back to the client upon connection.
FAKE_BANNER = 'Welcome to the secure server.\nLogin: '
# LOG_FILE: File to save the connection attempts.
LOG_FILE = 'honeypot_log.txt'
# --- End Configuration ---

def log_activity(ip, port, data=None):
    """Logs the connection and any received data to the log file."""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] CONNECTION from {ip}:{port}"
    if data:
        # Convert received bytes data to a readable string
        data_str = data.decode('utf-8', 'ignore').strip()
        log_message += f" | DATA: '{data_str}'"
    
    # Print to console and append to log file
    print(log_message)
    with open(LOG_FILE, 'a') as f:
        f.write(log_message + '\n')

def handle_connection(client_socket, addr):
    """Handles interaction with a connected client."""
    client_ip, client_port = addr
    
    # 1. Log the initial connection attempt
    log_activity(client_ip, client_port)
    
    try:
        # 2. Send the fake banner to the client
        client_socket.sendall(FAKE_BANNER.encode('utf-8'))
        
        # 3. Wait to receive data (e.g., a username/password attempt)
        # We only wait for a small amount of data (1024 bytes)
        data = client_socket.recv(1024)
        if data:
            # 4. Log the received data
            log_activity(client_ip, client_port, data)
            
    except Exception as e:
        # Log any errors during interaction
        log_activity(client_ip, client_port, data=f"Error: {e}")
        
    finally:
        # 5. Close the connection
        client_socket.close()

def start_honeypot():
    """Sets up the main listening socket and starts the honeypot."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allows immediate reuse of the port
    
    try:
        server.bind((LHOST, LPORT))
    except Exception as e:
        print(f"!!! Error binding socket: {e}")
        print(f"!!! Port {LPORT} may already be in use or you need administrative privileges (try 'sudo' on Linux/macOS).")
        return

    server.listen(5) # Max backlog of connections
    
    print(f"[*] Simple Honeypot listening on {LHOST}:{LPORT}")
    print(f"[*] Activity will be logged to {os.path.abspath(LOG_FILE)}")
    
    # The main loop that listens for new connections forever
    while True:
        try:
            # When a client connects, accept the connection
            client_sock, addr = server.accept()
            # Start a new thread to handle the client so the main loop can listen for others
            client_handler = threading.Thread(target=handle_connection, args=(client_sock, addr))
            client_handler.start()
        except KeyboardInterrupt:
            print("\n[*] Honeypot shutting down...")
            server.close()
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    start_honeypot()
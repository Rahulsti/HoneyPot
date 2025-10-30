import socket
import threading
import datetime
import os
import re

# --- Configuration ---
# LHOST: Local IP to listen on. '0.0.0.0' means listen on all available interfaces.
LHOST = '0.0.0.0'
# LPORT: Port to listen on. Port 23 is commonly used for Telnet.
LPORT = 8080 
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

# --- Configuration (Change LPORT in Step B) ---
LHOST = '0.0.0.0'
LPORT = 8080 # We'll change this in the next step
FAKE_BANNER = 'Welcome to the secure server.\nLogin: '
LOG_FILE = 'honeypot_log.txt'
# --- End Configuration ---

def handle_connection(client_socket, addr):
    """Handles interaction with a connected client by looping for commands."""
    client_ip, client_port = addr
    
    # 1. Log the initial connection attempt
    log_activity(client_ip, client_port)
    
    try:
        # Send the fake banner
        client_socket.sendall(FAKE_BANNER.encode('utf-8'))

        # Start the interactive loop
        while True:
            # Send a prompt to the "attacker"
            prompt = b'Command: '
            client_socket.sendall(prompt)
            
            # Wait to receive data
            data = client_socket.recv(1024)
            if not data:
                # Client disconnected gracefully
                break

            # Decode the data and log it
            data_str = data.decode('utf-8', 'ignore').strip()
            log_activity(client_ip, client_port, data)

            # Check for a user-quit command (for clean exit)
            if data_str.lower() in ('quit', 'exit'):
                client_socket.sendall(b'Goodbye.\n')
                break

            # Send a fake response for any command received
            fake_response = f"Command not recognized: '{data_str}'. Try 'help' or 'quit'.\n"
            client_socket.sendall(fake_response.encode('utf-8'))

    except Exception as e:
        # Log any errors during interaction
        log_activity(client_ip, client_port, data=f"Error: {e}")
        
    finally:
        # Close the connection
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

def analyze_logs(log_file):
    """Reads the log file and counts the frequency of commands sent."""
    print("\n\n--- Honeypot Log Analysis ---")
    
    if not os.path.exists(log_file):
        print(f"Error: Log file '{log_file}' not found.")
        return

    command_counts = {}
    total_connections = 0

    with open(log_file, 'r') as f:
        for line in f:
            # 1. Count Total Connections
            if "CONNECTION from" in line and not " | DATA:" in line:
                total_connections += 1
            
            # 2. Extract and Count Commands
            # Use regex to look for the ' | DATA:' part and capture the command inside quotes
            match = re.search(r" \| DATA: '(.*?)'", line)
            if match:
                # Clean up the command: remove surrounding quotes and newline characters
                command = match.group(1).strip().lower()
                
                # Check if it was an initial login attempt (before the "Command: " prompt)
                # By default, we'll assume any input is a 'command' for counting purposes.

                if command:
                    # Increment the count for this specific command
                    command_counts[command] = command_counts.get(command, 0) + 1

    print(f"Total Connections Logged: {total_connections}")

    # Sort the commands by frequency (most common first)
    sorted_commands = sorted(command_counts.items(), key=lambda item: item[1], reverse=True)

    print("\n--- Top 10 Collected Commands/Inputs ---")
    if not sorted_commands:
        print("No command data collected yet.")
    else:
        for i, (command, count) in enumerate(sorted_commands[:10]):
            # Use 'repr' for commands to show non-printable characters like newlines (\n)
            print(f"  {i+1}. '{repr(command)}' : {count} times")

    print("--------------------------------------")

if __name__ == '__main__':
    # start_honeypot()  # <--- COMMENTED
    analyze_logs(LOG_FILE) # <--- UNCOMMENTED

import re # Add this import at the very top with the others

# ... (Existing code for LHOST, LPORT, start_honeypot, etc.)


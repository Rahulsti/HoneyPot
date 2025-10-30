# Simple Honeypot Simulation (Threat Intelligence) 🎣

A **low-interaction honeypot** built in Python to simulate an accessible network service. Its purpose is to act as a decoy, divert automated attack traffic, and passively collect **Threat Intelligence (TI)** on attacker TTPs (Tactics, Techniques, and Procedures).

## 💡 Project Goal

To demonstrate foundational knowledge in **network programming**, **security deception**, and the process of generating actionable security data from malicious network activity.

## ✨ Features

* **Network Deception:** Simulates a network service (e.g., Telnet on port 23 or a custom service on port 8080) using Python's `socket` library.
* **High-Fidelity Logging:** Captures the source **IP address**, **timestamp**, and **every piece of data** sent by the connecting client (simulated brute-force usernames/passwords, attempted commands).
* **Log Analysis Utility:** Includes a custom script to parse the raw log file and rank attack attempts by frequency.
* **Safe Execution:** Designed for low interaction to prevent lateral movement or compromise of the host system.

## ⚙️ Technical Skills Demonstrated

* **Network Programming:** Mastery of TCP socket creation, binding, listening, and threading (`socket` and `threading` modules).
* **Security Principles:** Understanding of **Deception**, **Isolation**, and the difference between low-interaction vs. high-interaction honeypots.
* **Threat Intelligence:** Ability to generate, structure, and analyze raw attack data to prioritize defensive measures.
* **File I/O and Regex:** Used Python's `os` and `re` modules for robust, accurate log file parsing.

## 🚀 Installation and Usage

### Prerequisites

* Python 3.x installed.
* Run in an **isolated environment** (Virtual Machine) for real-world testing.

### Running the Honeypot (Listening Mode)

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/Rahulsti/HoneyPot.git](https://github.com/Rahulsti/HoneyPot.git)
    cd HoneyPot
    ```
2.  **Run the script:** The script is configured to listen on a high port (e.g., 8080) by default to avoid permission issues.
    ```bash
    python honeypot.py
    # Output: [*] Simple Honeypot listening on 0.0.0.0:8080
    ```
3.  **Monitor:** All successful connections and captured inputs are saved to `honeypot_log.txt`.

### Running the Analysis (Reporting Mode)

1.  **Stop the listening script** (if running) by pressing **Ctrl+C**.
2.  **Edit `honeypot.py`:** At the bottom, comment out `start_honeypot()` and uncomment `analyze_logs(LOG_FILE)`.
3.  **Run the script again:**
    ```bash
    python honeypot.py
    # Output: Displays ranked list of most common captured commands/inputs.
    ```

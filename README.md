# HoneyPot – Low-Interaction Honeypot in Python

A lightweight honeypot that pretends to be a login service, lures automated attackers and bots, and records everything they try. A built-in analyser then ranks the most common inputs, turning raw attack traffic into simple threat intelligence.

## How it works

1. A TCP server listens on `0.0.0.0:8080` (configurable) and accepts any connection.
2. Each attacker gets a fake banner (`Welcome to the secure server. Login:`) and a `Command:` prompt.
3. Every connection and every line typed is timestamped with the source IP and port and written to `honeypot_log.txt`.
4. Each connection runs in its own thread, so several attackers can be logged at the same time.
5. Nothing is ever executed. Every command gets a harmless "not recognized" reply, so the host stays safe.

## Features

- Fake service banner and interactive prompt to keep bots engaged
- Multi-threaded connection handling (`socket` + `threading`)
- Timestamped logging of source IP, port and every input received
- Log analyser that counts connections and lists the top 10 most-tried commands or credentials (regex parsing)
- Clean shutdown with `Ctrl+C`

## Tech stack

Python 3 standard library only: `socket`, `threading`, `datetime`, `re`, `os`. No external packages.

## Running it

```bash
git clone https://github.com/Rahulsti/HoneyPot.git
cd HoneyPot
python3 honeypot.py
```

Output:

```
[*] Simple Honeypot listening on 0.0.0.0:8080
[*] Activity will be logged to /path/to/honeypot_log.txt
```

Test it from another terminal:

```bash
nc localhost 8080
```

### Analysing the logs

Stop the honeypot with `Ctrl+C`. At the bottom of `honeypot.py`, comment out `start_honeypot()` and uncomment `analyze_logs(LOG_FILE)`, then run the script again. It prints the total number of connections and the top 10 inputs.

## Configuration

Edit the values at the top of `honeypot.py`:

| Setting | Default | Meaning |
| --- | --- | --- |
| `LHOST` | `0.0.0.0` | Interface to listen on |
| `LPORT` | `8080` | Port to listen on (ports below 1024, e.g. 23 for Telnet, need sudo) |
| `FAKE_BANNER` | `Welcome to the secure server.` | Text shown to the attacker |
| `LOG_FILE` | `honeypot_log.txt` | Where activity is recorded |

## Safety note

Run it only in an isolated environment, such as a VM or a lab network. It is a learning project, not a production honeypot.

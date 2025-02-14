import os
import time
import threading
import requests

# Coba import pyfiglet dan termcolor, jika tidak ada maka install otomatis
try:
    import pyfiglet
    from termcolor import colored
except ImportError:
    os.system("pip install pyfiglet termcolor")
    import pyfiglet
    from termcolor import colored

# Menampilkan Banner "PEMPEK LAHAT" dengan warna biru
text = "PEMPEK LAHAT"
ascii_art = pyfiglet.figlet_format(text, font="rectangles")
print(colored(ascii_art, "blue"))

# URL API Silent Protocol
position_url = "https://ceremony-backend.silentprotocol.org/ceremony/position"
ping_url = "https://ceremony-backend.silentprotocol.org/ceremony/ping"
token_file = "tokens.txt"

# Fungsi untuk memuat token dari file
def load_tokens():
    try:
        with open(token_file, "r") as file:
            tokens = [line.strip() for line in file if line.strip()]
            print(f"{len(tokens)} tokens loaded.")
            return tokens
    except Exception as e:
        print(f"Error loading tokens: {e}")
        return []

# Fungsi untuk membuat headers HTTP
def get_headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }

# Fungsi untuk mendapatkan posisi token dalam antrean
def get_position(token):
    try:
        response = requests.get(position_url, headers=get_headers(token))
        if response.status_code == 200:
            data = response.json()
            print(f"[Token {token[:6]}...] Position: Behind {data['behind']}, Time Remaining: {data['timeRemaining']}")
            return data
        print(f"[Token {token[:6]}...] Failed to fetch position. Status: {response.status_code}")
    except Exception as e:
        print(f"[Token {token[:6]}...] Error fetching position: {e}")

# Fungsi untuk mengirim ping ke server
def ping_server(token):
    try:
        response = requests.get(ping_url, headers=get_headers(token))
        if response.status_code == 200:
            data = response.json()
            print(f"[Token {token[:6]}...] Ping Status: {data}")
            return data
        print(f"[Token {token[:6]}...] Failed to ping. Status: {response.status_code}")
    except Exception as e:
        print(f"[Token {token[:6]}...] Error pinging: {e}")

# Fungsi utama untuk menjalankan proses otomatis
def run_automation(token):
    while True:
        get_position(token)
        ping_server(token)
        time.sleep(10)

# Fungsi utama untuk menjalankan semua token dalam thread
def main():
    tokens = load_tokens()
    if not tokens:
        print("No tokens available. Exiting.")
        return
    
    threads = []
    for token in tokens:
        thread = threading.Thread(target=run_automation, args=(token,))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
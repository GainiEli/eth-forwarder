import subprocess
import threading
import time

def run_eth():
    while True:
        print("[ETH] Starting...")
        proc = subprocess.run(["python3", "main.py"])
        print(f"[ETH] Exited (code {proc.returncode}), restarting in 5s...")
        time.sleep(5)

def run_tron():
    while True:
        print("[TRX] Starting...")
        proc = subprocess.run(["python3", "main_tron.py"])
        print(f"[TRX] Exited (code {proc.returncode}), restarting in 5s...")
        time.sleep(5)

if __name__ == "__main__":
    eth_thread = threading.Thread(target=run_eth, daemon=True)
    tron_thread = threading.Thread(target=run_tron, daemon=True)

    eth_thread.start()
    tron_thread.start()

    eth_thread.join()
    tron_thread.join()

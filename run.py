import subprocess
import threading
import time

def run_script(name, script):
    while True:
        print(f"[{name}] Starting...")
        proc = subprocess.run(["python3", script])
        print(f"[{name}] Exited (code {proc.returncode}), restarting in 5s...")
        time.sleep(5)

if __name__ == "__main__":
    scripts = [
        ("ETH",      "main.py"),
        ("Optimism", "main_optimism.py"),
        ("BNB",      "main_bnb.py"),
        ("TRX",      "main_tron.py"),
        ("Solana",   "main_solana.py"),
    ]

    threads = [threading.Thread(target=run_script, args=(name, script), daemon=True)
               for name, script in scripts]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

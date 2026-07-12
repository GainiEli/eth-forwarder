from tronpy import Tron
from tronpy.keys import PrivateKey
import time
import os

# ================== YOUR SETTINGS ==================
SOURCE_ADDRESS = "TLTwz7xyLbZvacqUSccqAQ9PG7VAmSHC9c"
DESTINATION_ADDRESS = "TDf3hyhF2173YPTB4E5NAcAS5gzuJeMaav"
TRON_PRIVATE_KEY = os.environ['TRON_PRIVATE_KEY']  # Do NOT put key here - use Secrets

client = Tron()  # Mainnet

print("✅ TRX Auto-Forwarder Started...")

last_balance = client.get_account_balance(SOURCE_ADDRESS)

while True:
    try:
        current_balance = client.get_account_balance(SOURCE_ADDRESS)

        # Only forward if meaningful amount received (~0.5 TRX threshold)
        if current_balance > last_balance + 0.5:
            print(f"💰 New TRX detected! Forwarding...")

            fee_reserve = 2  # Reserve 2 TRX for transaction fee
            amount_to_send = current_balance - fee_reserve

            if amount_to_send > 0:
                priv_key = PrivateKey(bytes.fromhex(TRON_PRIVATE_KEY))

                txn = (
                    client.trx.transfer(SOURCE_ADDRESS, DESTINATION_ADDRESS, int(amount_to_send * 1_000_000))
                    .memo("Auto-forward")
                    .build()
                    .sign(priv_key)
                )

                result = txn.broadcast().wait()
                print(f"✅ Forwarded! Tx: {result['id']}")

        last_balance = current_balance

    except Exception as e:
        print(f"Error: {e}")

    time.sleep(0.5)  # Check every 0.5 seconds

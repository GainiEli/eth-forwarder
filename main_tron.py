from tronpy import Tron
from tronpy.keys import PrivateKey
import time
import os

# ================== YOUR SETTINGS ==================
SOURCE_ADDRESS = "TLTwz7xyLbZvacqUSccqAQ9PG7VAmSHC9c"
DESTINATION_ADDRESS = "TDf3hyhF2173YPTB4E5NAcAS5gzuJeMaav"
TRON_PRIVATE_KEY = os.environ['TRON_PRIVATE_KEY']

client = Tron()

print("✅ TRX Auto-Forwarder Started...")

last_balance = 0

while True:
    try:
        current_balance = client.get_account_balance(SOURCE_ADDRESS)

        if last_balance == 0:
            last_balance = current_balance

        # Only forward if meaningful amount received (~0.5 TRX threshold)
        if current_balance > last_balance + 0.5:
            print(f"💰 New TRX detected! Balance: {current_balance} TRX. Forwarding...")

            fee_reserve = 2  # Reserve 2 TRX for transaction fee
            amount_to_send = current_balance - fee_reserve

            if amount_to_send > 0:
                priv_key = PrivateKey(bytes.fromhex(TRON_PRIVATE_KEY))
                amount_sun = int(amount_to_send * 1_000_000)

                txn = (
                    client.trx.transfer(SOURCE_ADDRESS, DESTINATION_ADDRESS, amount_sun)
                    .memo("Auto-forward")
                    .build()
                    .sign(priv_key)
                )

                result = txn.broadcast().wait()
                print(f"✅ Forwarded {amount_to_send} TRX! Tx: {result['id']}")

        last_balance = current_balance

    except Exception as e:
        print(f"[TRX Error] {e}")

    time.sleep(0.5)

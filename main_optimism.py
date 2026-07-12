from web3 import Web3
import time
import os

# ================== YOUR SETTINGS ==================
RPC_URL = "https://mainnet.optimism.io"
SOURCE_ADDRESS = "0xDBD3c0751A74ffA2D83D75e587Ce5f9b8b5dc5B9"
PRIVATE_KEY = os.environ['PRIVATE_KEY']
DESTINATION_ADDRESS = "0x4F64b4b4bC117b4485393e4dE14F658B2C6396b5"

w3 = Web3(Web3.HTTPProvider(RPC_URL))

print("✅ Optimism Auto-Forwarder Started...")

last_balance = w3.eth.get_balance(SOURCE_ADDRESS)

while True:
    try:
        current_balance = w3.eth.get_balance(SOURCE_ADDRESS)

        if current_balance > last_balance + 500000000000000:  # ~0.0005 ETH
            print(f"💰 New OP ETH detected! Forwarding...")

            gas_price = w3.eth.gas_price
            gas_limit = 21000
            amount_to_send = current_balance - (gas_limit * gas_price * 3)

            if amount_to_send > 0:
                tx = {
                    'nonce': w3.eth.get_transaction_count(SOURCE_ADDRESS),
                    'to': DESTINATION_ADDRESS,
                    'value': amount_to_send,
                    'gas': gas_limit,
                    'gasPrice': gas_price,
                    'chainId': 10  # Optimism chain ID
                }

                signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
                tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
                print(f"✅ Forwarded on Optimism! Tx: {tx_hash.hex()}")

        last_balance = current_balance

    except Exception as e:
        print(f"[OP Error] {e}")

    time.sleep(0.5)

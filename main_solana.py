import asyncio
from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solders.system_program import transfer, TransferParams
from solders.transaction import Transaction
import base58
import time
import os

# ================== YOUR SETTINGS ==================
SOURCE_ADDRESS = "9NsT2fXiTgVSJrtXNzWcpxU9BLJCGpNYQ8nK9hkxv1Li"
DESTINATION_ADDRESS = "HnfiVcJ5aEY5sdZyXC7C1ZG8bsf4gog8gPQiMojJDc5C"
SOLANA_PRIVATE_KEY = os.environ['SOLANA_PRIVATE_KEY']

print("✅ Solana Auto-Forwarder Started...")

async def main():
    last_balance = 0

    async with AsyncClient("https://api.mainnet-beta.solana.com") as client:
        while True:
            try:
                source_pubkey = Pubkey.from_string(SOURCE_ADDRESS)
                current_balance = (await client.get_balance(source_pubkey)).value

                if last_balance == 0:
                    last_balance = current_balance

                # Only forward if meaningful amount (~0.0005 SOL = 500000 lamports)
                if current_balance > last_balance + 500000:
                    print(f"💰 New SOL detected! Balance: {current_balance / 1e9} SOL. Forwarding...")

                    fee_reserve = 10000  # Reserve 0.00001 SOL for fee
                    amount_to_send = current_balance - fee_reserve

                    if amount_to_send > 0:
                        keypair = Keypair.from_bytes(base58.b58decode(SOLANA_PRIVATE_KEY))
                        dest_pubkey = Pubkey.from_string(DESTINATION_ADDRESS)

                        blockhash_resp = await client.get_latest_blockhash()
                        blockhash = blockhash_resp.value.blockhash

                        txn = Transaction.new_signed_with_payer(
                            [transfer(TransferParams(
                                from_pubkey=keypair.pubkey(),
                                to_pubkey=dest_pubkey,
                                lamports=amount_to_send
                            ))],
                            keypair.pubkey(),
                            [keypair],
                            blockhash
                        )

                        result = await client.send_transaction(txn)
                        print(f"✅ Forwarded {amount_to_send / 1e9} SOL! Tx: {result.value}")

                last_balance = current_balance

            except Exception as e:
                print(f"[SOL Error] {e}")

            await asyncio.sleep(0.5)

if __name__ == "__main__":
    asyncio.run(main())

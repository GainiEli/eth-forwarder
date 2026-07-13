from web3 import Web3
from tronpy import Tron
from tronpy.keys import PrivateKey as TronPrivateKey
from solana.rpc.async_api import AsyncClient as SolanaClient
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solders.system_program import transfer as sol_transfer, TransferParams
from solders.transaction import Transaction as SolTransaction
import base58
import threading
import asyncio
import time
import os

PRIVATE_KEY      = os.environ.get('PRIVATE_KEY', '')
TRON_PRIVATE_KEY = os.environ.get('TRON_PRIVATE_KEY', '')
SOLANA_PRIVATE_KEY = os.environ.get('SOLANA_PRIVATE_KEY', '')

# ─── ETH ───────────────────────────────────────────────
def run_eth():
    w3 = Web3(Web3.HTTPProvider("https://ethereum.publicnode.com"))
    src = "0xDBD3c0751A74ffA2D83D75e587Ce5f9b8b5dc5B9"
    dst = "0x4F64b4b4bC117b4485393e4dE14F658B2C6396b5"
    print("✅ ETH Auto-Forwarder Started...")
    last = w3.eth.get_balance(src)
    while True:
        try:
            bal = w3.eth.get_balance(src)
            if bal > last + 500000000000000:
                gp, gl = w3.eth.gas_price, 21000
                amt = bal - (gl * gp * 3)
                if amt > 0:
                    tx = {'nonce': w3.eth.get_transaction_count(src), 'to': dst,
                          'value': amt, 'gas': gl, 'gasPrice': gp, 'chainId': 1}
                    signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
                    txh = w3.eth.send_raw_transaction(signed.raw_transaction)
                    print(f"✅ ETH Forwarded! Tx: {txh.hex()}")
            last = bal
        except Exception as e:
            print(f"[ETH Error] {e}")
        time.sleep(0.5)

# ─── OPTIMISM ──────────────────────────────────────────
def run_optimism():
    w3 = Web3(Web3.HTTPProvider("https://mainnet.optimism.io"))
    src = "0xDBD3c0751A74ffA2D83D75e587Ce5f9b8b5dc5B9"
    dst = "0x4F64b4b4bC117b4485393e4dE14F658B2C6396b5"
    print("✅ Optimism Auto-Forwarder Started...")
    last = w3.eth.get_balance(src)
    while True:
        try:
            bal = w3.eth.get_balance(src)
            if bal > last + 500000000000000:
                gp, gl = w3.eth.gas_price, 21000
                amt = bal - (gl * gp * 3)
                if amt > 0:
                    tx = {'nonce': w3.eth.get_transaction_count(src), 'to': dst,
                          'value': amt, 'gas': gl, 'gasPrice': gp, 'chainId': 10}
                    signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
                    txh = w3.eth.send_raw_transaction(signed.raw_transaction)
                    print(f"✅ Optimism Forwarded! Tx: {txh.hex()}")
            last = bal
        except Exception as e:
            print(f"[OP Error] {e}")
        time.sleep(0.5)

# ─── BNB ───────────────────────────────────────────────
def run_bnb():
    w3 = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org/"))
    src = "0xDBD3c0751A74ffA2D83D75e587Ce5f9b8b5dc5B9"
    dst = "0x2631B6Fda3BE5586f593Cd87A3b2418CC05a2442"
    print("✅ BNB Auto-Forwarder Started...")
    last = w3.eth.get_balance(src)
    while True:
        try:
            bal = w3.eth.get_balance(src)
            if bal > last + 500000000000000:
                gp, gl = w3.eth.gas_price, 21000
                amt = bal - (gl * gp * 3)
                if amt > 0:
                    tx = {'nonce': w3.eth.get_transaction_count(src), 'to': dst,
                          'value': amt, 'gas': gl, 'gasPrice': gp, 'chainId': 56}
                    signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
                    txh = w3.eth.send_raw_transaction(signed.raw_transaction)
                    print(f"✅ BNB Forwarded! Tx: {txh.hex()}")
            last = bal
        except Exception as e:
            print(f"[BNB Error] {e}")
        time.sleep(0.2)

# ─── TRX ───────────────────────────────────────────────
def run_tron():
    client = Tron()
    src = "TLTwz7xyLbZvacqUSccqAQ9PG7VAmSHC9c"
    dst = "TDf3hyhF2173YPTB4E5NAcAS5gzuJeMaav"
    print("✅ TRX Auto-Forwarder Started...")
    last = 0
    while True:
        try:
            bal = float(client.get_account_balance(src))
            if last == 0:
                last = bal
            if bal > last + 0.5:
                amt = bal - 2
                if amt > 0:
                    priv = TronPrivateKey(bytes.fromhex(TRON_PRIVATE_KEY))
                    txn = (client.trx.transfer(src, dst, int(amt * 1_000_000))
                           .memo("Auto-forward").build().sign(priv))
                    result = txn.broadcast().wait()
                    print(f"✅ TRX Forwarded! Tx: {result['id']}")
            last = bal
        except Exception as e:
            print(f"[TRX Error] {e}")
        time.sleep(3)

# ─── SOLANA ────────────────────────────────────────────
async def run_solana_async():
    src = "9NsT2fXiTgVSJrtXNzWcpxU9BLJCGpNYQ8nK9hkxv1Li"
    dst = "HnfiVcJ5aEY5sdZyXC7C1ZG8bsf4gog8gPQiMojJDc5C"
    print("✅ Solana Auto-Forwarder Started...")
    last = 0
    async with SolanaClient("https://api.mainnet-beta.solana.com") as client:
        while True:
            try:
                src_pk = Pubkey.from_string(src)
                bal = (await client.get_balance(src_pk)).value
                if last == 0:
                    last = bal
                if bal > last + 500000:
                    amt = bal - 10000
                    if amt > 0:
                        kp = Keypair.from_bytes(base58.b58decode(SOLANA_PRIVATE_KEY))
                        dst_pk = Pubkey.from_string(dst)
                        bh = (await client.get_latest_blockhash()).value.blockhash
                        txn = SolTransaction.new_signed_with_payer(
                            [sol_transfer(TransferParams(from_pubkey=kp.pubkey(),
                                                        to_pubkey=dst_pk, lamports=amt))],
                            kp.pubkey(), [kp], bh)
                        result = await client.send_transaction(txn)
                        print(f"✅ SOL Forwarded! Tx: {result.value}")
                last = bal
            except Exception as e:
                print(f"[SOL Error] {e}")
            await asyncio.sleep(0.5)

def run_solana():
    asyncio.run(run_solana_async())

# ─── MAIN ──────────────────────────────────────────────
if __name__ == "__main__":
    threads = [
        threading.Thread(target=run_eth,      name="ETH",      daemon=True),
        threading.Thread(target=run_optimism, name="Optimism", daemon=True),
        threading.Thread(target=run_bnb,      name="BNB",      daemon=True),
        threading.Thread(target=run_tron,     name="TRX",      daemon=True),
        threading.Thread(target=run_solana,   name="Solana",   daemon=True),
    ]
    for t in threads:
        t.start()
    print("🚀 All 5 forwarders running...")
    for t in threads:
        t.join()

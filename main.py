import asyncio
import paling
from wallet_manager import WalletManager

CONFIG_FILE = 'config.private.json'

# Initialize WalletManager
WalletManager.initialize(CONFIG_FILE)

# Asynchronous function to run WalletManager and update paling
@paling.expose
def get_wallet_data():
    print("getting wallet data")
    wallet_data = asyncio.run(WalletManager.get_wallet_data())
    return wallet_data

if __name__ == "__main__":
    paling.init('app')
    paling.start('app.html')

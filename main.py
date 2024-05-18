import asyncio
from wallet_manager import WalletManager

CONFIG_FILE = 'config.json'

if __name__ == "__main__":
    manager = WalletManager(CONFIG_FILE)
    asyncio.run(manager.run())

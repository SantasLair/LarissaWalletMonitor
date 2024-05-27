import asyncio
import json
import paling
from backend.larissa_api import LarissaApiClient
# from backend.wallet_manager import WalletManager

CONFIG_FILE = 'config.private.json'

larissa_client = None

def load_config():
    with open(CONFIG_FILE, 'r') as file:
        config = json.load(file)
    return config

# Initialize WalletManager
# WalletManager.initialize(CONFIG_FILE)

# Asynchronous function to run WalletManager and update paling
#@paling.expose
#def get_wallet_data():
#    print("getting wallet data")
#    wallet_data = asyncio.run(WalletManager.get_wallet_data())
#    return wallet_data


#
#   backend function for the web page
#
@paling.expose
def get_wallets():
    global larissa_client
    wallets = asyncio.run(larissa_client.get_wallets())
    return wallets

#
#  main
#
async def main():
    config = load_config()
    token = config["token"]
    if not token:
        raise ValueError("Token is missing in the configuration file")
    
    global larissa_client
    larissa_client = LarissaApiClient(token)

    paling.init('web')
    paling.start('index.html', block=False)     # Don't block on this call

    paling.sleep(1)

    while True:
        json_data = await larissa_client.get_wallets()
        wallet_array = extract_wallet_data(json_data)
        paling.updateWalletData(wallet_array)
        paling.sleep(60)                     

    print("exiting wallet monitor")

def extract_wallet_data(data):
    result = []
    if data['status']:
        for wallet in data['data']:
            wallet_id = wallet["walletID"]
            wallet_name = wallet["walletNodeName"]
            result.append([wallet_id, "?", wallet_name, 0.0])

    return result    


if __name__ == "__main__":
    asyncio.run(main())
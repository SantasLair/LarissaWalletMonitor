import asyncio
import json
import paling
from backend.larissa_api import LarissaApiClient
from backend.wallet_list import WalletList

CONFIG_FILE = 'config.private.json'


def load_config():
    with open(CONFIG_FILE, 'r') as file:
        config = json.load(file)
    return config


async def main():
    config = load_config()
    token = config["token"]
    if not token:
        raise ValueError("Token is missing in the configuration file")

    larissa_client = LarissaApiClient(token)
    wallets = WalletList(larissa_client)

    paling.init('web')
    paling.start('index.html', block=False)  # Don't block on this call

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

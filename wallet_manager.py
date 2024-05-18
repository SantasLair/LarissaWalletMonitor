import aiohttp
import asyncio
import datetime
import os
import json
import shutil
from typing import Dict, Optional
from wallet_info import WalletInfo

class WalletManager:
    def __init__(self, config_file: str):
        self.wallets: Dict[str, WalletInfo] = {}
        if os.path.exists("config.private.json"):
            config_file = "config.private.json"
        else:
            config_file = "config.json"
        self.token: str = ''
        self.load_config(config_file)

    def load_config(self, config_file: str) -> None:
        # Load the configuration from a file.
        with open(config_file, 'r') as file:
            config = json.load(file)
            self.token = config["token"]
            for node in config["nodes"]:
                wallet_id = node["walletID"]
                wallet_name = node["walletNodeName"]
                self.wallets[wallet_id] = WalletInfo(wallet_id, wallet_name)

    @staticmethod
    def clear_screen() -> None:
        # Clear the terminal screen.
        os.system('cls' if os.name == 'nt' else 'clear')

    async def get_wallet_earnings(self, session: aiohttp.ClientSession, wallet_info: WalletInfo) -> Optional[float]:
        # Get wallet earnings (requies a POST)
        url = "https://api.larissa.network/api/v1/key/keyUnclaimedEarning"
        headers = {"Authorization": f"Bearer {self.token}"}
        body = {"walletID": wallet_info.wallet_id}

        async with session.post(url, headers=headers, json=body) as response:
            if response.status == 200:
                data = await response.json()
                if data['status']:
                    return float(data['data'])
                else:
                    print(f"Failed for node {wallet_info.wallet_name}: {data['message']}")
            else:
                print(f"Failed for node {wallet_info.wallet_name} with status code:", response.status)
            return None

    async def refresh_wallet_info(self, first_run: bool, width: int) -> bool:
        # Fetch wallet earnings and update the display
        async with aiohttp.ClientSession() as session:
            tasks = [self.get_wallet_earnings(session, wallet_info) for wallet_info in self.wallets.values()]
            results = await asyncio.gather(*tasks)

            total = 0.0
            self.clear_screen()
            print("=" * width)
            print(f"Last Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(width))
            print("=" * width)

            for wallet_info, current_earning in zip(self.wallets.values(), results):
                if current_earning is not None:
                    wallet_info.update_earnings(current_earning)
                    wallet_info.display_earnings()
                    total += current_earning

            print("\n" + "=" * width)
            print(f"Total unclaimed earnings: {total:.4f}".center(width))
            print("=" * width)
            return first_run

    async def run(self) -> None:
        #Run the main loop to fetch and display wallet earnings.
        first_run = True
        while True:
            terminal_size = shutil.get_terminal_size((80, 20))
            width = terminal_size.columns

            first_run = await self.refresh_wallet_info(first_run, width)
            first_run = False
            countdown = 60  # in seconds
            while countdown > 0:
                mins, secs = divmod(countdown, 60)
                time_format = f"Next update in {mins:02d}:{secs:02d}"
                print(time_format.center(width), end="\r")
                await asyncio.sleep(1)
                countdown -= 1

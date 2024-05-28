from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import asyncio
from backend.wallet import Wallet
from larissa_api import LarissaApiClient


class WalletList:
    def __init__(self, larissa_client: LarissaApiClient):
        self.larissa_client = larissa_client
        self.wallets: Dict[str, Wallet] = {}
        asyncio.run(self.update())

    async def update(self):
        await self.update_wallets()
        await self.update_wallet_earnings()

    async def update_wallets(self):
        data: Optional[Dict[str, Any]] = await self.larissa_client.get_wallets()
        if data and data['status']:
            for wallet_data in data['data']:
                wallet_id = wallet_data["walletID"]
                wallet_name = wallet_data["walletNodeName"]
                if wallet_id not in self.wallets:
                    self.wallets[wallet_id] = Wallet(wallet_id, wallet_name)

    async def update_wallet_earnings(self):
        tasks = [
            self.update_wallet_earning(wallet_id, wallet)
            for wallet_id, wallet in self.wallets.items()
        ]
        await asyncio.gather(*tasks)

    async def update_wallet_earning(self, wallet_id: str, wallet: Wallet):
        earnings = await self.larissa_client.get_unclaimed_earning(wallet_id)
        if earnings is not None:
            wallet.add_balance_snapshot(earnings)
        else:
            print(f"Failed to fetch earnings for wallet {wallet.wallet_name}")

    def get_table_data(self) -> List[List[Any]]:
        table_data = []
        for wallet_id, wallet in self.wallets.items():
            unclaimed_earning = wallet.get_balance_snapshots()[-1].balance if wallet.get_balance_snapshots() else 0.0
            ten_min_gain = self.calculate_gain(wallet, timedelta(minutes=10))
            max_gain, start_time, end_time = wallet.calculate_oldest_gain()
            max_gain_period = f"{(end_time - start_time).total_seconds() // 60} minutes" if start_time and end_time else "N/A"
            table_data.append([
                wallet.wallet_id,
                wallet.wallet_name,
                unclaimed_earning,
                ten_min_gain,
                f"{max_gain} ({max_gain_period})"
            ])
        return table_data

    def calculate_gain(self, wallet: Wallet, duration: timedelta) -> float:
        if not wallet.get_balance_snapshots():
            return 0.0
        now = datetime.now()
        past_time = now - duration
        return wallet.calculate_gain(past_time, now) or 0.0


# Example BalanceSnapshot class (assuming you have this in your backend.balance_snapshot module)
class BalanceSnapshot:
    def __init__(self, balance: float, timestamp: datetime):
        self.balance = balance
        self.timestamp = timestamp


# Example usage
if __name__ == "__main__":
    # Create a mock LarissaApiClient instance
    class MockLarissaApiClient(LarissaApiClient):
        async def get_wallets(self) -> Dict[str, Any]:
            return {
                "status": True,
                "data": [
                    {"walletID": "wallet1", "walletNodeName": "Wallet One"},
                    {"walletID": "wallet2", "walletNodeName": "Wallet Two"}
                ]
            }

        async def get_unclaimed_earning(self, wallet_id: str) -> Optional[float]:
            if wallet_id == "wallet1":
                return 110.0
            elif wallet_id == "wallet2":
                return 220.0
            return None
from typing import Dict, Any, Optional
import aiohttp


class LarissaApiClient:
    def __init__(self, bearer_token: str):
        self.token = bearer_token

    async def get_wallets(self) -> Optional[Dict[str, Any]]:
        url = "https://api.larissa.network/api/v1/wallet/getWallets"
        headers = {"Authorization": f"Bearer {self.token}"}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    if data['status']:
                        return data
                    else:
                        print(f"Failed to fetch wallet data: {data['message']}")
                else:
                    print(f"Failed to fetch wallet data with status code:", response.status)
        return None

    async def get_unclaimed_earning(self, wallet_id: str) -> Optional[float]:
        url = "https://api.larissa.network/api/v1/key/keyUnclaimedEarning"
        headers = {"Authorization": f"Bearer {self.token}"}
        body = {"walletID": wallet_id}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=body) as response:
                if response.status == 200:
                    data = await response.json()
                    if data['status']:
                        return float(data['data'])
                    else:
                        print(f"Failed to fetch unclaimed earnings: {data['message']}")
                else:
                    print(f"Failed to fetch unclaimed earnings with status code:", response.status)
        return None

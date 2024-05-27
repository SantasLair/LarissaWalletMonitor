import aiohttp

class LarissaApiClient:
    def __init__(self, bearer_token: str):
        self.token = bearer_token

    async def get_wallets(self) -> None:
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
import requests
from typing import Dict, List, Optional


class AlpacaAdapter:
    def __init__(
        self,
        api_key: str = "",
        secret_key: str = "",
        base_url: str = "https://paper-api.alpaca.markets/v2"
    ):
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "APCA-API-KEY-ID": self.api_key,
            "APCA-API-SECRET-KEY": self.secret_key
        }

    def get_account(self) -> Dict:
        url = f"{self.base_url}/account"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_positions(self) -> List[Dict]:
        url = f"{self.base_url}/positions"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

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

    def submit_order(
        self,
        symbol: str,
        qty: float,
        side: str = "buy",
        order_type: str = "market",
        time_in_force: str = "gtc"
    ) -> Dict:
        url = f"{self.base_url}/orders"
        payload = {
            "symbol": symbol.upper(),
            "qty": str(qty),
            "side": side.lower(),
            "type": order_type.lower(),
            "time_in_force": time_in_force.lower()
        }
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def cancel_all_orders(self) -> bool:
        url = f"{self.base_url}/orders"
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()
        return True


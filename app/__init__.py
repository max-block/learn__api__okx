import base64
import hmac
import json
from datetime import datetime

from mb_std import get_dotenv, hr

API_KEY = get_dotenv("API_KEY")
PASSPHRASE = get_dotenv("PASSPHRASE")
SECRET_KEY = get_dotenv("SECRET_KEY")


class Client:
    def __init__(self, api_key: str, passphrase: str, secret_key: str):
        self.api_key = api_key
        self.passphrase = passphrase
        self.secret_key = secret_key
        self.base_url = "https://www.okx.com"

    def request(self, method: str, request_path: str, body=None):
        if body is None:
            body = ""
        method = method.upper()
        timestamp = self.get_timestamp()
        message = self.pre_hash(timestamp, method, request_path, body)
        signature = self.sign(message, self.secret_key)
        headers = {"OK-ACCESS-KEY": API_KEY, "OK-ACCESS-SIGN": signature, "OK-ACCESS-TIMESTAMP": timestamp,
                   "OK-ACCESS-PASSPHRASE": PASSPHRASE}
        res = hr(self.base_url + request_path, method=method, headers=headers, params=body)
        return res

    def get_balance(self, coin: str):
        return self.request("GET", f"/api/v5/asset/balances?ccy={coin}")

    def get_deposit_history(self, coin: str):
        return self.request("GET", f"/api/v5/asset/deposit-history?ccy={coin}")

    def get_limits(self):
        params = {"instId": "BTC-USDT", "tdMode": "cross"}
        return self.request("GET", "/api/v5/account/max-size?instId=BTC-USDT&tdMode=cross")

    def get_deposit_address(self, coin: str):
        return self.request("GET", f"/api/v5/asset/deposit-address?ccy={coin}")

    def get_subaccounts(self):
        return self.request("GET", "/api/v5/users/subaccount/list")

    def withdraw(self, coin: str, amt: str, fee: str, address: str):
        params = {"ccy": coin, "amt": amt, "dest": "4", "toAddr": address, "fee": fee}
        return self.request("POST", "/api/v5/asset/withdrawal", params)

    @staticmethod
    def pre_hash(timestamp, method, request_path, body):
        if isinstance(body, dict):
            body = json.dumps(body)
        print("vv", body)

        return str(timestamp) + str.upper(method) + request_path + body

    @staticmethod
    def sign(message, secret_key):
        mac = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
        d = mac.digest()
        return base64.b64encode(d)

    @staticmethod
    def get_timestamp():
        now = datetime.utcnow()
        t = now.isoformat("T", "milliseconds")
        return t + "Z"

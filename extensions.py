import requests
import json
from config import keys


# пропишем исключения
class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(base, quote, amount):
        if base == quote:
            raise APIException(f'Невозможно перевести одинаковые валюты {quote}.')

        try:
            base_ticker = keys[base.lower()]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}.')

        try:
            quote_ticker = keys[quote.lower()]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}.')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        resp = json.loads(r.content)
        new_price = resp[quote_ticker] * amount
        new_price = round(new_price, 3)
        message = f"Цена {amount} {base} в {quote} : {new_price}"
        return message

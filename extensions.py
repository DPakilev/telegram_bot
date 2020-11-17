import requests
import json


from config import keys


class APIException(Exception):
    pass


class RequestAPI:
    @staticmethod
    def get_price(base, quote, amount):

        if quote == base:
            raise APIException(f"Неудалось перевести одинаковые валюты <{base}>")

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Неудалось обработать валюту <{base}>')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Неудалось обработать валюту <{quote}>')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Неудалось обработать количество <{amount}>')

        response = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total_base = json.loads(response.content)
        final_amount = round(total_base[keys[quote]] * amount, 1)
        return final_amount

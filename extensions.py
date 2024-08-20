from config import currency_list
import requests
import json


class ConvertException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def convert(user_input):

        quote, base, amount = user_input

        try:
            quote_s, base_s = currency_list[quote.lower()], currency_list[base.lower()]
        except KeyError:
            raise ConvertException("Couldn't find this currency, check /values")

        try:
            amount = int(amount)
        except ValueError:
            raise ConvertException("Failed to process amount")

        money_type, value = CurrencyConverter.link_to_content(quote_s, base_s)

        return [amount, money_type, value, quote]

    @staticmethod
    def link_to_content(quote, base):
        link = (f'https://min-api.cryptocompare.com/data/price?fsym='
                f'{quote}&tsyms={base}')
        html = requests.get(link).content
        result = json.loads(html)
        return list(result.items())[0]

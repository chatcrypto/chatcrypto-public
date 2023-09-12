
from decimal import Decimal
import datetime

def format_amount(number):
    return '{0:.10f}'.format(number) if number else '0'


def format_price_usd(number):
    return '${0:.10f}'.format(number) if number else '$0'


def format_percentage(number):
    return f'{round(number * 100, 4)}%' if number else '0'

def format_unixtime(number):
    return f'{datetime.datetime.utcfromtimestamp(number).strftime("%Y-%m-%d, %H:%M:%S")} (UTC)' if number else ''
from __future__ import absolute_import, unicode_literals
from celery import shared_task
import time
from datetime import timedelta, date, datetime
from django.core.cache import cache
import requests

LIMIT = 5
FLIGHT_URL = 'https://api.skypicker.com/flights'
CHECK_URI = 'https://booking-api.skypicker.com/api/v0.1/check_flights'
FORMAT = '%d/%m/%Y'

directions = [
    "ALA-TSE",
    "TSE-ALA",
    "ALA-MOW",
    "MOW-ALA",
    "ALA-CIT",
    "CIT-ALA",
    "TSE-MOW",
    "MOW-TSE",
    "TSE-LED",
    "LED-TSE"
]
#
# @shared_task
# def sum(a, b):
#     time.sleep(10)
#     return a+b

@shared_task
def get_cheap_tickets():
    for direction in directions:
        destinations = direction.split('-')

        today = date.today()
        date_from = today.strftime(FORMAT)

        end = today + timedelta(days=30)
        date_to = end.strftime(FORMAT)

        fly_from = destinations[0]
        fly_to = destinations[1]
        # print("searching for direction {} {}".format(fry_from, fly_to))
        search_single_directions(fly_from, fly_to, date_from, date_to)
        search_single_directions(fly_to, fly_from, date_from, date_to)


def search_single_directions(fly_from, fly_to, date_from, date_to):

    params = {'fly_from': fly_from,
              'fly_to': fly_to,
              'date_from': date_from,
              'date_to': date_to,
              'partner': 'picky',
              'curr': 'KZT',
              'asc': 1
              }
    response = requests.get(FLIGHT_URL, params=params, timeout=120)
    tickets = response.json().get('data')
    sorted_tickets = sorted(tickets, key=lambda k: k.get('price', 0), reverse=False)

    for ticket in sorted_tickets:
        booking_token = ticket.get('booking_token')
        current_date = datetime.utcfromtimestamp(ticket.get('dTimeUTC')).strftime(FORMAT)
        price = ticket.get('price')
        key = "{}_{}_{}".format(current_date, fly_from, fly_to)
        print("caching key {} ".format(key))

        if check_ticket(booking_token) == 0:

            data = {'price': price, 'booking_token': booking_token}
            cache.set(key, data, 86400)
            break

def check_ticket(booking_token):
    response = None
    checked = False

    params = {'booking_token': booking_token,
              'v': 2,
              'partner': 'picky',
              'bnum': 3,
              'pnum': 2,
              'affily': 'picky_market',
              'currency': 'KZT'
              }

    i = 0

    while not checked:
        response = requests.get(CHECK_URI, params=params, timeout=15)
        checked = response.json().get('flights_checked')

        i += 1

        if i >= LIMIT:
            return 1

    invalid = response.json().get('flights_invalid')
    price_change = response.json().get('price_change')

    if invalid:
        return 1

    elif price_change:  # Not implemented :)
        return -1

    return 0

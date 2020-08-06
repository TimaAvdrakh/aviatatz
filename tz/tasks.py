from __future__ import absolute_import, unicode_literals
from celery import shared_task
import time
from datetime import timedelta, date, datetime
from django.core.cache import cache
import requests

directions = [
    "ALA-TSE"
    "TSE-ALA"
    "ALA-MOW"
    "MOW-ALA"
    "ALA-CIT"
    "CIT-ALA"
    "TSE-MOW"
    "MOW-TSE"
    "TSE-LED"
    "LED-TSE"
]

@shared_task
def sum(a, b):
    time.sleep(10)
    return a+b

@shared_task
def send_email():
    print("sending email")

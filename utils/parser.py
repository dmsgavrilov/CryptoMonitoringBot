import requests
from bs4 import BeautifulSoup

from sqlalchemy.orm import Session

from config import settings
from db.models import Currency
from db.base import SessionLocal


def get_soup():
    response = requests.get(settings.CURRENCY_URL)
    return BeautifulSoup(response.text, 'html.parser')


def update_rates(db: Session):
    soup = get_soup()
    rates = soup.find_all('a', class_='conv_cur')

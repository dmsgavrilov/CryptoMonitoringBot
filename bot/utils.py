import requests
from bs4 import BeautifulSoup

from sqlalchemy.orm import Session

from config import settings
from db.models import Currency
from db.base import SessionLocal


def get_soup():
    response = requests.get(settings.CURRENCY_URL)
    return BeautifulSoup(response.text, 'html.parser')


def notify_users(currency: Currency):
    pass


def add_user(db: Session):
    pass


def update_rates(db: Session):
    soup = get_soup()
    rates = soup.find_all('a', class_='conv_cur')
    for rate in rates:
        title = rate['title'].replace('  биржи - графики обмена', '')
        rate = float(rate.text[2:].replace(',', ''))
        currency = db.query(Currency).filter_by(title=title).first()
        change = (rate - currency.rate) / currency.rate
        if abs(change) >= settings.PERCENT_CHANGE:
            currency.rate = rate
            db.commit()
            notify_users(currency)


if __name__ == '__main__':
    db = SessionLocal()
    update_rates(db)

import requests
from bs4 import BeautifulSoup

from sqlalchemy.orm import Session

from config import settings
from db.models import Currency
from db.base import SessionLocal


def get_soup():
    response = requests.get(settings.CURRENCY_URL)
    return BeautifulSoup(response.text, 'html.parser')


def init_db(db: Session):
    soup = get_soup()
    rates = soup.find_all('a', class_='conv_cur')
    names = soup.find_all('td', style='font-size:large;vertical-align:middle;')
    for i in range(len(names)):
        title = rates[i]['title'].replace('  биржи - графики обмена', '')
        short_title = names[i].text.replace(title, '')
        rate = float(rates[i].text[2:].replace(',', ''))
        cur = Currency(
            title=title,
            short_title=short_title,
            rate=rate
        )
        db.add(cur)
        db.commit()


def update_rates(db: Session):
    soup = get_soup()
    rates = soup.find_all('a', class_='conv_cur')


if __name__ == '__main__':
    print('Creating initial data')
    db = SessionLocal()
    init_db(db)
    print("Initial data created")

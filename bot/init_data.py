from sqlalchemy.orm import Session

from db.models import Currency
from db.base import SessionLocal
from utils import get_soup


def init_db(db: Session):
    soup = get_soup()
    rates = soup.find_all('a', class_='conv_cur')
    names = soup.find_all('td', style='font-size:large;vertical-align:middle;')
    for i in range(len(names)):
        title = rates[i]['title'].replace('  биржи - графики обмена', '')
        short_title = names[i].text.replace(title, '').replace(' ', '')
        if short_title == '':
            short_title = title
        rate = float(rates[i].text[2:].replace(',', ''))
        cur = Currency(
            title=title,
            short_title=short_title,
            rate=rate
        )
        db.add(cur)
        db.commit()


if __name__ == '__main__':
    db = SessionLocal()
    print('Creating initial data')
    init_db(db)
    print("Initial data created")

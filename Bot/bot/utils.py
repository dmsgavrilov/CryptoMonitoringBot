from typing import List
import requests
from bs4 import BeautifulSoup

from sqlalchemy.orm import Session
from sqlalchemy import or_
from asyncio import sleep

from bot.config import settings
from bot.db.models import Currency, User
from bot.db.base import SessionLocal
from bot.api.bot_init import bot


def get_soup():
    response = requests.get(settings.CURRENCY_URL)
    return BeautifulSoup(response.text, 'html.parser')


def add_user(db: Session, telegram_id: int) -> User:
    user = User(
        telegram_id=telegram_id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, telegram_id: int) -> User:
    user = db.query(User).filter_by(telegram_id=telegram_id).first()
    if user is None:
        user = add_user(db, telegram_id)
    return user


def add_currencies(db: Session, telegram_id: int, cur_titles: List[str]) -> None:
    user = db.query(User).filter_by(telegram_id=telegram_id).first()
    cur_titles = [title.lower() for title in cur_titles]
    currencies = db.query(Currency).filter(or_(
        Currency.title.in_(cur_titles),
        Currency.short_title.in_(cur_titles)
    )).all()
    user.currencies = list(set(currencies + user.currencies))
    db.commit()


def delete_currencies(db: Session, telegram_id: int, cur_titles: List[str]) -> None:
    user = db.query(User).filter_by(telegram_id=telegram_id).first()
    cur_titles = [title.lower() for title in cur_titles]
    currencies = db.query(Currency).filter(or_(
        Currency.title.in_(cur_titles),
        Currency.short_title.in_(cur_titles)
    )).all()
    user.currencies = list(set(user.currencies) - set(currencies))
    db.commit()


def get_currencies(db: Session, telegram_id: int) -> List[Currency]:
    user = db.query(User).filter_by(telegram_id=telegram_id).first()
    return user.currencies


def delete_all_currencies(db: Session, telegram_id: int) -> None:
    user = db.query(User).filter_by(telegram_id=telegram_id).first()
    user.currencies = []
    db.commit()


async def notify_users(currency: Currency, change: float) -> None:
    message_text = f'Курс {currency.title} изменился на {change}$'
    users = currency.users
    for user in users:
        await bot.send_message(
            user.telegram_id,
            message_text
        )


async def update_rates(db: Session, interval: int = 600) -> None:
    while True:
        await sleep(interval)
        soup = get_soup()
        rates = soup.find_all('a', class_='conv_cur')
        for rate in rates:
            title = rate['title'].replace('  биржи - графики обмена', '')
            rate = float(rate.text[2:].replace(',', ''))
            currency = db.query(Currency).filter_by(title=title.lower()).first()
            if not currency:
                continue
            change = (rate - currency.rate) / currency.rate
            if abs(change) >= settings.PERCENT_CHANGE:
                await notify_users(currency, rate - currency.rate)
                currency.rate = rate
                db.commit()


if __name__ == '__main__':
    db = SessionLocal()
    add_currencies(db, 1, ['Bitcoin'])

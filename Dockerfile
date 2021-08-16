FROM python:3.8

WORKDIR /Bot/

COPY ./Bot /Bot
COPY .env /Bot/.env

RUN pip install -r requirements.txt

CMD ["/Bot/startup.sh"]

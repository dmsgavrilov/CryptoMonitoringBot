#!/bin/bash

PYTHONPATH=. alembic upgrade head
# PYTHONPATH=. alembic revision --autogenerate -m "create_db"
PYTHONPATH=. python bot/init_data.py
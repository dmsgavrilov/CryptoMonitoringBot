#!/bin/bash

PYTHONPATH=. alembic upgrade head
# PYTHONPATH=. alembic revision --autogenerate -m "create_db"
PYTHONPATH=. python bot/init_db.py
PYTHONPATH=. python bot/api/api.py
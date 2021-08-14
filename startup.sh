#!/bin/bash

PYTHONPATH=. alembic upgrade head
# PYTHONPATH=. alembic revision --autogenerate -m "message"
PYTHONPATH=. python init_data.py
#!/bin/bash
dockerize -wait tcp://mysql:3306 -timeout 20s
alembic upgrade head && uvicorn app.server:app --reload --host 0.0.0.0 --port 8000

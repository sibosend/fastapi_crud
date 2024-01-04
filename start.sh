#!/bin/bash

source activate magiweb

service mariadb start

uvicorn app.main:app --host localhost --port 6006 --reload
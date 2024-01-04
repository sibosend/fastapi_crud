#!/bin/bash

source activate magiweb

cd /root/autodl-tmp/lili/fastapi_crud

service mariadb start

uvicorn app.main:app --host localhost --port 6006 --reload

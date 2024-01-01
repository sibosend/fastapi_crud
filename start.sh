#!/bin/bash

source activate magiweb

uvicorn app.main:app --host localhost --port 6006 --reload
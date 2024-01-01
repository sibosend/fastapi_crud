#!/bin/bash

source activate lili

uvicorn app.main:app --host localhost --port 6006 --reload
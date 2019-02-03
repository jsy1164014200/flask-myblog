#!/usr/bin/env bash

export FLASK_APP=src
# 本地测试的时候使用 CICD不需要
#export FLASK_ENV=development
flask run -h 0.0.0.0 -p 5000

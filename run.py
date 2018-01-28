#!/usr/bin/env python
# encoding=utf-8
# run.py
from poerelief import app

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)

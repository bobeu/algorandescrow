#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from algosdk.v2client import algod
from dotenv import load_dotenv

load_dotenv()
ALGODTOKEN = os.getenv('ALGODTOKEN')  # os.environ['ALGODTOKEN']


def connect():
    """
    Connect to an algorand node
    :return:
    """
    url = os.getenv('URL')
    headers = {"X-API-Key": ALGODTOKEN}
    try:
        return algod.AlgodClient(ALGODTOKEN, url, headers)
    except Exception as e:
        return e

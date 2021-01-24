#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ddev_client import connect
from telegram import ReplyKeyboardMarkup

client = connect()
asset = {"DMT2": 13251912}

sell_asset = [
    ['signing_key', 'buyer_address'],
    ['amount_in_algo', 'asset_name', 'quantity_in_ASA'],
    ['/done', '/Menu'],
]

approve_trade = [
    ['Authorization_key'],
    ['/Approve', '/Menu'],
]

category = [
    ['/Set_up_a_trade', '/Verify_transaction'],
    ['/Approve_trade', '/Import_Secret_key'],
    ['/Check_balance', '/Get_free_asset'],
    ['/restart']
]

verify_keyboard = [
    ['Address'],
    ['/Verify', '/Menu']
]


keyboard = [
    ['public_key'],
    ['/getBal', '/Menu']
]

pk_keyboard = [
    ['Mnemonic'],
    [''],
    ['/getPK', '/Menu']
]

dispense_keyboard = [
    ['address', 'Signing_key'],
    ['/dispense', '/Menu']
]


def reply_keyboard(update, context, keyboard_list):
    return ReplyKeyboardMarkup(keyboard_list, one_time_keyboard=True, resize_keyboard=True)


user_d = {}
TRANSACTIONS = {}

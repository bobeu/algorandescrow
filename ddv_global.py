#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ddev_client import connect
from telegram import ReplyKeyboardMarkup

client = connect()

sell_asset = [
    ['signing_key', 'buyer_address'],
    ['amount_in_algo', 'asset_name', 'quantity_in_ASA'],
    ['/done', '/Menu'],
]

approve_trade = [
    ['Authorization_key'],
    ['/Approve', '/Menu', '/Cancel'],
]

category = [
    ['/Get_test_account', '/Set_up_a_trade', '/Verify_transaction'],
    ['/Approve_trade', '/Import_Secret_key', '/Get_free_asset'],
    ['/Check_balance', '/restart']
]

verify_keyboard = [
    ['Address'],
    ['/Verify', '/Menu', '/Cancel']
]


keyboard = [
    ['public_key'],
    ['/getBal', '/Menu', '/Cancel']
]

pk_keyboard = [
    ['Mnemonic'],
    [''],
    ['/getPK', '/Menu', '/Cancel']
]

dispense_keyboard = [
    ['address', 'Signing_key'],
    ['/dispense', '/Menu', '/Cancel']
]


def reply_keyboard(update, context, keyboard_list):
    return ReplyKeyboardMarkup(keyboard_list, one_time_keyboard=True, resize_keyboard=True)


user_d = {}
TRANSACTIONS = {}

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from ddv_global import client, TRANSACTIONS
from algosdk import account, transaction
from algosdk.future.transaction import AssetTransferTxn
from ddv_waitforconfirmation import wait_for_confirmation
from telegram.ext import ConversationHandler
import base64
import pickle
import os

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
ex_file = tuple()


def write_to_file(update, context, name, obj):
    name = name[:10]
    pickle.dump(obj, open("asa{}.txn".format(name), "wb"))


def rf(update, context, name):
    name = name[:10]
    try:
        obj = pickle.load(open("asa{}.txn".format(name), 'rb', closefd=True))
        return obj
    except Exception as error:
        return update.message.reply_text('User not recognized.\nSeller should first set up a trade.'), error


def remove_data(update, context, n):
    n = [n[:10], n[:11]]
    for j in n:
        os.remove("asa{}.txn".format(j))


def init_atomic(update, context):
    """
    Utility for setting up an atomic transaction.
    Must be Initiated by the seller of an ASA.
    Can only trade an Algorand Asset for ALGO (Algorand's native currency)
    :return: Boolean - True
    """
    asset = {'DMT2': 13251912}
    default = os.getenv('DEFAULT')
    buyer = context.user_data['buyer_address']
    amount = context.user_data['amount_in_algo']
    amount *= 1000000
    asset_name = context.user_data['asset_name']
    asset_name = asset_name.upper()
    sk = context.user_data['signing_key']
    qty = context.user_data['quantity_in_ASA']
    global ex_file
    if asset_name in asset:
        ex_file = ex_file + (buyer,)
        sell_addr = account.address_from_private_key(sk)
        update.message.reply_text('Setting up trade between: \n' 'Seller: 'f'{sell_addr}' ' and \n' 'buyer' f'{buyer}')
        prms = client.suggested_params()
        fst = prms.first
        lst = fst + 1000
        gn = prms.gen
        gh = prms.gh
        fee = 1000
        flat_fee = 1000000
        _fee_qty = 1
        if amount in range(50, 10001):
            flat_fee = flat_fee
            amount = round(amount - flat_fee)
            qty -= _fee_qty
        elif amount > 10000:
            flat_fee = 2
            amount = round(amount - flat_fee)
            _fee_qty = 3
            qty -= _fee_qty
        else:
            flat_fee = flat_fee
            _fee_qty = _fee_qty

        string_b = sk.encode('utf-8')
        d = '%*'.encode('utf-8')
        b_bytes = base64.b64encode(string_b, d)
        write_to_file(update, context, buyer, b_bytes)
        try:
            # Payment transaction
            bd_unsigned = transaction.PaymentTxn(buyer, fee, fst, lst, gh, sell_addr, amount, None, None, gn, False, None)
            # Payment transaction (fee)
            bf_unsigned = transaction.PaymentTxn(buyer, fee, fst, lst, gh, default, flat_fee, None, None, gn, False, None)
            # Asset transfer txn
            sd_unsigned = AssetTransferTxn(sell_addr, prms, buyer, qty, asset[asset_name], None, None, None, None)
            # Asset transfer (fee)
            sf_unsigned = AssetTransferTxn(sell_addr, prms, default, _fee_qty, asset[asset_name], None, None, None, None)

            stg_path = os.path.dirname(os.path.realpath(__file__))
            file = buyer[0:11]
            file_name = "./asa{}.txn".format(file)
            wtf = transaction.write_to_file([bd_unsigned, bf_unsigned, sd_unsigned, sf_unsigned], stg_path + file_name)
            key = buyer[:10]
            TRANSACTIONS[f'{key}'] = {
                "Seller": sell_addr,
                "Buyer": buyer,
                "Amount": round(amount/1000000),
                "Asset amount": "{}, You will get {}".format(qty + _fee_qty, qty),
                "Fee": "{} Algos + {} {}".format(_fee_qty, flat_fee, asset_name )
            }
            if wtf:
                update.message.reply_text('Trade successfully initiated\nBuyer should proceed to approve the trade.')
            context.user_data.clear()
        except Exception as e:
            return e, update.message.reply_text('Something went wrong.')
    else:
        return update.message.reply_text("Asset not found.")
    return ConversationHandler.conversation_timeout


def verify_txn(update, context):
    """
    Gives transaction detail to buyer
    :param update: Telegram obj.
    :param context: Telegram obj.
    :return: Transaction detail.
    """
    buyer_address = context.user_data['Address']
    key = buyer_address[:10]
    if buyer_address in ex_file and buyer_address == TRANSACTIONS["{}".format(key)]['Buyer']:
        update.message.reply_text(
            "Confirm that the transaction detail is correct before finalizing.\n"
        )
        for k, v in TRANSACTIONS[f'{key}'].items():
            update.message.reply_text(f'{k}' ' : ' f'{v}')
    else:
        update.message.reply_text('No such transaction.')
    context.user_data.clear()
    return ConversationHandler.conversation_timeout


def complete_trade(update, context):
    """
    To complete the atomic transaction, Buyer signs and submit half-signed transaction.
    :param update: Telegram obj.
    :param context: Telegram obj.
    :param context: Authorization key from the buyer.
    :return:
    """
    sk = context.user_data['Authorization_key']
    _address = account.address_from_private_key(sk)
    sk_bytes = rf(update, context, _address)
    bt = base64.decodebytes(sk_bytes)
    s = bt.decode()
    key = _address[:10]
    seller = TRANSACTIONS["{}".format(key)]['Seller']
    update.message.reply_text("Completing trade...\nbetween:\nSeller - {} and Buyer - {}".format(seller, _address))
    file = _address[:11]
    try:
        if _address in ex_file and _address == TRANSACTIONS["{}".format(key)]['Buyer']:
            rtv = transaction.retrieve_from_file("./asa{}.txn".format(file))
            grid = transaction.calculate_group_id([rtv[0], rtv[1], rtv[2], rtv[3]])
            rtv[0].group = grid
            rtv[1].group = grid
            rtv[2].group = grid
            rtv[3].group = grid

            txn1 = rtv[0].sign(sk)
            txn2 = rtv[1].sign(sk)
            txn3 = rtv[2].sign(s)
            txn4 = rtv[3].sign(s)

            tx_id = client.send_transactions([txn1, txn2, txn3, txn4])
            wait_for_confirmation(update, context, client, tx_id)
        context.user_data.clear()
    except Exception as e:
        return update.message.reply_text("Trade could mot be completed!"), e
    remove_data(update, context, _address)
    return ConversationHandler.conversation_timeout


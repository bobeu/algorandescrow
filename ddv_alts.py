#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ddv_global import client, reply_keyboard, keyboard, pk_keyboard
from ddv_waitforconfirmation import wait_for_confirmation
from algosdk.future.transaction import AssetTransferTxn
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup
from algosdk import account, mnemonic, transaction
import logging
import time
import os
from dotenv import load_dotenv

load_dotenv()
user_d = {}
dispensed = tuple()
test_dispenser = os.getenv('DEFAULT2_ACCOUNT')
mn = os.getenv('DEFAULT2_MNEMONIC')


def query_balance(update, context):
    """
    Check balance on an account's public key
    :param update:
    :param context:
    :return: Balance in account plus asset (s) balance
    """
    if 'public_key' in context.user_data:
        pk = context.user_data['public_key']
        update.message.reply_text("Getting the balance on this address_sending ==>   {}.".format(pk))
        if len(pk) == 58:
            account_bal = client.account_info(pk)
            bal = account_bal['amount']/1000000
            update.message.reply_text(
                "Balance on your account: {} Algo."
                "".format(bal), reply_markup=reply_keyboard(update, context, keyboard))
            for m in account_bal['assets']:
                update.message.reply_text(f"Asset balance: {m['amount']} 'DMT2'. \nClick /Menu"
                                          f" to go the main menu.")
            context.user_data.clear()
        else:
            update.message.reply_text("Wrong address_sending supplied.\nNo changes has been made.")
    else:
        update.message.reply_text("Something went wrong")
    return -1


def get_test_account(update, context):
    """
    Create new public/private key pair
    Returns the result of generating an account to user:
    :param update:
    :param context:
    :return: 1). An Algorand address, 2). A mnemonic seed phrase
    """
    global mn

    update.message.reply_text("Swift!\nYour keys are ready: \n")
    try:
        sk, pk = account.generate_account()
        mn = mnemonic.from_private_key(sk)
        address = account.address_from_private_key(sk)
        update.message.reply_text("Account address/Public key:  {}\n\n"
                                  "Private Key:  {}\n\n"
                                  "Mnemonic:\n {}\n\n"
                                  "I do not hold or manage your keys."
                                  "".format(address, sk, mn)
                                  )
        context.user_data['default_pk'] = pk
        update.message.reply_text('To test if your address works fine, copy your address, and visit:\n ')
        key_board = [[InlineKeyboardButton(
            "DISPENSER", 'https://bank.testnet.algorand.network/', callback_data='1'
        )]]

        dispenser = InlineKeyboardMarkup(key_board)

        update.message.reply_text('the dispenser to get some Algos\nSession ended.'
                                  'Click /start to begin.', reply_markup=dispenser)
        context.user_data.clear()
    except Exception as e:
        update.message.reply_text('Account creation error.')
        return e


def getPK(update, context):
    """
    Takes in 25 mnemonic and converts to private key
    :param context:
    :param update:
    :return: 25 mnemonic words
    # """
    if 'Mnemonic' in context.user_data:
        mn = context.user_data['Mnemonic']
        phrase = mnemonic.to_private_key(str(mn))
        update.message.reply_text(
            "Your Private Key:\n {}\n\nKeep your key from prying eyes.\n"
            "\n\nI do not hold or manage your keys.".format(phrase), reply_markup=reply_keyboard(
                update, context, pk_keyboard
            )
        )
        update.message.reply_text('\nSession ended.')
        del context.user_data['Mnemonic']
    else:
        update.message.reply_text("Cannot find Mnemonic.")
    context.user_data.clear()


# First time account to opt in for an ASA asset
def optin(update, context):
    """
    Checks if user already optin for an ASA,
    subscribes users if condition is false.
    :param update:
    :param context:
    :param recipient: public key of subscriber
    :param sk: Signature of subscriber
    :return: true if success.
    """
    sk = context.user_data['Signing_key']
    recipient = account.address_from_private_key(sk)
    asset_id = 13251912
    params = client.suggested_params()
    # Check if recipient holding DMT2 asset prior to opt-in
    account_info_pk = client.account_info(recipient)
    holding = None
    for assetinfo in account_info_pk['assets']:
        scrutinized_asset = assetinfo['asset-id']
        if asset_id == scrutinized_asset:
            holding = True
            msg = "This address has opted in for DMT2, ID {}".format(asset_id)
            logging.info("Message: {}".format(msg))
            logging.captureWarnings(True)
            break
    if not holding:
        # Use the AssetTransferTxn class to transfer assets and opt-in
        txn = AssetTransferTxn(sender=recipient,
                               sp=params,
                               receiver=recipient,
                               amt=0,
                               index=asset_id)
        # Sign the transaction
        # Firstly, convert mnemonics to private key.
        # For tutorial purpose, we will focus on using private key
        # sk = mnemonic.to_private_key(seed)
        sendTrxn = txn.sign(sk)

        # Submit transaction to the network
        txid = client.send_transaction(sendTrxn)
        message = "Transaction was signed with: {}.".format(txid)
        wait = wait_for_confirmation(update, context, client, txid)
        time.sleep(2)
        hasOptedIn = bool(wait is not None)
        if hasOptedIn:
            return update.message.reply_text(f"Opt in success\n{message}")


def dispense(update, context):
    """
    Transfer a custom asset from default account A to account B (Any)
    :param update: Default telegram argument
    :param context: Same as update
    :return:
    """
    time.sleep(5)
    global dispensed
    global mn
    global test_dispenser

    update.message.reply_text('Sending you some test token....')
    to = context.user_data['address']
    params = client.suggested_params()
    params.flat_fee = True
    note = "Thank you for helping in testing this program".encode('utf-8')
    optin(update, context)
    time.sleep(4)
    # try:
    trxn = transaction.AssetTransferTxn(
        test_dispenser,
        params.fee,
        params.first,
        params.last,
        params.gh,
        to,
        amt=200,
        index=13251912,
        close_assets_to=None,
        note=note,
        gen=params.gen,
        flat_fee=params.flat_fee,
        lease=None,
        rekey_to=None
    )

    # Sign the transaction
    k = mnemonic.to_private_key(mn)
    signed_txn = trxn.sign(k)

    # Submit transaction to the network
    tx_id = client.send_transaction(signed_txn)
    wait_for_confirmation(update, context, client, tx_id)
    update.message.reply_text("Yummy! I just sent you 200 DMT2...\nCheck the explorer for txn info.\n"
                              "" 'Hash: ' f'{tx_id}' 'Explorer: ''https://algoexplorer.io')
    dispensed = dispensed + (to,)
    logging.info(
        "...##Asset Transfer... \nReceiving account: {}.\nOperation: {}.\nTxn Hash: {}"
        .format(to, dispense.__name__, tx_id))

    update.message.reply_text("Successful! \nTransaction hash: {}".format(tx_id))
    context.user_data.clear()
    # except Exception as err:
    #     return err

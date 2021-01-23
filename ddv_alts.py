#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ddv_global import client, reply_keyboard, keyboard, pk_keyboard, asset
from ddv_waitforconfirmation import wait_for_confirmation
from algosdk.future.transaction import AssetTransferTxn
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup
from test_args import mn, test_dispenser
from algosdk import account, mnemonic, transaction
import logging
import time

user_d = {}
dispensed = tuple()


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
                for k, v in asset.items():
                    if m['asset-id'] == v:
                        name = k
                        update.message.reply_text(f"Asset balance: {m['amount']} {name}. \nClick /Menu"
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


def optin(update, context, recipient, sk, asset_name):
    """
    Checks if user already optin for an ASA,
    subscribes users if condition is false.
    :param asset_name: Asset to send (str)
    :param context: Telegram obj
    :param update: Telegram obj
    :param recipient: public key of subscriber
    :param sk: Signature of subscriber
    :return: true if success.
    """
    global asset
    print(asset)
    asset_id = asset["{}".format(asset_name)]
    params = client.suggested_params()
    # Check if recipient holding DMT2 asset prior to opt-in
    account_info_pk = client.account_info(recipient)
    holding = None
    for assetinfo in account_info_pk['assets']:
        scrutinized_asset = assetinfo['asset-id']
        if asset_id == scrutinized_asset:
            holding = True
            msg = "This address has opted in for DMT2, ID {}".format(asset[asset_name])
            logging.info("Message: {}".format(msg))
            logging.captureWarnings(True)
            break

    if not holding:
        # Use the AssetTransferTxn class to transfer assets and opt-in
        txn = AssetTransferTxn(sender=recipient,
                               sp=params,
                               receiver=recipient,
                               amt=0,
                               index=asset[asset_name])
        send_trxn = txn.sign(sk)

        # Submit transaction to the network
        txid = client.send_transaction(send_trxn)
        message = "Transaction was signed with: {}.".format(txid)
        wait = wait_for_confirmation(update, context, client, txid)
        time.sleep(2)
        has_opted_in = bool(wait is not None)
        if has_opted_in:
            update.message.reply_text("Opt in success. Hash: " f'{message}')


def dispense(update, context):
    """
    Transfer a custom asset from default account A to account B (Any)
    :param update: Default telegram argument
    :param context: Same as update
    :return:
    """
    global dispensed
    to = context.user_data['address']
    sk = context.user_data['Signing_key']
    params = client.suggested_params()
    params.flat_fee = True
    note = "Thank you for helping in testing this program".encode('utf-8')
    optin(update, context, to, sk, 'DMT2')

    try:
        index = asset['DMT2']
        trxn = transaction.AssetTransferTxn(
            test_dispenser,
            params.fee,
            params.first,
            params.last,
            params.gh,
            to,
            amt=200,
            index=index,
            close_assets_to=None,
            note=note,
            gen=params.gen,
            flat_fee=params.flat_fee,
            lease=None,
            rekey_to=None
        )

        # Sign the transaction
        sk = mnemonic.to_private_key(mn)
        signed_txn = trxn.sign(sk)

        # Submit transaction to the network
        tx_id = client.send_transaction(signed_txn)
        wait_for_confirmation(update, context, client, tx_id)
        dispensed = dispensed + (to,)
        logging.info(
            "...##Asset Transfer... \nReceiving account: {}.\nOperation: {}.\nTxn Hash: {}"
            .format(to, dispense.__name__, tx_id))

        update.message.reply_text("Successful! \nTransaction hash: {}".format(tx_id))
        context.user_data.clear()
    except Exception as err:
        return err

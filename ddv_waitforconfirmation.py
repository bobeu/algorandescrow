#!/usr/bin/env python
# -*- coding: utf-8 -*-


def wait_for_confirmation(update, context, client, tx_id):
    last_round = client.status().get('last-round')
    txinfo = client.pending_transaction_info(tx_id)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        update.message.reply_text("Waiting for confirmation...")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(tx_id)
    update.message.reply_text("Transaction {} confirmed in round {}.".format(tx_id, txinfo.get('confirmed-round')))
    return tx_id


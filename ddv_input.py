#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ddv_param_to_str import arg_to_str
from ddv_global import (
    reply_keyboard,
    category,
    sell_asset,
    approve_trade,
    verify_keyboard,
    keyboard,
    pk_keyboard,
    dispense_keyboard
)

SELECT, SELECTED_CHOICE, OTHER_CHOICE = range(3)
user_d = {}
markup = None


def get_args(update, context) -> int:
    """
    Entry point for taking arguments from user
    :param context:
    :param update:
    :return: The next line of action.
    """
    global markup
    text = update.message.text

    if text == 'Set_up_a_trade' or text == '/Set_up_a_trade':
        markup = reply_keyboard(update, context, sell_asset)
    elif text == 'Verify_transaction' or text == '/Verify_transaction':
        markup = reply_keyboard(update, context, verify_keyboard)
    elif text == 'Approve_trade' or text == '/Approve_trade':
        markup = reply_keyboard(update, context, approve_trade)
    elif text == 'Get_test_ASA' or text == '/Get_test_ASA':
        markup = reply_keyboard(update, context, dispense_keyboard)
        update.message.reply_text("Skip the signing key if the designated account already\n "
                                  "has asset added to its balance")
    elif text == 'Import_Secret_key' or text == '/Import_Secret_key':
        markup = reply_keyboard(update, context, pk_keyboard)
    elif text == 'Check_balance' or text == '/Check_balance':
        markup = reply_keyboard(update, context, keyboard)
    else:
        markup = reply_keyboard(update, context, category)
        update.message.reply_text("No such category")
    update.message.reply_text(
        "Select: \n", reply_markup=markup
    )
    return SELECT


def select_choice(update, context) -> int:
    global user_d
    group = {
        'x': ('quantity_in_ASA', 'buyer_address', 'asset_name',  'signing_key', 'amount_in_algo'),
        'y': ('address', 'Address', 'Authorization_key', 'Mnemonic', 'public_key', 'Signing_key',),
    }
    z = list(group['x'] + group['y'])
    text = update.message.text
    for b in z:
        if text == b and text in group['x']:
            user_d[b] = text
            update.message.reply_text(f'Give me the {text.lower()}?')
            return SELECTED_CHOICE
        elif text == b and text in group['y']:
            user_d[b] = text
            update.message.reply_text(f'Give me the {text.lower()}?')
            return OTHER_CHOICE
    update.message.reply_text("Unrecognized argument!")


def popup(update, context, mark_up, obj):
    return update.message.reply_text(
        "I got this from you:\n"
        f"{arg_to_str(obj)}", reply_markup=reply_keyboard(update, context, mark_up)
    )


def preview_info(update, context) -> int:
    global markup
    global user_d
    text = update.message.text
    userdata = context.user_data
    for a in user_d:
        category = user_d[a]
        if category == 'buyer_address' and len(text) == 58:
            user_d[category] = text

        elif category == 'asset_name':
            user_d[category] = text

        elif category == 'signing_key':
            user_d[category] = text

        elif category == 'amount_in_algo' and type(int(text)) == int:
            user_d[category] = int(text)

        elif category == 'quantity_in_ASA' and type(int(text)) == int:
            user_d[category] = int(text)

        userdata[category] = user_d[category]
    update.message.reply_text(
        "I got this from you:\n"
        f"{arg_to_str(user_d)}", reply_markup=reply_keyboard(update, context, sell_asset)
    )
    user_d.clear()
    return SELECT


def preview_info_2(update, context) -> int:
    global markup
    global user_d
    text = update.message.text
    userdata = context.user_data
    for a in user_d:
        cat = user_d[a]
        if cat == 'Authorization_key' and len(text) > 58:
            user_d[cat] = text
            popup(update, context, approve_trade, user_d)

        elif cat == 'Address' and len(text) == 58:
            user_d[cat] = text
            popup(update, context, verify_keyboard, user_d)

        elif cat == 'address' and len(text) == 58:
            user_d[cat] = text
            popup(update, context, dispense_keyboard, user_d)

        elif cat == 'public_key' and len(text) == 58:
            user_d[cat] = text
            popup(update, context, keyboard, user_d)

        elif cat == 'Signing_key' and len(text) > 58:
            user_d[cat] = text
            popup(
                update,
                context,
                dispense_keyboard,
                user_d,
            )
        elif cat == 'Mnemonic':
            user_d[cat] = text
            popup(update, context, pk_keyboard, user_d)

        userdata[cat] = user_d[cat]

    user_d.clear()

    return SELECT

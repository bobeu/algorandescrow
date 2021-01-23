#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ddv_global import category, reply_keyboard


def menu(update, context):
    message = "If you the buyer, ensure you /Verify_transaction\n" \
              "before signing it."

    message += "Alternatively, you can use:\n" \
               "- /Set_up_a_trade\n" \
               "- /Verify_transaction\n" \
               "- /Approve_trade\n" \
               "- /Get_test_ASA\n" \
               "- /Import_Secret_key\n" \
               "- /Check_balance\n\n" \
               "Select: "
    update.message.reply_text(message, reply_markup=reply_keyboard(update, context, category))

    return -2

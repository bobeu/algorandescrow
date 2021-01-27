#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ddv_alts import *
from ddv_input import *
from ddv_global import category, reply_keyboard
from dotenv import load_dotenv
import os
from telegram import Bot

from telegram.ext import (
    Updater,
    CommandHandler,
    Filters,
    ConversationHandler,
    MessageHandler
)
from telegram import ReplyKeyboardMarkup
from ddv_menu import menu
from ddv_core import init_atomic, verify_txn, complete_trade

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
load_dotenv()
TOKEN = os.getenv('TOKEN')


def start(update, context):
    """
    Gives direction for use
    Displays information about the bot and available commands
    :param update:
    :param context:
    :return: None
    """
    dspensr = 'https://bank.testnet.algorand.network/'

    user = update.message.from_user
    reply = "Hi {}!\nI am DDV Escrow Bot.\n\n".format(user['first_name'])
    reply += "This is an Escrow contract to be initiated by the seller of an Algorand standard asset.\n\n" \
             "- It is expected that both parties already agreed to trade.\n- Seller invoke the escrow using the" \
             "secret key to the account where the ASA is deposited.\v - Seller also submits the account's public key " \
             "of the buyer from where the Algo will be sent\n\n - Thereafter the buyer created an escrow, the seller " \
             "may proceed to approving the\ntransaction using the authorization key to the account submitted by the " \
             "seller.\n\nTo test: \n   - /Get_test_account first or find a peer to act as the buyer.\n   " \
             "- Fund the account with testnet Algo from {}\n" \
             "- /Submit your address to our dispenser to get 200 Test DMT2.\n- Then try to trade with someone else" \
             "".format(dspensr)

    update.message.reply_text(reply, reply_markup=reply_keyboard(update, context, category))
    context.user_data.clear()
    return ConversationHandler.conversation_timeout


def help_command(update, context):
    """
    Gives direction for use
    :param update:
    :param context:
    :return: None
    """
    update.message.reply_text("Go to the /Menu.")


def cancel(update, context):
    """
    Terminates a session and disengaged the bot.
    :param update:
    :param context:
    :return: int --> Ends the session
    """
    context.user_data.clear()
    update.message.reply_text(
        "Your message is not recognized!\nSession terminated.", reply_markup=reply_keyboard(update, context, category)
    )
    return -2


def f(update, context):
    k = [['/start'], ]
    km = ReplyKeyboardMarkup(k, one_time_keyboard=True, resize_keyboard=True)
    return update.message.reply_text("Use: ", reply_markup=km), ConversationHandler.END


def main():
    """
    The heart of the bot.
    Keeps track of how program should run.
    Here you specify the token gotten from the BotFather,
    i.e the token for your bot. NB: Keep it secret.

    Updater class employs the telegram.ext.Dispatcher and
    provides a front-end to the bot for the users.
    So, you only need to focus on backend side.

    The ConversationHandler holds a conversation with a single
     user by managing four collections of other handlers
    :return:
    """

    updater = Updater(
        "PASTE YOUR BOT TOKEN HERE",
        use_context=True
    )

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    cul_handler = ConversationHandler(
        entry_points=[
            CommandHandler('Set_up_a_trade', get_args),
            CommandHandler('Verify_transaction', get_args),
            CommandHandler('Approve_trade', get_args),
            CommandHandler('Get_free_asset', get_args),
            CommandHandler('Import_Secret_key', get_args),
            CommandHandler('Check_balance', get_args)
        ],
        states={
            SELECT: [
                MessageHandler(
                    Filters.regex(
                        '^(signing_key|public_key|buyer_address|amount_in_algo|asset_name|Authorization_key|Address|'
                        'Mnemonic|address|quantity_in_ASA|Signing_key)$'
                    ), select_choice),
                CommandHandler('done', init_atomic),
                CommandHandler('getBal', query_balance),
                CommandHandler('getPK', getPK),
                CommandHandler('dispense', dispense),
                CommandHandler('Verify', verify_txn),
                CommandHandler('Approve', complete_trade),
                CommandHandler('Cancel', cancel)

            ],

            SELECTED_CHOICE: [
                MessageHandler(
                    Filters.text
                    & ~(Filters.command | Filters.regex('^Done$')),
                    preview_info,
                )
            ],

            OTHER_CHOICE: [
                MessageHandler(
                    Filters.text
                    & ~(Filters.command | Filters.regex('^Done$')),
                    preview_info_2,
                )
            ],
        },
        fallbacks=[CommandHandler('Done', cancel)],
        allow_reentry=True,

    )

    dp.add_handler(cul_handler)

    dp.add_handler(MessageHandler(Filters.regex('^(start|hey|hi|.|,)$'), f))
    dp.add_handler(CommandHandler('restart', start))
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('Cancel', cancel))
    dp.add_handler(CommandHandler('Help', help_command))
    dp.add_handler(CommandHandler('Menu', menu))
    dp.add_handler(CommandHandler('Get_test_account', get_test_account))

    # Start the Bot
    updater.start_polling()
    # updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
    # updater.bot.setWebhook('https://stormy-meadow-03242.herokuapp.com/' + TOKEN)
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

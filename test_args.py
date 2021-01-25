from algosdk import mnemonic

mn = "vital ignore hen exact mirror cruel flee hint topic stairs check bomb milk hammer " \
     "volume husband chronic wrap hub mass wool rather festival above imitate"

test_dispenser = mnemonic.to_public_key(mn)
test_buyer = "244IND3CFIWL54G5VANIW6YG6F4SUXAWL4SFAFA577QTLRBIFZEFQ2SDBQ"
buyerkey = "m1n1mfd9GgvjyieLsHO0VsEAXJPTZH8j+NgERPwpcxfXOIaPYiosvvDdqBqLewbxeSpcFl8kUBQd/+E1xCguSA=="
sellerkey = mnemonic.to_private_key(mn)
sellerPkey = "qDdc1uTERtIYy2soFzVOkkFGorn+b0OBP92IqH7Jpoo4JsJFOXZ1T+dL+RWD5PVsS5cT/bt49XU1tUi/M9ogOA=="
test_seller = mnemonic.to_public_key(mn)



# Account address:  FPWMTE6Q4OFDPTH3CIDB2SLVIYY4O6WMFJV5ZOWHCATLFAYAP3J3IIQ4GU
#
# Private Key:  f9rf8mfn4nH3yD/pGSxh2unj8OWo6B6SvEKemiXREf4r7MmT0OOKN8z7EgYdSXVGMcd6zCpr3LrHECaygwB+0w==
#
# Mnemonic:
#  exit legal west island shift symbol element divert diamond race correct oval sick label elbow trim duck venture candy prepare enroll inmate vacuum abstract border
#
# Public key: FPWMTE6Q4OFDPTH3CIDB2SLVIYY4O6WMFJV5ZOWHCATLFAYAP3J3IIQ4GU
#
# I do not hold or manage your keys.
# HATMERJZOZ2U7Z2L7EKYHZHVNRFZOE75XN4PK5JVWVEL6M62EA4IWQZHJU


# appdirs==1.4.4
# APScheduler==3.6.3
# beautifulsoup4==4.9.3
# certifi==2020.12.5
# cffi==1.14.4
# chardet==3.0.4
# colorama==0.4.4
# cryptography==3.3.1
# decorator==4.4.2
# distlib==0.3.1
# filelock==3.0.12
# idna==2.10
# lxml==4.5.2
# msgpack==1.0.2
# numpy==1.19.2
# pipenv==2020.8.13
# py-algorand-sdk==1.4.1
# pycparser==2.20
# pycryptodomex==3.9.9
# PyJWT==1.7.1
# PyNaCl==1.4.0
# pyteal==0.6.1
# python-dotenv==0.15.0
# python-telegram-bot==13.1
# pytz==2020.5
# requests==2.24.0
# six==1.15.0
# telegram==0.0.1
# soupsieve==2.0.1
# tornado==6.1
# tzlocal==2.1
# urllib3==1.25.10
# yapf==0.30.0
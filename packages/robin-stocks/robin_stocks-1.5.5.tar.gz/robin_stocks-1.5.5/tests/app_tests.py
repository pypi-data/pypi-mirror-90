import datetime
import sys
import pyotp
import os
from dotenv import load_dotenv
load_dotenv()
import requests

import robin_stocks as r



totp  = pyotp.TOTP(os.environ['robin_mfa']).now()
print("Current OTP:", totp)
login = r.login(os.environ['robin_username'], os.environ['robin_password'], store_session=True, mfa_code=totp)
# print("login data is ", login)

print("===")
print("running test at {}".format(datetime.datetime.now()))
print("===")
# r.set_output(open(os.devnull,"w"))
info = r.get_bank_transfers('received')
print(info)



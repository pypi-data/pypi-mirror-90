from uuid import uuid4
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

userid = "e4fa5751-951c-4d0d-81e0-678d7d4db6b2"
accountid = "5SS73779"
# url = 'https://api.robinhood.com/ach/relationships/{0}/'.format(accountid)
# url = 'https://api.robinhood.com/ach/relationships/'
url = 'https://api.robinhood.com/ach/transfers/' # url for post for withdrawl
# r.set_output(open(os.devnull,"w"))
payload = {
    "amount": 10.0, 
    "direction": "deposit", 
    "ach_relationship": "https://api.robinhood.com/ach/relationships/d5cb8013-f5b6-4da7-a238-a89a022d0025/",
    "ref_id": str(uuid4())
}
info = r.request_post(url, payload)
print(info)

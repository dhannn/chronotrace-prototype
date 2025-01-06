import pyotp
import qrcode
import uuid
from datetime import datetime

from database import *

totp = pyotp.TOTP(pyotp.random_base32(), interval=30)
db = DatabaseConnection()

def get_totp():
    current_token = totp.now()
    print(current_token)

    return {
        'session_id': str(uuid.uuid4()),
        'token': current_token
    }

def generate_qr_code(totp):
    # https://medium.com/@rahulmallah785671/create-qr-code-by-using-python-2370d7bd9b8d
    img = qrcode.make(totp, border=0)
    import os, glob
    for filename in glob.glob("static/qr-*"):
        os.remove(filename)
    img.save(f'static/qr-{totp['token']}.png')

def validate_entry(student_num, token):
    token_validity = totp.verify(token, valid_window=1)
    user_validity = db.is_valid_user(student_num)
    print(token_validity, user_validity)
    return token_validity and user_validity

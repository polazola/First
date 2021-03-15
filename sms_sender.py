import logging as log

def send_sms(msg,phone_num):
    log.info(f"We sent message: {msg} to: {phone_num}")

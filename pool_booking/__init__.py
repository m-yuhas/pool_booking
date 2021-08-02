"""Initialization code for the pool_booking package.  Initialize the logger
here."""


import logging


logging.basicConfig(
    format='%(asctime)s [%(threadName)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('pool_booking.log'),
        logging.StreamHandler()],
    level=logging.DEBUG)

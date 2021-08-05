#!/usr/bin/env python3
"""Entry point for module execution.  This script is meant to run continuously
in the background, booking pool slots automatically, until it is terminated."""


from typing import List, NamedTuple


import argparse
import csv
import datetime
import getpass
import logging
import time


from .booking import Booker, BookingError


def get_preferences(filename: str) -> List[int]:
    """Read a CSV file of desired times and days and return a list whose
    indices represent a day of the week (0 = Monday, ..., 7 = Sunday) and whose
    values represent the desired booking time on that day (in hours).  If no
    booking is desired, the entry is 0. The CSV file should be formatted as
    follows:

    Time | Monday | Tuesday | Wednesday | Thursday | Friday | Saturday | Sunday
    -----+--------+---------+-----------+----------+--------+----------+-------
    800  |   x    |         |     x     |     x    |        |     x    |

    If a cell contains any non-whitespace character, it is interpreted as a
    desired booking slot.  If multiple bookings are scheduled in one day, only
    the latest are used.  The CSV file must contain 8 columns and 13 rows,
    corresponding to Monday thru Sunday and 8h00 thru 19h00 respectively."""
    pref = [0 for i in range(7)]
    hour = 8
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if len(row) != 8:
                raise Exception(f'Expected 8 columns in CSV, not {len(row)}.')
            pref = [
                hour if j.strip() else pref[i] for i, j in enumerate(row[1:])]
            hour += 1
    if hour > 20:
        raise Exception('Can only book slots between 08h00 and 19h00')
    return pref


def get_next_booking(pref: List[int]) -> datetime.datetime:
    """Given a list of preferred booking times and their days of the week,
    find the next booking that needs to be made."""
    now = datetime.datetime.now()
    for inc in range(7):
        hours = pref[(now.weekday() + inc) % 7]
        if hours == 0:
            continue
        candidate = now.replace(hour=0, minute=0, second=0, microsecond=0) + \
            datetime.timedelta(days=inc, hours=hours)
        if candidate > now:
            return candidate
    raise Exception('No booking preferences were found.')


def wait_next_booking(next_booking: datetime.date) -> None:
    """Pause execution until the next booking time is reached."""
    rest = (next_booking - datetime.datetime.now()).total_seconds() // 2
    while datetime.datetime.now() < next_booking and rest > 0:
        logging.debug('Sleeping for %i seconds', rest)
        time.sleep(rest)
        rest = (next_booking - datetime.datetime.now()).total_seconds() // 2


def parse_args() -> NamedTuple:
    """Parse command line arguments.

    Returns:
        NamedTuple containing the name of the schedule file to read and the
        desired logging level.
    """
    parser = argparse.ArgumentParser(description='Automate NTU pool booking.')
    parser.add_argument(
        'schedule_file',
        help='Path to CSV file containing the desired booking times.  The '
             'format of this file is shown in this packages\'s repository; an '
             'example is also provided.')
    parser.add_argument(
        '-l',
        '--log',
        default='INFO',
        help='Logging level for this script.',
        choices=['DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL'])
    return parser.parse_args()


def main() -> None:
    """Entry point for code execution."""
    # Parse command line arguments
    args = parse_args()
    logging.basicConfig(level=logging.getLevelName(args.log))

    # Get login credentials
    username = input('NTU Network User Name: ')
    matricno = input('Matriculation Number: ')
    password = getpass.getpass(prompt='NTU Network Password ')
    booker = Booker(username, password, matricno)

    # Begin main loop
    logging.info('Launching Pool Booking Script...')
    logging.debug('Schedule file: %s', args.schedule_file)
    logging.debug('Logging level: %s', args.log)
    logging.info('Reading preferred booking slots...')
    next_slot = datetime.datetime.now()
    while True:
        try:
            logging.info('Finding next preferred booking slot...')
            next_slot = get_next_booking(get_preferences(args.schedule_file))
        except (AttributeError, IndexError) as error:
            logging.critical(
                'Error occurred reading preferences file.  Please ensure that '
                'the file exists and is in the proper format.')
            logging.critical('Error: %s', str(error))
            logging.critical('Trying again in 1 hour...')
            wait_next_booking(
                datetime.datetime.now() + datetime.timedelta(hours=1))
            continue
        try:
            logging.info('Attempting to book time slot %s...', str(next_slot))
            booker.book(next_slot)
            logging.info('Booking successful!')
        except BookingError as error:
            logging.critical('Failed to book slot %s', str(next_slot))
            logging.critical('Error: %s', str(error))
        sleep_time = next_slot + datetime.timedelta(hours=2)
        logging.info('Sleeping until %s.', str(sleep_time))
        wait_next_booking(sleep_time)


if __name__ == '__main__':
    main()

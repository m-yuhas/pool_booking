"""Class and functions to initialize and maintain a session with the NTU
facilities booking website.  Given a date and time slot, this module contains
the utilities to book it assuming proper login information is provided."""


from typing import Dict, Union


import datetime
import logging
import re


import bs4
import requests


class BookingError(Exception):
    """Exception raised by Booker class when an error occurs during booking due
    to the server not accepting a request."""


class Booker:
    """Booker books slots in the NTU sports facility web page.

    Args:
        username: NTU user name.
        password: NTU password.
        matricno: NTU matriculation number.
    """

    def __init__(self, username: str, password: str, matricno: str) -> None:
        self.username = username
        self.password = password
        self.matricno = matricno.upper()
        self.cookie_jar = {}

    def authenticate(self) -> None:
        """Authenticate with the NTU facilities booking web page.  Return the
        dictionary required to verify successful authentication for future
        requests.

        Raises:
            BookingError: if the authentication fails.
        """
        response = requests.post(
            'https://sso.wis.ntu.edu.sg/webexe88/owa/sso.asp',
            headers=self.get_headers(),
            data={
                'Domain': 'STUDENT',
                'PIN': self.password,
                'UserName': self.username,
                'bOption': 'OK',
                'extra': '',
                'map': '',
                'p2': 'https://wis.ntu.edu.sg/pls/webexe88/'
                      'srce_smain_s.Notice_O',
                'pg': '',
                't': '1',
                'title': ''})
        logging.debug(
            'POST to login page returned status code: %i',
            response.status_code)
        if 'Generation completed' not in response.text:
            logging.error(
                'Authentication failed: token generation not completed.')
            raise BookingError('Authentication failed')
        self.cookie_jar = response.cookies.get_dict()
        logging.debug('Received the following cookies:')
        for key, value in self.cookie_jar.items():
            logging.debug('%s: %s', key, value)

    def get_headers(self) -> Dict[str, str]:
        """Construct headers for a request.

        Returns:
            Dictionary containing the header data for a given request.
        """
        return {
            'Accept': 'text/html,application/xhtml+xml,application/xml;'
                      'q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-us',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'sso.wis.ntu.edu.sg',
            'Origin': 'https://sso.wis.ntu.edu.sg',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                          'AppleWebKit/605.1.15 (KHTML, like Gecko) '
                          'Version/14.1.1 Safari/605.1.15',
            'Cookie': ';'.join(
                [f'{key}={value}' for key, value in self.cookie_jar.items()])}

    def check_schedule(self) -> Dict[datetime.datetime, Union[str, None]]:
        """Get the availabe booking slots for the comming week.  Note: this
        code is very brittle and small changes to the format of the booking
        page could break it.

        Returns:
            Dictionary whose keys are a datetime object corresponding to the
            start of a booking slot and whose values are a string containing
            the lane information required to book this slot if desired.  If the
            value for a booking slot is None, it means there are no available
            lanes at that time.

        Raises:
            BookingError: if something went wrong while parsing the schedule
            page contents OR if the schedule page cannot be reached.  The
            error message accompanying the BookingError will provide more
            details depending on the case.
        """
        response = requests.get(
            f'https://wis.ntu.edu.sg/pls/webexe88/srce_smain_s.srce$sel31_o?'
            f'p1={self.matricno}&p2=&p_info=2SP225',
            headers=self.get_headers())
        logging.debug(
            'GET from schedule page returned status code: %i',
            response.status_code)
        if response.status_code != 200:
            raise BookingError('Schedule page not available.')
        try:
            slots = {}
            rows = bs4.BeautifulSoup(
                response.text,
                features='html.parser').find(
                    'table',
                    style='border-collapse:collapse;').find_all('tr')
            dates = {}
            for idx, cell in enumerate(rows[0].find_all('td')[2:]):
                date = re.match(
                    r'(?P<day>\d{2})(?P<month>\D{3})\s+(?P<year>\d{4})',
                    cell.get_text()).groupdict()
                dates[idx] = datetime.datetime(
                    int(date['year']),
                    datetime.datetime.strptime(date['month'], '%b').month,
                    int(date['day']))
            hour = 0
            for row in rows[1:]:
                cells = row.find_all('td')
                if len(cells) == 10:
                    hour = int(
                        re.match(
                            r'(\d{2})\d{2}\s+\-\s+\d{4}',
                            cells[0].get_text())[1])
                    cells = cells[1:]
                cells = cells[1:]
                for idx, cell in enumerate(cells):
                    content = cell.find('input')
                    cell_date = datetime.datetime(
                        dates[idx].year,
                        dates[idx].month,
                        dates[idx].day,
                        hour=hour)
                    if cell_date not in slots:
                        slots[cell_date] = None
                    if content:
                        slots[cell_date] = content.get('value')
            return slots
        except AttributeError as error:
            logging.error(
                'Could not check schedule.  This is likey do to a page format '
                'change.  Please open an issue on Github to notify the repo '
                'maintainers. ')
            raise BookingError('Could not parse schedule.') from error

    def book_slot(self, slot: datetime.datetime, info: str) -> None:
        """Book a slot with the information received from check_schedule.

        Args:
            slot: the date and hour of the desired booking.
            info: the info about the open slot based on the response from
            check_schedule.

        Raises:
            BookingError: if the booking cannot be completed.
        """
        # Book
        response = requests.post(
            'https://wis.ntu.edu.sg/pls/webexe88/srce_sub1.srceb$sel32',
            headers=self.get_headers(),
            data={
                'p_rec': info,
                'p1': self.matricno,
                'p2': '',
                'p_info': '2SP225'})
        logging.debug(
            'POST to booking page returned status code: %i',
            response.status_code)
        frmk = ''
        p_info = ''
        try:
            soup = bs4.BeautifulSoup(response.text, features='html.parser')
            frmk = soup.find('input', {'name': 'frmk'}).get('value')
            p_info = soup.find('input', {'name': 'P_info'}).get('value')
        except AttributeError as error:
            raise BookingError('Initial booking failed.') from error
        logging.debug('frmk=%s', frmk)
        logging.debug('P_info=%s', p_info)

        # Confirm
        response = requests.post(
            'https://wis.ntu.edu.sg/pls/webexe88/srce_sub1.srceb$sel33',
            headers=self.get_headers(),
            data={
                'noaguest': '0',
                'frmfrom': 'selfbook',
                'p1': self.matricno,
                'p2': '',
                'fdate': slot.strftime('%d-%b-%Y'),
                'fcode': 'SP',
                'floc': f'SP{info[6:8]}',
                'sno': slot.hour - 7,
                'stype': 'D',
                'paytype': 'CC',
                'fcourt': f'{int(info[6:8])}',
                'ftype': '2',
                'rptype': '2',
                'P_info': p_info,
                'opmode': '1',
                'frmk': frmk,
                'bOption': 'Confirm'})
        logging.debug(
            'POST to confirmation page returned status code: %i',
            response.status_code)
        if 'Official Permit' not in response.text:
            logging.error('Confirmation failed: invalid access.')
            raise BookingError('Booking confirmation failed')

    def book(self, time: datetime.datetime) -> None:
        """Book a lane in the pool at a desired time.  The next free lane
        will always be booked unless there are no more lanes available at that
        time.

        Args:
            time: a datetime object referring to the desired pool booking time.

        Raises:
            BookingError: if no slot is available at that the desired time.
        """
        self.authenticate()
        slots = self.check_schedule()
        if slots[time] is None:
            raise BookingError('No avaiable places at the desired time.')
        self.book_slot(time, slots[time])

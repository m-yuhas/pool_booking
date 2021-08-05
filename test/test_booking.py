"""Unit test cases for the booking module."""


from typing import Dict, NamedTuple


import collections
import datetime
import os
import unittest
import unittest.mock


import pool_booking.booking


TEST_COOKIE_JAR = {
    'NTUDMTYPE': '1',
    'TS014010ab': 'REDACTED',
    'mobi': 'N',
    'ntutestcookie': 'TEST',
    'TS01ba27f6': 'REDACTED',
    'NTUBAF4CA507737C55512A53913A8FCF8CB1700': 'REDACTED',
    'TS01a090a4': 'REDACTED',
    'mstrImpersonateFlag': 'N',
    'myNTUid': 'REDACTED',
    'ASPSESSIONIDCGCCTADD': 'REDACTED'}


MockResponse = collections.namedtuple(
    'MockResponse',
    ['cookies', 'headers', 'status_code', 'text'])


class MockCookieJar(NamedTuple):
    """Class to mock requests.CookieJar."""
    cookies: Dict[str, str]

    def get_dict(self) -> Dict[str, str]:
        """Return a dictionary of cookies, just like
        requests.CookieJar.get_dict().

        Returns:
            Dictionary of cookies stored in this obejct.
        """
        return self.cookies


def mock_request_fail(url: str, **kwargs) -> MockResponse:
    """Mock the server response in the case of a 404 status code.

    Args:
        url: URL the caller is trying to access.

    Returns:
        MockResponse containing generic data for when a 404 error occurs.
    """
    return MockResponse(
        cookies={},
        headers={**kwargs['headers'], **{'Referer': url}},
        status_code=404,
        text='')


def mock_auth_success(url: str, **kwargs) -> MockResponse:
    """Mock the server response when authentication succeeds.

    Args:
        url: URL the caller is trying to access.

    Returns:
        MockResponse containing a typical example of a response page when
        authentication is successful.
    """
    response_path = os.path.join('test_assets', 'authentication_success.html')
    text = ''
    with open(response_path, 'r') as response:
        text = response.read()
    return MockResponse(
        cookies=MockCookieJar(TEST_COOKIE_JAR),
        headers={**kwargs['headers'], **{'Referer': url}},
        status_code=200,
        text=text)


def mock_schedule_fchange(url: str, **kwargs) -> MockResponse:
    """Mock the server response when the format of the schedule page changes.

    Args:
        url: URL the caller is trying to access.

    Returns:
        MockResponse containing a schedule page with an unknown format.
    """
    response_path = os.path.join('test_assets', 'schedule_formatchange.html')
    text = ''
    with open(response_path, 'r') as response:
        text = response.read()
    return MockResponse(
        cookies=MockCookieJar(TEST_COOKIE_JAR),
        headers={**kwargs['headers'], **{'Referer': url}},
        status_code=200,
        text=text)


def mock_schedule_success(url: str, **kwargs) -> MockResponse:
    """Mock the server response when getting the schedule page succeeds.

    Args:
        url: URL the caller is trying to access.

    Returns:
        MockResponse containing a typical example of a schedule page.
    """
    response_path = os.path.join('test_assets', 'schedule_success.html')
    text = ''
    with open(response_path, 'r') as response:
        text = response.read()
    return MockResponse(
        cookies=MockCookieJar(TEST_COOKIE_JAR),
        headers={**kwargs['headers'], **{'Referer': url}},
        status_code=200,
        text=text)


def mock_book_invalidaccess(url: str, **kwargs) -> MockResponse:
    """Mock the server response when the 'Invalid access' error occurs on
    booking confirmation.

    Args:
        url: URL the caller is trying to access.

    Returns:
        MockResponse containing a successful inital booking, but a a failure if
        the confirmation url is received.
    """
    text = 'Invalid access.'
    if url.endswith('sel32'):
        response_path = os.path.join(
            'test_assets',
            'confirmation_success.html')
        with open(response_path, 'r') as response:
            text = response.read()
    return MockResponse(
        cookies=MockCookieJar(TEST_COOKIE_JAR),
        headers={**kwargs['headers'], **{'Referer': url}},
        status_code=200,
        text=text)


def mock_book_success(url: str, **kwargs) -> MockResponse:
    """Mock the server response on a successful booking.

    Args:
        url: URL the caller is trying to access.

    Returns:
        MockResponse containing successful confirmation and information needed
        for the confirmation.
    """
    response_path = os.path.join('test_assets', 'confirmation_success.html')
    text = ''
    with open(response_path, 'r') as response:
        text = response.read()
    return MockResponse(
        cookies=MockCookieJar(TEST_COOKIE_JAR),
        headers={**kwargs['headers'], **{'Referer': url}},
        status_code=200,
        text=text)


class TestConstructor(unittest.TestCase):
    """Test case for Booker class's constructor."""

    def test_constructor(self) -> None:
        """Ensure all provided values are stored in the proper format and
        class attributes are initialized properly."""
        booker = pool_booking.booking.Booker('abc123', 'def456', 'ghi789')
        self.assertEqual('abc123', booker.username)
        self.assertEqual('def456', booker.password)
        self.assertEqual('GHI789', booker.matricno)
        self.assertDictEqual({}, booker.cookie_jar)


class TestAuthentication(unittest.TestCase):
    """Test case for the Booker class's authentication method."""

    @unittest.mock.patch('requests.post', side_effect=mock_request_fail)
    def test_authentication_failure(self, mock_post) -> None:
        """Ensure that the authentication method raises an exception on
        failure."""
        booker = pool_booking.booking.Booker('abc', 'def', 'ghi')
        self.assertRaises(
            pool_booking.booking.BookingError,
            booker.authenticate)
        self.assertIn('headers', mock_post.call_args.kwargs)
        self.assertIn('data', mock_post.call_args.kwargs)
        mock_post.assert_called_once()

    @unittest.mock.patch('requests.post', side_effect=mock_auth_success)
    def test_authentication_success(self, mock_post) -> None:
        """Ensure cookie jar is updated properly on authentication success."""
        booker = pool_booking.booking.Booker('abc', 'def', 'ghi')
        booker.authenticate()
        self.assertDictEqual(TEST_COOKIE_JAR, booker.cookie_jar)
        self.assertIn('headers', mock_post.call_args.kwargs)
        self.assertIn('data', mock_post.call_args.kwargs)
        mock_post.assert_called_once()


class TestGetHeaders(unittest.TestCase):
    """Test case for the Booker class's get_headers method."""

    def test_get_headers(self) -> None:
        """Ensure headers dictionary contains the necessary keys."""
        booker = pool_booking.booking.Booker('abc', 'def', 'ghi')
        booker.cookie_jar = TEST_COOKIE_JAR
        self.assertIn('Upgrade-Insecure-Requests', booker.get_headers())
        self.assertIn('User-Agent', booker.get_headers())
        self.assertIn('Cookie', booker.get_headers())

    def test_get_headers_no_cookies(self) -> None:
        """Ensure the format of the 'Cookeies' key is correct when no cookies
        have been received yet."""
        booker = pool_booking.booking.Booker('abc', 'def', 'ghi')
        self.assertIn('Upgrade-Insecure-Requests', booker.get_headers())
        self.assertIn('User-Agent', booker.get_headers())
        self.assertIn('Cookie', booker.get_headers())
        self.assertEqual('', booker.get_headers()['Cookie'])


class TestCheckSchedule(unittest.TestCase):
    """Test case for the Booker class's check_schedule method."""

    @unittest.mock.patch('requests.get', side_effect=mock_request_fail)
    def test_get_failure(self, mock_get) -> None:
        """Ensure that the check_schedule method raises an exception on
        get failure."""
        booker = pool_booking.booking.Booker('abc', 'def', 'ghi')
        self.assertRaises(
            pool_booking.booking.BookingError,
            booker.check_schedule)
        self.assertIn('headers', mock_get.call_args.kwargs)
        mock_get.assert_called_once()

    @unittest.mock.patch('requests.get', side_effect=mock_schedule_fchange)
    def test_format_change(self, mock_get) -> None:
        """Ensure that the check_schedule method raises an exception if the
        schedule page format has changed."""
        booker = pool_booking.booking.Booker('abc', 'def', 'ghi')
        self.assertRaises(
            pool_booking.booking.BookingError,
            booker.check_schedule)
        self.assertIn('headers', mock_get.call_args.kwargs)
        mock_get.assert_called_once()

    @unittest.mock.patch('requests.get', side_effect=mock_schedule_success)
    def test_get_success(self, mock_get) -> None:
        """Ensure that the check_schedule method correctly parses the schedule
        page on a valid response."""
        booker = pool_booking.booking.Booker('abc', 'def', 'ghi')
        booker.check_schedule()  # Remember to validate response
        self.assertIn('headers', mock_get.call_args.kwargs)
        mock_get.assert_called_once()


class TestBookSlot(unittest.TestCase):
    """Test case for the Booker class's book_slot method."""

    @unittest.mock.patch('requests.post', side_effect=mock_request_fail)
    def test_post_fail(self, mock_post) -> None:
        """Ensure that the book_slot method raises an exception on post
        failure."""
        booker = pool_booking.booking.Booker('abc', 'def', 'ghi')
        with self.assertRaises(pool_booking.booking.BookingError):
            booker.book_slot(datetime.datetime.now(), '2SP2SP2201-Aug-20211')
        self.assertIn('headers', mock_post.call_args.kwargs)
        self.assertIn('data', mock_post.call_args.kwargs)

    @unittest.mock.patch('requests.post', side_effect=mock_book_invalidaccess)
    def test_confirmation_fail(self, mock_post) -> None:
        """Ensure that the book_slot method raises an exception when the
        'Invalid access' response occurs on the confirmation request."""
        booker = pool_booking.booking.Booker('abc', 'def', 'ghi')
        with self.assertRaises(pool_booking.booking.BookingError):
            booker.book_slot(datetime.datetime.now(), '2SP2SP2201-Aug-20211')
        self.assertIn('headers', mock_post.call_args.kwargs)
        self.assertIn('data', mock_post.call_args.kwargs)

    @unittest.mock.patch('requests.post', side_effect=mock_book_success)
    def test_success(self, mock_post) -> None:
        """Ensure that no exception is raised in the case of a successful
        booking."""
        booker = pool_booking.booking.Booker('abc', 'def', 'ghi')
        booker.book_slot(datetime.datetime.now(), '2SP2SP2201-Aug-20211')
        self.assertIn('headers', mock_post.call_args.kwargs)
        self.assertIn('data', mock_post.call_args.kwargs)


if __name__ == '__main__':
    unittest.main()

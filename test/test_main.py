"""Unit test cases for the __main__ module."""


import datetime
import os
import time
import unittest


import pool_booking.__main__


class TestGetPreferences(unittest.TestCase):
    """Test case for get_preferences function."""

    def test_good_csv(self) -> None:
        """Check that output is correct when parsing a properly formatted
        CSV file."""
        path = os.path.join('test_assets', 'pass.csv')
        preferences = pool_booking.__main__.get_preferences(path)
        self.assertEqual([0, 8, 8, 8, 8, 0, 8], preferences)

    def test_csv_too_many_rows(self) -> None:
        """Check that an exception is raised if the CSV has too many rows."""
        path = os.path.join('test_assets', 'fail_rows.csv')
        with self.assertRaises(Exception):
            pool_booking.__main__.get_preferences(path)

    def test_csv_too_many_columns(self) -> None:
        """Check that an exception is raised if the CSV has too many
        columns."""
        path = os.path.join('test_assets', 'fail_columns.csv')
        with self.assertRaises(Exception):
            pool_booking.__main__.get_preferences(path)


class TestWaitNextBooking(unittest.TestCase):
    """Test case for get_next_booking function."""

    def test_wait_next_booking(self) -> None:
        """Ensure that the wait_next_booking function waits at least the
        required amount of time."""
        start = time.time()
        pool_booking.__main__.wait_next_booking(
            datetime.datetime.now() + datetime.timedelta(seconds=10))
        stop = time.time()
        self.assertGreater(10, stop - start)


if __name__ == '__main__':
    unittest.main()

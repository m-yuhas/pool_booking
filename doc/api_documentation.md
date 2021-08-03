
# pool_booking
Initialization code for the pool_booking package.  Initialize the logger
here.

# pool_booking.booking
Class and functions to initialize and maintain a session with the NTU
facilities booking website.  Given a date and time slot, this module contains
the utilities to book it assuming proper login information is provided.

## BookingError
```python
BookingError()
```
Exception raised by Booker class when an error occurs during booking due
to the server not accepting a request.

## Booker
```python
Booker(self, username: str, password: str, matricno: str)
```
Booker books slots in the NTU sports facility web page.

Args:
    username: NTU user name.
    password: NTU password.
    matricno: NTU matriculation number.


### authenticate
```python
Booker.authenticate()
```
Authenticate with the NTU facilities booking web page.  Return the
dictionary required to verify successful authentication for future
requests.

Raises:
    BookingError: if the authentication fails.


### get_headers
```python
Booker.get_headers()
```
Construct headers for a request.

Returns:
    Dictionary containing the header data for a given request.


### check_schedule
```python
Booker.check_schedule()
```
Get the availabe booking slots for the comming week.  Note: this
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


### book_slot
```python
Booker.book_slot(slot: datetime, info: str)
```
Book a slot with the information received from check_schedule.

Args:
    slot: the date and hour of the desired booking.
    info: the info about the open slot based on the response from
    check_schedule.

Raises:
    BookingError: if the booking cannot be completed.


### book
```python
Booker.book(time: datetime)
```
Book a lane in the pool at a desired time.  The next free lane
will always be booked unless there are no more lanes available at that
time.

Args:
    time: a datetime object referring to the desired pool booking time.

Raises:
    BookingError: if no slot is available at that the desired time.


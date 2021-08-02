# Pool Booking
[中文指南](https://github.com/m-yuhas/pool_booking/blob/main/doc/读我档案.md)

[Documentación en español](https://github.com/m-yuhas/pool_booking/blob/main/doc/LÉAME.md)

[Documentation en français](https://github.com/m-yuhas/pool_booking/blob/main/doc/LISEZ-MOI.md)

## Introduction
This Python package simplifies the NTU pool booking process.  For those of us
who swim everyday and don't change our schedules from week to week, we wish
there was some way to just specify in advance the times we want to book and not
have to manually login everyday to find a spot.  This package reads a
predefined weekly schedule from a CSV file and attempts to book those slots at
the pool if they are available.

## Quick Start

### Optional: Set up a Virtual Environment
If you haven't already done so, setting up virtual environments can help ensure
that this package does not interfere with other python packages you may already
have installed on your system.  There are many virtual environment managers for
Python, for example: [venv](https://docs.python.org/3/library/venv.html),
[Virtualenv](https://docs.python.org/3/library/venv.html),
[Pipenv](https://pipenv.pypa.io/en/latest/),
[Conda](https://docs.conda.io/en/latest/), and
[Poetry](https://python-poetry.org).  These instructions will walk you through
the process on Pipenv, but you can use any of the aformentioned virtual
environment managers:

1. Install Pipenv:
```
pip installl pipenv
```

2. Create a new virtual environment and launch it:
```
pipenv shell
```

### Installation
3. If you are using Pipenv:
```
pipenv install git+https://github.com/m-yuhas/pool_booking.git
```

4. Otherwise:
```
pip install git+https://github.com/m-yuhas/pool_booking.git
```

### Running
5. First take the *times.csv* file present in the root directory of this
  repository and store it on your computer.  Put an 'X' in each cell when you
  would like to book that slot at the swimming pool.  (Note: only one booking
  per day is allowed.)  For example:

| Time | Monday | Tuesday | Wednesday | Thursday | Friday | Saturday | Sunday |
|------|--------|---------|-----------|----------|--------|----------|--------|
| 0800-0900 | | | | | | | X |
| 0900-1000 | | X | X | X | X | | |
| 1000-1100 | | | | | | | |
| 1100-1200 | | | | | | | |
| 1200-1300 | | | | | | | |
| 1300-1400 | | | | | | | |
| 1400-1500 | | | | | | | |
| 1500-1600 | | | | | | | |
| 1600-1700 | | | | | | | |
| 1700-1800 | | | | | | | |
| 1800-1900 | | | | | | | |
| 1900-2000 | X | | | | | X | |

6. Launch the package from the directory where your *times.csv* file is
  located:
```
python -m pool_booking times.csv
```

7. Enter you username, password, and matriculation number and the script will
  begin running.
8. Because this script runs for prolonged periods of time, you may want to
  launch it with *nohup* so it keeps running even after you kill your terminal
  session.
```
nohup python -m pool_booking times.csv
```

9. You can monitor the progress of the script by observing the
  *pool_booking.log* file it generates in the directory where you launched it:
```
tail pool_booking.log
```

## Dependencies
Only Python version 3.6 and greater are supported. This package should run on
any POSIX system as well as Windows 7 and greater.

The following packages are used:
* [beatifulsoup4](https://www.crummy.com/software/BeautifulSoup/)
* [requests](https://docs.python-requests.org/en/master/)

## Contributing
Suggestions and pull requests are welcome. If you find a bug and don't have
time to fix it yourself, feel free to open an issue.

## Future Tasks
* Increase unit test coverage:
  * Figure out how to mock multiple functions in one test
  * Figure out how to mock built-in functions like datetime.datetime.now()
* Expand booking capability to other facilities besides the swimming pool
* Push desktop notifications on successful booking or booking failure
* Package as a systemd service

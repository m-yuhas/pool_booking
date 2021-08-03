# Réservation de Piscine

## Introduction
Ce paquet Python simplifie le processus de réservation de piscine d'NTU.  À
nous qui nageons chaque jour et ne changeons pas nos horaires d'une semaine à
l'autre, nous souhaitons qu'il y ait une façon à spécifier d'avance les temps
que nous voulions réserver et nous n'ayons pas besoin d'entrer manuellement
chaque jour pour trouver une place.  Ce paquet lit un horaire prédéfini
hebdomadaire d'un fichier CSV et tente de réserver celles places à la piscine
si elles sont disponibles.

## Lancement Rapide

### Optionnel: Instaurer un Environnement Virtuel
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

### Exploitation
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

## Dépendances
Only Python version 3.6 and greater are supported. This package should run on
any POSIX system as well as Windows 7 and greater.

The following packages are used:
* [beatifulsoup4](https://www.crummy.com/software/BeautifulSoup/)
* [requests](https://docs.python-requests.org/en/master/)

## Contribuer
Suggestions and pull requests are welcome. If you find a bug and don't have
time to fix it yourself, feel free to open an issue.

## Tâches Futures
* Increase unit test coverage:
  * Figure out how to mock multiple functions in one test
  * Figure out how to mock built-in functions like datetime.datetime.now()
* Expand booking capability to other facilities besides the swimming pool
* Push desktop notifications on successful booking or booking failure
* Package as a systemd service

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
Si vous ne l'avez pas déjà fait, mettre en place un environnement virtuel peut
aider à assurer que ce paquet n'interfère pas avec les autres paquets Python
que vous auriez pu déjà installés dans votre système.  Il y a beaucoup de
gestionnaires d'environnements virtuels pour Python, par exemple:
[venv](https://docs.python.org/3/library/venv.html),
[Virtualenv](https://docs.python.org/3/library/venv.html),
[Pipenv](https://pipenv.pypa.io/en/latest/),
[Conda](https://docs.conda.io/en/latest/), et
[Poetry](https://python-poetry.org).  Ces instructions expliqueront le
processus en utilisant Pipenv, mais vous pouvez utiliser quelconque des
gestionnaires d'environnements virtuels susmentionnés:

1. Installez Pipenv:
```
pip installl pipenv
```

2. Créez un environnement virtuel et le lancez:
```
pipenv shell
```

### Installation
3. Si vous êtes utilisant Pipenv:
```
pipenv install git+https://github.com/m-yuhas/pool_booking.git#egg=pool_booking
```

4. Autrement:
```
pip install git+https://github.com/m-yuhas/pool_booking.git#egg=pool_booking
```

### Exploitation
5. Première prenez le fichier *times.csv* dans le directoire racine de ce dépôt
  et l'enregistrez dans votre ordinateur.  Mettez un 'X' dans chaque cellule
  quand vous voudriez réserver cette place à la piscine. (Veuillez noter:
  seulement se permet une réservation par jour.)  Par exemple:

| Temps | Lundi | Mardi | Mercredi | Jeudi | Vendredi | Samedi | Dimanche |
|-------|-------|-------|----------|-------|----------|--------|----------|
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

6. Lancez le paquet du directoire où se trouve votre fichier *times.csv*:
```
python -m pool_booking times.csv
```

7. Entrez votre nom d'utilisateur, mot de passe, et numéro d'immatriculation et
  la scripte commencera fonctionner.
8. Parce que cette script opère pour périodes prolongées, Peut-être que vous la
  vouliez lancer avec *nohup* afin qu'elle continuera fonctionner même après
  vous tuez votre session du terminal:
```
nohup python -m pool_booking times.csv
```

9. Vous pouvez surveiller le progrès de la script en observant le fichier
  *pool_booking.log* qu'elle produit dans le directoire où vous l'avez lancé.
```
tail pool_booking.log
```

## Dépendances
Seulement les versions Python 3.6 et plus sont soutenues.  Ce paquet doit
pouvoir exploité dans tous les systèmes POSIX aussi bien que Windows 7 et plus.

Les paquets suivants sont utilisés:
* [beatifulsoup4](https://www.crummy.com/software/BeautifulSoup/)
* [requests](https://docs.python-requests.org/en/master/)

## Contribuer
Suggestions et demandes de tirage sont bienvenus.  Si vous trouvez un bogue et
vous n'avez pas les temps pour la réparer vous-même, n'hesitez pas ouvrir un
problème.

## Tâches Futures
* Augmenter la couverture des tests unitaires:
  * Déterminer comment moquer plusieurs fonctions dans un test
  * Déterminer comment moquer functions intégrées comme datetime.datetime.now()
* Accroître la capacité de réservation à autres aménagements en plus de la
  piscine
* Emballer comme un service systemd

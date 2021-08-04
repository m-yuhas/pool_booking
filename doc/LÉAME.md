# Reserva de Piscina

## Introducción
Este paquete Python simplifica el proceso de reserva de piscina de NTU.  A
nosotros quiénes nadamos cada día y no cambiamos nuestros horarios entre
semanas, deseamos que haya alguna manera para especificar de antemano los
tiempos que queramos reservar y que no necesitemos manualmente ingresar cada
día para encontrar un lugar.  Este paquete lee un horario predefinido semanal
de un archivo CSV y intenta reservar aquellos huecos a la piscina si están
disponibles.

## Comienzo Rápido

### Opcional: Establecer un Ambiento Virtual
Si todavía no hizo así, estableciendo un ambiento virtual puede ayudar asegurar
que este paquete no interfiera con otros paquetes Python que ya habría podido
instalado en su sistema.  Hay muchos gerentes de ambientos virtuales para
Python, por ejemplo: [venv](https://docs.python.org/3/library/venv.html),
[Virtualenv](https://docs.python.org/3/library/venv.html),
[Pipenv](https://pipenv.pypa.io/en/latest/),
[Conda](https://docs.conda.io/en/latest/), y
[Poetry]( yhttps://python-poetry.org).  Estas instrucciones explicarán el
proceso en Pipenv, pero puede usar alguno de los gerentes de ambientos
virtuales susodichos:

1. Instale Pipenv:
```
pip installl pipenv
```

2. Cree un ambiento virtual nuevo y lo lance:
```
pipenv shell
```

### Instalación
3. Si usa usted Pipenv:
```
pipenv install git+https://github.com/m-yuhas/pool_booking.git#egg=pool_booking
```

4. De lo contrario:
```
pip install git+https://github.com/m-yuhas/pool_booking.git#egg=pool_booking
```

### Ejecutar
5. Primero tome el archivo *times.csv* que se ubica en el directorio raíz de
  este repositorio y lo cargue en su computadora.  Ponga un 'X' en cada celda
  cuando quiera reservar aquello hueco a la piscina.  (Por favor note: solo se
  permite una reserva por día.)  Por ejemplo:

| Tiempo | Lunes | Martes | Miércoles | Jueves | Viernes | Sábado | Domingo |
|--------|-------|--------|-----------|--------|---------|--------|---------|
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

6. Lance el paquete del directorio dónde se ubica su archivo de *times.csv*:
```
python -m pool_booking times.csv
```

7. Entre su nombre de usuario, contraseña, y número de matriculación y el
  script comenzará ejecutar.
8. Porque este script ejecuta por periodos prolongados, tal vez quiera
  lancarlo con *nohup* así continuará ejecutar aún después de mata su sesión
  del terminal:
```
nohup python -m pool_booking times.csv
```

9. Puede supervisar el progreso del script en observando el archivo
  *pool_booking.log* que genera en el directorio en el cual lo lanzó.
```
tail pool_booking.log
```

## Dependencias
Solo las versiones Python 3.6 y arriba están apoyadas.  Este paquete debe poder
ejecutado en alguno sistema POSIX además de Windows 7 y arriba.

Usa los paquetes siguientes:
* [beatifulsoup4](https://www.crummy.com/software/BeautifulSoup/)
* [requests](https://docs.python-requests.org/en/master/)

## Contribuir
Sugestiones y pull requests son bienvenidos. Si encuentra un error de
programación y no tiene el tiempo para arreglarlo su mismo, por supuesto abra
un asunto en Github.

## Tareas Futuras
* Aumentar la cobertura de las pruebas unitarias:
  * Resolver cómo imitar funciones múltiples en una prueba
  * Resolver cómo imitar funciones empotradas como datetime.datetime.now()
* Ampliar la capacidad de reserva a otras facilidades además de la piscina
* Empujar notificaciones al escritorio en el caso de un éxito o un fracaso
* Empaquetar como un servicio systemd

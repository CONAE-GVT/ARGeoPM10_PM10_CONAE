Training - Proyecto EMPATIA

Este script fue elaborado para incorporar a la tabla con los valores de AOD MAIAC de cada órbita para el pixel de cada estacion
superficial de PM, los valores correspondientes a dicho pixel de las bases de datos de MERRA-2 (valor con fecha y hora más cercano a dicha órbita), VIIRS (luces
de noche, un valor anual por estación) y DEM (altura sobre el nivel del mar, un valor por estación) y los valores de PM 10 de cada estacion superficial correspondientes
a la fecha-hora mas cercanos a la hora de pasada del satelite (orbita).

Se obtienen tablas intermedias a medida que se completa con cada base de datos y la tabla final para el entrenamiento denominada: 
TABLA_ENTRENAMIENTO_2010-2019_MAIAC_MERRA_VIIRS_DEM_PM.csv

# PROJECT: EMPATIA 
# CREATED BY: LARA S. DELLA CECA dellaceca.lara@gmail.com
# DATE: 01/11/2020
# LAST MODIFICATION: 03/11/2020
# OBJECTIVE: COMPLETE AOD (MAIAC/MODIS) ORBIT DAILY DATA TABLE WITH MERRA-2, VIIRS AND DEM -> PIXEL CORRESPONDING TO PM GROUND-BASED STATIONS
#            AND PM DATA CORRESPONDING TO NEAREST DATE-TIME PM STATIONS MEASUREMENTS.


Training - Proyecto EMPATIA

Este script fue elaborado para procesar los archivos HDF5 del producto VNP46A1 - VIIRS / NPP (luces nocturnas) descargado de https://ladsweb.modaps.eosdis.nasa.gov/
para los meses abril a junio del periodo 2012-2019.

Abre los archivos diarios HDF5 para obtener el subdataset DNB_At_Sensor_Radiance_500m, los resamplea según el archivo raster MOSAICO_MAIAC_dominio_modelo.tif (1 km de res. espacial, WGS84)
y guarda el resultado en formato TIF. 

# PROJECT: EMPATIA 
# CREATED BY: LARA S. DELLA CECA dellaceca.lara@gmail.com
# DATE: 21/10/2020
# LAST MODIFICATION: 21/10/2020
# OBJECTIVE: RESAMPLE AND SAVE AS TIF DAILY VIIRS DNB_At_Sensor_Radiance_500m SUBDATASET
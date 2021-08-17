Training - Proyecto EMPATIA

Este script fue elaborado para:
1- abrir los archivos diarios del producto MCD19A2 en formato HDF del mosaico h13v12 de MODIS
2- obtener el AOD a 470nm y 550nm para cada órbita (de Terra y Aqua disponibles para ese día) y filtrar el producto por la banda QA
3- reproyectar el resultado a WGS84
4- guardar un raster en formato TIF para cada órbita individual y longitud de onda


Los archivos de MAIAC descargados desde el servidor MOTA (https://e4ftl01.cr.usgs.gov/MOTA/) se encuentran organizados en carpetas por mosaico y año:
 
  DIRECTORIO MOSAICO
                   └ DIRECTORIO AÑO
                                  └ archivos HDF diarios producto MCD19A2



# PROJECT: EMPATIA 
# CREATED BY: LARA S. DELLA CECA dellaceca.lara@gmail.com
# DATE: 21/10/2020
# LAST MODIFICATION: 21/10/2020
# OBJECTIVE: OPEN hdf MAIAC/MODIS FILES, FILTER AOD BY QUALITY BAND, REPROJECT TO WGS84 AND SAVE INDIVIDUAL ORBITS AS .tif FOR AOD AT 470 AND 500 nm SEPARATELY 

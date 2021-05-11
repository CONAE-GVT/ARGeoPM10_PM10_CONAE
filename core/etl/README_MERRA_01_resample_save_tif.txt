Training - Proyecto EMPATIA

Este script fue elaborado para:
1- abrir el archivo .nc de MERRA-2
2- obtener los atributos (variables atmosfericas y climaticas) correspondientes a la hora de pasada del sensor MODIS (Terra y Aqua) como raster individuales
3- resamplear los raster obtenidos en el punto 2 a la grilla de 1 km (WGS84) de MODIS para todo el territorio argentino
4- guardar los raster obtenidos en el punto 3 como .tif


Los archivos de MERRA-2 descargados de https://disc.gsfc.nasa.gov/ se encuentran organizados en 4 carpetas que corresponden a los productos originales que contienen distintas variables (atributos) de interés para el proyecto:

  DIRECTORIO (producto)                       Variables (atributos que contiene)
     tavg1_2d_aer_Nx          BCSMASS, DMSSMASS, DUSMASS, OCSMASS, SO2SMASS, SO4SMASS, SSSMASS
     tavg1_2d_flx_Nx          PBLH, PRECTOT, SPEED, SPEEDMAX, USTAR 
     avg1_2d_rad_Nx           ALBEDO, CLDHGH, CLDLOW
     inst3_3d_asm_Nv          PS, T, RH, U, V

Para el training se descargo un area correspondiente a las coordenadas  -59.2, -35, -57.7, -34 que comprende las estaciones de PM en superficie de la ciudad de BsAs y AMBA.


# PROJECT: EMPATIA 
# CREATED BY: LARA S. DELLA CECA dellaceca.lara@gmail.com
# DATE: 21/10/2020
# LAST MODIFICATION: 21/10/2020
# OBJECTIVE: SAVE AS GEOTIF (RESAMPLED TO MAIAC/MODIS WGS84 GRID) MERRA2 nc FILES (VARIABLES OF INTEREST) FOR THE INDIVIDUAL MAIAC/MODIS ORBITS OVERPASS DATE-TIME 

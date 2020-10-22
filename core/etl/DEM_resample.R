# PROJECT: EMPATIA 
# CREATED BY: LARA S. DELLA CECA dellaceca.lara@gmail.com
# DATE: 21/10/2020
# LAST MODIFICATION: 21/10/2020
# OBJECTIVE: RESAMPLE USGS 30 ARC DEM FOR ARGENTINA TO MAIAC/MODIS 1KM GRID (WGS84)


rm( list = ls() )

library(R.utils)
library(gdalUtils)
library(raster)
library(rgdal)
library(readr)


dominio_modelo=raster('D:/MOSAICO_MAIAC_dominio_modelo.tif') # OPEN RASTER WITH MAIAC/MODIS 1KM GRID (WGS84)
  
raster_res=raster('/media/lara/Blue/2020/CONAE/EMPATIA/USGS/DEM_Arg_30arcsec_1km_USGS.tif') # OPEN RASTER WITH USGS DEM

raster_resampled=resample(raster_res,dominio_modelo,method='bilinear',filename='/media/lara/Blue/2020/CONAE/EMPATIA/DEM_Arg_30arcsec_1km_USGS_dominio_modelo.tif') # RESAMPLE AND SAVE DEM AS TIF


# PROJECT: EMPATIA 
# CREATED BY: LARA S. DELLA CECA dellaceca.lara@gmail.com
# DATE: 21/10/2020
# LAST MODIFICATION: 21/10/2020
# OBJECTIVE: RESAMPLE USGS 30 ARC DEM FOR ARGENTINA TO MODIS 1KM GRID (WGS84) AND GET DATA FOR PM GROUND-BASED STATIONS


rm( list = ls() )

library(R.utils)
library(gdalUtils)
library(raster)
library(rgdal)
library(readr)


###########################################################################################
###########   GET DEM DATA FOR PIXELS CORRESPONDING TO PM GROUND-BASED STATIONS  ##########
###########################################################################################


dominio_modelo=raster('/media/lara/Blue/2020/CONAE/EMPATIA/MAIAC/mosaico/MOSAICO_MAIAC_dominio_modelo.tif')
  
raster_res=raster('/media/lara/Blue/2020/CONAE/EMPATIA/USGS/DEM_Arg_30arcsec_1km_USGS.tif')

raster_resampled=resample(raster_res,dominio_modelo,method='bilinear',filename='/media/lara/Blue/2020/CONAE/EMPATIA/USGS/DEM_Arg_30arcsec_1km_USGS_dominio_modelo_resampled.tif')


###########################################################################################
###########   GET DEM DATA FOR PIXELS CORRESPONDING TO PM GROUND-BASED STATIONS  ##########
###########################################################################################

rm( list = ls() )

setwd('/media/lara/Blue/2020/CONAE/EMPATIA/USGS/')

dem_filename='DEM_Arg_30arcsec_1km_USGS_dominio_modelo.tif'

pm.data=read.table('/media/lara/Blue/2020/CONAE/EMPATIA/estaciones_PM10.csv', sep=';',dec='.',header=TRUE) # TABLE WITH GORUND-BASED PM STATIONS INFORMATION (I.E LOCATION)
pm.data$ID=as.character(pm.data$ID)

fileout='DEM_pixel_data_pm_stations.csv'

data=raster(dem_filename)

coordenadas=cbind(pm.data$LON,pm.data$LAT)
valor=raster::extract(data, SpatialPoints(coordenadas))

tabla=cbind(pm.data$ID, valor)

colnames(tabla)<-c('estacion','valor_DEM_asnm')
write.csv(tabla,fileout,row.names = FALSE) #SAVE TABLE AS .csv

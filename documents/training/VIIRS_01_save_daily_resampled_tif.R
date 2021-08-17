# PROJECT: EMPATIA 
# CREATED BY: LARA S. DELLA CECA dellaceca.lara@gmail.com
# DATE: 21/10/2020
# LAST MODIFICATION: 21/10/2020
# OBJECTIVE: RESAMPLE AND SAVE AS TIF DAILY VIIRS DNB_At_Sensor_Radiance_500m SUBDATASET

rm( list = ls() )

library(gdalUtils)
library(raster)
library(rgdal)

setwd("/media/lara/Blue/2020/CONAE/EMPATIA/VIIRS/LAADS/h5")  # DIRECTORY WERE HDF5 FILES WERE DOWNLOADED
dirout=("/media/lara/Blue/2020/CONAE/EMPATIA/VIIRS/LAADS/tif/") # DIRECTORY WERE DAILY REPROYECTED FILES WILL BE SAVED

files=findFiles(pattern="h5", allFiles=TRUE, firstOnly=FALSE)
dominio_modelo=raster('/home/lara/Documentos/EMPATIA/MOSAICO_MAIAC_dominio_modelo.tif') # RASTER FILE WITH MAIAC MOSAICKING FOR ARGENTINA (WGS84)

for (f in 1:length(files)){
  
  filename = files[f]
  file_save <-paste(substr(filename,1,nchar(filename)-3),'.tif',sep='')
  file_export <-paste(dirout,substr(filename,1,24),'DNB_Sensor_Radiance_resampled.tif',sep='')
  
  info <-  gdalinfo(filename) # OPEN HDF5 FILE
  
  info[207]  #Long Name

  crs_project = "+proj=longlat +datum=WGS84 +no_defs +ellps=WGS84 +towgs84=0,0,0" 

  sds <- get_subdatasets(filename) # GET SUBDATASETS FROM HDF5 FILE
  
  gdal_translate(sds[5], dst_dataset = file_save) # GET DNB_At_Sensor_Radiance_500m SUBDATASET AND SAVE TIF

  VIIRS_raster <- raster(file_save, crs = crs_project) 
  
  # SET NA VALUES 
  NAvalue(VIIRS_raster) <- 65535
  
  # DEFINE EXTENTION
  xmax =  as.numeric(substr(info[183], nchar(info[183])-3,nchar(info[183])-1)) #EastBoundingCoord
  ymax = as.numeric(substr(info[191], nchar(info[191])-3,nchar(info[191])-1)) #NorthBoundingCoord
  ymin = as.numeric(substr(info[204], nchar(info[204])-3,nchar(info[204])-1)) #SouthBoundingCoord
  xmin = as.numeric(substr(info[209], nchar(info[209])-3,nchar(info[209])-1))  #WestBoundingCoord
  
  
  extent(VIIRS_raster) <- extent(xmin, xmax, ymin, ymax)
  
  # RESAMPLE DNB_At_Sensor_Radiance_500m SUBDATASET AND SAVE AS TIF
  raster_resampled=raster::resample(VIIRS_raster,dominio_modelo,method='bilinear',filename=file_export) 
  
  
  file.remove(file_save) # REMOVE INTERMEDIATE FILE
}
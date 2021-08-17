# PROJECT: EMPATIA 
# MODIFIED FROM https://github.com/solrepresa/AQ-Valencia/tree/master/src AC_33.R
# CREATED BY: LARA S. DELLA CECA dellaceca.lara@gmail.com
# DATE: 02/11/2020
# LAST MODIFICATION: 02/11/2020
# OBJECTIVE: CROP TILE AND FILL GAPS OF MAIAC DATA 

rm( list = ls() )

library(raster)
library(gstat)
library(gdata)
library(maptools)
library(dismo) #kfold
library(caret)
library(parallel)

crs_project= '+proj=longlat +datum=WGS84 +no_defs +ellps=WGS84 +towgs84=0,0,0'

# DEFINITION OF DOMAIN FOR CABA AND GREAT BSAS TO CROP RASTER (SO MAIAC INTERPOLATION TAKES LESS TIME...), 
# THIS DOMAIN IS THE SAME AS THE ONE USED TO DOWNLOAD MERRA-2 DATA
merra_domain=as(extent(-59.2,-57.7,-35,-34),'SpatialPolygons')
crs(merra_domain)= crs_project

dirin=('/media/lara/Blue/2020/CONAE/EMPATIA/MAIAC/h13v12/2010/') # PATH TO MAIAC HDF INDIVIDUAL ORBITS OBTAINED WITH MAIAC_01_filterQA_save_orbits_TIF.R SCRIPT

files=list.files(path=dirin, pattern='.tif',full.names =FALSE)

dirout = '/media/lara/Blue/2020/CONAE/EMPATIA/MAIAC/h13v12/MAIAC_recorte_interpolado/' 

for (i in 1:length(files)){
  
  filename=files[i]

  modis_file=raster(paste(dirin,filename,sep=''))
  
  # CROP MAIAC FILE 
  maiac_recorte <- crop(modis_file, merra_domain) 
  maiac_recorte <- mask(maiac_recorte,  merra_domain) 

  # CREATE GRID FOR INTERPOLATION
  raster_template <- raster(nrows = nrow(maiac_recorte), ncols = ncol(maiac_recorte), 
                            crs = crs_project, 
                            ext = extent(maiac_recorte)) 
  
  idw.grid <- rasterToPoints(raster_template, spatial = TRUE)

  gridded(idw.grid) <- TRUE #SpatialPixelsDataFrame

  raster_points <- as.data.frame(rasterToPoints(maiac_recorte))

    if(nrow(raster_points) > 1764){ #INTERPOLATE ONLY FOR RASTER WITH AT LEAST 10% OF DATA
    
       coordinates(raster_points) <- ~x+y
    
       projection(raster_points) <- CRS(crs_project)
       names(raster_points)[1] <- "AOD"
    
       set.seed(513) # 5-fold cross-validation
  
       # APPLY INTERPOLATION MODEL
       kat.idw <- gstat::idw(AOD ~ 1, raster_points, idw.grid, 
                          debug.level = -1,   
                          idp = 5) # IDW power
    
       # CONVERT TO RASTER
       final.idw <- raster(kat.idw)
  
       # SAVE INTERPOLATION RESULT AS RASTER
       writeRaster(final.idw, paste(dirout, substr(filename,1,nchar(filename)-4),'_rec_interpol.tif', sep = ""), 
                format = "GTiff",
                overwrite = TRUE)
    }
  

}


# PROJECT: EMPATIA 
# CREATED BY: LARA S. DELLA CECA dellaceca.lara@gmail.com
# DATE: 21/10/2020
# LAST MODIFICATION: 21/10/2020
# OBJECTIVE: OPEN hdf MAIAC/MODIS FILES, FILTER AOD BY QUALITY BAND, REPROJECT TO WGS84 AND SAVE INDIVIDUAL ORBITS AS .tif FOR AOD AT 470 AND 500 nm SEPARATELY 



rm( list = ls() )

library(R.utils)
library(gdalUtils)
library(raster)
library(rgdal)
library(readr)

tile='h13v12'

dir_i <- paste('/media/lara/Blue/2020/CONAE/EMPATIA/MAIAC/', tile,sep='') # FOR TRAINING ONLY SOME TILES WERE USED

for (y in 2010:2019){ 

dirin <-paste(dir_i,'/',y,'/hdf/',sep='')
dirout<-paste(dir_i,'/',y,'/',sep='')
setwd(dirin)

files=findFiles(pattern="hdf", allFiles=TRUE, firstOnly=FALSE)

valid_qa = c(1,2,9,10,17,18,25,26,97,105,113,121,98,106,114,122) # INVALID QA VALUES FOR AOD

newproj <- "+proj=longlat +datum=WGS84" 

for (i in 10:length(files)){
 
   filename=files[i]
  
   sds <- get_subdatasets( filename ) # SUBDATASETS IN hdf FILE
   
   #AOD 470 nm
   get_aod047 = grep("Optical_Depth_047", sds) # READ Aerosol Optical Depth de 0.47 um
   aod047 <- readGDAL( sds[get_aod047])   # OPEN AS SpatialGridDataFrame
   aod047 <- brick( aod047 )                # CONVERT TO Raster Brick
  
   #AOD 550 nm   
   get_aod055 = grep("Optical_Depth_055", sds) # READ Aerosol Optical Depth de 0.55 um
   aod055 <- readGDAL( sds[get_aod055])   
   aod055 <- brick( aod055 )                
   
   # QA
   get_aodqa = grep("AOD_QA", sds) # READ QUALITY BAND
   aodqa <- readGDAL( sds[get_aodqa] )
   aodqa <- brick( aodqa )
   ind = which( ! values(aodqa) %in% valid_qa )   # WHICH PIXELS ARE NOT QA VALID
   values(aod047)[ind] <- NA  
   values(aod055)[ind] <- NA 
  
  # REPROJECT FROM MODIS Sinusoidal TO WGS84
  aod047pr <- projectRaster(aod047, crs=newproj) #reproyecta a WGS84
  aod055pr <- projectRaster(aod047, crs=newproj) 
  
  metadatos <- gdalinfo(filename) #obtiene los metadatos
  orbits=(metadatos[ grep("Orbit", metadatos) ])  #obtiene info de las orbitas
  n=parse_number(orbits[1]) # numero de orbitas
  or1=unlist(strsplit(orbits[2], "="))
  orbits=unlist(strsplit(or1[2], "  "))

  # SAVE EACH ORBIT AS .tif
  for (or in 1:length(orbits)){
    orbita=orbits[or]
    year=substr(orbita,1,4) 
    jd=substr(orbita,5,7) 
    hora=paste(substr(orbita,8,9),substr(orbita,10,11), sep="") 
    sat=substr(orbita,12,12) 
    
    aod047or=aod047pr[[or]] 
    control470=cellStats(aod047or, stat='sum', na.rm=TRUE) # CHECK IF THE ORBIT HAS ANY VALID DATA
    if (control470!=0){ # IF THERE IS NO VALID DATA IN THE WHOLE TILE, IT IS NOT SAVED
      fileout470=paste(dirout,'MCD19A2.',tile,'.',sat,'.', '470.',year,jd,'.',hora,'.tif',sep="")
      writeRaster(aod047or,fileout470,overwrite=TRUE)
    }
    
    aod055or=aod055pr[[or]] 
    control550=cellStats(aod055or, stat='sum', na.rm=TRUE) 
    if (control550!=0){ 
      fileout550=paste(dirout,'MCD19A2.',tile,'.',sat,'.', '550.',year,jd,'.',hora,'.tif',sep="")
      writeRaster(aod055or,fileout550,overwrite=TRUE)
    }
    
  }
  
 }  
    
} 
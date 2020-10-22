# PROJECT: EMPATIA 
# CREATED BY: LARA S. DELLA CECA dellaceca.lara@gmail.com
# DATE: 21/10/2020
# LAST MODIFICATION: 21/10/2020
# OBJECTIVE: SAVE AS GEOTIF (RESAMPLED TO MAIAC/MODIS WGS84 GRID) MERRA2 nc FILES (VARIABLES OF INTEREST) FOR THE INDIVIDUAL MAIAC/MODIS ORBITS OVERPASS DATE-TIME 


rm( list = ls() )

library(ncdf4)
library(raster)
library(R.utils)
library(lubridate)                                                    
library(dplyr)
library(rgdal)

dominio_modelo=raster('D:/EMPATIA/MOSAICO_MAIAC_dominio_modelo.tif')        # RASTER FILE WITH MAIAC MOSAICKING FOR ARGENTINA (WGS84) -> used for resampling
horario_maiac=read.csv('D:/EMPATIA/MCD19A2_dia_hora_orbitas_h13v12.csv', sep=';', dec='.', header=TRUE)  # TABLE (csv FILE) WITH DATE-TIME OVERPASS FOR MODIS (AQUA + TERRA) ORBITS 


# GET LIST OF FILES
#sitio='BUE'  
#producto='02-tavg1_2d_flx_Nx'  

dirin=paste('D:/EMPATIA/02-BUE/') # WHERE MERRA2 .nc FILES WERE DOWNLOADED

dirout=paste('D:/EMPATIA/02-BUE_tif/',sep='')  # WHERE MERRA2 resampled .tif FILES WILL BE SAVED

setwd(dirin)  
id <- list.files(path = dirin,
                 pattern = "*.nc",
                 full.names = FALSE)

sds_error <- list() 
k=1 


# START ANALYSIS

mapply(file = id,
       FUN = function(file){
         tryCatch(
           {

           filename <- file
          
   nc_file=nc_open(filename) # OPEN MERRA .nc FILE

   # GET DATE-TIME OF MERRA2  
   timeDim=ncvar_get(nc_file,'time') # TIME OF MERRA2 ARE IN DIFFERENT BANDS OD MERRA .nc FILE, AS MINUTES FROM tORIGIN
   tinfo=ncatt_get(nc_file,'time')$units 
   tOrigin <- unlist(strsplit(tinfo, "[ ]")) 

  # CONVERT timeDim TO DATE-TIME FORMAT
  tFact   <- switch(which(tOrigin[1] == c("days", "hours", "minutes", "seconds")), 24*60*60, 60*60, 60, 1)
  tOrigin <- paste(tOrigin[-1:-2], collapse = " ")
  date_time_MERRA2 <- as.POSIXct(timeDim*tFact, tz = "UTC", origin = tOrigin)

  # GET DATE-TIME FROM MAIAC
  # GET NEAREST DATE-TIME FOR EACH MAIAC ORBIT FROM MERRA AND SAVE MERRA2 AS TIF

  index=which(horario_maiac$y==year(date_time_MERRA2[1]) & horario_maiac$m==month(date_time_MERRA2[1]) & horario_maiac$d==day(date_time_MERRA2[1]))
  t_ind=distinct(horario_maiac[index,])
  
  date_time_MAIAC <- ymd_hms(t_ind$fecha) 
  
  bandas=c()
  for (k1 in 1:nrow(t_ind)){           
    date_time_MAIAC_or=date_time_MAIAC[k1]
    dif_tiempo=difftime(date_time_MAIAC_or, date_time_MERRA2, 'minutes')
    b=which.min(abs(dif_tiempo))
    bandas=cbind(bandas,b)
  } 
  
  bandas=unique(bandas) # THE DATE-TIME OF MERRA2 CORRESPOND TO BAND NUMBER IN nc FILE
  
  variables=attributes(nc_file$var)$names # GET ATTRIBUTES OF MERRA2
  
for (k2 in 1:length(bandas)){  # FOR EACH DATE-TIME OF MERRA2 OF INTEREST WE GET A TIF OF EACH ATTRIBUTE
  
  fecha=date_time_MERRA2[bandas[k2]]
  jd_n=yday(fecha)
  
  if (jd_n<10){
     jd=paste('00',jd_n,sep='')
     }else if (jd_n>9 & jd_n<100){
     jd=paste('0',jd_n,sep='')
     }else{
       jd=jd_n
  }
  
  for (k3 in 1:length(variables)){

   
    parametro=variables[k3]

    ras=raster(filename,varname=parametro, band=bandas[k2], ncdf=TRUE)  # CREATE A RASTER WITH ATTRIBUTE AND DATE-TIME OF MERRA-2 OF INTEREST

    fileout=paste(dirout,'MERRA2.',year(fecha),jd,'.',hour(fecha),minute(fecha),'.resampled.',parametro,'.tif',sep='') 

    raster_final=raster::resample(ras,dominio_modelo,method='bilinear',fileout)
    
    
       
      } 
     }
  
  
         }, 
         
         error = function(error_message){
           message("ERROR")
           message(error_message)
           sds_error[k] <- file
           k = k + 1
         } 
         
         
 
         ) })


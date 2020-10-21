
rm( list = ls() )

library(ncdf4)
library(raster)
library(R.utils)
library(openxlsx)
library(lubridate)                                                    
library(dplyr)
library(rgdal)

dominio_modelo=raster('D:/EMPATIA/MOSAICO_MAIAC_dominio_modelo.tif')
horario_maiac=read.xlsx('D:/EMPATIA/MCD19A2_dia_hora_orbitas_h13v12.xlsx')

sitio='BUE'  # 'BB'
#sitiout='BUE_01'
producto='02-tavg1_2d_flx_Nx'

mtile='h13v12' #corresponde a BUE y BB
#mtile='h12v12' #corresponde a CORDOBA

# PARA CADA ARCHIVO DE MERRA HACER

dirin=paste('D:/EMPATIA/02-BUE/')


#files=findFiles(pattern="nc",paths = dirin, allFiles=TRUE, firstOnly=FALSE)

setwd(dirin)  

#id <- dir(pattern = ".hdf") 

id <- list.files(path = dirin,
                 pattern = "*.nc",
                 full.names = FALSE)



sds_error <- list() # junto file que dan error
k=1 

mapply(file = id,
       FUN = function(file){
         tryCatch(
           {

           filename <- file
          # filename2 <- paste(substr(file, 0, 36), ".tif", sep=""),

  # filename=files[k0]

   #nc_file=nc_open(filename), #ABRO EL ARCHIVO
  nc_file=nc_open(filename)

  #a=attributes(nc_file)$names # VEO LOS ATRIBUTOS
# [1] "filename"    "writable"    "id"          "safemode"    "format"      "is_GMT"      "groups"      "fqgn2Rindex"
#[9] "ndims"       "natts"       "dim"         "unlimdimid"  "nvars"       "var"     

  # FECHA-HORA DISPONIBLES MERRA-2 
   timeDim=ncvar_get(nc_file,'time') # VEO LAS HORAS PARA LAS CUALES HAY DATOS (QUE CORRESPONDE CON EL NUMERO DE BANDA QUE VOY A GUARDAR PARA AQUA Y PARA TERRA)
   tinfo=ncatt_get(nc_file,'time')$units 
#  timeDim <- var.get.nc(nc_file, "time") 
  tOrigin <- unlist(strsplit(tinfo, "[ ]")) # VEO EL ORIGEN DESDE EL CUAL PARTE LA HORA

  # convierto timeDim a formato fecha hora:
  tFact   <- switch(which(tOrigin[1] == c("days", "hours", "minutes", "seconds")), 24*60*60, 60*60, 60, 1)
  tOrigin <- paste(tOrigin[-1:-2], collapse = " ")
  date_time_MERRA2 <- as.POSIXct(timeDim*tFact, tz = "UTC", origin = tOrigin)

  # FECHA-HORA DISPONIBLES MAIAC
  # BUSCO EN LA TABLA DE HORARIOS DE MAIAC EL DIA Y LAS HORAS DE PASADA DE ESE DIA DE MODIS 
  # y busco el horario en merra mas cercano a esas horas

  index=which(horario_maiac$y==year(date_time_MERRA2[1]) & horario_maiac$m==month(date_time_MERRA2[1]) & horario_maiac$d==day(date_time_MERRA2[1]))
  t_ind=distinct(horario_maiac[index,])
  
  date_time_MAIAC <- ymd_hms(t_ind$fecha) # para fecha_hora de maiac igual formato que esta
  
  bandas=c()
  for (k1 in 1:nrow(t_ind)){           
    date_time_MAIAC_or=date_time_MAIAC[k1]
    dif_tiempo=difftime(date_time_MAIAC_or, date_time_MERRA2, 'minutes')
    b=which.min(abs(dif_tiempo))
    bandas=cbind(bandas,b)
  } #cierro k1
  bandas=unique(bandas)
  
  variables=attributes(nc_file$var)$names # VEO LAS VARIABLES
  
for (k2 in 1:length(bandas)){
  
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

    ### PARA CADA VARIABLE EN EL ARCHIVO NETCDF Y PARA CADA BANDA (HORA) QUE ME INTERESA HACER:
    
    parametro=variables[k3]

    ras=raster(filename,varname=parametro, band=bandas[k2], ncdf=TRUE)  # PASAR NETCDF A RASTER , LA BANDA INDICA LA HORA...

    dirout=paste('D:/EMPATIA/02-BUE_tif/',sep='')
    
    fileout=paste(dirout,'MERRA2.',year(fecha),jd,'.',hour(fecha),minute(fecha),'.resampled.',parametro,'.tif',sep='') 

    raster_final=raster::resample(ras,dominio_modelo,method='bilinear',fileout)
    
    
       
      } # cierro k3
     }# cierro k2
  
  
         }, 
         
         error = function(error_message){
           message("ERROR")
           message(error_message)
           sds_error[k] <- file
           k = k + 1
         } #CIERRA MENSAJE ERROR
         
         
 
         ) })# cierro FUN


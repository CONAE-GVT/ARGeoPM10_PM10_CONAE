# PROJECT: EMPATIA 
# CREATED BY: LARA S. DELLA CECA dellaceca.lara@gmail.com
# DATE: 21/10/2020
# LAST MODIFICATION: 21/10/2020
# OBJECTIVE: GET MAIAC/MODIS DATA FOR PIXELS CORRESPONDING TO GROUND-BASED PM STATIONS

rm( list=ls())

library(raster)
library(openxlsx)
library(lubridate)

pm.data=read.table('/home/lara/Documentos/EMPATIA/estaciones_PM10.csv', sep=';',dec='.',header=TRUE) # TABLE WITH GORUND-BASED PM STATIONS INFORMATION (I.E LOCATION)
pm.data$ID=as.character(pm.data$ID)
dir_inicial='/media/lara/Blue/2020/CONAE/EMPATIA/MAIAC/h13v12/MAIAC_recorte_interpolado/'  

tabla=c() 

dirin=dir_inicial
files=list.files(path=dirin, pattern='.tif',full.names =FALSE)

 for (k1 in 1:length(files)){
  
  filename=files[k1]
  
  #GET DATE-TIME FROM MAIAC ORBITE
  y=as.numeric(substr(filename,22,25))
  jd=as.numeric(substr(filename,26,28))
  hh=as.numeric(substr(filename,30,31))
  mm=as.numeric(substr(filename,32,33))
 
  origen=paste(as.numeric(y),"-01-01",sep="")
  date=as.Date(as.numeric(jd)-1, origin = origen)
  fecha=paste(as.character(date),' ',hh,':',mm,':00',sep='')

  # GET WAVELENGHT FROM MAIAC PRODUCT (470 0R 550 nm)
  taod=as.numeric(substr(filename,18,20))
 
  # GET SATELLITE (A FOR AQUA, T FOR TERRA)
  sat=substr(filename,16,16)
  
  # GET AOD AS RASTER
  datos=raster(paste(dirin,filename,sep='')) 
  
  # GET AOD PIXEL VALUE FOR EACH GROUND-BASED PM STATION
  for (k2 in 1:nrow(pm.data)){
    
    coordenadas=cbind(pm.data$LON[k2],pm.data$LAT[k2])
    valor=raster::extract(datos, SpatialPoints(coordenadas))
    
    linea=cbind(fecha, sat,taod, valor, pm.data$ID[k2])
    tabla=rbind(tabla,linea)
  } 
  
  print(length(files)-k1)
} 


# SET NAME OF TABLE COLUMNS
tabla=as.data.frame(tabla)
names(tabla)[1]='Fecha_Hora (yyyy-mm-dd hh:mm:ss)'
names(tabla)[2]='Satelite'
names(tabla)[3]='AODnm'
names(tabla)[4]='valor_AOD'
names(tabla)[5]='estacion_pm'

fileout=paste(dir_inicial,'/MAIAC_pixel_data_pm_stations_2010-2019_INTERPOLADO.csv',sep='')
write.csv(tabla,fileout,row.names = FALSE) # SAVE TABLE AS .csv







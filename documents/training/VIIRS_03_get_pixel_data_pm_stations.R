# PROJECT: EMPATIA 
# CREATED BY: LARA S. DELLA CECA dellaceca.lara@gmail.com
# DATE: 21/10/2020
# LAST MODIFICATION: 21/10/2020
# OBJECTIVE: THIS SCRIPTS USES THE OUTPUT FILES FROM THE VIIRS_02_year_mean.R SCRIPT: GET APR-JUN YEARLY MEAN OF VIIRS NIGHT LIGHT DATA FOR PIXELS CORRESPONDING TO GROUND-BASED PM STATIONS 

rm( list=ls())

library(raster)
library(openxlsx)

pm.data=read.table('/home/lara/Documentos/EMPATIA/estaciones_PM10.csv', sep=';',dec='.',header=TRUE) # TABLE WITH GORUND-BASED PM STATIONS INFORMATION (I.E LOCATION)
pm.data$ID=as.character(pm.data$ID) 

dirin='/home/lara/Documentos/EMPATIA'
dirout=dirin

fileout=paste(dirout,'/VIIRS_st_pixel_data_mean_Apr_to_Jun_2012_2019.csv',sep='') 
  
files=list.files(path=dirin, pattern='_sc_complete_resampled',full.names = FALSE)

tabla=c()  
  
# GET PIXEL VALUE FOR EACH GROUND-BASED PM STATION LOCATION
for (k0 in 1:length(files)){
      
    filename=files[k0]
    datos=raster(paste(dirin,filename,sep=''))
    
    year=as.numeric(substr(filename,20,23))
    
    for (k1 in 1:nrow(pm.data)){
    
      coordenadas=cbind(pm.data$LON[k1],pm.data$LAT[k1])
      valor=raster::extract(datos, SpatialPoints(coordenadas))
      
      linea=cbind(year,valor,pm.data$ID[k1])
      tabla=rbind(tabla,linea)
    }
    
    
}

tabla=as.data.frame(tabla)
names(tabla)[1]='año'
names(tabla)[2]='valor_VIIRS'
names(tabla)[3]='estacion'

write.csv(tabla,fileout,row.names = FALSE) #SAVE TABLE WITH DATA AS .csv


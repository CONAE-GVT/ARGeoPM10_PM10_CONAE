# PROJECT: EMPATIA 
# CREATED BY: LARA S. DELLA CECA dellaceca.lara@gmail.com
# DATE: 01/11/2020
# LAST MODIFICATION: 03/11/2020
# OBJECTIVE: COMPLETE AOD (MAIAC/MODIS) ORBIT DAILY DATA TABLE WITH MERRA-2, VIIRS AND DEM -> PIXEL CORRESPONDING TO PM GROUND-BASED STATIONS
#            AND PM DATA CORRESPONDING TO NEAREST DATE-TIME PM STATIONS MEASUREMENTS.


###################################################################################################
#################           APPEND MERRA-2 DATA TO TRAINING TABLE         #########################
###################################################################################################
rm( list = ls() )

library(R.utils)
library(epitools)
library(openxlsx)
library(lubridate)
library(dplyr)
library(raster)

# OPEN FILE WITH PM STATIONS INFORMATION 
pm.data=read.table('E:/2020/CONAE/EMPATIA/estaciones_PM10.csv', sep=';',dec='.',header=TRUE) # TABLE WITH GORUND-BASED PM STATIONS INFORMATION (I.E LOCATION)
pm.data$ID=as.character(pm.data$ID) # NAME OF STATIONS
coordenadas=cbind(pm.data$LON,pm.data$LAT) # LAT LON LOCATION OF STATION

# OPEN CSV FILE WHERE MERRA2 DATA WILL BE SAVED (CONSIDERING MAIAC/MODIS OVERPASS TIME)
tabla_entrenamiento=read.csv('E:/2020/CONAE/EMPATIA/Tabla_Entrenamiento/Tabla_Entrenamiento_MAIAC.csv',sep=';',dec='.',header=TRUE)
tabla_entrenamiento=as.data.frame(tabla_entrenamiento)  
cname=colnames(tabla_entrenamiento) # NAME OF COLUMNS CORRESPOND TO DIFFERENT VARIABLES (I.E MERRA2 VARIABLES)

#OPEN TABLE WITH DATE-TIME AND FILENAME OF MERRA DOWNLOADED FILES (pack 1 to 3)
merra_info_1_3=read.csv('E:/2020/CONAE/EMPATIA/MERRA-2/GEOTIFF/MERRA2_DATE-TIME_filename_1-3.csv',sep=',',dec='.',header=TRUE)
merra_info_1_3=as.data.frame(merra_info_1_3)

merra_info_4=read.csv('E:/2020/CONAE/EMPATIA/MERRA-2/GEOTIFF/MERRA2_DATE-TIME_filename_4.csv',sep=',',dec='.',header=TRUE)
merra_info_4=as.data.frame(merra_info_4)

# CHANGE INFO TO DATE-TIME FORMAT
dates=as.POSIXct(tabla_entrenamiento$Fecha_Hora..yyyy.mm.dd.hh.mm.ss.,format="%d/%m/%Y %H:%M", tz='UTC')
dates_maiac=unique(dates) # UNIQUE IS APPLY BECAUSE DATES ARE REPEATED FOR PM STATIONS AND AOD 470 AND 500 NM FILES


date_time_MERRA_1_3=as.POSIXct(merra_info_1_3$fecha,format="%Y-%m-%d %H:%M:%S", tz='UTC')
date_time_MERRA_4=as.POSIXct(merra_info_4$fecha,format="%Y-%m-%d %H:%M:%S", tz='UTC')

# FOR EACH DATE-TIME OF MAIAC DATA WE GET MERRA2 VARIABLE VALUES FOR EACH PM STATION CORRESPONDING PIXEL 
for (k0 in 1:length(dates_maiac)){
 
  date_time_MAIAC <- dates_maiac[k0]
  
##### MERRA-2 PACK VARIABLES 1 A 3
      dif_tiempo_1_3=difftime(date_time_MAIAC, date_time_MERRA_1_3, 'minutes')
      min_time_dif_1_3=which.min(abs(dif_tiempo_1_3))
      merra_index_1_3= which(merra_info_1_3$fecha==merra_info_1_3$fecha[ min_time_dif_1_3]) 
      merra_files_1_3=merra_info_1_3[merra_index_1_3,] # INFO OF MERRA VARIABLE FILES NEAREST TO MODIS DATE-TIME
  
      # OPEN EACH MERRA VARIABLE FILE AND GET PIXEL VALUE FOR PM STATIONS
      for (k1 in 1:nrow(merra_files_1_3)){
    
        filename=paste('E:/2020/CONAE/EMPATIA/MERRA-2/GEOTIFF/BUE-0',merra_files_1_3$k0[k1],'/',merra_files_1_3$files[k1],sep='')
   
        raster_merra=raster(filename)
    
        variable=merra_files_1_3$variables[k1]
    
        valores_merra=cbind(raster::extract(raster_merra, SpatialPoints(coordenadas)),pm.data$ID)
    
        cvalue=which(cname==variable)
    
        maiac_index=which(dates==date_time_MAIAC)
    
        tabla_entrenamiento$estacion_pm[maiac_index]
    
        for (k2 in 1:length(pm.data$ID)){
          
             posicion=maiac_index[which(tabla_entrenamiento$estacion_pm[maiac_index]==valores_merra[k2,2])]
             tabla_entrenamiento[posicion,cvalue]=valores_merra[k2,1]
    
         }#cierro k2
    
      }# cierro k1
     
  
###### MERRA-2 PACK VARIABLES 4    (TIME INTERVALS ARE DIFFERENT FROM 1 TO 3 MERRA-2 PRODUCTS, THATS WHY IS DONE SEPARATELY)
  
  dif_tiempo_4=difftime(date_time_MAIAC, date_time_MERRA_4, 'minutes')
  min_time_dif_4=which.min(abs(dif_tiempo_4))
  merra_index_4= which(merra_info_4$fecha==merra_info_4$fecha[ min_time_dif_4]) 
  merra_files_4=merra_info_4[merra_index_4,] # INFO OF MERRA VARIABLE FILES NEAREST TO MODIS DATE-TIME
  
  # OPEN EACH MERRA VARIABLE FILE AND GET PIXEL VALUE FOR PM STATIONS
  for (k3 in 1:nrow(merra_files_4)){
    
    filename=paste('E:/2020/CONAE/EMPATIA/MERRA-2/GEOTIFF/BUE-0',merra_files_4$k0[k3],'/',merra_files_4$files[k3],sep='')
    
    raster_merra=raster(filename)
    
    variable=merra_files_4$variables[k3]
    
    valores_merra=cbind(raster::extract(raster_merra, SpatialPoints(coordenadas)),pm.data$ID)
    
    cvalue=which(cname==variable)
    
    maiac_index=which(dates==date_time_MAIAC)
    
    tabla_entrenamiento$estacion_pm[maiac_index]
    
    for (k4 in 1:length(pm.data$ID)){
      
      posicion=maiac_index[which(tabla_entrenamiento$estacion_pm[maiac_index]==valores_merra[k4,2])]
      tabla_entrenamiento[posicion,cvalue]=valores_merra[k4,1]
      
    }#cierro k4
    
  }# cierro k3
  
  t_save=tabla_entrenamiento[maiac_index,]
  
  write.table(t_save, file='E:/2020/CONAE/EMPATIA/Tabla_Entrenamiento/Tabla_Entrenamiento_MAIAC_MERRA.csv', append = T, 
               sep=',', row.names=F, col.names = FALSE)
  
  print(length(dates_maiac) - k0) 

} #cierro k0
  

###################################################################################################
#################           APPEND VIIRS DATA TO TRAINING TABLE           #########################
###################################################################################################
rm( list = ls() )

library(lubridate)

viirs_data=read.csv('E:/2020/CONAE/EMPATIA/VIIRS/LAADS/VIIRS_pixel_data_pm_stations_2012-2019.csv',sep=',',dec='.',header=TRUE)

tabla_entrenamiento=read.csv('E:/2020/CONAE/EMPATIA/Tabla_Entrenamiento/Tabla_Entrenamiento_MAIAC_MERRA.csv',sep=';',dec='.',header=TRUE)

years=year(as.POSIXct(tabla_entrenamiento$Fecha_Hora..yyyy.mm.dd.hh.mm.ss., format="%d/%m/%Y %H:%M", tz='UTC'))

# FOR 2010-2011 & 2012 VIIRS VALUE FOR EACH STATION CORRESPONDS TO 2012 APR-JUN MEAN
estacion=unique(viirs_data$estacion)
for (k0 in 1:length(estacion)){
  viirs_index=which(viirs_data$aÃ.o ==2012 & viirs_data$estacion==estacion[k0])
  viirs_value=viirs_data$valor_VIIRS[viirs_index]
  
  train_index= which(years<=2012 & tabla_entrenamiento$estacion_pm==estacion[k0])
  tabla_entrenamiento$VIIRS_night_lights[train_index]=viirs_value
}

#FOR 2013 TO 2019 VIIRS VALUE FOR EACH STATION CORRESPONDS TO EACH YEAR'S APR-JUN MEAN
for (y in 2013:2019){
for (k1 in 1:length(estacion)){
  viirs_index=which(viirs_data$aÃ.o==y & viirs_data$estacion==estacion[k1])
  viirs_value=viirs_data$valor_VIIRS[viirs_index]
  
  train_index= which(years==y & tabla_entrenamiento$estacion_pm==estacion[k1])
  tabla_entrenamiento$VIIRS_night_lights[train_index]=viirs_value
}
}

write.table(tabla_entrenamiento, file='E:/2020/CONAE/EMPATIA/Tabla_Entrenamiento/Tabla_Entrenamiento_MAIAC_MERRA_VIIRS.csv', append = T, 
            sep=',', row.names=F)



###################################################################################################
#################           APPEND DEM DATA TO TRAINING TABLE             #########################
###################################################################################################

rm( list = ls() )

tabla_entrenamiento=read.csv('E:/2020/CONAE/EMPATIA/Tabla_Entrenamiento/Tabla_Entrenamiento_MAIAC_MERRA_VIIRS.csv',sep=',',dec='.',header=TRUE)

dem_data=read.csv('E:/2020/CONAE/EMPATIA/USGS/DEM_pixel_data_pm_stations.csv',sep=',',dec='.',header=TRUE)

for (k0 in 1:length(dem_data$estacion)){
  train_index= which(tabla_entrenamiento$estacion_pm==dem_data$estacion[k0])
  tabla_entrenamiento$DEM_asnm[train_index]=dem_data$valor_DEM_asnm[k0]
}  
  
write.table(tabla_entrenamiento, file='E:/2020/CONAE/EMPATIA/Tabla_Entrenamiento/Tabla_Entrenamiento_MAIAC_MERRA_VIIRS_DEM.csv', 
            sep=',', row.names=F)

  
###################################################################################################
#################           APPEND PM10    DATA TO TRAINING TABLE         #########################
###################################################################################################

rm( list = ls() )

tabla_pm=read.csv('D:/EMPATIA/PM/PM_ACUMAR_y_APRAconvenio_PREPROCESADO.csv', sep=',', dec='.',header=TRUE)

tabla_entrenamiento=read.csv('E:/2020/CONAE/EMPATIA/Tabla_Entrenamiento/Tabla_Entrenamiento_MAIAC_MERRA_VIIRS_DEM.csv',sep=',',dec='.',header=TRUE)

# PM CHANGE DATE-TIME FORMAT AND CONVERT TO UTC (MAIAC DATA ARE IN UTC)
date_time_pm=as.POSIXct(tabla_pm$fecha,format="%Y-%m-%d %H:%M:%S")
attr(date_time_pm, "tzone") <- "UTC" 

y_pm=year(date_time_pm)
m_pm=month(date_time_pm)
d_pm=day(date_time_pm)

estaciones=as.character(tabla_pm$estacion)
columna_pm_valor=c()
columna_fechas_control=c()
for (k0 in 1:nrow(tabla_entrenamiento)){
   
  fecha_fila=as.POSIXct(tabla_entrenamiento$Fecha_Hora..yyyy.mm.dd.hh.mm.ss.[k0],format="%d/%m/%Y %H:%M",tz="UTC")
  
  st_fila=tabla_entrenamiento$estacion_pm[k0]
  
  index= which(y_pm==year(fecha_fila) & m_pm==month(fecha_fila) & d_pm==day(fecha_fila) &  estaciones==st_fila)
  
  if (length(index)==0){
    valor_pm=NA
    fila_date=cbind(fecha_fila,'no hay date_time_pm','no hay fecha en tabla_pm')
    
  }else{
  fechas_Seleccion= date_time_pm[index]
 
  dif_tiempo=difftime(fecha_fila, fechas_Seleccion, 'minutes')
  min_time_dif=which.min(abs(dif_tiempo))
  
  valor_pm=tabla_pm$value[index[min_time_dif]]
  
  fila_date=cbind(fecha_fila,date_time_pm[index[min_time_dif]],tabla_pm$fecha[index[min_time_dif]])
  
  }
  
  columna_pm_valor=rbind(columna_pm_valor,valor_pm)
  
  columna_fechas_control=rbind(columna_fechas_control,fila_date)
  
  print(nrow(tabla_entrenamiento)-k0)
  
}

tabla_final=cbind(tabla_entrenamiento[,1:5],columna_pm_valor[,1],tabla_entrenamiento[,6:ncol(tabla_entrenamiento)])

colnames(tabla_final)[6] <- "PM10_valor"

write.table(tabla_final, file='E:/2020/CONAE/EMPATIA/Tabla_Entrenamiento/Tabla_Entrenamiento_MAIAC_MERRA_VIIRS_DEM_PMconvenio.csv', 
            sep=',', row.names=F)



###################################################################################################
#################           APPEND PM10 BAHIA BLANCA -estacion I -  DATA TO TRAINING TABLE         #########################
###################################################################################################

rm( list = ls() )

tabla_pm=read.csv('D:/EMPATIA/BahiaBlanca/PM10_MediaMovil_24hs_BahiaBlanca_2010-2018.csv', sep=',', dec='.',header=TRUE)

tabla_entrenamiento=read.csv('E:/2020/CONAE/EMPATIA/Tabla_Entrenamiento/Tabla_Entrenamiento_MAIAC_MERRA_VIIRS_DEM_PMconvenio.csv',sep=',',dec='.',header=TRUE)

# PM CHANGE DATE-TIME FORMAT AND CONVERT TO UTC (MAIAC DATA ARE IN UTC)
date_time_pm=as.POSIXct(tabla_pm$Fecha,format="%Y-%m-%d %H:%M:%S")
attr(date_time_pm, "tzone") <- "UTC" 

y_pm=year(date_time_pm)
m_pm=month(date_time_pm)
d_pm=day(date_time_pm)

indice=which(tabla_entrenamiento$estacion_pm=='BB1')



for (k0 in 1:length(indice)){
  fecha_fila=as.POSIXct(tabla_entrenamiento$Fecha_Hora..yyyy.mm.dd.hh.mm.ss.[indice[k0]],format="%d/%m/%Y %H:%M",tz="UTC")
  
  
  st_fila=tabla_entrenamiento$estacion_pm[indice[k0]]
  
  index= which(y_pm==year(fecha_fila) & m_pm==month(fecha_fila) & d_pm==day(fecha_fila))
  
  if (length(index)==0){
    valor_pm=NA
    fila_date=cbind(fecha_fila,'no hay date_time_pm','no hay fecha en tabla_pm')
    tabla_entrenamiento$PM10_valor[indice[k0]]=valor_pm
    
  }else{
    fechas_Seleccion= date_time_pm[index]
    
    dif_tiempo=difftime(fecha_fila, fechas_Seleccion, 'minutes')
    min_time_dif=which.min(abs(dif_tiempo))
    
    valor_pm=tabla_pm$PM10[index[min_time_dif]]
    tabla_entrenamiento$PM10_valor[indice[k0]]=valor_pm
    
    #fila_date=cbind(fecha_fila,date_time_pm[index[min_time_dif]],tabla_pm$Fecha[index[min_time_dif]])
    
  }
  
   print(length(indice)-k0)
  
}

write.table( tabla_entrenamiento, file='E:/2020/CONAE/EMPATIA/Tabla_Entrenamiento/Tabla_Entrenamiento_MAIAC_MERRA_VIIRS_DEM_PMconvenio_BahiaBlanca.csv', 
            sep=',', row.names=F)


###################################################################################################
#################           APPEND PM10 BAHIA BLANCA -estacion II -  DATA TO TRAINING TABLE         #########################
###################################################################################################

rm( list = ls() )

tabla_pm=read.csv('D:/EMPATIA/BahiaBlanca/PM10_MediaMovil_24hs_BahiaBlanca_EII_2017-2018.csv', sep=',', dec='.',header=TRUE)

tabla_entrenamiento=read.csv('E:/2020/CONAE/EMPATIA/Tabla_Entrenamiento/Tabla_Entrenamiento_MAIAC_MERRA_VIIRS_DEM_PMconvenio_BahiaBlanca.csv',sep=',',dec='.',header=TRUE)

# PM CHANGE DATE-TIME FORMAT AND CONVERT TO UTC (MAIAC DATA ARE IN UTC)
date_time_pm=as.POSIXct(tabla_pm$Fecha,format="%Y-%m-%d %H:%M:%S")
attr(date_time_pm, "tzone") <- "UTC" 

y_pm=year(date_time_pm)
m_pm=month(date_time_pm)
d_pm=day(date_time_pm)

indice=which(tabla_entrenamiento$estacion_pm=='BB2')

for (k0 in 1:length(indice)){
  fecha_fila=as.POSIXct(tabla_entrenamiento$Fecha_Hora..yyyy.mm.dd.hh.mm.ss.[indice[k0]],format="%d/%m/%Y %H:%M",tz="UTC")
  
  st_fila=tabla_entrenamiento$estacion_pm[indice[k0]]
  
  index= which(y_pm==year(fecha_fila) & m_pm==month(fecha_fila) & d_pm==day(fecha_fila))
  
  if (length(index)==0){
    valor_pm=NA
    fila_date=cbind(fecha_fila,'no hay date_time_pm','no hay fecha en tabla_pm')
    tabla_entrenamiento$PM10_valor[indice[k0]]=valor_pm
    
  }else{
    fechas_Seleccion= date_time_pm[index]
    
    dif_tiempo=difftime(fecha_fila, fechas_Seleccion, 'minutes')
    min_time_dif=which.min(abs(dif_tiempo))
    
    valor_pm=tabla_pm$PM10[index[min_time_dif]]
    tabla_entrenamiento$PM10_valor[indice[k0]]=valor_pm
    
    #fila_date=cbind(fecha_fila,date_time_pm[index[min_time_dif]],tabla_pm$Fecha[index[min_time_dif]])
    
  }
  
  print(length(indice)-k0)
  
}

write.table( tabla_entrenamiento, file='E:/2020/CONAE/EMPATIA/Tabla_Entrenamiento/Tabla_Entrenamiento_MAIAC_MERRA_VIIRS_DEM_PMconvenio_BahiaBlancaIyII.csv', 
             sep=',', row.names=F)




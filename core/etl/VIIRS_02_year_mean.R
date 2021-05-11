# PROJECT: EMPATIA 
# CREATED BY: LARA S. DELLA CECA dellaceca.lara@gmail.com
# DATE: 21/10/2020
# LAST MODIFICATION: 21/10/2020
# OBJECTIVE: THIS SCRIPTS USES THE OUTPUT FILES FROM THE VIIRS_01_save_daily_resampled_tif.R SCRIPT: CALCULATES VIIRS NIGHT 
#             LIGHTS MEAN VALUES (DNB_At_Sensor_Radiance_500m) FOR APRIL-JUNE PERIOD OF EACH CONSIDERED YEAR AND SAVE THE
#             RESULT AS TIF

rm( list = ls() )

library(raster)

dirin='/media/lara/Blue/2020/CONAE/EMPATIA/VIIRS/LAADS/tif/' # DIRECTORY WHERE DAILY RESAMPLED VIIRS FILES WERE SAVED
dirout='/media/lara/Blue/2020/CONAE/EMPATIA/VIIRS/LAADS/'    # DIRECTORY WHERE THE RESULTS OF THIS SCRIPT WILL BE SAVED

setwd(dirin)

files=findFiles(pattern="tif", allFiles=TRUE, firstOnly=FALSE)

y=as.numeric(substring(files,10,13))

years=unique(y)

for (k0 in min(years):max(years)){

  index=which(y==k0)
 
  lista.anio=files[index]
  
  raster_stack=stack(lista.anio) 
  
  promedio=calc(raster_stack,fun=mean,na.rm=T)
  
  fileout=paste(dirout,'VIIRS_Promedio_',k0,'_Abr-Jun_LAADS.tif',sep='')
  
  writeRaster(promedio,fileout)
  
} 


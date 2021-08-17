Training - Proyecto EMPATIA

Este script utiliza los archivos resultantes del script VIIRS_02_year_mean.R. 
Obtiene el valor promedio del periodo Abril-Junio para cada año con datos VIIRS disponibles (2012-2019) del subdataset 
DNB_At_Sensor_Radiance_500m resampleados, para cada estación superficial de MP considerada para el entrenamiento del modelo.

El resultado de este script se guarda en la tabla denominada VIIRS_st_pixel_data_mean_Apr_to_Jun_2012_2019.csv

# PROJECT: EMPATIA 
# CREATED BY: LARA S. DELLA CECA dellaceca.lara@gmail.com
# DATE: 21/10/2020
# LAST MODIFICATION: 21/10/2020
# OBJECTIVE: THIS SCRIPTS USES THE OUTPUT FILES FROM THE VIIRS_02_year_mean.R SCRIPT: GET APR-JUN YEARLY MEAN OF VIIRS NIGHT LIGHT DATA 
#            FOR PIXELS CORRESPONDING TO GROUND-BASED PM STATIONS 

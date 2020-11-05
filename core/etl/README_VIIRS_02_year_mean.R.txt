Training - Proyecto EMPATIA

Este script fue elaborado para procesar los archivos TIF que se obtienen del script VIIRS_01_save_daily_resampled_tif.R: archivos diarios
del subdataset DNB_At_Sensor_Radiance_500m resampleados.

Abre los archivos diarios TIF y realiza un promedio anual (periodo Abril - Junio) pixel a pixel y guarda el resultado en formato TIF. 


# PROJECT: EMPATIA 
# CREATED BY: LARA S. DELLA CECA dellaceca.lara@gmail.com
# DATE: 21/10/2020
# LAST MODIFICATION: 21/10/2020
# OBJECTIVE: THIS SCRIPTS USES THE OUTPUT FILES FROM THE VIIRS_01_save_daily_resampled_tif.R SCRIPT: CALCULATES VIIRS NIGHT 
#             LIGHTS MEAN VALUES (DNB_At_Sensor_Radiance_500m) FOR APRIL-JUNE PERIOD OF EACH CONSIDERED YEAR AND SAVE THE
#             RESULT AS TIF
Training - Proyecto EMPATIA

Este script trabaja con los archivos TIF de las orbitas individuales obtenidos del script MAIAC_01_filterQA_save_orbits_TIF.R, 
los recorta al dominio  59.2°–57.7° O  35°–34° S que cubre la superficie de la Ciudad Autónoma de Buenos Aires y Gran Buenos Aires, 
donde se encuentran localizadas las estaciones superficiales de material particulado (MP), y aplica un modelo de interpolacion
para completar los datos de AOD faltantes.

Finalmente guarda las orbitas individuales con los valores interpolados en formato TIF agregando al final del nombre del 
archivo '_rec_interpol.tif'


# PROJECT: EMPATIA 
# MODIFIED FROM https://github.com/solrepresa/AQ-Valencia/tree/master/src AC_33.R
# CREATED BY: LARA S. DELLA CECA dellaceca.lara@gmail.com
# DATE: 02/11/2020
# LAST MODIFICATION: 02/11/2020
# OBJECTIVE: CROP TILE AND FILL GAPS OF MAIAC DATA
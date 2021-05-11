# PROJECT: EMPATIA 
# CREATED BY: SOL REPRESA, JUNE 2020
# MODIFIED BY: LARA S. DELLA CECA dellaceca.lara@gmail.com
# LAST MODIFICATION: 21/10/2020
# OBJECTIVE: REORDER ACUMAR AND C.A.B.A PM10 MONITORING DATABASES, CALCULATE MOVIL MEAN FOR ACUMAR HOURLY MEASUREMENTS

rm( list = ls() )

library("openxlsx")
library(reshape2)
library(RcppRoll)
library(dplyr)


###################################### 
### PREPROCESSING ACUMAR DATABASE ####
######################################

setwd('D:/EMPATIA/PM/ACUMAR')

ini = "2010-12-04 00:00"
fin = "2019-12-31 00:00"

# SELECTION OF TIME-PERIOD
seq_fechas <- seq(from = as.POSIXct(ini), to = as.POSIXct(fin), by = "hour")
datos_acumar <- data.frame(seq_fechas)
names(datos_acumar) <- "fecha"

# GET PM10 VALUES FROM DATABASE
sheetIndex = c("EMC I DS-PM10", "EMCII LM-AER-PM10 " )

for( i in 1:length(sheetIndex)){
  datos <- read.xlsx("D:/EMPATIA/PM/ACUMAR/baseDeDatos230920.xlsx",
                     sheetIndex[i])
  datos <- datos[, c(1,2)]
  datos[,1] <- convertToDateTime(datos[,1])
  names(datos) <- c("fecha", substr(sheetIndex[i], 7, nchar(sheetIndex[i])))
  datos <- datos[c(which(datos$fecha == ini): nrow(datos)), ]
  seq_f <- seq(datos$fecha[1], datos$fecha[nrow(datos)], by ="hour")
  if(length(seq_f) != nrow(datos)){
   break }   
  datos$fecha <- seq_f   
  datos_acumar <- merge(datos_acumar, datos, by = "fecha", all = TRUE)
}

names(datos_acumar) <- c("fecha", 
                         "DS_PM10", "LM_PM10" )

# Media movil >> PM10 - 24hs ACUMAR >>>> CALCULATE MOVIL MEAN
datos_acumar2 <- datos_acumar %>% mutate(DS_PM10 = roll_mean(DS_PM10, n = 24, fill = NA, align = "right"))
datos_acumar2 <- datos_acumar %>% mutate(LM_PM10 = roll_mean(LM_PM10, n = 24, fill = NA, align = "right"))

# REORDER TABLE >> MELT
datosM_acumar <- melt(datos_acumar2, id.vars = "fecha")
datosM_acumar$variable <- as.character(datosM_acumar$variable) 
datosM_acumar$contaminante <- substring(datosM_acumar$variable, 
                                        regexpr("_", datosM_acumar$variable)+1,
                                        nchar(datosM_acumar$variable))
datosM_acumar$contaminante <- factor(datosM_acumar$contaminante)
datosM_acumar$estacion <- substring(datosM_acumar$variable, 
                                    1,
                                    regexpr("_", datosM_acumar$variable)-1)

datosM_acumar$estacion[datosM_acumar$estacion=='DS']='DKS'
datosM_acumar$estacion[datosM_acumar$estacion=='LM']='LMA'
datosM_acumar$estacion <- factor(datosM_acumar$estacion)
datosM_acumar <- datosM_acumar[-2]

# SAVE PM10 ACUMAR DATABASE
write.table(datosM_acumar, file='D:/EMPATIA/PM/PM_ACUMAR_PREPROCESADO.csv',
            sep=',', row.names=F)

################################################ 
### PREPROCESSING C.A.B.A DATABASE CONVENIO ####
################################################

rm( list = ls() )

library("openxlsx")
library(reshape2)
library(RcppRoll)
library(dplyr)


datos_apra <- read.csv("D:/EMPATIA/datos_conae_PROCESADO.csv", sep=',',dec='.')
fecha_c= as.POSIXct(datos_apra$fecha,format="%Y-%m-%d %H:%M:%OS")

datos_apra$fecha=fecha_c

# REORDER TABLE >> MELT
datosM_apra <- melt(datos_apra, id.vars = "fecha")
datosM_apra$variable <- as.character(datosM_apra$variable) 
datosM_apra$estacion <- substring(datosM_apra$variable, 
                                  regexpr("_", datosM_apra$variable)+1,
                                  nchar(datosM_apra$variable))

datosM_apra$estacion [datosM_apra$variable =='centenario']='CEN'
datosM_apra$estacion [datosM_apra$variable =='cordoba']='COR'
datosM_apra$estacion [datosM_apra$variable =='la_boca']='LBO'
#datosM_apra$estacion [datosM_apra$estacion =='PALERMO']='PAL'

datosM_apra$estacion <- factor(datosM_apra$estacion)
# datosM_apra$contaminante <- substring(datosM_apra$variable, 
#                                       1,
#                                       regexpr("_", datosM_apra$variable)-1)
# datosM_apra$contaminante <- factor(datosM_apra$contaminante)
# datosM_apra$value=as.numeric(datosM_apra$value)
# 
#datosM_apra=datosM_apra[,c(1,2,3,5,4)]
datosM_apra=datosM_apra[,c(1,3,4)]
# 
# 
# datosM_apra <- datosM_apra[-2]

# SAVE C.A.B.A DATABASE
write.table(datosM_apra, file='D:/EMPATIA/PM/PM_APRA_enviado_PROCESADO.csv',
            sep=',', row.names=F)

####################################################################################

rm( list = ls() )

# JOIN ACUMAR AND C.A.B.A DATABASES

data_acumar1=read.csv('D:/EMPATIA/PM/PM_ACUMAR_PREPROCESADO.csv',sep=',',dec='.', header=TRUE)
data_acumar=data_acumar1[,c(1,2,4)]

data_apra=read.csv('D:/EMPATIA/PM/PM_APRA_enviado_PROCESADO.csv',sep=',',dec='.', header=TRUE)


data_total=rbind(data_acumar,data_apra[,])

write.table(data_total, file='D:/EMPATIA/PM/PM_ACUMAR_y_APRA_enviado_PREPROCESADO.csv',
            sep=',', row.names=F)

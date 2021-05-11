# PROJECT: EMPATIA 
# CREATED BY: LARA DELLA cECA, FEB 2021
# MODIFIED BY: LARA S. DELLA CECA dellaceca.lara@gmail.com
# LAST MODIFICATION: 08/02/2020
# OBJECTIVE: REORDER BAHIA BLANCA PM10 DATA & CALCULATE 24 HR MOVIL MEAN FOR BAHIA BLANCA HOURLY MEASUREMENTS from BB1 and BB2 stations

setwd('D:/EMPATIA/BahiaBlanca')

library("openxlsx")
library(reshape2)
library(RcppRoll)
library(dplyr)

             
###############
####  ORGANIZE ORIGINAL DATA FROM BB1 SATATION
###############
PMBB <- read.xlsx("2010 PM10 horario.xlsx", sheet =1, startRow = 1)

PMBB[,4]=paste(PMBB[,1],' ',as.numeric(PMBB[,2]),':00:00',sep='')

PMBB[,5]=as.POSIXct(PMBB[,4],format="%Y-%m-%d %H:%M:%S")

index.LD=which(PMBB[,3]== '< LD')
index.NA=which(PMBB[,3]== '----')

PMBB[,3]=as.numeric(PMBB[,3])
PMBB[index.LD,3]=0.1333333
PMBB[index.NA,3]=NA

tabla=as.data.frame(PMBB)
tabla=tabla[,c(5,3)]

colnames(tabla)=c('Fecha','PM10')
  
for (y in 2011:2018){
  
  filename=paste(y," PM10 horario.xlsx",sep="")
  PMBB <- read.xlsx(filename, sheet =1, startRow = 1, na.strings = c("----"))
  
  PMBB[,4]=paste(PMBB[,1],' ',as.numeric(PMBB[,2]),':00:00',sep='')
  
  PMBB[,5]=as.POSIXct(PMBB[,4],format="%Y-%m-%d %H:%M:%S")
 
  index.LD=which(PMBB[,3]== '< LD')
  index.NA=which(PMBB[,3]== '----')
  
  PMBB[,3]=as.numeric(PMBB[,3])
  PMBB[index.LD,3]=0.1333333
  PMBB[index.NA,3]=NA
  
  new.df=as.data.frame(PMBB)
  new.df=new.df[,c(5,3)]
  
  colnames(new.df)=c('Fecha','PM10')
  
  filas=new.df[1:nrow(new.df),]
  
  tabla=rbind(tabla, filas)
  }

#ld.value=(min( tabla[,3],na.rm=T))/3

write.table(tabla, file='PM10_BahiaBlanca_2010-2018.csv', 
            sep=',', row.names=F)

# CALCULATION OF 24 HS MOVIL MEAN FOR BB1
tabla2 <- tabla %>% mutate(PM10 = roll_mean(PM10, n = 24, fill = NA, align = "right"))

write.table(tabla2, file='PM10_MediaMovil_24hs_BahiaBlanca_2010-2018.csv', 
            sep=',', row.names=F)




###############
####  ORGANIZE ORIGINAL DATA FROM BB2 STATION
###############


PMBB <- read.xlsx("2017 EII PM10-PM2,5 horarios.xlsx", sheet =1, startRow = 1)

PMBB[,4]=paste(PMBB[,1],' ',as.numeric(PMBB[,2]),':00:00',sep='')

PMBB[,5]=as.POSIXct(PMBB[,4],format="%Y-%m-%d %H:%M:%S")

index.LD=which(PMBB[,3]== 'F')
index.NA=which(PMBB[,3]== '---')

PMBB[,3]=as.numeric(PMBB[,3])
PMBB[index.LD,3]=0.2333333
PMBB[index.NA,3]=NA

tabla=as.data.frame(PMBB)
tabla=tabla[,c(5,3)]

colnames(tabla)=c('Fecha','PM10')

for (y in 2018:2018){
  
  filename=paste(y," EII PM10-PM2,5 horarios.xlsx",sep="")
  PMBB <- read.xlsx(filename, sheet =1, startRow = 1, na.strings = c("----"))
  
  PMBB[,4]=paste(PMBB[,1],' ',as.numeric(PMBB[,2]),':00:00',sep='')
  
  PMBB[,5]=as.POSIXct(PMBB[,4],format="%Y-%m-%d %H:%M:%S")
  
  index.LD=which(PMBB[,3]== 'F')
  index.NA=which(PMBB[,3]== '---')
  
  PMBB[,3]=as.numeric(PMBB[,3])
  PMBB[index.LD,3]=0.2333333
  PMBB[index.NA,3]=NA
  
  new.df=as.data.frame(PMBB)
  new.df=new.df[,c(5,3)]
  
  colnames(new.df)=c('Fecha','PM10')
  
  filas=new.df[1:nrow(new.df),]
  
  tabla=rbind(tabla, filas)
}

#ld.value=(min( tabla[,2],na.rm=T))/3

write.table(tabla, file='PM10_BahiaBlanca_EII_2017-2018.csv', 
            sep=',', row.names=F)

# CALCULATION OF 24 HS MOVIL MEAN FOR BB2
tabla2 <- tabla %>% mutate(PM10 = roll_mean(PM10, n = 24, fill = NA, align = "right"))

write.table(tabla2, file='PM10_MediaMovil_24hs_BahiaBlanca_EII_2017-2018.csv', 
            sep=',', row.names=F)
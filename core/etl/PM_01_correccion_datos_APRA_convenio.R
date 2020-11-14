# PROJECT: EMPATIA 
# CREATED BY: SOL REPRESA
# DATE: 12/11/2020
# OBJECTIVE: ADAPT APRA PM DATA TO WORK WITH R


rm( list = ls() )

setwd("D:/EMPATIA")

library(openxlsx)

### OPEN SENT PM DATA (CONVENIO)
CABA_APRA <- read.xlsx("datos_conae.xlsx", sheet =1, startRow = 2, detectDates = TRUE, na.strings = c("s/d", "s/d ", "S/d", "S/D"))

# Periodo de tiempo: "2010-01-01 00:01" - "2019-12-31 24:00"

fecha <- seq.POSIXt(from = as.POSIXct("2010-01-01 01:00"), to = as.POSIXct("2019-12-31 24:00"), by = "1 hour")

CABA_APRA <- data.frame( fecha = fecha,
                         centenario = CABA_APRA[,3],
                         cordoba = CABA_APRA[,4],
                         la_boca = CABA_APRA[,5])

# Reemplazo los LD <4 por LD/3
CABA_APRA$centenario <- as.character(CABA_APRA$centenario)
CABA_APRA$cordoba <- as.character(CABA_APRA$cordoba)
CABA_APRA$la_boca <- as.character(CABA_APRA$la_boca)

CABA_APRA[which(CABA_APRA$centenario == "<4"), 2]  <- 1.3
CABA_APRA[which(CABA_APRA$cordoba == "<4"), 3]  <- 1.3
CABA_APRA[which(CABA_APRA$la_boca == "<4"), 4]  <- 1.3

# Paso a numero
CABA_APRA$centenario <- as.numeric(CABA_APRA$centenario)
CABA_APRA$cordoba <- as.numeric(CABA_APRA$cordoba)
CABA_APRA$la_boca <- as.numeric(CABA_APRA$la_boca)

fileout=paste('datos_conae_PROCESADO.xlsx',sep='')
write.xlsx(CABA_APRA,fileout)

fileout=paste('datos_conae_PROCESADO.csv',sep='')
write.csv(CABA_APRA,fileout, row.names = FALSE)


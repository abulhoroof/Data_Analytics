# Author fouad@genunsys.com 
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.


###################################################
# Project specification:
# data: daily call duration in minutes
# duration: 3/1/2014 - 31/3/2016 (date format : mm/dd/yyyy)
# objective: forecast for 1 week (daily situation)
####################################################

# Clear workspace
rm(list=ls())
gc()
dev.off()
cat("\014")

#read data. SPECIFY THE PATH OF THE CSV FILE
dd <- read.csv("~/Data/Daily_min.csv",header=T) #dd = daily minutes

# Clean data
dd$X <- NULL

# Load xts and create xts
library(xts)
dd <-xts(dd[,2],order.by=as.Date(dd[,2],format="%m/%d/%Y"))
names(dd) <- "Daily minutes"

#specify frequency
p.d <- 7

# Make periodic time series
ts.dd <- ts(as.numeric(dd),
            start=1,
            frequency=p.d)



# Specify forecast period
h.daily <- 7

ts.dd
plot.ts(ts.dd, xlim=c(80,100))

# Holt Winters forecast
daily.hw <- HoltWinters(ts.dd)
daily.hw.f <- c(predict(daily.hw, h.daily))

# ARIMA forecast. 
# Diagnostic check for ARIMA fit
# plot of ACF and PACF
par(mfrow=c(2,2))
acf(ts.dd, main="ACF for observed data")
pacf(ts.dd, main="PACF for observed data")
acf(diff(ts.dd), main="ACF for differenced data")
pacf(diff(ts.dd), main="PACF for differenced data")
par(mfrow=c(1,1))

# From ACF and PACF the following orders are chosen for ARIMA fit
daily.arima <- arima(ts.dd, order = c(2,1,2), 
                     seasonal = list(order=c(1,0,0), period=p.d))

# Calculate forecast from ARIMA fit
daily.arima.f <- c(predict(daily.arima, h.daily)$pred)

# In sample fitted values
HWfitted <- c(daily.hw$fitted[,1])
ARIMAfitted <- c(fitted(daily.arima))

plot.ts(HWfitted)
# The results are complied in the accompanied csv file.

library(ggplot2)
library(forecast)
library(plotly)
library(ggfortify)
library(tseries)
library(gridExtra)
library(docstring)
library(readr)
library(here)
data_google <- read.csv("/home/praneet/Desktop/desktop2/post_paper/final_project/arima_models/mandiprice_mumbai.csv")
data_goog <- ts(data_google[2])
data_diff_goog <- diff(data_goog)
data_log_goog <- log(data_goog)
data_diff_log_goog <- diff(data_log_goog)
data_diff2_log_goog <- diff(data_diff_log_goog)
data_diff2_goog <- diff(data_diff_goog)

acf(data_goog)
acf(data_diff_goog)
acf(data_log_goog)
acf(data_diff_log_goog)
acf(data_diff2_log_goog)
acf(data_diff2_goog)

pacf(data_goog)
pacf(data_diff_goog)
pacf(data_log_goog)
pacf(data_diff_log_goog)
pacf(data_diff2_log_goog)
pacf(data_diff2_goog)


#Testing for stationarity of the data
adf.test(data_goog)
adf.test(data_diff_goog)
adf.test(data_log_goog)
adf.test(data_diff_log_goog)
adf.test(data_diff2_log_goog)
adf.test(data_diff2_goog)
#order = c(2,1,1) for retail price
model <- arima(data_goog,order=c(2,1,2))
#Need to set correct path of the file for proper execution
block_test <- read.csv("/home/praneet/Desktop/desktop2/post_paper/final_project/arima_models/mandiprice_mumbai_test.csv")
block_test = ts(block_test[2])
test_data = block_test[1:14]
predicted <- predict(model,n.ahead=14)
predicted = ts(predicted$pred)
accuracy = 100*mean(abs(exp(predicted)-test_data)/test_data)

#This model was found to be the best by using auto.arima function of R and enforcing D to be 1
seasonalmodel <-arima(ts(data,frequency=365),order=c(4,1,2),seasonal=list(order=c(0,1,0),period=365.25))
predicted2 <- predict(c,n.ahead=14)
predicted2 = ts(predicted2$pred)
accuracy = 100*mean(abs(exp(predicted2)-test_data)/test_data)

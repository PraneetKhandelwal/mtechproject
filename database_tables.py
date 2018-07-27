# This code prepares all the data files required for the web portal.
# After using this, database.sql file needs to be run to create and fill the required tables in the mysql server. 

from sklearn.metrics import f1_score
from datetime import timedelta
from datetime import datetime
import pandas as pd
import numpy as np
from constants import CONSTANTS
import matplotlib.pyplot as plt
import matplotlib
from sklearn import preprocessing
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix

import os
cwd = os.getcwd()

'''
'''




delhilabels = [2,4,1,3,1,2,2,2,3,4,1,2,2,1,4,2,5,5,2,2,3,1,5,4,2,5,5,5,3,5,3,5,2,2,5,2,2,5,5,5,2,5,5,5,2,2,2,3,1,5,1,2]
lucknowlabels = [2,1,1,2,2,2,5,4,3,1,5,5,5,3,2,2,5,5,4,3,4,5,4,2,5,5,5,5,2,2,3,2,2,5,3,2,5,2]
mumbailabels = [2,2,2,3,5,1,2,5,2,5,2,2,2,4,2,3,2,3,3,1,1,2,5,5,3,3,2,5,3,5,5,5,2,5,5,5,2,5,2,5,3,2,5,2,5,3,2,1,5,5,2,1,2,2,2,1,5,5,2]
bangalorelabels = [2,2,2,5,2,2,2,2,2,2,5,2,5,5,2,5,5,2,2,5,2,5,2,5]


# from reading_timeseries import retailP, mandiP, mandiA, retailPM, mandiPM, mandiAM
# retailpriceseriesmumbai = retailP[3]
# retailpriceseriesdelhi = retailP[1]
# retailpriceserieslucknow = retailP[2]
# print retailpriceseriesmumbai
from averageretail import getcenter
retailpriceseriesmumbai = getcenter('MUMBAI')
retailpriceseriesdelhi = getcenter('DELHI')
retailpriceserieslucknow = getcenter('LUCKNOW')
retailpriceseriesbhub = getcenter('BHUBANESHWAR')
retailpriceseriespatna = getcenter('PATNA')
retailpriceseriesbangalore = getcenter('BENGALURU')

# [retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesmumbai] = whiten_series_list([retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesmumbai])

from averagemandi import getmandi
mandipriceseriesdelhi = getmandi('Azadpur',True)
mandiarrivalseriesdelhi = getmandi('Azadpur',False)
mandipriceserieslucknow = getmandi('Bahraich',True)
mandiarrivalserieslucknow = getmandi('Bahraich',False)

mandipriceseriesbangalore = getmandi('Bangalore',True)
mandiarrivalseriesbangalore = getmandi('Bangalore',False)

from averagemandi import mandipriceseries
from averagemandi import mandiarrivalseries 
mandipriceseriesmumbai = mandipriceseries
mandiarrivalseriesmumbai = mandiarrivalseries

print mandipriceseriesdelhi
# [mandipriceseriesdelhi,mandipriceserieslucknow,mandipriceseriesmumbai] = whiten_series_list([mandipriceseriesdelhi,mandipriceserieslucknow,mandipriceseries])
# [mandiarrivalseriesdelhi,mandiarrivalserieslucknow,mandiarrivalseriesmumbai] = whiten_series_list([mandiarrivalseriesdelhi,mandiarrivalserieslucknow,mandiarrivalseries])
# mandipriceseriesdelhi = mandiP[3]
# mandipriceserieslucknow = mandiP[4]
# mandipriceseriesmumbai = mandiP[5]
# mandiarrivalseriesdelhi = mandiA[3]
# mandiarrivalserieslucknow = mandiA[4]
# mandiarrivalseriesmumbai = mandiA[5]
# print mandipriceseriesdelhi


# def adjust_anomaly_window(anomalies,series):
# 	for i in range(0,len(anomalies)):
# 		anomaly_period = series[anomalies[0][i]:anomalies[1][i]]
# 		mid_date_index = anomaly_period[10:31].argmax()
# 		# print type(mid_date_index),mid_date_index
# 		# mid_date_index - timedelta(days=21)
# 		anomalies[0][i] = mid_date_index - timedelta(days=21)
# 		anomalies[1][i] = mid_date_index + timedelta(days=21)
# 		anomalies[0][i] = datetime.strftime(anomalies[0][i],'%Y-%m-%d')
# 		anomalies[1][i] = datetime.strftime(anomalies[1][i],'%Y-%m-%d')
# 	return anomalies

def get_anomalies(path,series):
	anomalies = pd.read_csv(path, header=None, index_col=None)
	anomalies[0] = [ datetime.strftime(datetime.strptime(date, '%Y-%m-%d'),'%Y-%m-%d') for date in anomalies[0]]
	anomalies[1] = [ datetime.strftime(datetime.strptime(date, ' %Y-%m-%d'),'%Y-%m-%d') for date in anomalies[1]]
	# anomalies = adjust_anomaly_window(anomalies,series)
	return anomalies

def newlabels(anomalies,oldlabels):
	# print len(anomalies[anomalies[2] != ' Normal_train']), len(oldlabels)
	labels = []
	k=0
	for i in range(0,len(anomalies)):
		if(anomalies[2][i] == ' Normal_semi_super'):
			labels.append(9)
		elif(anomalies[2][i] != ' Normal_train'):
			labels.append(oldlabels[k])
    	  #print k,oldlabels[k]
			k = k+1
		else:
			labels.append(8)
	return labels

anomaliesmumbai = get_anomalies('data/anomaly/normal_h_w_semi_mumbai.csv',retailpriceseriesmumbai)
anomaliesdelhi = get_anomalies('data/anomaly/normal_h_w_semi_delhi.csv',retailpriceseriesdelhi)
anomalieslucknow = get_anomalies('data/anomaly/normal_h_w_semi_lucknow.csv',retailpriceserieslucknow)
anomaliesbangalore = get_anomalies('data/anomaly/normal_h_w_semi_bangalore.csv',retailpriceseriesbangalore)

delhilabelsnew = newlabels(anomaliesdelhi,delhilabels)
lucknowlabelsnew = newlabels(anomalieslucknow,lucknowlabels)
mumbailabelsnew = newlabels(anomaliesmumbai,mumbailabels)
bangalorelabelsnew = newlabels(anomaliesbangalore,bangalorelabels)

def make_csvs(retailpriceseries,anomalies,labels,mandipriceseries,mandiarrivalseries,city):
	retailpriceseries = retailpriceseries.rolling(window=30,center=True).mean()
	retailpriceseries.to_csv("../portal2/retail_"+city+".csv",sep=',',header=False)
	f = open("../portal2/anomalies_"+city+".csv",'w')
	for i in range(0,len(anomalies)):
		f.write(str(i+1)+","+str(anomalies[0][i])+","+str(anomalies[1][i])+","+str(labels[i])+"\n")
	mandipriceseries.to_csv("../portal2/mandiprice_"+city+".csv",sep=',',header=False)
	mandiarrivalseries.to_csv("../portal2/mandiarrival_"+city+".csv",sep=',',header=False)

make_csvs(retailpriceseriesmumbai,anomaliesmumbai,mumbailabelsnew,mandipriceseriesmumbai,mandiarrivalseriesmumbai,"mumbai")
make_csvs(retailpriceseriesdelhi,anomaliesdelhi,delhilabelsnew,mandipriceseriesdelhi,mandiarrivalseriesdelhi,"delhi")
make_csvs(retailpriceserieslucknow,anomalieslucknow,lucknowlabelsnew,mandipriceserieslucknow,mandiarrivalserieslucknow,"lucknow")
make_csvs(retailpriceseriesbangalore,anomaliesbangalore,bangalorelabelsnew,mandipriceseriesbangalore,mandiarrivalseriesbangalore,"bangalore")

# this code creates the normal period for all the centers and stores in the file named 'normal h w semi <centername>.csv'
# The normal periods do not overlap with any other anomalies.
# These normal periods are only introduced to serve as unlabelled articles for the semi supervised setting

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
import math

import os
cwd = os.getcwd()

'''
'''




delhilabels = [2,4,1,3,1,2,2,2,3,4,1,2,2,1,4,2,5,5,2,2,3,1,5,4,2,5,5,5,3,5,3,5,2,2,5,2,2,5,5,5,2,5,5,5,2,2,2,3,1,5,1,2]
lucknowlabels = [2,1,1,2,2,2,5,4,3,1,5,5,5,3,2,2,5,5,4,3,4,5,4,2,5,5,5,5,2,2,3,2,2,5,3,2,5,2]
mumbailabels = [2,2,2,3,5,1,2,5,2,5,2,2,2,4,2,3,2,3,3,1,1,2,5,5,3,3,2,5,3,5,5,5,2,5,5,5,2,5,2,5,3,2,5,2,5,3,2,1,5,5,2,1,2,2,2,1,5,5,2]
bangalorelabels = [2,2,2,5,2,2,2,2,2,2,5,2,5,5,2,5,5,2,2,5,2,5,2,5]

'''
['BHUBANESHWAR']
['DELHI']
['LUCKNOW']
['MUMBAI']
['PATNA']
'''

# def whiten(series):
#   '''
#   Whitening Function
#   Formula is
#     W[x x.T] = E(D^(-1/2))E.T
#   Here x: is the observed series
#   Read here more:
#   https://www.cs.helsinki.fi/u/ahyvarin/papers/NN00new.pdf
#   '''
#   import scipy
#   EigenValues, EigenVectors = np.linalg.eig(series.cov())
#   D = [[0.0 for i in range(0, len(EigenValues))] for j in range(0, len(EigenValues))]
#   for i in range(0, len(EigenValues)):
#     D[i][i] = EigenValues[i]
#   DInverse = np.linalg.matrix_power(D, -1)
#   DInverseSqRoot = scipy.linalg.sqrtm(D)
#   V = np.dot(np.dot(EigenVectors, DInverseSqRoot), EigenVectors.T)
#   series = series.apply(lambda row: np.dot(V, row.T).T, axis=1)
#   return series

# def whiten_series_list(list):
# 	for i in range(0,len(list)):
# 		mean = list[i].mean()
# 		list[i] -= mean
# 	temp = pd.DataFrame()
# 	for i in range(0,len(list)):
# 		temp[i] = list[i]
# 	temp = whiten(temp)
# 	newlist = [temp[i] for i in range(0,len(list))]
# 	return newlist

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

# print mandipriceseriesmumbai
# [mandipriceseriesdelhi,mandipriceserieslucknow,mandipriceseriesmumbai] = whiten_series_list([mandipriceseriesdelhi,mandipriceserieslucknow,mandipriceseries])
# [mandiarrivalseriesdelhi,mandiarrivalserieslucknow,mandiarrivalseriesmumbai] = whiten_series_list([mandiarrivalseriesdelhi,mandiarrivalserieslucknow,mandiarrivalseries])
# mandipriceseriesdelhi = mandiP[3]
# mandipriceserieslucknow = mandiP[4]
# mandipriceseriesmumbai = mandiP[5]
# mandiarrivalseriesdelhi = mandiA[3]
# mandiarrivalserieslucknow = mandiA[4]
# mandiarrivalseriesmumbai = mandiA[5]
# print mandipriceseriesdelhi

# def Normalise(arr):
#   '''
#   Normalise each sample
#   '''
#   m = arr.mean()
#   am = arr.min()
#   aM = arr.max()
#   arr -= m
#   arr /= (aM - am)
#   return arr

def get_derivative (series):
	derivative_series = series
	derivative_series[0] = series[1] - series[0]
	for i in range(1,len(series)-1):
		derivative_series[i] = (series[i+1]-series[i-1])/2.0
	derivative_series[len(series)-1] = series[len(series)-1]-series[len(series)-2]
	return derivative_series

mandipriceseriesmumbai_derivative = get_derivative(mandipriceseriesmumbai)
mandipriceseriesdelhi_derivative = get_derivative(mandipriceseriesdelhi)
mandipriceserieslucknow_derivative = get_derivative(mandipriceserieslucknow)
retailpriceseriesmumbai_derivative = get_derivative(retailpriceseriesmumbai)
retailpriceseriesdelhi_derivative = get_derivative(retailpriceseriesmumbai)
retailpriceserieslucknow_derivative = get_derivative(retailpriceseriesmumbai)

retailpriceseriesbangalore_derivative = get_derivative(retailpriceseriesbangalore)
mandipriceseriesbangalore_derivative = get_derivative(mandipriceseriesbangalore)


def overlapping(anomalies,s,e,labels):
  startdate = datetime.strptime(s,'%Y-%m-%d')
  # if(startdate.month >=2 and startdate.month <= 7):
  #   return True
  for i in range(0,len(anomalies)):
    if(labels[i] == 2 or labels[i] == 5 or labels[i] == 8):  
      if((anomalies[0][i]<=s and s<=anomalies[1][i]) or  (anomalies[0][i]<=e and e<=anomalies[1][i])):
        return True
  return False


# function which iterates over the entire duration and tries to generate new normal periods for the semi supervised learning

def findnormal_restricted(anomalies,series,labels):
  sdate = []
  edate = []
  date = CONSTANTS['STARTDATE']
  enddate = CONSTANTS['ENDDATE']
  from datetime import timedelta
  date = datetime.strptime(date,'%Y-%m-%d')+timedelta(days=21)
  enddate = datetime.strptime(enddate,'%Y-%m-%d')
  window = 42
  duration = timedelta(days=window)
  count  = 0
  while(duration <= enddate-date):
    s = datetime.strftime(date,'%Y-%m-%d')
    e = datetime.strftime(date+timedelta(days=window),'%Y-%m-%d') 
    x1 = (series.rolling(window=14,center=True).mean())[s:e]
    # x1 = series[s:e]
    date = date+timedelta(days=5)
    if not overlapping(anomalies,s,e,labels):
      a = x1.min()
      b = x1.max()
      if(math.isnan(a) == False and math.isnan(b) == False and b-a > 300 ):
        sdate.append(s)
        edate.append(e)
        # print b-a
        count = count + 1
        date = date+timedelta(days=40)
  print count
  return sdate,edate


def createnormalfile(path,anomaliesmumbai,retailpriceseriesmumbai,labels):
  a,b = findnormal_restricted(anomaliesmumbai,retailpriceseriesmumbai,labels)
  newdf = anomaliesmumbai
  newdf[1] = ' '+newdf[1]
  for i in range(len(a)):
    newdf.loc[i+len(anomaliesmumbai)] = [a[i],' '+b[i],' Normal_semi_super']
  result = newdf.sort_values([0])
  result.to_csv(path, header=None,index=None)



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

def get_anomalies_year(anomalies):
	mid_date_labels=[]
	for i in range(0,len(anomalies[0])):
		mid_date_labels.append(datetime.strftime(datetime.strptime(anomalies[0][i],'%Y-%m-%d')+timedelta(days=21),'%Y-%m-%d'))
	return mid_date_labels



def newlabels(anomalies,oldlabels):
  # print len(anomalies[anomalies[2] != ' Normal_train']), len(oldlabels)
  labels = []
  k=0
  for i in range(0,len(anomalies)):
    if(anomalies[2][i] != ' Normal_train'):
      labels.append(oldlabels[k])
      #print k,oldlabels[k]
      k = k+1
    else:
      labels.append(8)
  return labels




def create_normal_semi_supervised(align_m,align_d,align_l,align_b,data_m,data_d,data_l,data_b):
	anomaliesmumbai = get_anomalies('data/anomaly/normal_h_w_mumbai.csv',align_m)
	anomaliesdelhi = get_anomalies('data/anomaly/normal_h_w_delhi.csv',align_d)
	anomalieslucknow = get_anomalies('data/anomaly/normal_h_w_lucknow.csv',align_l)
	anomaliesbangalore = get_anomalies('data/anomaly/normal_h_w_bangalore.csv',align_b)

	delhilabelsnew = newlabels(anomaliesdelhi,delhilabels)
	lucknowlabelsnew = newlabels(anomalieslucknow,lucknowlabels)
	mumbailabelsnew = newlabels(anomaliesmumbai,mumbailabels)
	bangalorelabelsnew = newlabels(anomaliesbangalore,bangalorelabels)

	delhi_anomalies_year = get_anomalies_year(anomaliesdelhi)
	mumbai_anomalies_year = get_anomalies_year(anomaliesmumbai)
	lucknow_anomalies_year = get_anomalies_year(anomalieslucknow)
	bangalore_anomalies_year = get_anomalies_year(anomaliesbangalore)

	createnormalfile('data/anomaly/normal_h_w_semi_mumbai.csv',anomaliesmumbai,retailpriceseriesmumbai,mumbailabelsnew)
	createnormalfile('data/anomaly/normal_h_w_semi_delhi.csv',anomaliesdelhi,retailpriceseriesdelhi,delhilabelsnew)
	createnormalfile('data/anomaly/normal_h_w_semi_lucknow.csv',anomalieslucknow,retailpriceserieslucknow,lucknowlabelsnew)
	createnormalfile('data/anomaly/normal_h_w_semi_bangalore.csv',anomaliesbangalore,retailpriceseriesbangalore,bangalorelabelsnew)


# print type(retailpriceseriesmumbai)
# create_normal_semi_supervised(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai],[retailpriceseriesdelhi],[retailpriceserieslucknow],[retailpriceseriesbangalore])
# create_normal_semi_supervised(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[mandipriceseriesmumbai],[mandipriceseriesdelhi],[mandipriceserieslucknow],[mandipriceseriesbangalore])
# create_normal_semi_supervised(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai,mandipriceseriesmumbai],[retailpriceseriesdelhi,mandipriceseriesdelhi],[retailpriceserieslucknow,mandipriceserieslucknow],[retailpriceseriesbangalore,mandipriceseriesbangalore])
# create_normal_semi_supervised(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai-mandipriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi-mandipriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow-mandipriceserieslucknow,mandiarrivalserieslucknow],[retailpriceseriesbangalore-mandipriceseriesbangalore,mandiarrivalseriesbangalore])
# create_normal_semi_supervised(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai-mandipriceseriesmumbai],[retailpriceseriesdelhi-mandipriceseriesdelhi],[retailpriceserieslucknow-mandipriceserieslucknow],[retailpriceseriesbangalore-mandipriceseriesbangalore])
# create_normal_semi_supervised(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow,mandiarrivalserieslucknow],[retailpriceseriesbangalore,mandiarrivalseriesbangalore])
# create_normal_semi_supervised(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai,mandipriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi,mandipriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow,mandipriceserieslucknow,mandiarrivalserieslucknow],[retailpriceseriesbangalore,mandipriceseriesbangalore,mandiarrivalseriesbangalore])
# create_normal_semi_supervised(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai/mandipriceseriesmumbai],[retailpriceseriesdelhi/mandipriceseriesdelhi],[retailpriceserieslucknow/mandipriceserieslucknow],[retailpriceseriesbangalore/mandipriceseriesbangalore])

# create_normal_semi_supervised(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai,mandipriceseriesmumbai_derivative,retailpriceseriesmumbai_derivative],[retailpriceseriesdelhi,mandipriceseriesdelhi_derivative,retailpriceseriesdelhi_derivative],[retailpriceserieslucknow,mandipriceserieslucknow_derivative,retailpriceserieslucknow_derivative],[retailpriceseriesbangalore,mandipriceseriesbangalore_derivative,retailpriceseriesbangalore_derivative])
create_normal_semi_supervised(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[mandipriceseriesmumbai,mandipriceseriesmumbai_derivative,retailpriceseriesmumbai_derivative],[mandipriceseriesdelhi,mandipriceseriesdelhi_derivative,retailpriceseriesdelhi_derivative],[mandipriceserieslucknow,mandipriceserieslucknow_derivative,retailpriceserieslucknow_derivative],[mandipriceseriesbangalore,mandipriceseriesbangalore_derivative,retailpriceseriesbangalore_derivative])
# create_normal_semi_supervised(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai,mandipriceseriesmumbai,mandipriceseriesmumbai_derivative,retailpriceseriesmumbai_derivative],[retailpriceseriesdelhi,mandipriceseriesdelhi,mandipriceseriesdelhi_derivative,retailpriceseriesdelhi_derivative],[retailpriceserieslucknow,mandipriceserieslucknow,mandipriceserieslucknow_derivative,retailpriceserieslucknow_derivative],[retailpriceseriesbangalore,mandipriceseriesbangalore,mandipriceseriesbangalore_derivative,retailpriceseriesbangalore_derivative])
# create_normal_semi_supervised(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai-mandipriceseriesmumbai,mandiarrivalseriesmumbai,mandipriceseriesmumbai_derivative,retailpriceseriesmumbai_derivative],[retailpriceseriesdelhi-mandipriceseriesdelhi,mandiarrivalseriesdelhi,mandipriceseriesdelhi_derivative,retailpriceseriesdelhi_derivative],[retailpriceserieslucknow-mandipriceserieslucknow,mandiarrivalserieslucknow,mandipriceserieslucknow_derivative,retailpriceserieslucknow_derivative],[retailpriceseriesbangalore-mandipriceseriesbangalore,mandiarrivalseriesbangalore,mandipriceseriesbangalore_derivative,retailpriceseriesbangalore_derivative])
# create_normal_semi_supervised(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai-mandipriceseriesmumbai,mandipriceseriesmumbai_derivative,retailpriceseriesmumbai_derivative],[retailpriceseriesdelhi-mandipriceseriesdelhi,mandipriceseriesdelhi_derivative,retailpriceseriesdelhi_derivative],[retailpriceserieslucknow-mandipriceserieslucknow,mandipriceserieslucknow_derivative,retailpriceserieslucknow_derivative],[retailpriceseriesbangalore-mandipriceseriesbangalore,mandipriceseriesbangalore_derivative,retailpriceseriesbangalore_derivative])
# create_normal_semi_supervised(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai,mandiarrivalseriesmumbai,mandipriceseriesmumbai_derivative,retailpriceseriesmumbai_derivative],[retailpriceseriesdelhi,mandiarrivalseriesdelhi,mandipriceseriesdelhi_derivative,retailpriceseriesdelhi_derivative],[retailpriceserieslucknow,mandiarrivalserieslucknow,mandipriceserieslucknow_derivative,retailpriceserieslucknow_derivative],[retailpriceseriesbangalore,mandiarrivalseriesbangalore,mandipriceseriesbangalore_derivative,retailpriceseriesbangalore_derivative])
# create_normal_semi_supervised(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai,mandipriceseriesmumbai,mandiarrivalseriesmumbai,mandipriceseriesmumbai_derivative,retailpriceseriesmumbai_derivative],[retailpriceseriesdelhi,mandipriceseriesdelhi,mandiarrivalseriesdelhi,mandipriceseriesdelhi_derivative,retailpriceseriesdelhi_derivative],[retailpriceserieslucknow,mandipriceserieslucknow,mandiarrivalserieslucknow,mandipriceserieslucknow_derivative,retailpriceserieslucknow_derivative],[retailpriceseriesbangalore,mandipriceseriesbangalore,mandiarrivalseriesbangalore,mandipriceseriesbangalore_derivative,retailpriceseriesbangalore_derivative])
# create_normal_semi_supervised(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai/mandipriceseriesmumbai,mandipriceseriesmumbai_derivative,retailpriceseriesmumbai_derivative],[retailpriceseriesdelhi/mandipriceseriesdelhi,mandipriceseriesdelhi_derivative,retailpriceseriesdelhi_derivative],[retailpriceserieslucknow/mandipriceserieslucknow,mandipriceserieslucknow_derivative,retailpriceserieslucknow_derivative],[retailpriceseriesbangalore/mandipriceseriesbangalore,mandipriceseriesbangalore_derivative,retailpriceseriesbangalore_derivative])


# create_normal_semi_supervised(mandipriceseriesmumbai,mandipriceseriesdelhi,mandipriceserieslucknow,mandipriceseriesbangalore,[retailpriceseriesmumbai],[retailpriceseriesdelhi],[retailpriceserieslucknow],[retailpriceseriesbangalore])
# create_normal_semi_supervised(mandipriceseriesmumbai,mandipriceseriesdelhi,mandipriceserieslucknow,mandipriceseriesbangalore,[mandipriceseriesmumbai],[mandipriceseriesdelhi],[mandipriceserieslucknow],[mandipriceseriesbangalore])
# create_normal_semi_supervised(mandipriceseriesmumbai,mandipriceseriesdelhi,mandipriceserieslucknow,mandipriceseriesbangalore,[retailpriceseriesmumbai,mandipriceseriesmumbai],[retailpriceseriesdelhi,mandipriceseriesdelhi],[retailpriceserieslucknow,mandipriceserieslucknow],[retailpriceseriesbangalore,mandipriceseriesbangalore])
# create_normal_semi_supervised(mandipriceseriesmumbai,mandipriceseriesdelhi,mandipriceserieslucknow,mandipriceseriesbangalore,[retailpriceseriesmumbai-mandipriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi-mandipriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow-mandipriceserieslucknow,mandiarrivalserieslucknow],[retailpriceseriesbangalore-mandipriceseriesbangalore,mandiarrivalseriesbangalore])
# create_normal_semi_supervised(mandipriceseriesmumbai,mandipriceseriesdelhi,mandipriceserieslucknow,mandipriceseriesbangalore,[retailpriceseriesmumbai-mandipriceseriesmumbai],[retailpriceseriesdelhi-mandipriceseriesdelhi],[retailpriceserieslucknow-mandipriceserieslucknow],[retailpriceseriesbangalore-mandipriceseriesbangalore])
# create_normal_semi_supervised(mandipriceseriesmumbai,mandipriceseriesdelhi,mandipriceserieslucknow,mandipriceseriesbangalore,[retailpriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow,mandiarrivalserieslucknow],[retailpriceseriesbangalore,mandiarrivalseriesbangalore])
# create_normal_semi_supervised(mandipriceseriesmumbai,mandipriceseriesdelhi,mandipriceserieslucknow,mandipriceseriesbangalore,[retailpriceseriesmumbai,mandipriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi,mandipriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow,mandipriceserieslucknow,mandiarrivalserieslucknow],[retailpriceseriesbangalore,mandipriceseriesbangalore,mandiarrivalseriesbangalore])
# create_normal_semi_supervised(mandipriceseriesmumbai,mandipriceseriesdelhi,mandipriceserieslucknow,mandipriceseriesbangalore,[retailpriceseriesmumbai/mandipriceseriesmumbai],[retailpriceseriesdelhi/mandipriceseriesdelhi],[retailpriceserieslucknow/mandipriceserieslucknow],[retailpriceseriesbangalore/mandipriceseriesbangalore])


# create_normal_semi_supervised(retailpriceseriesmumbai-mandipriceseriesmumbai,retailpriceseriesdelhi-mandipriceseriesdelhi,retailpriceserieslucknow-mandipriceserieslucknow,retailpriceseriesbangalore-mandipriceseriesbangalore,[retailpriceseriesmumbai],[retailpriceseriesdelhi],[retailpriceserieslucknow])
# create_normal_semi_supervised(retailpriceseriesmumbai-mandipriceseriesmumbai,retailpriceseriesdelhi-mandipriceseriesdelhi,retailpriceserieslucknow-mandipriceserieslucknow,retailpriceseriesbangalore-mandipriceseriesbangalore,[mandipriceseriesmumbai],[mandipriceseriesdelhi],[mandipriceserieslucknow])
# create_normal_semi_supervised(retailpriceseriesmumbai-mandipriceseriesmumbai,retailpriceseriesdelhi-mandipriceseriesdelhi,retailpriceserieslucknow-mandipriceserieslucknow,retailpriceseriesbangalore-mandipriceseriesbangalore,[retailpriceseriesmumbai,mandipriceseriesmumbai],[retailpriceseriesdelhi,mandipriceseriesdelhi],[retailpriceserieslucknow,mandipriceserieslucknow])
# create_normal_semi_supervised(retailpriceseriesmumbai-mandipriceseriesmumbai,retailpriceseriesdelhi-mandipriceseriesdelhi,retailpriceserieslucknow-mandipriceserieslucknow,retailpriceseriesbangalore-mandipriceseriesbangalore,[retailpriceseriesmumbai-mandipriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi-mandipriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow-mandipriceserieslucknow,mandiarrivalserieslucknow])
# create_normal_semi_supervised(retailpriceseriesmumbai-mandipriceseriesmumbai,retailpriceseriesdelhi-mandipriceseriesdelhi,retailpriceserieslucknow-mandipriceserieslucknow,retailpriceseriesbangalore-mandipriceseriesbangalore,[retailpriceseriesmumbai-mandipriceseriesmumbai],[retailpriceseriesdelhi-mandipriceseriesdelhi],[retailpriceserieslucknow-mandipriceserieslucknow])
# create_normal_semi_supervised(retailpriceseriesmumbai-mandipriceseriesmumbai,retailpriceseriesdelhi-mandipriceseriesdelhi,retailpriceserieslucknow-mandipriceserieslucknow,retailpriceseriesbangalore-mandipriceseriesbangalore,[retailpriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow,mandiarrivalserieslucknow])
# create_normal_semi_supervised(retailpriceseriesmumbai-mandipriceseriesmumbai,retailpriceseriesdelhi-mandipriceseriesdelhi,retailpriceserieslucknow-mandipriceserieslucknow,retailpriceseriesbangalore-mandipriceseriesbangalore,[retailpriceseriesmumbai,mandipriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi,mandipriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow,mandipriceserieslucknow,mandiarrivalserieslucknow])
# create_normal_semi_supervised(retailpriceseriesmumbai-mandipriceseriesmumbai,retailpriceseriesdelhi-mandipriceseriesdelhi,retailpriceserieslucknow-mandipriceserieslucknow,retailpriceseriesbangalore-mandipriceseriesbangalore,[retailpriceseriesmumbai/mandipriceseriesmumbai],[retailpriceseriesdelhi/mandipriceseriesdelhi],[retailpriceserieslucknow/mandipriceserieslucknow])


# # Change the argmax to idxmin for running the part below

# create_normal_semi_supervised(mandiarrivalseriesmumbai,mandiarrivalseriesdelhi,mandiarrivalserieslucknow,mandiarrivalseriesbangalore,[retailpriceseriesmumbai],[retailpriceseriesdelhi],[retailpriceserieslucknow])
# create_normal_semi_supervised(mandiarrivalseriesmumbai,mandiarrivalseriesdelhi,mandiarrivalserieslucknow,mandiarrivalseriesbangalore,[mandipriceseriesmumbai],[mandipriceseriesdelhi],[mandipriceserieslucknow])
# create_normal_semi_supervised(mandiarrivalseriesmumbai,mandiarrivalseriesdelhi,mandiarrivalserieslucknow,mandiarrivalseriesbangalore,[retailpriceseriesmumbai,mandipriceseriesmumbai],[retailpriceseriesdelhi,mandipriceseriesdelhi],[retailpriceserieslucknow,mandipriceserieslucknow])
# create_normal_semi_supervised(mandiarrivalseriesmumbai,mandiarrivalseriesdelhi,mandiarrivalserieslucknow,mandiarrivalseriesbangalore,[retailpriceseriesmumbai-mandipriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi-mandipriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow-mandipriceserieslucknow,mandiarrivalserieslucknow])
# create_normal_semi_supervised(mandiarrivalseriesmumbai,mandiarrivalseriesdelhi,mandiarrivalserieslucknow,mandiarrivalseriesbangalore,[retailpriceseriesmumbai-mandipriceseriesmumbai],[retailpriceseriesdelhi-mandipriceseriesdelhi],[retailpriceserieslucknow-mandipriceserieslucknow])
# create_normal_semi_supervised(mandiarrivalseriesmumbai,mandiarrivalseriesdelhi,mandiarrivalserieslucknow,mandiarrivalseriesbangalore,[retailpriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow,mandiarrivalserieslucknow])
# create_normal_semi_supervised(mandiarrivalseriesmumbai,mandiarrivalseriesdelhi,mandiarrivalserieslucknow,mandiarrivalseriesbangalore,[retailpriceseriesmumbai,mandipriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi,mandipriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow,mandipriceserieslucknow,mandiarrivalserieslucknow])
# create_normal_semi_supervised(mandiarrivalseriesmumbai,mandiarrivalseriesdelhi,mandiarrivalserieslucknow,mandiarrivalseriesbangalore,[retailpriceseriesmumbai/mandipriceseriesmumbai],[retailpriceseriesdelhi/mandipriceseriesdelhi],[retailpriceserieslucknow/mandipriceserieslucknow])

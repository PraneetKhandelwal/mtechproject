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
This file checks the accuracies for only four classes of periods - Hoarding, Weather, Inflation and Normal
'''




delhilabels = [2,4,1,3,1,2,2,2,3,4,1,2,2,1,4,2,5,5,2,2,3,1,5,4,2,5,5,5,3,5,3,5,2,2,5,2,2,5,5,5,2,5,5,5,2,2,2,3,1,5,1,2]
lucknowlabels = [2,1,1,2,2,2,5,4,3,1,5,5,5,3,2,2,5,5,4,3,4,5,4,2,5,5,5,5,2,2,3,2,2,5,3,2,5,2]
mumbailabels = [2,2,2,3,5,1,2,5,2,5,2,2,2,4,2,3,2,3,3,1,1,2,5,5,3,3,2,5,3,5,5,5,2,5,5,5,2,5,2,5,3,2,5,2,5,3,2,1,5,5,2,1,2,2,2,1,5,5,2]
bangalorelabels = [2,2,2,5,2,2,2,2,2,2,5,2,5,5,2,5,5,2,2,5,2,5,2,5,2,5,2,5,5,2,2,2,2,5,5,2]
'''
['BHUBANESHWAR']
['DELHI']
['LUCKNOW']
['MUMBAI']
['PATNA']
'''

def whiten(series):
  '''
  Whitening Function
  Formula is
    W[x x.T] = E(D^(-1/2))E.T
  Here x: is the observed series
  Read here more:
  https://www.cs.helsinki.fi/u/ahyvarin/papers/NN00new.pdf
  '''
  import scipy
  EigenValues, EigenVectors = np.linalg.eig(series.cov())
  D = [[0.0 for i in range(0, len(EigenValues))] for j in range(0, len(EigenValues))]
  for i in range(0, len(EigenValues)):
    D[i][i] = EigenValues[i]
  DInverse = np.linalg.matrix_power(D, -1)
  DInverseSqRoot = scipy.linalg.sqrtm(D)
  V = np.dot(np.dot(EigenVectors, DInverseSqRoot), EigenVectors.T)
  series = series.apply(lambda row: np.dot(V, row.T).T, axis=1)
  return series

def whiten_series_list(list):
	for i in range(0,len(list)):
		mean = list[i].mean()
		list[i] -= mean
	temp = pd.DataFrame()
	for i in range(0,len(list)):
		temp[i] = list[i]
	temp = whiten(temp)
	newlist = [temp[i] for i in range(0,len(list))]
	return newlist

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
retailpriceseriesbangalore = getcenter('DELHI')

#[retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesmumbai] = whiten_series_list([retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesmumbai])

from averagemandi import getmandi
mandipriceseriesdelhi = getmandi('Azadpur',True)
mandiarrivalseriesdelhi = getmandi('Azadpur',False)
mandipriceserieslucknow = getmandi('Bahraich',True)
mandiarrivalserieslucknow = getmandi('Bahraich',False)

mandipriceseriesbangalore = getmandi('Azadpur',True)
mandiarrivalseriesbangalore = getmandi('Azadpur',False)

from averagemandi import mandipriceseries
from averagemandi import mandiarrivalseries 
mandipriceseriesmumbai = mandipriceseries
mandiarrivalseriesmumbai = mandiarrivalseries
# [mandipriceseriesdelhi,mandipriceserieslucknow,mandipriceseriesmumbai] = whiten_series_list([mandipriceseriesdelhi,mandipriceserieslucknow,mandipriceseries])
# [mandiarrivalseriesdelhi,mandiarrivalserieslucknow,mandiarrivalseriesmumbai] = whiten_series_list([mandiarrivalseriesdelhi,mandiarrivalserieslucknow,mandiarrivalseries])
# mandipriceseriesdelhi = mandiP[3]
# mandipriceserieslucknow = mandiP[4]
# mandipriceseriesmumbai = mandiP[5]
# mandiarrivalseriesdelhi = mandiA[3]
# mandiarrivalserieslucknow = mandiA[4]
# mandiarrivalseriesmumbai = mandiA[5]
# print mandipriceseriesdelhi

def Normalise(arr):
  '''
  Normalise each sample
  '''
  m = arr.mean()
  am = arr.min()
  aM = arr.max()
  arr -= m
  if(am == aM):
  	# print "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"
  	arr /= aM
  else:
  	arr /= (aM - am)
  # print arr
  return arr

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

mandipriceseriesbangalore_derivative = get_derivative(mandipriceseriesbangalore)
retailpriceseriesbangalore_derivative = get_derivative(retailpriceseriesbangalore)

def adjust_anomaly_window(anomalies,series):
	for i in range(0,len(anomalies)):
		anomaly_period = series[anomalies[0][i]:anomalies[1][i]]
		mid_date_index = anomaly_period[10:31].argmax()
		# print type(mid_date_index),mid_date_index
		# mid_date_index - timedelta(days=21)
		anomalies[0][i] = mid_date_index - timedelta(days=7)
		anomalies[1][i] = mid_date_index + timedelta(days=7)
		anomalies[0][i] = datetime.strftime(anomalies[0][i],'%Y-%m-%d')
		anomalies[1][i] = datetime.strftime(anomalies[1][i],'%Y-%m-%d')
	return anomalies

def get_anomalies(path,series):
	anomalies = pd.read_csv(path, header=None, index_col=None)
	anomalies[0] = [ datetime.strftime(datetime.strptime(date, '%Y-%m-%d'),'%Y-%m-%d') for date in anomalies[0]]
	anomalies[1] = [ datetime.strftime(datetime.strptime(date, ' %Y-%m-%d'),'%Y-%m-%d') for date in anomalies[1]]
	anomalies = adjust_anomaly_window(anomalies,series)
	return anomalies

def get_anomalies_year(anomalies):
	mid_date_labels=[]
	for i in range(0,len(anomalies[0])):
		mid_date_labels.append(datetime.strftime(datetime.strptime(anomalies[0][i],'%Y-%m-%d')+timedelta(days=21),'%Y-%m-%d'))
	return mid_date_labels



# def newlabels(anomalies,oldlabels):
# 	# print len(anomalies[anomalies[2] != ' Normal']), len(oldlabels)
# 	labels = []
# 	k=0
# 	for i in range(0,len(anomalies)):
# 		if(anomalies[2][i] == ' Normal'):
# 			labels.append(7)
# 		elif(anomalies[2][i] == ' NormalR'):
# 			labels.append(6)
# 		else:
# 			labels.append(oldlabels[k])
# # print k,oldlabels[k]
# 			k = k+1
# 	return labels


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



def prepare(anomalies,labels,priceserieslist):
	x = []
	for i in range(0,len(anomalies)):
		
		p=[]
		for j in range(0,len(priceserieslist)):
			start = anomalies[0][i]
			# end = datetime.strptime(anomalies[0][i],'%Y-%m-%d') + timedelta(days = 34)
			# end = datetime.strftime(end,'%Y-%m-%d')
			# print priceserieslist[j][start:end]
			# p += (Normalise(np.array(priceserieslist[j][start:end].tolist()))).tolist()
			p += ((np.array(priceserieslist[j][start:anomalies[1][i]].tolist()))).tolist()
		x.append(np.array(p))
	return np.array(x),np.array(labels)		


def getKey(item):
	return item[0]

def partition(xseries,yseries,year,months):
	# min_month = datetime.strptime(min(year),'%Y-%m-%d')
	# max_month = datetime.strptime(max(year),'%Y-%m-%d')
	combined_series = zip(year,xseries,yseries)
	combined_series = sorted(combined_series,key=getKey)
	train = []
	train_labels = []
	fixed = datetime.strptime('2006-01-01','%Y-%m-%d')
	i=0
	while(fixed < datetime.strptime('2017-11-01','%Y-%m-%d')):
		currx=[]
		curry=[]
		for anomaly in combined_series:
			i += 1
			if(datetime.strptime(anomaly[0],'%Y-%m-%d') > fixed and datetime.strptime(anomaly[0],'%Y-%m-%d')- fixed <= timedelta(days=months*30)):
				currx.append(anomaly[1])
				curry.append(anomaly[2])
		train.append(currx)
		train_labels.append(curry)
		fixed = fixed +timedelta(days = months*30)
	
	return np.array(train),np.array(train_labels)

def get_score(xtrain,xtest,ytrain,ytest):
	scaler = preprocessing.StandardScaler().fit(xtrain)
	xtrain = scaler.transform(xtrain)
	xtest = scaler.transform(xtest)
	model = RandomForestClassifier(max_depth=2, random_state=0)
	# model = SVC(kernel='rbf', C=0.8)
	model.fit(xtrain,ytrain)
	test_pred = np.array(model.predict(xtest))
	# ytest = np.array(ytest)
	# if(test_pred[0] == ytest[0]):
	# 	return 1
	# else:
	# 	return 0
	return test_pred

def train_test_function(align_m,align_d,align_l,align_b,data_m,data_d,data_l,data_b):
	# align = [1,2,3]
	anomaliesmumbai = get_anomalies('data/anomaly/normal_h_w_mumbai.csv',align_m)
	anomaliesdelhi = get_anomalies('data/anomaly/normal_h_w_delhi.csv',align_d)
	anomalieslucknow = get_anomalies('data/anomaly/normal_h_w_lucknow.csv',align_l)
	anomaliesbangalore = get_anomalies('data/anomaly/normal_h_w_bangalore.csv',align_b)
	delhilabelsnew = newlabels(anomaliesdelhi,delhilabels)
	lucknowlabelsnew = newlabels(anomalieslucknow,lucknowlabels)
	mumbailabelsnew = newlabels(anomaliesmumbai,mumbailabels)
	bangalorelabelsnew = newlabels(anomaliesbangalore,bangalorelabels)
	# print "Delhi --------------------------"
	x1,y1 = prepare(anomaliesdelhi,delhilabelsnew,data_d)
	# print "Mumbai --------------------------"

	x2,y2 = prepare(anomaliesmumbai,mumbailabelsnew,data_m)
	# print "Lucknow --------------------------"

	x3,y3 = prepare(anomalieslucknow,lucknowlabelsnew,data_l)

	x4,y4 = prepare(anomaliesbangalore,bangalorelabelsnew,data_b)
	# temp = 0
	# for y in y1:
	# 	if(y == 2 or y==3 or y==5):
	# 		temp = temp + 1 
	# print temp

	# temp = 0
	# for y in y2:
	# 	if(y == 2 or y==3 or y==5):
	# 		temp = temp + 1 
	# print temp
	
	# temp = 0
	# for y in y3:
	# 	if(y == 2 or y==3 or y==5):
	# 		temp = temp + 1 
	# print temp
	
	delhi_anomalies_year = get_anomalies_year(anomaliesdelhi)
	mumbai_anomalies_year = get_anomalies_year(anomaliesmumbai)
	lucknow_anomalies_year = get_anomalies_year(anomalieslucknow)
	bangalore_anomalies_year = get_anomalies_year(anomaliesbangalore)
	xall = np.array(x1.tolist()+x2.tolist()+x3.tolist()+x4.tolist())
	yall = np.array(y1.tolist()+y2.tolist()+y3.tolist()+y4.tolist())
	xall_new =[]
	yall_new = []
	yearall_new = []
	yearall = np.array(delhi_anomalies_year+mumbai_anomalies_year+lucknow_anomalies_year+bangalore_anomalies_year)
	for y in range(0,len(yall)):
		if( yall[y] == 2 or yall[y]==5 ):
			xall_new.append(xall[y])
			yall_new.append(yall[y])
			yearall_new.append(yearall[y])
		# elif(yall[y] == 3):
		# 	xall_new.append(xall[y])
		# 	yall_new.append(0)
		# 	yearall_new.append(yearall[y])

	assert(len(xall_new) == len(yearall_new))
	# print len(xall_new)
	total_data, total_labels = partition(xall_new,yall_new,yearall_new,6)
	predicted = []
	actual_labels = []
	# for temp in range(0,len(total_data)):
	# 	print len(total_data[temp])
	for i in range(0,len(total_data)):
		if( len(total_data[i]) != 0):
			test_split = total_data[i]
			test_labels = total_labels[i]
			actual_labels = actual_labels + test_labels
			train_split = []
			train_labels_split = []
			for j in range(0,len(total_data)):
				if( j != i):
					train_split = train_split + total_data[j]
					train_labels_split = train_labels_split+total_labels[j]
			# print i, train_split
			pred_test = get_score(train_split,test_split,train_labels_split,test_labels)	
			predicted = predicted + pred_test.tolist()
	predicted = np.array(predicted)
	actual_labels= np.array(actual_labels)
	# print len(actual_labels)
	print sum(predicted == actual_labels)/140.0
	from sklearn.metrics import confusion_matrix
	print confusion_matrix(actual_labels,predicted)

	# train_data = []
	# train_labels = []
	# actual_train_labels = []
	# for i in range(0,len(total_data)):
	# 	if(len(total_data[i])!= 0):
	# 		train_data = train_data + total_data[i]
	# 		train_labels = train_labels + total_labels[i]
	# 		actual_train_labels = actual_train_labels + total_labels[i]
	# pred_test = get_score(train_data,train_data,train_labels,train_labels)	
	# print sum(pred_test == actual_train_labels)/124.0

	# print actual_labels
	# print predicted
	# print f1_score(actual_labels,predicted,labels=[2,3,5],average="macro")


train_test_function(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai],[retailpriceseriesdelhi],[retailpriceserieslucknow],[retailpriceseriesbangalore])
# train_test_function(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[mandipriceseriesmumbai],[mandipriceseriesdelhi],[mandipriceserieslucknow],[mandipriceseriesbangalore])
# train_test_function(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai,mandipriceseriesmumbai],[retailpriceseriesdelhi,mandipriceseriesdelhi],[retailpriceserieslucknow,mandipriceserieslucknow],[retailpriceseriesbangalore,mandipriceseriesbangalore])
# train_test_function(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai-mandipriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi-mandipriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow-mandipriceserieslucknow,mandiarrivalserieslucknow],[retailpriceseriesbangalore-mandipriceseriesbangalore,mandiarrivalseriesbangalore])
# train_test_function(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai-mandipriceseriesmumbai],[retailpriceseriesdelhi-mandipriceseriesdelhi],[retailpriceserieslucknow-mandipriceserieslucknow],[retailpriceseriesbangalore-mandipriceseriesbangalore])
# train_test_function(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow,mandiarrivalserieslucknow],[retailpriceseriesbangalore,mandiarrivalseriesbangalore])
# train_test_function(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai,mandipriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi,mandipriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow,mandipriceserieslucknow,mandiarrivalserieslucknow],[retailpriceseriesbangalore,mandipriceseriesbangalore,mandiarrivalseriesbangalore])
# train_test_function(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai/mandipriceseriesmumbai],[retailpriceseriesdelhi/mandipriceseriesdelhi],[retailpriceserieslucknow/mandipriceserieslucknow],[retailpriceseriesbangalore/mandipriceseriesbangalore])

# train_test_function(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai,mandipriceseriesmumbai_derivative,retailpriceseriesmumbai_derivative],[retailpriceseriesdelhi,mandipriceseriesdelhi_derivative,retailpriceseriesdelhi_derivative],[retailpriceserieslucknow,mandipriceserieslucknow_derivative,retailpriceserieslucknow_derivative],[retailpriceseriesbangalore,mandipriceseriesbangalore_derivative,retailpriceseriesbangalore_derivative])
# train_test_function(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[mandipriceseriesmumbai,mandipriceseriesmumbai_derivative,retailpriceseriesmumbai_derivative],[mandipriceseriesdelhi,mandipriceseriesdelhi_derivative,retailpriceseriesdelhi_derivative],[mandipriceserieslucknow,mandipriceserieslucknow_derivative,retailpriceserieslucknow_derivative],[mandipriceseriesbangalore,mandipriceseriesbangalore_derivative,retailpriceseriesbangalore_derivative])
# train_test_function(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai,mandipriceseriesmumbai,mandipriceseriesmumbai_derivative,retailpriceseriesmumbai_derivative],[retailpriceseriesdelhi,mandipriceseriesdelhi,mandipriceseriesdelhi_derivative,retailpriceseriesdelhi_derivative],[retailpriceserieslucknow,mandipriceserieslucknow,mandipriceserieslucknow_derivative,retailpriceserieslucknow_derivative],[retailpriceseriesbangalore,mandipriceseriesbangalore,mandipriceseriesbangalore_derivative,retailpriceseriesbangalore_derivative])
# train_test_function(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai-mandipriceseriesmumbai,mandiarrivalseriesmumbai,mandipriceseriesmumbai_derivative,retailpriceseriesmumbai_derivative],[retailpriceseriesdelhi-mandipriceseriesdelhi,mandiarrivalseriesdelhi,mandipriceseriesdelhi_derivative,retailpriceseriesdelhi_derivative],[retailpriceserieslucknow-mandipriceserieslucknow,mandiarrivalserieslucknow,mandipriceserieslucknow_derivative,retailpriceserieslucknow_derivative],[retailpriceseriesbangalore-mandipriceseriesbangalore,mandiarrivalseriesbangalore,mandipriceseriesbangalore_derivative,retailpriceseriesbangalore_derivative])
# train_test_function(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai-mandipriceseriesmumbai,mandipriceseriesmumbai_derivative,retailpriceseriesmumbai_derivative],[retailpriceseriesdelhi-mandipriceseriesdelhi,mandipriceseriesdelhi_derivative,retailpriceseriesdelhi_derivative],[retailpriceserieslucknow-mandipriceserieslucknow,mandipriceserieslucknow_derivative,retailpriceserieslucknow_derivative],[retailpriceseriesbangalore-mandipriceseriesbangalore,mandipriceseriesbangalore_derivative,retailpriceseriesbangalore_derivative])
# train_test_function(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai,mandiarrivalseriesmumbai,mandipriceseriesmumbai_derivative,retailpriceseriesmumbai_derivative],[retailpriceseriesdelhi,mandiarrivalseriesdelhi,mandipriceseriesdelhi_derivative,retailpriceseriesdelhi_derivative],[retailpriceserieslucknow,mandiarrivalserieslucknow,mandipriceserieslucknow_derivative,retailpriceserieslucknow_derivative],[retailpriceseriesbangalore,mandiarrivalseriesbangalore,mandipriceseriesbangalore_derivative,retailpriceseriesbangalore_derivative])
# train_test_function(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai,mandipriceseriesmumbai,mandiarrivalseriesmumbai,mandipriceseriesmumbai_derivative,retailpriceseriesmumbai_derivative],[retailpriceseriesdelhi,mandipriceseriesdelhi,mandiarrivalseriesdelhi,mandipriceseriesdelhi_derivative,retailpriceseriesdelhi_derivative],[retailpriceserieslucknow,mandipriceserieslucknow,mandiarrivalserieslucknow,mandipriceserieslucknow_derivative,retailpriceserieslucknow_derivative],[retailpriceseriesbangalore,mandipriceseriesbangalore,mandiarrivalseriesbangalore,mandipriceseriesbangalore_derivative,retailpriceseriesbangalore_derivative])
# train_test_function(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai/mandipriceseriesmumbai,mandipriceseriesmumbai_derivative,retailpriceseriesmumbai_derivative],[retailpriceseriesdelhi/mandipriceseriesdelhi,mandipriceseriesdelhi_derivative,retailpriceseriesdelhi_derivative],[retailpriceserieslucknow/mandipriceserieslucknow,mandipriceserieslucknow_derivative,retailpriceserieslucknow_derivative],[retailpriceseriesbangalore/mandipriceseriesbangalore,mandipriceseriesbangalore_derivative,retailpriceseriesbangalore_derivative])


# train_test_function(mandipriceseriesmumbai,mandipriceseriesdelhi,mandipriceserieslucknow,mandipriceseriesbangalore,[retailpriceseriesmumbai],[retailpriceseriesdelhi],[retailpriceserieslucknow],[retailpriceseriesbangalore])
# train_test_function(mandipriceseriesmumbai,mandipriceseriesdelhi,mandipriceserieslucknow,mandipriceseriesbangalore,[mandipriceseriesmumbai],[mandipriceseriesdelhi],[mandipriceserieslucknow],[mandipriceseriesbangalore])
# train_test_function(mandipriceseriesmumbai,mandipriceseriesdelhi,mandipriceserieslucknow,mandipriceseriesbangalore,[retailpriceseriesmumbai,mandipriceseriesmumbai],[retailpriceseriesdelhi,mandipriceseriesdelhi],[retailpriceserieslucknow,mandipriceserieslucknow],[retailpriceseriesbangalore,mandipriceseriesbangalore])
# train_test_function(mandipriceseriesmumbai,mandipriceseriesdelhi,mandipriceserieslucknow,mandipriceseriesbangalore,[retailpriceseriesmumbai-mandipriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi-mandipriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow-mandipriceserieslucknow,mandiarrivalserieslucknow],[retailpriceseriesbangalore-mandipriceseriesbangalore,mandiarrivalseriesbangalore])
# train_test_function(mandipriceseriesmumbai,mandipriceseriesdelhi,mandipriceserieslucknow,mandipriceseriesbangalore,[retailpriceseriesmumbai-mandipriceseriesmumbai],[retailpriceseriesdelhi-mandipriceseriesdelhi],[retailpriceserieslucknow-mandipriceserieslucknow],[retailpriceseriesbangalore-mandipriceseriesbangalore])
# train_test_function(mandipriceseriesmumbai,mandipriceseriesdelhi,mandipriceserieslucknow,mandipriceseriesbangalore,[retailpriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow,mandiarrivalserieslucknow],[retailpriceseriesbangalore,mandiarrivalseriesbangalore])
# train_test_function(mandipriceseriesmumbai,mandipriceseriesdelhi,mandipriceserieslucknow,mandipriceseriesbangalore,[retailpriceseriesmumbai,mandipriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi,mandipriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow,mandipriceserieslucknow,mandiarrivalserieslucknow],[retailpriceseriesbangalore,mandipriceseriesbangalore,mandiarrivalseriesbangalore])
# train_test_function(mandipriceseriesmumbai,mandipriceseriesdelhi,mandipriceserieslucknow,mandipriceseriesbangalore,[retailpriceseriesmumbai/mandipriceseriesmumbai],[retailpriceseriesdelhi/mandipriceseriesdelhi],[retailpriceserieslucknow/mandipriceserieslucknow],[retailpriceseriesbangalore/mandipriceseriesbangalore])


# train_test_function(retailpriceseriesmumbai-mandipriceseriesmumbai,retailpriceseriesdelhi-mandipriceseriesdelhi,retailpriceserieslucknow-mandipriceserieslucknow,[retailpriceseriesmumbai],[retailpriceseriesdelhi],[retailpriceserieslucknow])
# train_test_function(retailpriceseriesmumbai-mandipriceseriesmumbai,retailpriceseriesdelhi-mandipriceseriesdelhi,retailpriceserieslucknow-mandipriceserieslucknow,[mandipriceseriesmumbai],[mandipriceseriesdelhi],[mandipriceserieslucknow])
# train_test_function(retailpriceseriesmumbai-mandipriceseriesmumbai,retailpriceseriesdelhi-mandipriceseriesdelhi,retailpriceserieslucknow-mandipriceserieslucknow,[retailpriceseriesmumbai,mandipriceseriesmumbai],[retailpriceseriesdelhi,mandipriceseriesdelhi],[retailpriceserieslucknow,mandipriceserieslucknow])
# train_test_function(retailpriceseriesmumbai-mandipriceseriesmumbai,retailpriceseriesdelhi-mandipriceseriesdelhi,retailpriceserieslucknow-mandipriceserieslucknow,[retailpriceseriesmumbai-mandipriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi-mandipriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow-mandipriceserieslucknow,mandiarrivalserieslucknow])
# train_test_function(retailpriceseriesmumbai-mandipriceseriesmumbai,retailpriceseriesdelhi-mandipriceseriesdelhi,retailpriceserieslucknow-mandipriceserieslucknow,[retailpriceseriesmumbai-mandipriceseriesmumbai],[retailpriceseriesdelhi-mandipriceseriesdelhi],[retailpriceserieslucknow-mandipriceserieslucknow])
# train_test_function(retailpriceseriesmumbai-mandipriceseriesmumbai,retailpriceseriesdelhi-mandipriceseriesdelhi,retailpriceserieslucknow-mandipriceserieslucknow,[retailpriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow,mandiarrivalserieslucknow])
# train_test_function(retailpriceseriesmumbai-mandipriceseriesmumbai,retailpriceseriesdelhi-mandipriceseriesdelhi,retailpriceserieslucknow-mandipriceserieslucknow,[retailpriceseriesmumbai,mandipriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi,mandipriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow,mandipriceserieslucknow,mandiarrivalserieslucknow])
# train_test_function(retailpriceseriesmumbai-mandipriceseriesmumbai,retailpriceseriesdelhi-mandipriceseriesdelhi,retailpriceserieslucknow-mandipriceserieslucknow,[retailpriceseriesmumbai/mandipriceseriesmumbai],[retailpriceseriesdelhi/mandipriceseriesdelhi],[retailpriceserieslucknow/mandipriceserieslucknow])


#Change the argmax to idxmin for running the part below

# train_test_function(mandiarrivalseriesmumbai,mandiarrivalseriesdelhi,mandiarrivalserieslucknow,[retailpriceseriesmumbai],[retailpriceseriesdelhi],[retailpriceserieslucknow])
# train_test_function(mandiarrivalseriesmumbai,mandiarrivalseriesdelhi,mandiarrivalserieslucknow,[mandipriceseriesmumbai],[mandipriceseriesdelhi],[mandipriceserieslucknow])
# train_test_function(mandiarrivalseriesmumbai,mandiarrivalseriesdelhi,mandiarrivalserieslucknow,[retailpriceseriesmumbai,mandipriceseriesmumbai],[retailpriceseriesdelhi,mandipriceseriesdelhi],[retailpriceserieslucknow,mandipriceserieslucknow])
# train_test_function(mandiarrivalseriesmumbai,mandiarrivalseriesdelhi,mandiarrivalserieslucknow,[retailpriceseriesmumbai-mandipriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi-mandipriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow-mandipriceserieslucknow,mandiarrivalserieslucknow])
# train_test_function(mandiarrivalseriesmumbai,mandiarrivalseriesdelhi,mandiarrivalserieslucknow,[retailpriceseriesmumbai-mandipriceseriesmumbai],[retailpriceseriesdelhi-mandipriceseriesdelhi],[retailpriceserieslucknow-mandipriceserieslucknow])
# train_test_function(mandiarrivalseriesmumbai,mandiarrivalseriesdelhi,mandiarrivalserieslucknow,[retailpriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow,mandiarrivalserieslucknow])
# train_test_function(mandiarrivalseriesmumbai,mandiarrivalseriesdelhi,mandiarrivalserieslucknow,[retailpriceseriesmumbai,mandipriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi,mandipriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow,mandipriceserieslucknow,mandiarrivalserieslucknow])
# train_test_function(mandiarrivalseriesmumbai,mandiarrivalseriesdelhi,mandiarrivalserieslucknow,[retailpriceseriesmumbai/mandipriceseriesmumbai],[retailpriceseriesdelhi/mandipriceseriesdelhi],[retailpriceserieslucknow/mandipriceserieslucknow])


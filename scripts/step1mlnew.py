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
from sklearn.semi_supervised import label_propagation
from random import random
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

from weightedarrivals import delhians,mumbaians,lucknowans
mandiarrivalseriesdelhi = delhians
mandiarrivalseriesmumbai = mumbaians
mandiarrivalserieslucknow = lucknowans 
mandiarrivalseriesbangalore = mandiarrivalseriesbangalore
# This is because only one mandi in bangalore had more than 0 data that is Bangalore


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

def adjust_anomaly_window(anomalies,series):
	for i in range(0,len(anomalies)):
		anomaly_period = series[anomalies[0][i]:anomalies[1][i]]
		mid_date_index = anomaly_period[10:31].argmax()
		# print type(mid_date_index),mid_date_index
		# mid_date_index - timedelta(days=21)
		anomalies[0][i] = mid_date_index - timedelta(days=21)
		anomalies[1][i] = mid_date_index + timedelta(days=21)
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



def newlabels(anomalies,semilabels_path):
  # print len(anomalies[anomalies[2] != ' Normal_train']), len(oldlabels)
	labels = []
	semi_labels = pd.read_csv(semilabels_path, header=None, index_col=None)
	for i in range(0,len(anomalies)): 
	    labels.append(semi_labels[0][i])
	return labels

# def cost_function(yaxis):
# 	# yaxis = yaxis[0:days]
# 	a = yaxis.min()
# 	b = yaxis.max()
# 	# if( b- a > 10000):
# 	# 	print yaxis
# 	return b-a

# def semisuperlabels(anomalies,oldlabels,retailseries):
# 	labels = []
# 	count1 = 0
# 	count2 =0
# 	count3 = 0
# 	count4 = 0
# 	for i in range(0,len(anomalies)):
# 		parameter = cost_function(retailseries[anomalies[0][i]:anomalies[1][i]])
# 		# print oldlabels[i], "    ",parameter
# 		if(oldlabels[i] == 8 and parameter <= 300):
# 			labels.append(0)
# 			count1 +=1 
# 		elif(oldlabels[i] == 8 and parameter > 300):
# 			labels.append(-1)
# 			count2 +=1 
# 		elif((oldlabels[i] == 2 or oldlabels[i] == 5) and parameter >= 100):
# 			labels.append(1)
# 			count3 +=1 
# 		elif((oldlabels[i] == 2 or oldlabels[i] == 5) and parameter < 100):
# 			labels.append(-1)
# 			count4 +=1 
# 		else:
# 			labels.append(oldlabels[i])
# 	print count1
# 	print count2
# 	print count3
# 	print count4
# 	return labels




def prepare(anomalies,labels,priceserieslist):
	x = []
	last_index = -1
	for i in range(0,len(anomalies)):
		p=[]

		# if(last_index==-1):
		# 	p=p+[0]
		# else:
		# 	if(datetime.strptime(anomalies[0][i],'%Y-%m-%d') - datetime.strptime(anomalies[1][last_index],'%Y-%m-%d') <= timedelta(days=15)):
		# 		p=p+[1]
		# 	else:
		# 		p=p+[0]
		# if(labels[i] == 1):
		# 	last_index = i
		for j in range(0,len(priceserieslist)):
			start = anomalies[0][i]
			end = datetime.strptime(anomalies[0][i],'%Y-%m-%d') + timedelta(days = 43)
			# p += (Normalise(np.array(priceserieslist[j][anomalies[0][i]:anomalies[1][i]].tolist()))).tolist()
			p += ((np.array(priceserieslist[j][start:end].tolist()))).tolist()

			# if(i==0):
			# 	print anomalies[0][i], anomalies[1][i]
		# print len(p), anomalies[0][i], anomalies[1][i]
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
	# print fixed
	# train.append(currx)
	# train_labels.append(curry)
	return np.array(train),np.array(train_labels)

def get_score(xtrain,xtest,ytrain,ytest):
	scaler = preprocessing.StandardScaler().fit(xtrain)
	xtrain = scaler.transform(xtrain)
	xtest = scaler.transform(xtest)
	# model = label_propagation.LabelSpreading(kernel='rbf', alpha=0.2)
	model = RandomForestClassifier(max_depth=2, random_state=0)
	
	model.fit(xtrain,ytrain)
	test_pred = np.array(model.predict(xtest))
	# ytest = np.array(ytest)
	# if(test_pred[0] == ytest[0]):
	# 	return 1
	# else:
	# 	return 0
	return test_pred

def get_anomaly_id(anomalies,center):
	anomaly_id_list = []
	for i in range(0,len(anomalies)):
		anomaly_id_list.append((center,i))
	return anomaly_id_list

def newlabels2(anomalies,oldlabels):
  # print len(anomalies[anomalies[2] != ' Normal_train']), len(oldlabels)
  labels = []
  k=0
  for i in range(0,len(anomalies)):
    if(anomalies[2][i] == ' Normal_train'):
      labels.append(8)
    elif(anomalies[2][i] == ' Normal_semi_super'):
    	labels.append(9)
    else:
      labels.append(oldlabels[k])
      #print k,oldlabels[k]
      k = k+1
  return labels

def train_test_function(align_m,align_d,align_l,align_b,data_m,data_d,data_l,data_b):
	anomaliesmumbai = get_anomalies('data/anomaly/normal_h_w_semi_mumbai.csv',align_m)
	anomaliesdelhi = get_anomalies('data/anomaly/normal_h_w_semi_delhi.csv',align_d)
	anomalieslucknow = get_anomalies('data/anomaly/normal_h_w_semi_lucknow.csv',align_l)
	anomaliesbangalore = get_anomalies('data/anomaly/normal_h_w_semi_bangalore.csv',align_b)



	delhilabelsnew = newlabels(anomaliesdelhi,"data/anomaly/semi_labels_delhi.csv")
	lucknowlabelsnew = newlabels(anomalieslucknow,"data/anomaly/semi_labels_lucknow.csv")
	mumbailabelsnew = newlabels(anomaliesmumbai,"data/anomaly/semi_labels_mumbai.csv")
	bangalorelabelsnew = newlabels(anomaliesbangalore,"data/anomaly/semi_labels_bangalore.csv")

	# anomaliesall = pd.concat([anomaliesdelhi,anomaliesmumbai,anomalieslucknow,anomaliesbangalore],ignore_index = True)
	
	# delhilabelsnew = newlabels2(anomaliesdelhi,delhilabels)
	# lucknowlabelsnew = newlabels2(anomalieslucknow,lucknowlabels)
	# mumbailabelsnew = newlabels2(anomaliesmumbai,mumbailabels)
	# bangalorelabelsnew = newlabels2(anomaliesbangalore,bangalorelabels)


	delhi_anomaly_id = get_anomaly_id(anomaliesdelhi,"Delhi")
	mumbai_anomaly_id = get_anomaly_id(anomaliesmumbai,"Mumbai")
	lucknow_anomaly_id = get_anomaly_id(anomalieslucknow,"Lucknow")
	bangalore_anomaly_id = get_anomaly_id(anomaliesbangalore,"Bangalore")


	delhi_anomalies_year = get_anomalies_year(anomaliesdelhi)
	mumbai_anomalies_year = get_anomalies_year(anomaliesmumbai)
	lucknow_anomalies_year = get_anomalies_year(anomalieslucknow)
	bangalore_anomalies_year = get_anomalies_year(anomaliesbangalore)

	x1,y1 = prepare(anomaliesdelhi,delhilabelsnew,data_d)
	x2,y2 = prepare(anomaliesmumbai,mumbailabelsnew,data_m)
	x3,y3 = prepare(anomalieslucknow,lucknowlabelsnew,data_l)
	x4,y4 = prepare(anomaliesbangalore,bangalorelabelsnew,data_b)

	xall = np.array(x1.tolist()+x2.tolist()+x3.tolist()+x4.tolist())
	yall = np.array(y1.tolist()+y2.tolist()+y3.tolist()+y4.tolist())
	xall_new =[]
	yall_new = []
	yearall_new = []
	yearall = np.array(delhi_anomalies_year+mumbai_anomalies_year+lucknow_anomalies_year+bangalore_anomalies_year)
	
	anomaly_id = np.array(delhi_anomaly_id+mumbai_anomaly_id+lucknow_anomaly_id+bangalore_anomaly_id)
	# delhilabels_semi_super = semisuperlabels(anomaliesdelhi,delhilabelsnew,retailpriceseriesdelhi)
	# lucknowlabels_semi_super = semisuperlabels(anomalieslucknow,lucknowlabelsnew,retailpriceserieslucknow)
	# mumbailabels_semi_super = semisuperlabels(anomaliesmumbai,mumbailabelsnew,retailpriceseriesmumbai)
	# bangalorelabels_semi_super = semisuperlabels(anomaliesbangalore,bangalorelabelsnew,retailpriceseriesbangalore)
	# assert(len(delhilabels_semi_super) == len(delhilabelsnew))
	delhilabels_semi_super = np.array(delhilabelsnew)
	mumbailabels_semi_super = np.array(mumbailabelsnew)
	lucknowlabels_semi_super = np.array(lucknowlabelsnew)
	bangalorelabels_semi_super = np.array(bangalorelabelsnew)
	yall_semi_super = np.array(delhilabels_semi_super.tolist()+mumbailabels_semi_super.tolist()+lucknowlabels_semi_super.tolist()+bangalorelabels_semi_super.tolist())
	yall_semi_super_new = []
	anomaly_id_new = []



	 
	count = 0
	for y in range(0,len(yall)):
		if( yall[y] == 0 or yall[y] == 1 ):
			xall_new.append(xall[y])
			yall_new.append(yall[y])
			yearall_new.append(yearall[y])
			yall_semi_super_new.append(yall_semi_super[y])
			anomaly_id_new.append(anomaly_id[y])
		# elif (yall[y] == -1):
		# 	xall_new.append(xall[y])
		# 	yall_new.append(-1)
		# 	yearall_new.append(yearall[y])
		# 	yall_semi_super_new.append(-1)
		# 	count +=1
		# elif (yall[y] == 2):
		# 	xall_new.append(xall[y])
		# 	yall_new.append(0)
		# 	yearall_new.append(yearall[y])
		# 	yall_semi_super_new.append(0)

	# print count
	# xall_new = np.array(xall_new)
	# yall_new = np.array(yall_new)
	assert(len(xall_new) == len(yearall_new))
	assert(len(yall_new) == len(yall_semi_super_new))
	total_data_extra, actual_anomaly_id = partition(xall_new,anomaly_id_new,yearall_new,6)
	total_data, total_labels = partition(xall_new,yall_semi_super_new,yearall_new,6)
	
	# for pra in range(0,len(total_data)):
	# 	for pra2 in range(0,len(total_data[pra])):
	# 		print len(total_data[pra][pra2])			
	predicted = []
	actual_labels = []
	test_anomaly_id = []
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
			pred_test = get_score(train_split,test_split,train_labels_split,test_labels)	
			predicted = predicted + pred_test.tolist()
			test_anomaly_id = test_anomaly_id + actual_anomaly_id[i]
	predicted = np.array(predicted)
	actual_labels= np.array(actual_labels)
	test_anomaly_id = np.array(test_anomaly_id)
	actual_labels_new = []
	predicted_new = []
	test_anomaly_id_new = []

	for j in range(0,len(actual_labels)):
		if(actual_labels[j] >= 0):
			actual_labels_new.append(actual_labels[j])
			predicted_new.append(predicted[j])
			# test_anomaly_id_new.append(test_anomaly_id[j])
			
	
	predicted_new = np.array(predicted_new)
	actual_labels_new = np.array(actual_labels_new)
	test_anomaly_id_new = np.array(test_anomaly_id_new)
	correct_anomaly_id = []
	# print len(actual_labels_new)
	print sum(predicted_new == actual_labels_new)/161.0
	# for k in range(0,len(predicted_new)):
	# 	if(predicted_new[k] == actual_labels_new[k]):
	# 		correct_anomaly_id.append(test_anomaly_id_new[k])
	# f = open("data/correct_predictions.csv",'w')
	# for m in range(0,len(correct_anomaly_id)):
	# 	f.write(correct_anomaly_id[m][0]+","+str(correct_anomaly_id[m][1])+"\n")
	

	# print acc/total
	# print actual_labels
	# print predicted
	# print f1_score(actual_labels,predicted,labels=[0,1],average="macro")
	from sklearn.metrics import confusion_matrix
	print confusion_matrix(actual_labels_new,predicted_new)

# train_test_function(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai],[retailpriceseriesdelhi],[retailpriceserieslucknow],[retailpriceseriesbangalore])
# train_test_function(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[mandipriceseriesmumbai],[mandipriceseriesdelhi],[mandipriceserieslucknow],[mandipriceseriesbangalore])
# train_test_function(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai,mandipriceseriesmumbai],[retailpriceseriesdelhi,mandipriceseriesdelhi],[retailpriceserieslucknow,mandipriceserieslucknow],[retailpriceseriesbangalore,mandipriceseriesbangalore])
# train_test_function(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai-mandipriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi-mandipriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow-mandipriceserieslucknow,mandiarrivalserieslucknow],[retailpriceseriesbangalore-mandipriceseriesbangalore,mandiarrivalseriesbangalore])
# train_test_function(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai-mandipriceseriesmumbai],[retailpriceseriesdelhi-mandipriceseriesdelhi],[retailpriceserieslucknow-mandipriceserieslucknow],[retailpriceseriesbangalore-mandipriceseriesbangalore])
# train_test_function(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow,mandiarrivalserieslucknow],[retailpriceseriesbangalore,mandiarrivalseriesbangalore])
# train_test_function(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai,mandipriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi,mandipriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow,mandipriceserieslucknow,mandiarrivalserieslucknow],[retailpriceseriesbangalore,mandipriceseriesbangalore,mandiarrivalseriesbangalore])
# train_test_function(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai/mandipriceseriesmumbai],[retailpriceseriesdelhi/mandipriceseriesdelhi],[retailpriceserieslucknow/mandipriceserieslucknow],[retailpriceseriesbangalore/mandipriceseriesbangalore])

train_test_function(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai,mandipriceseriesmumbai_derivative,retailpriceseriesmumbai_derivative],[retailpriceseriesdelhi,mandipriceseriesdelhi_derivative,retailpriceseriesdelhi_derivative],[retailpriceserieslucknow,mandipriceserieslucknow_derivative,retailpriceserieslucknow_derivative],[retailpriceseriesbangalore,mandipriceseriesbangalore_derivative,retailpriceseriesbangalore_derivative])
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


# train_test_function(retailpriceseriesmumbai-mandipriceseriesmumbai,retailpriceseriesdelhi-mandipriceseriesdelhi,retailpriceserieslucknow-mandipriceserieslucknow,retailpriceseriesbangalore-mandipriceseriesbangalore,[retailpriceseriesmumbai],[retailpriceseriesdelhi],[retailpriceserieslucknow])
# train_test_function(retailpriceseriesmumbai-mandipriceseriesmumbai,retailpriceseriesdelhi-mandipriceseriesdelhi,retailpriceserieslucknow-mandipriceserieslucknow,retailpriceseriesbangalore-mandipriceseriesbangalore,[mandipriceseriesmumbai],[mandipriceseriesdelhi],[mandipriceserieslucknow])
# train_test_function(retailpriceseriesmumbai-mandipriceseriesmumbai,retailpriceseriesdelhi-mandipriceseriesdelhi,retailpriceserieslucknow-mandipriceserieslucknow,retailpriceseriesbangalore-mandipriceseriesbangalore,[retailpriceseriesmumbai,mandipriceseriesmumbai],[retailpriceseriesdelhi,mandipriceseriesdelhi],[retailpriceserieslucknow,mandipriceserieslucknow])
# train_test_function(retailpriceseriesmumbai-mandipriceseriesmumbai,retailpriceseriesdelhi-mandipriceseriesdelhi,retailpriceserieslucknow-mandipriceserieslucknow,retailpriceseriesbangalore-mandipriceseriesbangalore,[retailpriceseriesmumbai-mandipriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi-mandipriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow-mandipriceserieslucknow,mandiarrivalserieslucknow])
# train_test_function(retailpriceseriesmumbai-mandipriceseriesmumbai,retailpriceseriesdelhi-mandipriceseriesdelhi,retailpriceserieslucknow-mandipriceserieslucknow,retailpriceseriesbangalore-mandipriceseriesbangalore,[retailpriceseriesmumbai-mandipriceseriesmumbai],[retailpriceseriesdelhi-mandipriceseriesdelhi],[retailpriceserieslucknow-mandipriceserieslucknow])
# train_test_function(retailpriceseriesmumbai-mandipriceseriesmumbai,retailpriceseriesdelhi-mandipriceseriesdelhi,retailpriceserieslucknow-mandipriceserieslucknow,retailpriceseriesbangalore-mandipriceseriesbangalore,[retailpriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow,mandiarrivalserieslucknow])
# train_test_function(retailpriceseriesmumbai-mandipriceseriesmumbai,retailpriceseriesdelhi-mandipriceseriesdelhi,retailpriceserieslucknow-mandipriceserieslucknow,retailpriceseriesbangalore-mandipriceseriesbangalore,[retailpriceseriesmumbai,mandipriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi,mandipriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow,mandipriceserieslucknow,mandiarrivalserieslucknow])
# train_test_function(retailpriceseriesmumbai-mandipriceseriesmumbai,retailpriceseriesdelhi-mandipriceseriesdelhi,retailpriceserieslucknow-mandipriceserieslucknow,retailpriceseriesbangalore-mandipriceseriesbangalore,[retailpriceseriesmumbai/mandipriceseriesmumbai],[retailpriceseriesdelhi/mandipriceseriesdelhi],[retailpriceserieslucknow/mandipriceserieslucknow])


# # Change the argmax to idxmin for running the part below

# train_test_function(mandiarrivalseriesmumbai,mandiarrivalseriesdelhi,mandiarrivalserieslucknow,mandiarrivalseriesbangalore,[retailpriceseriesmumbai],[retailpriceseriesdelhi],[retailpriceserieslucknow])
# train_test_function(mandiarrivalseriesmumbai,mandiarrivalseriesdelhi,mandiarrivalserieslucknow,mandiarrivalseriesbangalore,[mandipriceseriesmumbai],[mandipriceseriesdelhi],[mandipriceserieslucknow])
# train_test_function(mandiarrivalseriesmumbai,mandiarrivalseriesdelhi,mandiarrivalserieslucknow,mandiarrivalseriesbangalore,[retailpriceseriesmumbai,mandipriceseriesmumbai],[retailpriceseriesdelhi,mandipriceseriesdelhi],[retailpriceserieslucknow,mandipriceserieslucknow])
# train_test_function(mandiarrivalseriesmumbai,mandiarrivalseriesdelhi,mandiarrivalserieslucknow,mandiarrivalseriesbangalore,[retailpriceseriesmumbai-mandipriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi-mandipriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow-mandipriceserieslucknow,mandiarrivalserieslucknow])
# train_test_function(mandiarrivalseriesmumbai,mandiarrivalseriesdelhi,mandiarrivalserieslucknow,mandiarrivalseriesbangalore,[retailpriceseriesmumbai-mandipriceseriesmumbai],[retailpriceseriesdelhi-mandipriceseriesdelhi],[retailpriceserieslucknow-mandipriceserieslucknow])
# train_test_function(mandiarrivalseriesmumbai,mandiarrivalseriesdelhi,mandiarrivalserieslucknow,mandiarrivalseriesbangalore,[retailpriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow,mandiarrivalserieslucknow])
# train_test_function(mandiarrivalseriesmumbai,mandiarrivalseriesdelhi,mandiarrivalserieslucknow,mandiarrivalseriesbangalore,[retailpriceseriesmumbai,mandipriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi,mandipriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow,mandipriceserieslucknow,mandiarrivalserieslucknow])
# train_test_function(mandiarrivalseriesmumbai,mandiarrivalseriesdelhi,mandiarrivalserieslucknow,mandiarrivalseriesbangalore,[retailpriceseriesmumbai/mandipriceseriesmumbai],[retailpriceseriesdelhi/mandipriceseriesdelhi],[retailpriceserieslucknow/mandipriceserieslucknow])

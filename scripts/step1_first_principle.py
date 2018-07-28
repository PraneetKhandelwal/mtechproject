# Function to perform step 1 analysis using rule based classification
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
from sklearn import linear_model

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
# [mandipriceseriesdelhi,mandipriceserieslucknow,mandipriceseriesmumbai] = whiten_series_list([mandipriceseriesdelhi,mandipriceserieslucknow,mandipriceseries])
# [mandiarrivalseriesdelhi,mandiarrivalserieslucknow,mandiarrivalseriesmumbai] = whiten_series_list([mandiarrivalseriesdelhi,mandiarrivalserieslucknow,mandiarrivalseries])

'''
Returns average series from start date to end date after rolling.
If end-start > 1year the pattern repeats
'''
def give_average_series(start,end,mandiarrivalseries):
  mandiarrivalexpected = mandiarrivalseries.rolling(window=30,center=True).mean()
  #mandiarrivalexpected = mandiarrivalseries
  mandiarrivalexpected = mandiarrivalexpected.groupby([mandiarrivalseries.index.month, mandiarrivalseries.index.day]).mean()
  idx = pd.date_range(start, end)
  data = [ (mandiarrivalexpected[index.month][index.day]) for index in idx]
  expectedarrivalseries = pd.Series(data, index=idx)
  return expectedarrivalseries


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

def get_anomalies(path,series,align):
	anomalies = pd.read_csv(path, header=None, index_col=None)
	anomalies[0] = [ datetime.strftime(datetime.strptime(date, '%Y-%m-%d'),'%Y-%m-%d') for date in anomalies[0]]
	anomalies[1] = [ datetime.strftime(datetime.strptime(date, ' %Y-%m-%d'),'%Y-%m-%d') for date in anomalies[1]]
	# for i in range(0,len(anomalies[0])):
	# 	print anomalies[0][i], anomalies[1][i]
	if align:
		anomalies = adjust_anomaly_window(anomalies,series)
	return anomalies

def get_anomalies_year(anomalies):
	mid_date_labels=[]
	for i in range(0,len(anomalies[0])):
		mid_date_labels.append(datetime.strftime(datetime.strptime(anomalies[0][i],'%Y-%m-%d')+timedelta(days=21),'%Y-%m-%d'))
	return mid_date_labels



# def newlabels(anomalies,oldlabels):
#   # print len(anomalies[anomalies[2] != ' Normal']), len(oldlabels)
# 	labels = []
# 	k=0
# 	for i in range(0,len(anomalies)):
# 		if(anomalies[2][i] == ' Normal'):
# 			labels.append(7)
# 		elif(anomalies[2][i] == ' NormalR'):
# 			labels.append(6)
# 		else:
# 			labels.append(oldlabels[k])
#       #print k,oldlabels[k]
# 			k = k+1
# 	return labels

def newlabels(anomalies,oldlabels):
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

def Normalise(arr):
  '''
  Normalise each sample
  '''
  m = arr.mean()
  am = arr.min()
  aM = arr.max()
  arr -= m
  arr /= (aM - am)
  return arr




def prepare(anomalies,labels,priceserieslist):
	x = []
	for i in range(0,len(anomalies)):
		p=[]
		for j in range(0,len(priceserieslist)):
			p += ((np.array(priceserieslist[j][anomalies[0][i]:anomalies[1][i]].tolist()))).tolist()
		x.append(np.array(p))
	return np.array(x),np.array(labels)		

DAYS = 21



# Different cost fucntions used for experimentation
# Fucntion which regresses on the input series as outputs the slope of the regression
def cost_function(yaxis,start,end,days):
	xaxis = []
	for i in range(1,days+1):
		xaxis.append([i])
	yaxis = yaxis[0:days]
	xaxis = np.array(xaxis)
	# print len(xaxis), len(yaxis)
	regr = linear_model.LinearRegression()
	regr.fit(xaxis,yaxis)

	return regr.coef_[0]

# Function which returns the difference between max and min of the series in the 3 day window
def cost_function2(yaxis,start,end,days):
	yaxis = yaxis[0:days]
	a = yaxis.min()
	b = yaxis.max()
	# if( b- a > 10000):
	# 	print yaxis
	return b-a
# Function which returns the mean of the deviation of the current 43 day window from the average during that time of the year
def cost_function3(yaxis,start,end,series,days):
	avg = give_average_series(start,end,series)
	avg = np.array(avg)
	deviation = yaxis - avg
	# print len(avg), len(yaxis), len(deviation)
	# print type(avg), type(yaxis), type(deviation)
	# print avg
	# print yaxis
	# print deviation
	deviation = deviation[0:days]
	return deviation.mean()
	# return 0
def newlabels2(anomalies,semilabels_path):
  # print len(anomalies[anomalies[2] != ' Normal_train']), len(oldlabels)
	labels = []
	semi_labels = pd.read_csv(semilabels_path, header=None, index_col=None)
	for i in range(0,len(anomalies)): 
	    labels.append(semi_labels[0][i])
	return labels


def first_principle(align_m,align_d,align_l,align_b,data_m,data_d,data_l,data_b):
	
	anomaliesdelhi = get_anomalies('data/anomaly/normal_h_w_semi_delhi.csv',align_d,True)
	anomaliesmumbai = get_anomalies('data/anomaly/normal_h_w_semi_mumbai.csv',align_m,True)
	anomalieslucknow = get_anomalies('data/anomaly/normal_h_w_semi_lucknow.csv',align_l,True)
	anomaliesbangalore = get_anomalies('data/anomaly/normal_h_w_semi_bangalore.csv',align_b,True)
	
	anomaliesall = pd.concat([anomaliesdelhi,anomaliesmumbai,anomalieslucknow,anomaliesbangalore],ignore_index = True)
	
	delhilabelsnew = newlabels2(anomaliesdelhi,"data/anomaly/semi_labels_delhi.csv")
	lucknowlabelsnew = newlabels2(anomalieslucknow,"data/anomaly/semi_labels_lucknow.csv")
	mumbailabelsnew = newlabels2(anomaliesmumbai,"data/anomaly/semi_labels_mumbai.csv")
	bangalorelabelsnew = newlabels2(anomaliesbangalore,"data/anomaly/semi_labels_bangalore.csv")


	# delhilabelsnew = newlabels(anomaliesdelhi,delhilabels)
	# lucknowlabelsnew = newlabels(anomalieslucknow,lucknowlabels)
	# mumbailabelsnew = newlabels(anomaliesmumbai,mumbailabels)
	# bangalorelabelsnew = newlabels(anomaliesbangalore,bangalorelabels)
	# print delhilabelsnew
	x1,y1 = prepare(anomaliesdelhi,delhilabelsnew,data_d)
	x2,y2 = prepare(anomaliesmumbai,mumbailabelsnew,data_m)
	x3,y3 = prepare(anomalieslucknow,lucknowlabelsnew,data_l)
	x4,y4 = prepare(anomaliesbangalore,bangalorelabelsnew,data_b)
	xall = np.array(x1.tolist()+x2.tolist()+x3.tolist()+x4.tolist())
	yall = np.array(y1.tolist()+y2.tolist()+y3.tolist()+y4.tolist())
	assert(len(anomaliesdelhi) == len(delhilabelsnew))
	assert(len(anomaliesall) == len(yall))

	# print len(y1),len(y2)
	'''
	normal Points mean those with labels 6 or 7
	H / W mean hoarding and weather
	F / I / T mean fuel , transport, inflation 
	'''
	normal_points_index = []
	normal_points_value = []
	h_w_points_index = []
	h_w_points_value = []
	f_i_t_points_index = []
	f_i_t_points_value = []
	

	slope = []
	
	# Iterateing over all the anomalies and calculating the cost function for all the anomalies and storing in a alist
	for i in range(0,len(yall)):
		# print i
		# if( i < len(y1)):
		# 	parameter = cost_function3(xall[i],anomaliesall[0][i],anomaliesall[1][i],retailpriceseriesdelhi,DAYS)
		# elif( i < (len(y1)+len(y2)) ):
		# 	parameter = cost_function3(xall[i],anomaliesall[0][i],anomaliesall[1][i],retailpriceseriesmumbai,DAYS)
		# else:
		# 	parameter = cost_function3(xall[i],anomaliesall[0][i],anomaliesall[1][i],retailpriceserieslucknow,DAYS)

		parameter = cost_function(xall[i],anomaliesall[0][i],anomaliesall[1][i],DAYS)
		# parameter = cost_function2(xall[i],anomaliesall[0][i],anomaliesall[1][i],DAYS)
		# if( parameter == 0):
		# 	if(yall[i] == 5):
		# 		print xall[i][0:DAYS]
		# print i,"  ",anomaliesall[0][i],"------> ",parameter
		slope.append((parameter,yall[i]))
		if(yall[i] == 1 or yall[i] == 1 ):
			h_w_points_index.append(i)
			h_w_points_value.append(parameter)
		elif(yall[i] == 0):
			normal_points_index.append(i)
			normal_points_value.append(parameter)
		# elif(yall[i] == 3):
		# 	f_i_t_points_index.append(i)
		# 	f_i_t_points_value.append(parameter)
		
	plt.scatter(h_w_points_index,h_w_points_value,color = 'red', label = "H / W")
	plt.scatter(normal_points_index,normal_points_value,color = 'green', label = "Normal")
	# plt.scatter(f_i_t_points_index,f_i_t_points_value,color = 'black', label = "F / I / T")
	
	
	slope.sort(reverse = True)
	plt.tick_params()
	plt.xlabel('Anomaly',fontsize = 20)
  	# plt.ylabel('Parameter (Mean Deviation of Retail Price from average R.P(over all years))',fontsize = 20)
  	plt.ylabel('Parameter (Slope of Retail Price during the window)',fontsize = 20)
  	# plt.ylabel('Parameter (Max - Min for Retail Price during the window)',fontsize = 20)
  	# plt.ylabel('Parameter (Mean Deviation of Mandi Price from average M.P(over all years))',fontsize = 20)
  	# plt.ylabel('Parameter (Slope of Mandi Price during the window)',fontsize = 20)
  	# plt.ylabel('Parameter (Max - Min for Mandi Price during the window)',fontsize = 20)
  	# plt.ylabel('Parameter (Slope of Retail - Mandi Price during the window)',fontsize = 20)
  	# plt.ylabel('Parameter (Max - Min of Retail - Mandi Price during the window)',fontsize = 20)
  	# plt.ylabel('Parameter (Mean Deviation of Retail - Mandi Price during the window)',fontsize = 20)


  	plt.legend(loc = 'best')
	plt.show()
	
# Checking to see how many anomalies passed the step 1 based on some threshold on a cost function
	step_1_pass= []
	threshold = 2
	total1 = 0
	total2 = 0
	correct1 = 0
	correct2 = 0
	for i in range(0,len(yall)):
		if(yall[i] == 1 or yall[i] == 1 or yall[i] == 0):
			if(yall[i] == 0):
				total2 +=1 
			else:
				total1 += 1
			parameter = cost_function(xall[i][0:43],anomaliesall[0][i],anomaliesall[1][i],DAYS)
			# parameter2 = cost_function(xall[i][43:],anomaliesall[0][i],anomaliesall[1][i],DAYS)
			
			if(parameter > threshold):
				if(yall[i] == 1 or yall[i] == 1):
					correct1 += 1
				if( i < len(y1)):
					step_1_pass.append((i,yall[i],0))
				elif( i < (len(y1)+len(y2)) ):
					step_1_pass.append((i,yall[i],1))
				elif( i < len(y1)+len(y2)+len(y3) ):
					step_1_pass.append((i,yall[i],2))
				else:
					step_1_pass.append((i,yall[i],3))
			else:
				if(yall[i] == 0):
					correct2 += 1
				

	print "Correct ",correct1, correct2
	print "Total ", total1, total2
	file = open('data/anomaly/qualify_mumbai.csv','w')
	for i in range(0,len(step_1_pass)):
		if(step_1_pass[i][2] == 1):
			file.write(str(anomaliesall[0][step_1_pass[i][0]])+", "+str(anomaliesall[1][step_1_pass[i][0]])+", "+str(step_1_pass[i][1])+"\n")
	file = open('data/anomaly/qualify_delhi.csv','w')
	for i in range(0,len(step_1_pass)):
		if(step_1_pass[i][2] == 0):
			file.write(str(anomaliesall[0][step_1_pass[i][0]])+", "+str(anomaliesall[1][step_1_pass[i][0]])+", "+str(step_1_pass[i][1])+"\n")
	file = open('data/anomaly/qualify_lucknow.csv','w')
	for i in range(0,len(step_1_pass)):
		if(step_1_pass[i][2] == 2):
			file.write(str(anomaliesall[0][step_1_pass[i][0]])+", "+str(anomaliesall[1][step_1_pass[i][0]])+", "+str(step_1_pass[i][1])+"\n")
	file = open('data/anomaly/qualify_bangalore.csv','w')
	for i in range(0,len(step_1_pass)):
		if(step_1_pass[i][2] == 3):
			file.write(str(anomaliesall[0][step_1_pass[i][0]])+", "+str(anomaliesall[1][step_1_pass[i][0]])+", "+str(step_1_pass[i][1])+"\n")

	return step_1_pass
		

	


	

# print type(retailpriceseriesmumbai)
first_principle(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai],[retailpriceseriesdelhi],[retailpriceserieslucknow],[retailpriceseriesbangalore])
# first_principle(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[mandipriceseriesmumbai],[mandipriceseriesdelhi],[mandipriceserieslucknow],[mandipriceseriesbangalore])
# first_principle(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai,mandipriceseriesmumbai],[retailpriceseriesdelhi,mandipriceseriesdelhi],[retailpriceserieslucknow,mandipriceserieslucknow],[retailpriceseriesbangalore,mandipriceseriesbangalore])
# first_principle(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai-mandipriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi-mandipriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow-mandipriceserieslucknow,mandiarrivalserieslucknow],[retailpriceseriesbangalore-mandipriceseriesbangalore,mandiarrivalseriesbangalore])
# first_principle(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai-mandipriceseriesmumbai],[retailpriceseriesdelhi-mandipriceseriesdelhi],[retailpriceserieslucknow-mandipriceserieslucknow],[retailpriceseriesbangalore-mandipriceseriesbangalore])
# first_principle(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow,mandiarrivalserieslucknow],[retailpriceseriesbangalore,mandiarrivalseriesbangalore])
# first_principle(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai,mandipriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi,mandipriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow,mandipriceserieslucknow,mandiarrivalserieslucknow],[retailpriceseriesbangalore,mandipriceseriesbangalore,mandiarrivalseriesbangalore])
# first_principle(retailpriceseriesmumbai,retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesbangalore,[retailpriceseriesmumbai/mandipriceseriesmumbai],[retailpriceseriesdelhi/mandipriceseriesdelhi],[retailpriceserieslucknow/mandipriceserieslucknow],[retailpriceseriesbangalore/mandipriceseriesbangalore])


# first_principle(mandipriceseriesmumbai,mandipriceseriesdelhi,mandipriceserieslucknow,[retailpriceseriesmumbai],[retailpriceseriesdelhi],[retailpriceserieslucknow])
# first_principle(mandipriceseriesmumbai,mandipriceseriesdelhi,mandipriceserieslucknow,[mandipriceseriesmumbai],[mandipriceseriesdelhi],[mandipriceserieslucknow])
# first_principle(mandipriceseriesmumbai,mandipriceseriesdelhi,mandipriceserieslucknow,[retailpriceseriesmumbai,mandipriceseriesmumbai],[retailpriceseriesdelhi,mandipriceseriesdelhi],[retailpriceserieslucknow,mandipriceserieslucknow])
# first_principle(mandipriceseriesmumbai,mandipriceseriesdelhi,mandipriceserieslucknow,[retailpriceseriesmumbai-mandipriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi-mandipriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow-mandipriceserieslucknow,mandiarrivalserieslucknow])
# first_principle(mandipriceseriesmumbai,mandipriceseriesdelhi,mandipriceserieslucknow,[retailpriceseriesmumbai-mandipriceseriesmumbai],[retailpriceseriesdelhi-mandipriceseriesdelhi],[retailpriceserieslucknow-mandipriceserieslucknow])
# first_principle(mandipriceseriesmumbai,mandipriceseriesdelhi,mandipriceserieslucknow,[retailpriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow,mandiarrivalserieslucknow])
# first_principle(mandipriceseriesmumbai,mandipriceseriesdelhi,mandipriceserieslucknow,[retailpriceseriesmumbai,mandipriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi,mandipriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow,mandipriceserieslucknow,mandiarrivalserieslucknow])
# first_principle(mandipriceseriesmumbai,mandipriceseriesdelhi,mandipriceserieslucknow,[retailpriceseriesmumbai/mandipriceseriesmumbai],[retailpriceseriesdelhi/mandipriceseriesdelhi],[retailpriceserieslucknow/mandipriceserieslucknow])


# first_principle(retailpriceseriesmumbai-mandipriceseriesmumbai,retailpriceseriesdelhi-mandipriceseriesdelhi,retailpriceserieslucknow-mandipriceserieslucknow,[retailpriceseriesmumbai],[retailpriceseriesdelhi],[retailpriceserieslucknow])
# first_principle(retailpriceseriesmumbai-mandipriceseriesmumbai,retailpriceseriesdelhi-mandipriceseriesdelhi,retailpriceserieslucknow-mandipriceserieslucknow,[mandipriceseriesmumbai],[mandipriceseriesdelhi],[mandipriceserieslucknow])
# first_principle(retailpriceseriesmumbai-mandipriceseriesmumbai,retailpriceseriesdelhi-mandipriceseriesdelhi,retailpriceserieslucknow-mandipriceserieslucknow,[retailpriceseriesmumbai,mandipriceseriesmumbai],[retailpriceseriesdelhi,mandipriceseriesdelhi],[retailpriceserieslucknow,mandipriceserieslucknow])
# first_principle(retailpriceseriesmumbai-mandipriceseriesmumbai,retailpriceseriesdelhi-mandipriceseriesdelhi,retailpriceserieslucknow-mandipriceserieslucknow,[retailpriceseriesmumbai-mandipriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi-mandipriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow-mandipriceserieslucknow,mandiarrivalserieslucknow])
# first_principle(retailpriceseriesmumbai-mandipriceseriesmumbai,retailpriceseriesdelhi-mandipriceseriesdelhi,retailpriceserieslucknow-mandipriceserieslucknow,[retailpriceseriesmumbai-mandipriceseriesmumbai],[retailpriceseriesdelhi-mandipriceseriesdelhi],[retailpriceserieslucknow-mandipriceserieslucknow])
# first_principle(retailpriceseriesmumbai-mandipriceseriesmumbai,retailpriceseriesdelhi-mandipriceseriesdelhi,retailpriceserieslucknow-mandipriceserieslucknow,[retailpriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow,mandiarrivalserieslucknow])
# first_principle(retailpriceseriesmumbai-mandipriceseriesmumbai,retailpriceseriesdelhi-mandipriceseriesdelhi,retailpriceserieslucknow-mandipriceserieslucknow,[retailpriceseriesmumbai,mandipriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi,mandipriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow,mandipriceserieslucknow,mandiarrivalserieslucknow])
# first_principle(retailpriceseriesmumbai-mandipriceseriesmumbai,retailpriceseriesdelhi-mandipriceseriesdelhi,retailpriceserieslucknow-mandipriceserieslucknow,[retailpriceseriesmumbai/mandipriceseriesmumbai],[retailpriceseriesdelhi/mandipriceseriesdelhi],[retailpriceserieslucknow/mandipriceserieslucknow])


# # Change the argmax to idxmin for running the part below

# first_principle(mandiarrivalseriesmumbai,mandiarrivalseriesdelhi,mandiarrivalserieslucknow,[retailpriceseriesmumbai],[retailpriceseriesdelhi],[retailpriceserieslucknow])
# first_principle(mandiarrivalseriesmumbai,mandiarrivalseriesdelhi,mandiarrivalserieslucknow,[mandipriceseriesmumbai],[mandipriceseriesdelhi],[mandipriceserieslucknow])
# first_principle(mandiarrivalseriesmumbai,mandiarrivalseriesdelhi,mandiarrivalserieslucknow,[retailpriceseriesmumbai,mandipriceseriesmumbai],[retailpriceseriesdelhi,mandipriceseriesdelhi],[retailpriceserieslucknow,mandipriceserieslucknow])
# first_principle(mandiarrivalseriesmumbai,mandiarrivalseriesdelhi,mandiarrivalserieslucknow,[retailpriceseriesmumbai-mandipriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi-mandipriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow-mandipriceserieslucknow,mandiarrivalserieslucknow])
# first_principle(mandiarrivalseriesmumbai,mandiarrivalseriesdelhi,mandiarrivalserieslucknow,[retailpriceseriesmumbai-mandipriceseriesmumbai],[retailpriceseriesdelhi-mandipriceseriesdelhi],[retailpriceserieslucknow-mandipriceserieslucknow])
# first_principle(mandiarrivalseriesmumbai,mandiarrivalseriesdelhi,mandiarrivalserieslucknow,[retailpriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow,mandiarrivalserieslucknow])
# first_principle(mandiarrivalseriesmumbai,mandiarrivalseriesdelhi,mandiarrivalserieslucknow,[retailpriceseriesmumbai,mandipriceseriesmumbai,mandiarrivalseriesmumbai],[retailpriceseriesdelhi,mandipriceseriesdelhi,mandiarrivalseriesdelhi],[retailpriceserieslucknow,mandipriceserieslucknow,mandiarrivalserieslucknow])
# first_principle(mandiarrivalseriesmumbai,mandiarrivalseriesdelhi,mandiarrivalserieslucknow,[retailpriceseriesmumbai/mandipriceseriesmumbai],[retailpriceseriesdelhi/mandipriceseriesdelhi],[retailpriceserieslucknow/mandipriceserieslucknow])

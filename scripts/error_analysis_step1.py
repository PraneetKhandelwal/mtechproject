# This code plots the correct predictions for step 1 for different centers on the time scale over the entire period.
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


font = {'family' : 'normal',
        #'weight' : 'bold',
        'size'   : 18}

matplotlib.rc('font', **font)

colors = [ '#e6194b', '#3cb44b' ,'#ffe119', '#0082c8', '#f58231', '#911eb4',  '#000080' , '#800000'  ,'#000000', '#900c3f' ]

'''
Plot Series from dates specified in the function
'''
def plot_series(anomalies, retailpriceseries,labels,semi_labels,lbl):
  inpseries = retailpriceseries.rolling(window=15,center=True).mean()
  for i in range(0,len(anomalies)):
    yaxis_region = inpseries[anomalies[0][i]:anomalies[1][i]]
    # yaxis = [inpseries.mean()]*len(inpseries)
    xaxis_region = list(yaxis_region.index)
    if(labels[i] == 2 and semi_labels[i] == 1):
      plt.fill_between(xaxis_region,yaxis_region, color ='g')
    elif(labels[i] == 5 and semi_labels[i] == 1):
      plt.fill_between(xaxis_region,yaxis_region, color ='r')
  yaxis = inpseries
  xaxis = list(inpseries.index)
  plt.plot(xaxis,yaxis, color ='b', label=lbl,linewidth=2.5)


'''
Plot Series for only correctly predicted anomalies from dates specified in the function
'''
def plot_series_correct(anomalies, retailpriceseries,semi_labels,correct_pred,anomaly_list):
  inpseries = retailpriceseries.rolling(window=15,center=True).mean()
  count =  0
  cor_count  = 0
  count2 = 0
  for i in range(0,len(anomaly_list)):
    yaxis_region = inpseries[anomalies[0][i]:anomalies[1][i]]
    # yaxis = [inpseries.mean()]*len(inpseries)
    xaxis_region = list(yaxis_region.index)
    if(anomaly_list[i][1] in correct_pred[anomaly_list[i][0]] and (semi_labels[i] == 1 or semi_labels[i]==0)):
      if(cor_count == 0):
        plt.fill_between(xaxis_region,yaxis_region, color ='g',label='Correct Predictions')
      else:
        plt.fill_between(xaxis_region,yaxis_region, color ='g')

      cor_count += 1
    elif(semi_labels[i] == 1 ):
      if(count == 0):
        plt.fill_between(xaxis_region,yaxis_region, color ='r',label='Predicted:Normal, Actual:Anomaly')

      else:
        plt.fill_between(xaxis_region,yaxis_region, color ='r')
      count = count + 1
    elif(semi_labels[i]==0):
      if(count2 ==0):
        plt.fill_between(xaxis_region,yaxis_region, color ='black',label='Predicted:Anomaly, Actual:Normal')

      else:
        plt.fill_between(xaxis_region,yaxis_region, color ='black')
      count2 += 1

  yaxis = inpseries
  xaxis = list(inpseries.index)
  plt.legend(loc='best')
  plt.plot(xaxis,yaxis, color ='b',linewidth=2.5)
  print count

def plot_series_cor_avg(anomalies, retailpriceseries,semi_labels,correct_pred,anomaly_list):
  inpseries = retailpriceseries.rolling(window=15,center=True).mean()
  count =  0
  count2 = 0 
  yaxis = np.array([0]*43)
  for i in range(0,len(anomaly_list)):
    yaxis_region = []
    series = inpseries[anomalies[0][i]:anomalies[1][i]]
    for p in range(0,len(series)):
    	yaxis_region.append(series[p])
    # yaxis = [inpseries.mean()]*len(inpseries)
    # xaxis_region = list(yaxis_region.index)
    if(anomaly_list[i][1] in correct_pred[anomaly_list[i][0]] and (semi_labels[i] == 1 or semi_labels[i]==0)):
      # plt.fill_between(xaxis_region,yaxis_region, color ='g')
      yaxis_region = np.array(yaxis_region)
      yaxis = yaxis + yaxis_region
      count = count + 1
    elif(semi_labels[i] == 1 or semi_labels[i]==0):
      # plt.fill_between(xaxis_region,yaxis_region, color ='r')
      count2 = count2 + 1
  print yaxis
  yaxis = yaxis/count
  xaxis = range(43)
  plt.plot(xaxis,yaxis, color ='b',linewidth=2.5)
  print count



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

#[retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesmumbai] = whiten_series_list([retailpriceseriesdelhi,retailpriceserieslucknow,retailpriceseriesmumbai])

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
# mandipriceseriesdelhi = mandiP[3]
# mandipriceserieslucknow = mandiP[4]
# mandipriceseriesmumbai = mandiP[5]
# mandiarrivalseriesdelhi = mandiA[3]
# mandiarrivalserieslucknow = mandiA[4]
# mandiarrivalseriesmumbai = mandiA[5]
# print mandipriceseriesdelhi



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

def newsemilabels(anomalies,semilabels_path):
  # print len(anomalies[anomalies[2] != ' Normal_train']), len(oldlabels)
  labels = []
  semi_labels = pd.read_csv(semilabels_path, header=None, index_col=None)
  for i in range(0,len(anomalies)): 
      labels.append(semi_labels[0][i])
  return labels






def get_anomaly_id(anomalies,center):
  anomaly_id_list = []
  for i in range(0,len(anomalies)):
    anomaly_id_list.append((center,i))
  return anomaly_id_list

def load_correct_predictions(path):
  correct_pred = {}
  f = open(path,'r')
  for line in f:
    line_split = line.split(',')
    center = line_split[0]
    anomaly_idno = int(line_split[1])
    if center in correct_pred:
      correct_pred[center].append(anomaly_idno)
    else:
      correct_pred[center] = [anomaly_idno]
  return correct_pred

def train_test_function(align_m,align_d,align_l,align_b,data_m,data_d,data_l,data_b):
  # align = [1,2,3]
  anomaliesmumbai = get_anomalies('data/anomaly/normal_h_w_semi_mumbai.csv',align_m)
  anomaliesdelhi = get_anomalies('data/anomaly/normal_h_w_semi_delhi.csv',align_d)
  anomalieslucknow = get_anomalies('data/anomaly/normal_h_w_semi_lucknow.csv',align_l)
  anomaliesbangalore = get_anomalies('data/anomaly/normal_h_w_semi_bangalore.csv',align_b)
  # delhilabelsnew = newlabels(anomaliesdelhi,delhilabels)
  # lucknowlabelsnew = newlabels(anomalieslucknow,lucknowlabels)
  # mumbailabelsnew = newlabels(anomaliesmumbai,mumbailabels)
  # bangalorelabelsnew = newlabels(anomaliesbangalore,bangalorelabels)
  delhi_semilabelsnew = newsemilabels(anomaliesdelhi,"data/anomaly/semi_labels_delhi.csv")
  lucknow_semilabelsnew = newsemilabels(anomalieslucknow,"data/anomaly/semi_labels_lucknow.csv")
  mumbai_semilabelsnew = newsemilabels(anomaliesmumbai,"data/anomaly/semi_labels_mumbai.csv")
  bangalore_semilabelsnew = newsemilabels(anomaliesbangalore,"data/anomaly/semi_labels_bangalore.csv")
  
  correct_predictions = load_correct_predictions("data/correct_predictions.csv")

  delhi_anomaly_id = get_anomaly_id(anomaliesdelhi,"Delhi")
  mumbai_anomaly_id = get_anomaly_id(anomaliesmumbai,"Mumbai")
  lucknow_anomaly_id = get_anomaly_id(anomalieslucknow,"Lucknow")
  bangalore_anomaly_id = get_anomaly_id(anomaliesbangalore,"Bangalore")

  # assert(len(delhilabelsnew) == len(delhi_semilabelsnew))
  # plot_series(anomalieslucknow,retailpriceserieslucknow,lucknowlabelsnew,lucknow_semilabelsnew,"MUMBAI Anomalies")
  # plot_series_correct(anomaliesmumbai,retailpriceseriesmumbai,mumbai_semilabelsnew,correct_predictions,mumbai_anomaly_id)
  plot_series_correct(anomaliesdelhi,retailpriceseriesdelhi,delhi_semilabelsnew,correct_predictions,delhi_anomaly_id)
  # plot_series_correct(anomaliesbangalore,retailpriceseriesbangalore,bangalore_semilabelsnew,correct_predictions,bangalore_anomaly_id)

  # plot_series_cor_avg(anomaliesdelhi,retailpriceseriesdelhi,delhi_semilabelsnew,correct_predictions,delhi_anomaly_id)


  plt.title('Delhi Anomalies Step 1 Result')
  plt.xlabel('Time')
  plt.ylabel('Retail Price')
  plt.show()



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


# This file contains code for studying correlation between different parameters

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
from averagemandi import give_avg_series  

import os
cwd = os.getcwd()
matplotlib.rcParams.update({'font.size': 26})




# from reading_timeseries import retailP, mandiP, mandiA, retailPM, mandiPM, mandiAM
# retailpriceseriesmumbai = retailP[3]
# retailpriceseriesdelhi = retailP[1]
# retailpriceserieslucknow = retailP[2]
# print retailpriceseriesmumbai
from averageretail import getcenter
retailpriceseriesmumbai = getcenter('MUMBAI')
retailpriceseriesdelhi = getcenter('DELHI')
retailpriceserieslucknow = getcenter('LUCKNOW')
retailpriceseriesbangalore = getcenter('BENGALURU')


avg_retailpriceseriesmumbai = give_avg_series(retailpriceseriesmumbai)
avg_retailpriceseriesdelhi = give_avg_series(retailpriceseriesdelhi)
avg_retailpriceserieslucknow = give_avg_series(retailpriceserieslucknow)
avg_retailpriceseriesbangalore = give_avg_series(retailpriceseriesbangalore)


from averagemandi import getmandi
mandipriceseriesdelhi = getmandi('Azadpur',True)
mandiarrivalseriesdelhi = getmandi('Azadpur',False)
mandipriceserieslucknow = getmandi('Bahraich',True)
mandiarrivalserieslucknow = getmandi('Bahraich',False)
mandipriceseriespune = getmandi('Pune',True)
mandiarrivalseriespune = getmandi('Pune',False)
mandipriceserieslasalgaon = getmandi('Lasalgaon',True)
mandiarrivalserieslasalgaon = getmandi('Lasalgaon',False)
mandipriceseriesbangalore = getmandi('Bangalore',True)
mandiarrivalseriesbangalore = getmandi('Bangalore',False)
from averagemandi import mandipriceseries
from averagemandi import mandiarrivalseries 
mandipriceseriesmumbai = mandipriceseries
mandiarrivalseriesmumbai = mandiarrivalseries

avg_mandipriceseriesdelhi = give_avg_series(mandipriceseriesdelhi)
avg_mandipriceserieslucknow = give_avg_series(mandipriceserieslucknow)
avg_mandiarrivalseriesdelhi = give_avg_series(mandiarrivalseriesdelhi)
avg_mandiarrivalserieslucknow = give_avg_series(mandiarrivalserieslucknow)
avg_mandipriceseriespune = give_avg_series(mandipriceseriespune)
avg_mandipriceserieslasalgaon = give_avg_series(mandipriceserieslasalgaon)
avg_mandiarrivalseriespune = give_avg_series(mandiarrivalseriespune)
avg_mandiarrivalserieslasalgaon = give_avg_series(mandiarrivalserieslasalgaon)
avg_mandiarrivalseriesbangalore = give_avg_series(mandiarrivalseriesbangalore)
avg_mandipriceseriesbangalore = give_avg_series(mandipriceseriesbangalore)



def delay_corr(datax,datay,min,max,namex,namey):
	delay_corr_values=[]
	delays = []
	min = min*30
	max = max*30
	for delay in range(min,max+1):
		curr_corr = datax.corr(datay.shift(delay))
		delay_corr_values.append(curr_corr)
		delays.append(delay)
	# plt.plot(delays,delay_corr_values, label = namex +'-'+namey)
	# plt.xlabel('Cor ( X1(t), X2(t-days) )')
	# # print np.array(delay_corr_values).argmax()
	# plt.axvline(x=np.array(delay_corr_values).argmax()-90,color ='black',linestyle='-')
	# print np.array(delay_corr_values).argmax()-90
	# # delays.append(np.array(delay_corr_values).argmax()-90)
	# plt.xticks([-90,0,90,np.array(delay_corr_values).argmax()-90])
	# # If days come out to be positive, then X1 follows X2
	# plt.ylabel('Shifted Correlations')
	# plt.legend(loc='best')
	# plt.title('Shifted Correlations ')
	return delay_corr_values
# ------------------------------------------------------------------------------------
#
# def delay_corr2(datax,datay,min,max,namex,namey):
# 	delay_corr_values_early_kharif=[]
# 	delay_corr_values_kharif=[]
# 	delay_corr_values_rabi =[]
# 	delays = []
# 	for delay in range(min,max+1):
# 		new_datay = datay.shift(-1*delay)
# 		curr_corr_early = 0
# 		for year in range(1,8):
# 			short_y = new_datay[year*365+285:365*(year+1)+365]
# 			short_x = datax[year*365+285:365*(year+1)+365]
# 			curr_corr_early = curr_corr_early + short_x.corr(short_y)
# 		# curr_corr = datax.corr(datay.shift(delay*30))
# 		curr_corr_early = curr_corr_early/7
# 		delay_corr_values_early_kharif.append(curr_corr_early)

# 		curr_corr_kharif = 0
# 		for year in range(0,8):
# 			short_y = new_datay[year*365+365:365*(year+1)+120]
# 			short_x = datax[year*365+365:365*(year+1)+120]
# 			curr_corr_kharif = curr_corr_kharif + short_x.corr(short_y)
# 		# curr_corr = datax.corr(datay.shift(delay*30))
# 		curr_corr_kharif = curr_corr_kharif/8
# 		delay_corr_values_kharif.append(curr_corr_kharif)

# 		curr_corr_rabi = 0
# 		for year in range(1,9):
# 			short_y = new_datay[year*365+100:365*(year)+240]
# 			short_x = datax[year*365+100:365*(year)+240]
# 			curr_corr_rabi = curr_corr_rabi + short_x.corr(short_y)
# 		# curr_corr = datax.corr(datay.shift(delay*30))
# 		curr_corr_rabi = curr_corr_rabi/8
# 		delay_corr_values_rabi.append(curr_corr_rabi)
# 		delays.append(delay)
# 	plt.plot(delays,delay_corr_values_early_kharif,color='r', label='Early Kharif')
# 	plt.plot(delays,delay_corr_values_kharif, color='g', label = 'Kharif')
# 	plt.plot(delays,delay_corr_values_rabi, color='b', label='Rabi')
# 	plt.xlabel('<-----------'+namex+' follows '+namey+'\n'+namey+' follows '+namex+'------------>\n'+'Correlation of '+namex +' with '+namey+' X days later ------>')
# 	plt.ylabel('Shifted Correlations')
# 	plt.legend(loc='best')
# 	plt.title('Shifted Correlations - '+namex+' vs '+namey)
# 	plt.show()




# Code starts for shifted correlation between mandi prices and retail prices
# a=delay_corr(mandipriceseriesdelhi,retailpriceseriesdelhi,-3,3,"Delhi","Delhi")
# b=delay_corr(mandipriceserieslucknow,retailpriceserieslucknow,-3,3,"Lucknow","Lucknow")
# c=delay_corr(mandipriceserieslasalgaon,retailpriceseriesmumbai,-3,3,"Mandi Price","Retail Price")
# d=delay_corr(mandipriceseriesbangalore,retailpriceseriesbangalore,-3,3,"Bangalore","Bangalore")

# a=np.array(a)
# b=np.array(b)
# c=np.array(c)
# d=np.array(d)

# e=(a+b+c+d)/4.0
# delays =[]
# for sm in range(-90,91):
# 	delays.append(sm)
# namex='Mandi Price'
# namey='Retail Price'
# e=list(e)
# plt.plot(delays,e, label = namex +'-'+namey)
# plt.xlabel('Cor ( X1(t), X2(t-days) )')
# # print np.array(e).argmax()
# plt.axvline(x=np.array(e).argmax()-90,color ='black',linestyle='-')
# print np.array(e).argmax()-90
# # delays.append(np.array(e).argmax()-90)
# plt.xticks([-90,0,90,np.array(e).argmax()-90])
# # If days come out to be positive, then X1 follows X2
# plt.ylabel('Shifted Correlations')
# plt.legend(loc='best')
# plt.title('Shifted Correlations ')

# plt.show()

# Code ends for shifted correlation between MP and RP


# Code starts for shifted correlation between arrivals and mandi prices
# a=delay_corr(mandiarrivalseriesdelhi,mandipriceseriesdelhi,-3,3,"Delhi","Delhi")
# b=delay_corr(mandiarrivalserieslucknow,mandipriceserieslucknow,-3,3,"Lucknow","Lucknow")
# c=delay_corr(mandiarrivalseriesmumbai,mandipriceseriespune,-3,3,"Mumbai","Mumbai")
# d=delay_corr(mandiarrivalseriesbangalore,mandipriceseriesbangalore,-3,3,"Bangalore","Bangalore")

# a=np.array(a)
# b=np.array(b)
# c=np.array(c)
# d=np.array(d)

# e=(a+b+c+d)/4.0
# delays =[]
# for sm in range(-90,91):
# 	delays.append(sm)
# namex='Arrivals'
# namey='Mandi Price'
# e=list(e)
# plt.plot(delays,e, label = namex +'-'+namey)
# plt.xlabel('Cor ( X1(t), X2(t-days) )')
# # print np.array(e).argmax()
# plt.axvline(x=np.array(e).argmin()-90,color ='black',linestyle='-')
# print np.array(e).argmin()-90
# # delays.append(np.array(e).argmin()-90)
# plt.xticks([-90,0,90,np.array(e).argmin()-90])
# # If days come out to be positive, then X1 follows X2
# plt.ylabel('Shifted Correlations')
# plt.legend(loc='best')
# plt.title('Shifted Correlations ')

# plt.show()

# Code ends for shifted correlation between Arrivals and MP


# Code starts for shifted correlation between Source and Terminal Retail Prices
# a=delay_corr(retailpriceseriesmumbai,retailpriceseriesdelhi,-3,3,"Mumbai","Delhi")
# b=delay_corr(retailpriceseriesmumbai,retailpriceserieslucknow,-3,3,"Mumbai","Lucknow")
# c=delay_corr(retailpriceseriesbangalore,retailpriceseriesdelhi,-3,3,"Bangalore","Delhi")
# d=delay_corr(retailpriceseriesbangalore,retailpriceserieslucknow,-3,3,"Bangalore","Lucknow")

# a=np.array(a)
# b=np.array(b)
# c=np.array(c)
# d=np.array(d)

# e=(a+b+c+d)/4.0
# delays =[]
# for sm in range(-90,91):
# 	delays.append(sm)
# namex='Source'
# namey='Terminal'
# e=list(e)
# plt.plot(delays,e, label = namex +'-'+namey)
# plt.xlabel('Cor ( X1(t), X2(t-days) )')
# # print np.array(e).argmax()
# plt.axvline(x=np.array(e).argmax()-90,color ='black',linestyle='-')
# print np.array(e).argmax()-90
# # delays.append(np.array(e).argmax()-90)
# plt.xticks([-90,0,90,np.array(e).argmax()-90])
# # If days come out to be positive, then X1 follows X2
# plt.ylabel('Shifted Correlations')
# plt.legend(loc='best')
# plt.title('Shifted Correlations for Retail Prices')

# plt.show()

# Code ends for shifted correlation between Source and Terminal Retail Prices


# Code starts for shifted correlation between Source and Terminal Mandi Prices
a=delay_corr(mandipriceserieslasalgaon,mandipriceseriesdelhi,-3,3,"Lasalgaon","Delhi")
b=delay_corr(mandipriceserieslasalgaon,mandipriceserieslucknow,-3,3,"Lasalgaon","Lucknow")
c=delay_corr(mandipriceseriesbangalore,mandipriceseriesdelhi,-3,3,"Bangalore","Delhi")
d=delay_corr(mandipriceseriesbangalore,mandipriceserieslucknow,-3,3,"Bangalore","Lucknow")
f=delay_corr(mandipriceseriespune,mandipriceseriesdelhi,-3,3,"Pune","Delhi")
g=delay_corr(mandipriceseriespune,mandipriceserieslucknow,-3,3,"Pune","Lucknow")
a=np.array(a)
b=np.array(b)
c=np.array(c)
d=np.array(d)
f=np.array(f)
g=np.array(g)


e=(a+b+c+d+f+g)/6.0
delays =[]
for sm in range(-90,91):
	delays.append(sm)
namex='Source'
namey='Terminal'
e=list(e)
plt.plot(delays,e, label = namex +'-'+namey)
plt.xlabel('Cor ( X1(t), X2(t-days) )')
# print np.array(e).argmax()
plt.axvline(x=np.array(e).argmax()-90,color ='black',linestyle='-')
print np.array(e).argmax()-90
# delays.append(np.array(e).argmax()-90)
plt.xticks([-90,0,90,np.array(e).argmax()-90])
# If days come out to be positive, then X1 follows X2
plt.ylabel('Shifted Correlations')
plt.legend(loc='best')
plt.title('Shifted Correlations for Mandi Prices')

plt.show()

# Code ends for shifted correlation between Source and Terminal Mandi Prices
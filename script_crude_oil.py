import time
import datetime
import os
import csv
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
# centernames = ["Uttar Pradesh"]
# start_year = 2005
# end_year = 2017
# months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
# months2 = ["January","February","March","April","May","June","July"]
# months3 = ["August","September","October","November","December"]
# months4 = ["December"]
# mandi_file = pd.read_csv('mandis.csv')
# mandicode = mandi_file['mandicode']
# mandiname = mandi_file['mandiname']
# mandistate = mandi_file['statecode']
# mandi_map = {}
# mandi_state_map={}
# i=0
# for row in mandiname:
# 	mandi_map[row] = mandicode[i]
# 	mandi_state_map[row] = mandistate[i]
# 	i = i+1






# def past_date(x,current_date):
# 	date = current_date
# 	# print current_date
# 	for i in range(1,x+1):
# 		date = prev_date(date)
# 	return (date)

# def prev_date(current_date): #returns the previous date from the current date
# 	date = int(current_date.split("/")[0])
# 	month = int(current_date.split("/")[1])
# 	year = int(current_date.split("/")[2])
# 	if date > 1:
# 		date = date - 1 
# 	elif date == 1 and month > 1:
# 		if month == 2 or month == 4 or month == 6 or month == 8 or month == 9 or month == 11:
# 			date = 31
# 			month = month - 1
# 		elif month == 5 or month == 7 or month == 10 or month == 12:
# 			date = 31
# 			month = month - 1
# 		else:
# 			if year%4 == 0:
# 				date = 29
# 				month = 2
# 			else:
# 				date = 28
# 				month = 2
# 	else:
# 		date = 31
# 		month = 12
# 		year = year - 1
# 	date = str(date)
# 	month = str(month)
# 	year = str(year)
# 	if (len(date) == 1):
# 		date = "0" + date
# 	if (len(month) == 1):
# 		month = "0" + month
# 	prev_date = date + "/" + month + "/" + year
# 	return prev_date

# def present_date():
# 	i = datetime.datetime.now()
# 	# print(i.date())
# 	list_date = str(i.date()).split('-')
# 	new_date = list_date[2]+'/'+list_date[1]+'/'+list_date[0]
# 	return new_date

# def make_csv(date,name, table):
# 	date = date.replace('/','-')
# 	file_name = date+'.csv'
# 	newpath = '/Users/DC/Desktop/data_files/'+name+'/'
# 	if not os.path.exists(newpath):
# 		os.makedirs(newpath)
# 	path = newpath + file_name
# 	print(path)
# 	g = open(path, 'w', newline='')
# 	csvWriter = csv.writer(g)
# 	for row in table:
# 		# print(type(newrow))
# 		csvWriter.writerow(row)

def extract_rainfall_data():
	# f1 = open('title_2_del.txt','w')
	# f2 = open('content_2_del.txt','w')

	path_to_chromedriver = '/home/praneet/Downloads/chromedriver' # change path as needed
	# path_to_chromedriver = '/home/praneet/Downloads/phantomjs-2.1.1-linux-x86_64/bin/phantomjs'
	browser = webdriver.Chrome(executable_path = path_to_chromedriver)
	
	print "1"

	# html = browser.switch_to_frame("mainFrame")			#clicking on 'here' hyperlink

	# with open('new_WS_data_orissa2.csv', 'wb') as csvfile_WS:
	# 	spamwriter = csv.writer(csvfile_WS, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)

	file_fuel = open('crude_oil_monthly.csv','w')
# filing the form for times of india archive
	
	# for center in centernames:
	# 	start_year = 2015
	# 	if(center == "Orissa"):
	# 		start_year = 2016
	# for year in range(start_year,end_year+1):
	url = 'https://www.iocl.com/Product_PreviousPrice/CrudeOilPreviousPrice.aspx'
	browser.get(url)
	# months = months1
	# for month in months:
	st="Month-Year,Brent,Dubai,Indian-Basket,Oman,WTI\n"
	# browser.find_element_by_xpath("//*[@id=\"dnn_ctr980_MonthwiseExportReport_ddlCrop\"]/option[contains(text(),\""+"Onion"+"\")]").click()
	# browser.find_element_by_xpath("//*[@id=\"dnn_ctr980_MonthwiseExportReport_Year\"]/option[contains(text(),\""+str(year)+"\")]").click()
	# browser.find_element_by_xpath("//*[@id=\"dnn_ctr980_MonthwiseExportReport_MonthName\"]/option[contains(text(),\""+"All"+"\")]").click()
	# browser.find_element_by_xpath("//*[@id=\"cboCommodity\"]/option[contains(text(),\""+"Onion"+"\")]").click()
	# browser.find_element_by_xpath("//*[@id=\"dnn_ctr980_MonthwiseExportReport_Button1\"]").click()
	table = browser.find_element_by_xpath("//*[@id=\"form1\"]/div[3]/div[3]/div/div[1]/table/tbody/tr/td/div/table")
	# head = table.find_elements_by_tag_name("thead")
	# head_ele = browser.find_elements_by_xpath("//*[@id=\"Form1\"]/div[4]/div[3]/div[1]/div/table/thead/tr")
	# print len(head_ele)
	# st+=head_ele.find_elements_by_tag_name("td")[0].text+","+head_ele.find_elements_by_tag_name("td")[1].text+","+head_ele.find_elements_by_tag_name("td")[2].text+","+head_ele.find_elements_by_tag_name("td")[3].text+","+head_ele.find_elements_by_tag_name("td")[4].text+"\n"
	# body = table.find_elements_by_tag_name("tbody")
	rows = table.find_elements_by_tag_name("tr")
	count = 0
	print len(rows)
	for row in rows:
		print count
		cell = row.find_elements_by_tag_name("td")[0]
		cell = cell.text.replace(',','')
		cell = cell.replace(' ','-')
		cell1 = row.find_elements_by_tag_name("td")[1]

		cell2 = row.find_elements_by_tag_name("td")[2]

		cell3 = row.find_elements_by_tag_name("td")[3]

		cell4 = row.find_elements_by_tag_name("td")[4]
		cell5 = row.find_elements_by_tag_name("td")[5]
		# cell6 = row.find_elements_by_tag_name("td")[6]
		# if(cell.text <>""):
		# 	if(mandi_map.has_key(cell.text)):
		# 		curr_mandi = mandi_map[cell.text]
		# 		curr_state = mandi_state_map[cell.text]
		# 	else:
		# 		print "This mandi-",cell.text," does not exist"
		# 		curr_mandi = -2
		# 		curr_state = -2

		# spamwriter.writerow([cell1.text,curr_mandi,curr_state,cell2.text,cell3.text,cell4.text,cell5.text,cell6.text])
		st+=cell+","+cell1.text+","+cell2.text+","+cell3.text+","+cell4.text+","+cell5.text+"\n"
		count = count + 1
	file_fuel.write(st)

if __name__ == '__main__':
	extract_rainfall_data()
	# for i in range(1,8):
	# 	extract_rainfall_data(past_date(i,present_date()),past_date(i,present_date()))

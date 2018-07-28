import time
import datetime
import os
import csv
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
centernames = ["Uttar Pradesh"]
start_year = 2014
end_year = 2017
months1 = ["January","February","March","April","May","June","July","August","September","October","November","December"]
months2 = ["January","February","March","April","May","June","July"]
months3 = ["August","September","October","November","December"]
months4 = ["December"]
mandi_file = pd.read_csv('mandis.csv')
mandicode = mandi_file['mandicode']
mandiname = mandi_file['mandiname']
mandistate = mandi_file['statecode']
mandi_map = {}
mandi_state_map={}
i=0
for row in mandiname:
	mandi_map[row] = mandicode[i]
	mandi_state_map[row] = mandistate[i]
	i = i+1




# Function to download the data for a new center or mandi
def extract_data():
	# f1 = open('title_2_del.txt','w')
	# f2 = open('content_2_del.txt','w')

	path_to_chromedriver = '/home/praneet/Downloads/chromedriver' # change path as needed
	# path_to_chromedriver = '/home/praneet/Downloads/phantomjs-2.1.1-linux-x86_64/bin/phantomjs'
	browser = webdriver.Chrome(executable_path = path_to_chromedriver)
	url = 'http://agmarknet.nic.in/agnew/NationalBEnglish/DatewiseCommodityReport.aspx'
	browser.get(url)
	print "1"

	# html = browser.switch_to_frame("mainFrame")			#clicking on 'here' hyperlink

	# with open('new_WS_data_orissa2.csv', 'wb') as csvfile_WS:
	# 	spamwriter = csv.writer(csvfile_WS, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)

	file_orissa = open('new_WS_data_up.csv','a')
# filing the form for times of india archive
	curr_mandi = -1
	curr_state = -1
	for center in centernames:
		start_year = 2015
		if(center == "Orissa"):
			start_year = 2016
		for year in range(start_year,end_year+1):
			months = months1
			if(year == 2017):
				months = months2
			print center,year
			if(year == 2015 and center=="Uttar Pradesh"):
				months = months3
			for month in months:
				st=""
				browser.find_element_by_xpath("//*[@id=\"cboYear\"]/option[contains(text(),\""+str(year)+"\")]").click()
				browser.find_element_by_xpath("//*[@id=\"cboMonth\"]/option[contains(text(),\""+month+"\")]").click()
				browser.find_element_by_xpath("//*[@id=\"cboState\"]/option[contains(text(),\""+center+"\")]").click()
				browser.find_element_by_xpath("//*[@id=\"cboCommodity\"]/option[contains(text(),\""+"Onion"+"\")]").click()
				browser.find_element_by_xpath("//*[@id=\"btnSubmit\"]").click()
				table = browser.find_element_by_xpath("//*[@id=\"gridRecords\"]")
				rows = table.find_elements_by_tag_name("tr")
				count = 0
				for row in rows:
					if(count >= 1):
						# print"ballu"
						cell = row.find_elements_by_tag_name("td")[0]
						cell1 = row.find_elements_by_tag_name("td")[1]

						cell2 = row.find_elements_by_tag_name("td")[2]

						cell3 = row.find_elements_by_tag_name("td")[3]

						cell4 = row.find_elements_by_tag_name("td")[4]
						cell5 = row.find_elements_by_tag_name("td")[5]
						cell6 = row.find_elements_by_tag_name("td")[6]
						if(cell.text <>""):
							if(mandi_map.has_key(cell.text)):
								curr_mandi = mandi_map[cell.text]
								curr_state = mandi_state_map[cell.text]
							else:
								print "This mandi-",cell.text," does not exist"
								curr_mandi = -2
								curr_state = -2

						# spamwriter.writerow([cell1.text,curr_mandi,curr_state,cell2.text,cell3.text,cell4.text,cell5.text,cell6.text])
						st += cell1.text+","+str(curr_mandi)+","+str(curr_state)+","+cell2.text+","+cell3.text+","+cell4.text+","+cell5.text+","+cell6.text+"\n"
					count = count + 1
				file_orissa.write(st)
				browser.find_element_by_xpath("//*[@id=\"LinkButton1\"]").click()
		
    	# print(cell.text)
# 	browser.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/form/table/tbody/tr[2]/td[3]/input").send_keys("onion and price")

# 	browser.find_element_by_xpath("//*[@id=\"sPublication\"]/option[contains(text(),\""+"The Times Of India Delhi"+"\")]").click()
# 	browser.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/form/table/tbody/tr[6]/td[3]/input[1]").click()
	
# 	browser.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/form/table/tbody/tr[7]/td[3]/table/tbody/tr[2]/td[1]/input").send_keys("2006")

# 	browser.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/form/table/tbody/tr[7]/td[3]/table/tbody/tr[2]/td[2]/select/option[contains(text(),\""+"January"+"\")]").click()
# 	browser.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/form/table/tbody/tr[7]/td[3]/table/tbody/tr[2]/td[3]/select/option[contains(text(),\""+"1"+"\")]").click()

# 	browser.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/form/table/tbody/tr[7]/td[3]/table/tbody/tr[3]/td[1]/input").send_keys("2014")
# 	browser.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/form/table/tbody/tr[7]/td[3]/table/tbody/tr[3]/td[2]/select/option[contains(text(),\""+"December"+"\")]").click()
# 	browser.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/form/table/tbody/tr[7]/td[3]/table/tbody/tr[3]/td[3]/select/option[contains(text(),\""+"31"+"\")]").click()

# 	browser.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/form/table/tbody/tr[11]/td[3]/input[2]").click()
	
# 	browser.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/form/table/tbody/tr[12]/td[3]/select/option[contains(text(),\""+"Complete Text"+"\")]").click()
# 	print "4"
# 	# print browser.page_source
# 	browser.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/form/table/tbody/tr[14]/td[3]/select/option[contains(text(),\""+"Date Ascending"+"\")]").click()
	
# 	browser.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/form/table/tbody/tr[16]/td/input[2]").click()	
# # /html/body/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/form/table/tbody/tr[16]/td/input[2]
# 	# for district in district_list:
# 		# browser.find_element_by_xpath("//*[@id=\"CmbDistrict\"]/option[contains(text(),\""+district+"\")]").click()
# 	count = 0
# 	page = 0
# 	for x in range(0,0):
# 		page = page + 1
# 		count = count +8
# 		browser.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[3]/td/table/tbody/tr/td[3]/a/b").click()	

# 	while(1):
# 		page = page +1
# 		time.sleep(3)
# 		a = browser.find_elements_by_class_name("Result_Title")
# 		for i in range(0,len(a)):
# 			count = count + 1
# 			print "Page ",page,"  Article count ",count, "line 122"
# 			Currentwindow = browser.window_handles
# 			f1.write("Page"+str(page)+"article"+str(count)+a[i].text.encode('utf-8'))
# 			f1.write('\n')
# 			a[i].click()
# 			newwindow = browser.window_handles
# 			# print newwindow
			
# 			# newwindow2 = list(set(newwindow) - set(Currentwindow))[0]
# 			browser.switch_to.window(newwindow[1])
# 	# print browser.page_source
# 	# print browser.current_url
# 			new_url = browser.current_url[:-3]+"HTML"
# 			browser.get(new_url)
# 			html2 = browser.switch_to_frame("ArticleContent")
# 			html2= browser.page_source
# 			soup = BeautifulSoup(html2,"html.parser")
# 			temp = soup.find('div',{'name':'textContainer'})
# 			if temp == None:
# 				f2.write("Page"+str(page)+"article"+str(count)+"EXCEPTION HERE\n")
# 			else:
# 				links = (soup.find('div',{'name':'textContainer'})).find_all('span')
# 				f2_string ="Page"+str(page)+"article"+str(count)
# 				for link in links:
# 					f2_string = f2_string + link.text
# 				f2_string.replace('\n',' ')
# 				f2.write(f2_string.encode('utf-8'))
# 				f2.write('\n')

# 			# print len(links)
# 			# browser.close()
# 			browser.switch_to.window(newwindow[0])
# 			browser.switch_to_frame("mainFrame")	

# 			# print browser.page_source
# 			# print newwindow[0]
# 			# a = browser.find_elements_by_class_name("Result_Title")
# 			# print len(a)

# 		browser.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[3]/td/table/tbody/tr/td[3]/a/b").click()	
# 	# browser.switch_to.window(Currentwindow)



if __name__ == '__main__':
	extract_data()
	# for i in range(1,8):
	# 	extract_rainfall_data(past_date(i,present_date()),past_date(i,present_date()))

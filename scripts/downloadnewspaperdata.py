import time
import datetime
import os
import csv
from selenium import webdriver
from bs4 import BeautifulSoup

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
	f1 = open('title_2_del.txt','w')
	f2 = open('content_2_del.txt','w')

	path_to_chromedriver = '/home/praneet/Downloads/chromedriver' # change path as needed
	# path_to_chromedriver = '/home/praneet/Downloads/phantomjs-2.1.1-linux-x86_64/bin/phantomjs'
	browser = webdriver.Chrome(executable_path = path_to_chromedriver)
	url = 'http://epaper.timesofindia.com/Default/ClientEpaperBeta.asp?skin=pastissues2&enter=LowLevel'
	browser.get(url)
	print "1"

	html = browser.switch_to_frame("mainFrame")			#clicking on 'here' hyperlink


# filing the form for times of india archive
	browser.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/form/table/tbody/tr[9]/td[2]/a/span").click()
	
	time.sleep(1)

	print "2"
	browser.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/form/table/tbody/tr[2]/td[3]/input").send_keys("onion and price")

	browser.find_element_by_xpath("//*[@id=\"sPublication\"]/option[contains(text(),\""+"The Times Of India Delhi"+"\")]").click()
	browser.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/form/table/tbody/tr[6]/td[3]/input[1]").click()
	
	browser.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/form/table/tbody/tr[7]/td[3]/table/tbody/tr[2]/td[1]/input").send_keys("2006")

	browser.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/form/table/tbody/tr[7]/td[3]/table/tbody/tr[2]/td[2]/select/option[contains(text(),\""+"January"+"\")]").click()
	browser.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/form/table/tbody/tr[7]/td[3]/table/tbody/tr[2]/td[3]/select/option[contains(text(),\""+"1"+"\")]").click()

	browser.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/form/table/tbody/tr[7]/td[3]/table/tbody/tr[3]/td[1]/input").send_keys("2014")
	browser.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/form/table/tbody/tr[7]/td[3]/table/tbody/tr[3]/td[2]/select/option[contains(text(),\""+"December"+"\")]").click()
	browser.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/form/table/tbody/tr[7]/td[3]/table/tbody/tr[3]/td[3]/select/option[contains(text(),\""+"31"+"\")]").click()

	browser.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/form/table/tbody/tr[11]/td[3]/input[2]").click()
	
	browser.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/form/table/tbody/tr[12]/td[3]/select/option[contains(text(),\""+"Complete Text"+"\")]").click()
	print "4"
	# print browser.page_source
	browser.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/form/table/tbody/tr[14]/td[3]/select/option[contains(text(),\""+"Date Ascending"+"\")]").click()
	
	browser.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/form/table/tbody/tr[16]/td/input[2]").click()	
# /html/body/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/form/table/tbody/tr[16]/td/input[2]
	# for district in district_list:
		# browser.find_element_by_xpath("//*[@id=\"CmbDistrict\"]/option[contains(text(),\""+district+"\")]").click()
	count = 0
	page = 0
	for x in range(0,0):
		page = page + 1
		count = count +8
		browser.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[3]/td/table/tbody/tr/td[3]/a/b").click()	

	while(1):
		page = page +1
		time.sleep(3)
		a = browser.find_elements_by_class_name("Result_Title")
		for i in range(0,len(a)):
			count = count + 1
			print "Page ",page,"  Article count ",count, "line 122"
			Currentwindow = browser.window_handles
			f1.write("Page"+str(page)+"article"+str(count)+a[i].text.encode('utf-8'))
			f1.write('\n')
			a[i].click()
			newwindow = browser.window_handles
			# print newwindow
			
			# newwindow2 = list(set(newwindow) - set(Currentwindow))[0]
			browser.switch_to.window(newwindow[1])
	# print browser.page_source
	# print browser.current_url
			new_url = browser.current_url[:-3]+"HTML"
			browser.get(new_url)
			html2 = browser.switch_to_frame("ArticleContent")
			html2= browser.page_source
			soup = BeautifulSoup(html2,"html.parser")
			temp = soup.find('div',{'name':'textContainer'})
			if temp == None:
				f2.write("Page"+str(page)+"article"+str(count)+"EXCEPTION HERE\n")
			else:
				links = (soup.find('div',{'name':'textContainer'})).find_all('span')
				f2_string ="Page"+str(page)+"article"+str(count)
				for link in links:
					f2_string = f2_string + link.text
				f2_string.replace('\n',' ')
				f2.write(f2_string.encode('utf-8'))
				f2.write('\n')

			# print len(links)
			# browser.close()
			browser.switch_to.window(newwindow[0])
			browser.switch_to_frame("mainFrame")	

			# print browser.page_source
			# print newwindow[0]
			# a = browser.find_elements_by_class_name("Result_Title")
			# print len(a)

		browser.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[3]/td/table/tbody/tr/td[3]/a/b").click()	
	# browser.switch_to.window(Currentwindow)

	# a[1].click()
	# print soup.prettify()
	# data = soup.find_all('span',{'class':'Result_Title'})
	# for article in data:
	# 	print article.text
		# for tag in soup.find(id="CmbLocation").find_all('option'):
		# 	# print(tag.text)
		# 	list_location.append(tag.text)
		# # print(list_location[1:])
		# for location in list_location[1:]:
		# 	x = "//*[@id='CmbLocation']/option[contains(text(),\""+location+"\")]"/
		# 	browser.find_element_by_xpath(x).click()
			
		# 	first = browser.find_element_by_xpath('//*[@id="txtFromDate"]')
		# 	browser.execute_script("arguments[0].setAttribute('value',\""+fromDate+"\")", first)

		# 	last = browser.find_element_by_xpath('//*[@id="txtToDate"]')
		# 	browser.execute_script("arguments[0].setAttribute('value',\""+toDate+"\")", last)

		# 	browser.find_element_by_xpath('//*[@id="BtnData"]').click()
		# 	time.sleep(2)
		# 	html = browser.page_source
		# 	soup = BeautifulSoup(html,"lxml")
		# 	try:
		# 		table = soup.find('table',{'id':'DeviceData'})//*[@id="CmbState"]
		# 		table_rows = table.find_all('tr')
		# 		new_table = []
		# 		for row in table_rows:
		# 			table_columns = row.find_all('td')
		# 			new_row = []
		# 			for column in table_columns:
		# 				column = column.text
		# 				new_row.append(column)
		# 			new_table.append(new_row)
		# 		# print(new_table)
		# 		make_csv(toDate,location,new_table)
		# 	except:
		# 		continue

if __name__ == '__main__':
	extract_rainfall_data()
	# for i in range(1,8):
	# 	extract_rainfall_data(past_date(i,present_date()),past_date(i,present_date()))

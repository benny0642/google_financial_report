# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
# 放進公司代碼
# NASDAQ_CODES = ['GOOG']
NASDAQ_CODES = []
with open('nasdaq_100.txt', 'r') as f:
	read_data = f.read()
	NASDAQ_CODES = read_data.replace(' ', '').split(',')
	print NASDAQ_CODES
# 三種財報選項
fs_type_tabs = ['Income_Statement', 'Balance_Sheet', 'Cash_Flow']
# (季報 & 年報) 的id name
views = ['interim' ,'annual']

start_time = datetime.datetime.now()
driver = webdriver.Chrome()

for NASDAQ_CODE in NASDAQ_CODES:
	file_data = []
	try:
		driver.get("https://www.google.com/finance?q=NASDAQ:" + NASDAQ_CODE + "&fstype=ii")

		for fs_type_tab in fs_type_tabs:
			fs_type_tab = fs_type_tab.replace('_', ' ')		
			element = driver.find_element_by_link_text(fs_type_tab)
			element.click()
			for view in views:
				element = driver.find_element_by_id(view)
				element.click()
				financial_table_div = '#' + fs_type_tab[0:3].lower() + view + 'div'

				financial_table = driver.find_elements_by_css_selector(financial_table_div + ' #fs-table')
				head = financial_table[0].find_element_by_tag_name('thead')
				body = financial_table[0].find_element_by_tag_name('tbody')


				file_header = []
				head_line = head.find_element_by_tag_name('tr')
				headers = head_line.find_elements_by_tag_name('th')
				for header in headers:
				    header_text = header.text.encode('utf8')
				    file_header.append(header_text)
				file_data.append(",".join(file_header))

				body_rows = body.find_elements_by_tag_name('tr')
				for row in body_rows:
				    data = row.find_elements_by_tag_name('td')
				    file_row = []
				    for datum in data:
				        datum_text = datum.text.encode('utf8')
				        datum_text = datum_text.replace(',', '')
				        file_row.append(datum_text)
				    file_data.append(",".join(file_row))

		with open(NASDAQ_CODE + '.csv', "w") as f:
		    f.write("\n".join(file_data))
	except Exception, e:
		print "%s Got Error, Error Message:" %NASDAQ_CODE
		print e
		pass
driver.close()
end_time = datetime.datetime.now()

print 'start_time: %s' %start_time
print 'end_time: %s' %end_time
print end_time - start_time

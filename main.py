import zlibrary
import asyncio
import time
import os
import re
from lxml import etree
import urllib.request
from io import StringIO
import pandas as pd
from operator import itemgetter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import logging

logging.getLogger("zlibrary").addHandler(logging.StreamHandler())
logging.getLogger("zlibrary").setLevel(logging.DEBUG)
downpath = "/home/yapudjus/Documents/code/kindle_zlib/down"
#object of Options class
c = Options()
#passing headless parameter
c.add_argument("--headless")
#adding headless parameter to webdriver object

def check_exists_by_xpath(driver, xpath):
	try:
		driver.find_element(By.XPATH, xpath)
	except NoSuchElementException:
		return False
	return True


loc = 0
locations = ["AR", "DZ", "AM", "AU", "AUADL", "AUBNE", "AUMEL", "AUPER", "AUSYD", "AT", "AZ", "BS", "BD", "BY", "BZ", "BE", "BT", "BA", "BR", "BN", "BG", "CA", "CAYMQ", "CAYTO", "CAYVR", "CL", "CN", "CO", "CR", "HR", "KH", "CZ", "DK", "EE", "EC", "EG", "FI", "FR", "FRPAR", "GE", "GR", "DE", "HK", "HU", "IE", "ID", "IL", "IM", "IN", "IS", "IT", "ITMIL", "ITROM", "JP", "KG", "KZ", "LA", "LI", "LT", "LU", "LV", "ME", "MC", "MD", "MT", "MX", "MY", "NL", "NO", "NP", "NZ", "PA", "PE", "PH", "PK", "PL", "PT", "RO", "RU", "SG", "KR", "ES", "ESBCN", "SE", "SK", "ZA", "CH", "TH", "TR", "TW", "UA", "US", "USATL", "USBOS", "USCLT", "USCHI", "USCOL", "USDAL", "USHOU", "USIND", "USMCI", "USLAS", "USLAX", "USMIA", "USEWR", "USNYC", "USORD", "USPHL", "USPHX", "USPDX", "USSFO", "USSJC", "USSEA", "USWAS", "UY", "AE", "GB", "GBCVT", "VE", "VN"]

loaded = []
with open("loaded.txt", "r") as f:
	for line in f:
		loaded.append(line.strip())

def reload_vpn() :
	global loc
	time.sleep(2)
	print('reloading vpn')
	os.system('hotspotshield disconnect')
	time.sleep(2)
	os.system(f'hotspotshield connect {locations[loc]}')
	loc += 1
	time.sleep(5)


async def main():
	lib = zlibrary.AsyncZlib()
	# init fires up a request to check currently available domain
	await lib.init()
	newline = "\n"
	lang = list(); inp = input('please input languages, comma separated: '); lang = [*inp.split(', ')]
	format = list(); inp = input('please input format, comma separated: '); format = [*inp.split(', ')];
	exact = True
	if input('exact search [Yn]: ').lower() == 'n' : exact = False
	q = (f'{str(input("search query: "))}')
	print(f'searching for querry {q} | languages = {lang} | formats = {format} | exact = {exact}')
	paginator = await lib.search(q=q, count=50, extensions=[*format], lang=[*lang], exact=exact)  #
	all_results = list()
	print('scraping zlibrary')
	while True:  # get all results of querry inside all_result
		next_set = await paginator.next()
		for i in paginator.result : all_results.append(i)
		if (len(paginator.result) == 1) : break

	filtered_results = list()
	print('removing double')
	for i in all_results :
		hit = 0
		for x in all_results:
			if str(i["name"]).lower() == str(x["name"]).lower() :
				if str(i["extension"]).lower() == str(x["extension"]).lower() :
					if str(i["language"]).lower() == str(x["language"]).lower() :
						hit += 1
		if hit == 1 :
			filtered_results.append(i)

	sorted_results = sorted(filtered_results, key=itemgetter('name') )
	lst = list()
	e= int(0)
	for i in sorted_results: lst.append([i["language"], i["extension"], i["rating"], str([z["author"] for z in i["authors"]]).replace("[", "").replace("]", "").replace("'", ""), i["name"]]); e += 1
	# Find maximal length of all elements in list
	df = pd.DataFrame(lst)
	print(df)

	inp = input('please choose book id [0](use -- for inclusive range or a comma+single space separated list): ') or 0
	if inp.find('--') != -1 :
		temp = inp.split('--')
		ids = [i for i in range(int(temp[0]), int(temp[1]) + 1)]
	elif inp.find(', ') != -1 :
		ids = [*inp.split(', ')]
	elif inp.find('. ') != -1 :
		ids = [*inp.split('. ')]
	elif inp.find('*') != -1 :
		ids = [i for i in range(0, e)]
	else :
		ids = list([inp])
	print(ids)
	all_sets = [sorted_results[int(x)] for x in ids]

	reload_vpn()
	q_safe = re.sub('\ |\?|\.|\!|\/|\;|\:|\n|\r|\\\'', '', q)
	os.system(f'mkdir {downpath}/{q_safe}')
	locations = ["DZ", "AM", "AU", "AUADL", "AUBNE", "AUMEL", "AUPER", "AUSYD", "AT", "AZ", "BS", "BD", "BY", "BZ", "BE", "BT", "BA", "BR", "BN", "BG", "CA", "CAYMQ", "CAYTO", "CAYVR", "CL", "CN", "CO", "CR", "HR", "KH", "CZ", "DK", "EE", "EC", "EG", "FI", "FR", "FRPAR", "GE", "GR", "DE", "HK", "HU", "IE", "ID", "IL", "IM", "IN", "IS", "IT", "ITMIL", "ITROM", "JP", "KG", "KZ", "LA", "LI", "LT", "LU", "LV", "ME", "MC", "MD", "MT", "MX", "MY", "NL", "NO", "NP", "NZ", "PA", "PE", "PH", "PK", "PL", "PT", "RO", "RU", "SG", "KR", "ES", "ESBCN", "SE", "SK", "ZA", "CH", "TH", "TR", "TW", "UA", "US", "USATL", "USBOS", "USCLT", "USCHI", "USCOL", "USDAL", "USHOU", "USIND", "USMCI", "USLAS", "USLAX", "USMIA", "USEWR", "USNYC", "USORD", "USPHL", "USPHX", "USPDX", "USSFO", "USSJC", "USSEA", "USWAS", "UY", "AE", "GB", "GBCVT", "VE", "VN"]
	options=Options()
	service=Service('./drivers/geckodriver-v0.30.0-linux64/geckodriver')
	options.set_preference("browser.download.folderList", 2)
	# options.set_preference("browser.download.manager.showWhenStarting", "false")
	options.set_preference("browser.download.dir", f"{downpath}/{q_safe}")
	options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/epub+zip,application/vnd.airzip.filesecure.azs,application/octet-stream")
	driver = webdriver.Firefox(service=service, options=options)
	for current_set in all_sets :
		# # print(current_set["url"])
		# fp = urllib.request.urlopen(current_set["url"])
		# mybytes = fp.read()
		# mystr = mybytes.decode("utf8")
		# fp.close()
		# html_parser = etree.HTMLParser()
		# str_io_obj = StringIO(mystr)
		# dom_tree = etree.parse(str_io_obj, parser=html_parser)
		# a_tag_list = dom_tree.xpath('//html/body/table/tbody/tr[2]/td/div/div/div/div[2]/div[2]/div[1]/div[1]/div/a')
		# url = None
		# for a in a_tag_list:
		#     tmp1 = a.get('href')
		#     url = tmp1
		#     # print(url)
		# if url == None :
		#     a_tag_list = dom_tree.xpath('//html/body/table/tbody/tr[2]/td/div/div/div/div[2]/b/div[1]/div[1]/div[1]/div/a')
		#     for a in a_tag_list:
		#         tmp1 = a.get('href')
		#         url = tmp1
		#     # print(url)
		# # print('fuck you')
		while True :
			# print("here")
			driver.get(current_set["url"])
			print('Page title: ' + driver.title)

			ext = re.sub(r'^.*?book', '', current_set["url"])
			print(ext)
			if ext in loaded : break

			try:
				WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//html/body/table/tbody/tr[2]/td/div/div/div/div[2]/div[2]/div[1]/div[1]/div/a")))
			except :
				try :
					WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//html/body/table/tbody/tr[2]/td/div/div/div/div[2]/b/div[1]/div[1]/div[1]/div/a")))
				except :
					pass
			# if check_exists_by_xpath(driver, "/html/body/table/tbody/tr[2]/td/div/div/div/div[2]/div[2]/div[1]/div") :
			#     print('file not yet available'); break
			try :
				element = driver.find_element(By.XPATH, "//html/body/table/tbody/tr[2]/td/div/div/div/div[2]/div[2]/div[1]/div[1]/div/a")
			except :
				try :
					element = driver.find_element(By.XPATH, "//html/body/table/tbody/tr[2]/td/div/div/div/div[2]/b/div[1]/div[1]/div[1]/div/a")
				except :
					print(f'file not available, or other error on {ext}'); break
			element.click()
			if check_exists_by_xpath(driver, '/html/body/table/tbody/tr[2]/td/div/div/div/section') == True :
				reload_vpn()
			else :
				loaded.append(ext)
				with open("loaded.txt", "w") as f:
					for s in loaded:
						f.write(str(s) +"\n")
				break
		# print('there')
		# driver.implicitly_wait(10)
	driver.quit()


if __name__ == '__main__':
	asyncio.run(main())
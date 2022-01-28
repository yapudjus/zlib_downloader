import zlibrary
import asyncio
import time
import os
from lxml import etree
import urllib.request
from io import StringIO
import pandas as pd
from operator import itemgetter
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
#object of Options class
c = Options()
#passing headless parameter
c.add_argument("--headless")
#adding headless parameter to webdriver object




async def main():
    lib = zlibrary.AsyncZlib()
    # init fires up a request to check currently available domain
    await lib.init()
    paginator = await lib.search(q=input("search query: "), count=50, extensions=["mobi", "epub"], lang=["french", "english"])
    all_results = list()
    while True:  # get all results of querry inside all_result
        next_set = await paginator.next()
        for i in paginator.result : all_results.append(i)
        if (len(paginator.result) == 1) : break
    
    filtered_results = list()
    for i in all_results :
        hit = 0
        for x in all_results:
            if i["name"] == x["name"] :
                if i["extension"] == x["extension"] :
                    if i["language"] == x["language"] :
                        hit += 1
        if hit == 1 :
            filtered_results.append(i)

    sorted_results = sorted(filtered_results, key=itemgetter('name') )
    lst = list()
    e= int(0)
    for i in sorted_results: lst.append([i["language"], i["extension"], i["rating"], str([z["author"] for z in i["authors"]]).replace("[", "").replace("]", "").replace("'", ""), i["name"]])
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
    else :
        ids = list([inp])
    print(ids)
    all_sets = [sorted_results[int(x)] for x in ids]

    ran = 0
    print('reloading vpn')
    os.system('hotspotshield disconnect')
    time.sleep(1)
    os.system('hotspotshield connect')
    time.sleep(1)

    options=Options()
    service=Service('./drivers/geckodriver-v0.30.0-linux64/geckodriver')
    options.set_preference("browser.download.folderList", 2)
    # options.set_preference("browser.download.manager.showWhenStarting", "false")
    options.set_preference("browser.download.dir", "/home/yapudjus/Documents/code/kindle_zlib/down")
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/epub+zip,application/vnd.airzip.filesecure.azs,application/octet-stream")
    driver = webdriver.Firefox(service=service, options=options)

    for current_set in all_sets :
        # print(current_set["url"])
        fp = urllib.request.urlopen(current_set["url"])
        mybytes = fp.read()
        mystr = mybytes.decode("utf8")
        fp.close()
        html_parser = etree.HTMLParser()
        str_io_obj = StringIO(mystr)
        dom_tree = etree.parse(str_io_obj, parser=html_parser)
        a_tag_list = dom_tree.xpath('//html/body/table/tbody/tr[2]/td/div/div/div/div[2]/div[2]/div[1]/div[1]/div/a')
        
        for a in a_tag_list:
            tmp0 = current_set["url"][:(current_set["url"].find('/book'))]
            tmp1 = a.get('href')
            url = str(f'{tmp0}{tmp1}')
            # print(url)

        driver.implicitly_wait(1)
        driver.get(current_set["url"])
        print('Page title: ' + driver.title)
        element = driver.find_element_by_xpath("//html/body/table/tbody/tr[2]/td/div/div/div/div[2]/div[2]/div[1]/div[1]/div/a")
        element.click()
        # driver.implicitly_wait(10)
        ran += 1
        if ran == 5 :
            print('reloading vpn')
            os.system('hotspotshield disconnect')
            time.sleep(1)
            os.system('hotspotshield connect')
            time.sleep(1)
    driver.quit()


if __name__ == '__main__':
    asyncio.run(main())
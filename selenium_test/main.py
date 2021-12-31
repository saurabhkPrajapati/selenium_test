import json
import re
import os
import sys
import time
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import math
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class Trendyol:
    csvpath1 = r"D:\codes\selenium_test\csvfile\trendyol1.csv"   # original csv file
    output = r"D:\codes\selenium_test\csvfile\trendyoloutput.csv"   # output csv file

    def __init__(self, run):
        self.run = run

    def executer(self, driver):
        print("Testing for", self.run)
        with open(self.output, "w", encoding="utf-8", newline="") as wd:
            csvwriter = csv.writer(wd)
            csvwriter.writerow(["URL", "SIZES", "ORDERRED/NOT ORDERED", "SKU", "PRICE"])
            wd.close()
        try:
            with open(self.csvpath1, 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                fields = next(csvreader)
                for row in csvreader:
                    url = row[0]
                    size = row[1].split()
                    print(url)
                    print(size)
                    driver.execute_script("window.open('%s')" % (url,))
                    time.sleep(4)
                    driver.switch_to.window(driver.window_handles[1])
                    time.sleep(2)
                    odsize = []
                    try:
                        sku = driver.find_element_by_xpath(
                            '//*[@id="product-detail-app"]/div/div[2]/div[1]/div[2]/div[1]/div/div/div[1]/h1/span').text.split()[-1]
                    except:
                        sku = ""
                    try:
                        price = driver.find_element_by_xpath(
                            '//div[contains(@class,"product-price-container")]/div/div/span[contains(text(),"TL")]').text
                    except:
                        price = driver.find_element_by_xpath(
                            '//div[contains(text(),"Sepette")]/following-sibling::div/span').text
                    else:pass
                    try:
                        for i in size:
                            try:
                                element = driver.find_element_by_xpath(f'//div[contains(text(),"{i}")]')
                                action = ActionChains(driver)
                                action.move_to_element(element).click().perform()
                                time.sleep(2)
                                element = driver.find_element_by_xpath('//div[contains(text(),"Sepete Ekle")][1]')
                                action = ActionChains(driver)
                                action.move_to_element(element).click().perform()
                                odsize.append(i)
                                time.sleep(4)
                            except:
                                pass

                        alldata = [url, size, f"Ordered sizes {odsize}", sku, price]


                        with open(self.output, "a", encoding="utf-8", newline="") as wd:
                            csvwriter = csv.writer(wd)
                            csvwriter.writerow(alldata)
                            wd.close()
                    except:
                        alldata = [url, size, "Not ordered", sku, price]
                        with open(self.output, "a", encoding="utf-8", newline="") as wd:
                            csvwriter = csv.writer(wd)
                            csvwriter.writerow(alldata)
                            wd.close()
                    try:
                        driver.switch_to.alert.accept()
                    except:
                        pass
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
        except Exception as e:
            print(e)
            # sys.exit(1)
        # os._exit(1)

        driver.quit()



if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(options=options, executable_path="chromedriver.exe")
    driver.get('https://www.trendyol.com/')
    driver.implicitly_wait(3)
    driver.refresh()
    time.sleep(2)
    try:
        driver.switch_to.alert.accept()
    except:
        pass
    a = Trendyol("27")
    a.executer(driver)
    print("Process Completed")
    driver.quit()

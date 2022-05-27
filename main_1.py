import json
from pprint import pprint
import lxml
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
import time

url = "https://watch.ua/?gclid=EAIaIQobChMIgobbwNrm9wIVh6kYCh1hYgAjEAAYASAAEgImNPD_BwE"


def get_data(url):
    option = webdriver.FirefoxOptions()
    option.set_preference("general.useragent.override",
                          "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0")
    option.headless = False
    driver = webdriver.Firefox(executable_path="G:\Парсер\Часи\\firefox_driver\geckodriver.exe",options=option)

    with open("page_1.html", "w", encoding="utf-8") as file:
        file.write(driver.page_source)
    try:
        driver.get(url=url)
        driver.implicitly_wait(5)
        element = [item.find_element(By.TAG_NAME, "a").get_attribute("href") for item in
                   (driver.find_elements(By.CLASS_NAME, "ty-scroller-list__img-block"))]
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
    return element


def bs4_req():
    hrefs = get_data(url)
    headers = {
        "User - Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"
    }
    all_json=[]
    for i in hrefs:
        r = requests.get(i,headers=headers)
        soup=BeautifulSoup(r.text,"lxml")
        price = soup.find(class_="ty-price-num")
        name=soup.find(class_="ut2-pb__title")
        characteristics = {}
        characteristics["Назва"] = name.text
        characteristics["Ціна"]=price.text+" грн"
        characteristic=soup.find(class_="ty-features-list").find_next().find_next().find_next()
        items=[item.text for item in characteristic.find_all("em")]
        i=0
        if len(items)<1:
                characteristic=soup.find(class_="ty-features-list").find_next().find_next().find_next().find_next().find_next().find_next().find_next().find_next().find_next().find_next().find_next().find_next().find_next()
                items = [item.text for item in characteristic.find_all("em")]
        while i<len(items):
            characteristics[items[i+1]]=items[i+2]
            i+=3
        all_json.append(characteristics)

    with open(f"Часи"
              f".json", "a", encoding="utf-8") as file:
        json.dump(all_json, file, indent=4, ensure_ascii=False)
def main():
    bs4_req()


if __name__ == '__main__':
    main()

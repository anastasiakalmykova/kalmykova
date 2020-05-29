import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv
import time
import lxml

def get_html(url):
    """"" returns text of page """
    try:
       r = requests.get(url)
       return r.text
    except:
        print("Нет соединения")
        time.sleep(5)
        get_html(url)


def get_csv(data_table):
    """"" makes csv file with parsed data """
    with open ("contact_data.csv", mode='a', encoding='utf8') as f:
          writer = csv.writer(f, lineterminator = '\n')
          writer.writerow( (data_table['link_to_ecard'],
                          data_table["about"],
                            data_table["address"],
                           data_table["website"]) )

def get_page_data(html):
    """"" get data about companies and passes it to get_csv() """
    soup = BeautifulSoup(html, "lxml")
    info = soup.find("div", class_ = "container wrapper clearfix")
    try:
        company_about = info.find("p", class_ = "compDesc").text
    except AttributeError:
        company_about = info.find("div", class_="compDesc").text.replace("\n", "").split()
        company_about = " ".join(company_about)
    except:
         company_about = "No information"
    try:
        company_cart =  soup.find( rel = "canonical").get("href")
    except:
        company_cart = "No ecard"
    try:
        address = info.find("div", class_ = "compInfo").find("pre").text.split("\n")
        address = " ".join(address)
    except:
        address = "No address"
    try:
        website = info.find("span", class_ = "compUrlRight textns").text
    except:
        website = "No website"

    parsed_data = {"link_to_ecard" : company_cart,
                   "about" : company_about,
                   "address": address,
                   "website" : website}
    data_table = get_csv(parsed_data)

def main():
    """"" get csv with main data about companies, makes list of ecard urls """
    data = pd.read_csv("main_data.csv", header=None)
    urls = list()
    for i in data[1]:
        urls.append(i)

    for url in urls:
       html = get_html(url)
       get_page_data(html)



if __name__ == "__main__":
    main()

import requests
from bs4 import BeautifulSoup
import lxml
import csv
import time
import pandas as pd
import user_modul as p4

def get_html(url):
    """"" returns text of page """
    try:
        r = requests.get(url)
        return r.text
    except:
        print("Нет соединения")
        time.sleep(5)
        get_html(url)

def get_all_pages(html):
    """"" finds out how many pages with company ecards are """
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find("div", class_ = "page-navi").find_all("a", class_ = "page display-spinner")[2].get('href')
    total_pages = pages.split("pg-")[1].split("/")[0]
    return int(total_pages)

def get_csv(data_table):
    """"" writes data to csv file """
    with open ("main_data.csv", mode='a', encoding='utf8') as f:
          writer = csv.writer(f, lineterminator = '\n')
          writer.writerow( (data_table['company'],
                          data_table["link_to_ecard"],
                            data_table["country"],
                           data_table["city"],
                           data_table['main_tag']) )

def get_page_data(html):
    """"" collects data about companies, passes it get_csv() """
    soup = BeautifulSoup(html, "lxml")
    carts = soup.find("ul", class_ = "full-list-article").findAll("li", class_ = "list-article vcard")
    for cart in carts:
            try:
                company_name = cart.find("a", class_ = "company-name display-spinner").text
                company_name = company_name[5: len(company_name) - 4]
            except:
                 company_name = "No name"
            try:
                company_cart =  cart.find("a", class_ = "company-name display-spinner").get("href")
            except:
                company_cart = "No ecard"
            try:
                company_location = cart.find("div", class_ = "loc").find(class_ = "country-name").text
            except:
                company_location = "No country"
            try:
                city_location = cart.find("div", class_ = "loc").find(class_ = "street-address postal-code locality").text
            except:
                city_location = "No city"
            try:
                company_description = cart.find("div", class_ = "content ecard-delegate").find("span", class_ = "dfn").text
            except:
                company_description = "No description"

            parsed_data = {"company" : company_name,
                           "link_to_ecard" : company_cart,
                           "country" : company_location,
                           "city": city_location,
                           "main_tag" : company_description}
            data_table = get_csv(parsed_data)

def data_clean():
    """"" deletes duplicates and data strings without link to company ecard, makes new csv """
    names_ = ["company", "link_to_ecard", "country", "city", "main_tag"]
    data = pd.read_csv("main_data.csv", header = 0, names = names_ )
    data = pd.DataFrame(data)
    data['link_to_ecard'] = data['link_to_ecard'].astype(str)
    data = data.loc[data['link_to_ecard'] != "No ecard"]
    data = data.drop_duplicates(subset =["link_to_ecard"], keep = 'first', inplace = False)
    data.to_csv("main_data.csv", header= None, index=False, encoding='utf-8')

def main(url, basic_url, changing_url):
    """"" gets url and number of pages to find data, passes urls to get_html() """
    url =  url
    basic_url = basic_url
    changing_url = changing_url
    total_pages = get_all_pages(get_html(url))
    #for i in range(1, total_pages + 1):
    for i in range(11, 41):
        next_page = basic_url + str(i) + changing_url
        html = get_html(next_page)
        get_page_data(html)


if __name__ == "__main__":
    main(p4.url, p4.basic_url, p4.changing_url)
    data_clean()



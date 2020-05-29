import pandas as pd
from bs4 import BeautifulSoup
import csv, lxml, os, requests, sqlite3
import time

import main_pars as p1
import contact_pars as p2
import pars_base as p3

url =  "https://www.europages.com.ru/предприятия/Пакеты%20программ,%20обработка%20данных/ss-13a/pg-1/электронная%20обработка%20данных%20-%20по.html"
basic_url = "https://www.europages.com.ru/предприятия/Пакеты%20программ,%20обработка%20данных/ss-13a/pg-"
changing_url = "/электронная%20обработка%20данных%20-%20по.html"


def request_to_db():
    """"" connects to database, makes users requests """
    conn = sqlite3.connect("Parsing_database.db")
    cursor = conn.cursor()

    sql = "SELECT * from parsed_main left join parsed_contacts on parsed_main.link_to_ecard = parsed_contacts.link_to_ecard"
    print("Результат запроса:")
    for row in cursor.execute(sql):
        print(row)

if __name__ == "__main__":
     p1.main(url, basic_url, changing_url)
     p1.data_clean()
     p2.main()
     p3.make_base()
     #p3.delete_csv()
     request_to_db()
     #p3.delete_db()

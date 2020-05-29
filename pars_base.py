import sqlite3
import csv
import os

def make_base():
    """"" makes database with two tables, geta data from csv files, created in main_pars and contact_pars """
    connection = sqlite3.connect("Parsing_database.db")
    sql = "CREATE TABLE parsed_contacts (link_to_ecard TEXT, about TEXT, address TEXT, website TEXT)"
    cur = connection.cursor()
    cur.execute("DROP TABLE if exists parsed_contacts")
    cur.execute(sql)

    with open('contact_data.csv','r', encoding='utf-8', newline='') as c_table:
        csv_reader = csv.reader(c_table, delimiter = ",")
        rows = list(csv_reader)
        for jj, row in enumerate(rows):
            for i, ii in enumerate(row):
                link_to_ecard = rows[jj][0]
                about = rows[jj][1]
                address = rows[jj][2]
                website = rows[jj][3]
                cur.execute(''' INSERT INTO parsed_contacts(link_to_ecard, about, address, website)
                    VALUES(?, ?, ?, ?) ''', (link_to_ecard, about, address, website))
                connection.commit()
                break

    sql = "CREATE TABLE parsed_main (company TEXT, link_to_ecard TEXT, country TEXT, city TEXT, main_tag TEXT)"
    cur = connection.cursor()
    cur.execute("DROP TABLE if exists parsed_main")
    cur.execute(sql)

    with open('main_data.csv', 'r', encoding='utf-8', newline='') as m_table:
         csv_reader = csv.reader(m_table, delimiter=",")
         rows = list(csv_reader)
         for jj, row in enumerate(rows):
             for i, ii in enumerate(row):
                company = rows[jj][0]
                link_to_ecard = rows[jj][1]
                country = rows[jj][2]
                city = rows[jj][3]
                main_tag = rows[jj][4]
                cur.execute(''' INSERT INTO parsed_main(company, link_to_ecard, country, city, main_tag)
                VALUES(?, ?, ?, ?, ?) ''', (company, link_to_ecard, country, city, main_tag))
                connection.commit()
                break
               #connection.close()

def delete_csv():
    """"" deletes csv files """
    os.remove("main_data.csv")
    os.remove("contact_data.csv")

def delete_db():
    """"" deletes database """
    os.remove("Parsing_database.db")

if __name__ == "__main__":
    make_base()


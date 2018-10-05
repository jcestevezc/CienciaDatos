'''
Created on 4/10/2018

@author: co1012351486
'''

import lxml.etree
import lxml.html
import requests
import pandas as pd
import psycopg2


r = requests.get("https://www.larepublica.co/economia/ministerio-de-comercio-presento-estrategia-estado-simple-colombia-agil-2777011")
root = lxml.html.fromstring(r.content)


def laRepublica(root):
    title = root.xpath("//meta[@property='og:title']/@content")
    content = root.xpath("//div[contains(@class,'articleWrapper')]")
    author = root.xpath("//div[@class='autorArticle']")
    date = root.xpath("//div[@class='columns medium-3 date']")
    medio = root.xpath("//meta[@name='author']/@content")
    type_article = root.xpath("//meta[@property='og:type']/@content") 
    key_words = root.xpath("//meta[@name='keywords']/@content")
    
    dictionary = {'title': title, 
                'content': content, 
                'author':author,
                'date':date,
                'medio':medio,
                'type_article':type_article,
                'key_words':key_words}
    print('El tipo de dato es:  ')
    print(type(dictionary))
    register = pd.DataFrame(data = dictionary)
    input()

laRepublica(root)

connection  = psycopg2.connect(host="localhost",database="data_science", user="postgres", password="root")
cursor = connection.cursor()
print('PostgreSQL database version:')
cursor.execute('SELECT version()')

#sql = """INSERT INTO vendors(vendor_name) VALUES(%s) RETURNING vendor_id;"""
#cursor.execute(sql, (value1,value2))
connection.commit()
cursor.close()
connection.close()

#file = pd.read_csv("pages.csv", sep=";")
#print(file.iloc[0])


'''
Created on 4/10/2018

@author: Juan Camilo Estevez
'''

import lxml.etree
import lxml.html
import requests
import pandas as pd
import psycopg2

connection  = psycopg2.connect(
    host="localhost",
    database="data_science", 
    user="postgres", 
    password="root"
)

cursor = connection.cursor()
sql_digital_press = 'INSERT INTO "DS_DIGITAL_PRESS" ("TITLE", "AUTHOR", "DATE", "MEDIO", "TYPE_ARTICLE", "KEY_WORDS","CONTENT")  VALUES ('
r = requests.get("https://www.larepublica.co/economia/ministerio-de-comercio-presento-estrategia-estado-simple-colombia-agil-2777011")
root = lxml.html.fromstring(r.content)

r = requests.get("http://www.elcolombiano.com/colombia/los-danos-de-la-mineria-ilegal-en-el-medio-ambiente-antioqueno-GY9450967")
root2 = lxml.html.fromstring(r.content)

def laRepublica(root,sql_digital_press):
    title = root.xpath("//meta[@property='og:title']/@content")
    content = root.xpath("//div[contains(@class,'articleWrapper')]")[0].text_content()
    author = root.xpath("//div[@class='autorArticle']")[0].text_content()
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
    
    register = clean(dictionary)
    sql_digital_press = sql_digital_press +"'"+ register.title.values[0] + "','"+str(register.author.values[0]) + "','"+ str(register.date.values[0]) + "','"+ str(register.medio.values[0]) + "','"+ str(register.type_article.values[0]) + "','"+ str(register.key_words.values[0]) + "','"+ str(register.content.values[0]) + "');"
    cursor.execute(sql_digital_press)
    
def elColombiano(root,sql_digital_press):
    title = root.xpath("//meta[@property='og:title']/@content")
    content = root.xpath("//div[@class='text']")[0].text_content()
    #content = format(content[0].text.strip())
    author = root.xpath("//meta[@name='author']/@content")
    date = root.xpath("//div[@class='autor']//h6")
    date = format(date[0].text.strip())
    medio = root.xpath("//meta[@property='og:site_name']/@content")
    type_article = root.xpath("//meta[@property='og:type']/@content") 
    key_words = root.xpath("//meta[@name='keywords']/@content")
    key_words = str(key_words)
    
    dictionary = {'title': title, 
                'content': content, 
                'author':author,
                'date':date,
                'medio':medio,
                'type_article':type_article,
                'key_words':key_words
    }
    
    #print(dictionary)
    #input()
    register = clean(dictionary)
    sql_digital_press = sql_digital_press +"'"+ register.title.values[0] + "','"+str(register.author.values[0]) + "','"+ str(register.date.values[0]) + "','"+ str(register.medio.values[0]) + "','"+ str(register.type_article.values[0]) + "','"+ str(register.key_words.values[0]) + "','"+ str(register.content.values[0]) + "');"
    print(sql_digital_press)
    cursor.execute(sql_digital_press)
    
def clean(dictionary):
    register = pd.DataFrame(data = dictionary)
    register.title = str(register.title.values[0]).replace("[", "").replace("]", "").replace("  ", "")
    register.content = str(register.content.values[0]).replace("[", "").replace("]", "").replace("  ", "").replace("\t", "").replace("\n", "").replace("\r", "")
    register.author = str(register.author.values[0]).replace("[", "").replace("]", "").replace("  ", "")
    register.date = str(register.date.values[0]).replace("[", "").replace("]", "").replace("  ", "").replace("\t", "").replace("\n", "").replace("\r", "")
    register.medio = str(register.medio.values[0]).replace("[", "").replace("]", "").replace("  ", "")
    register.type_article = str(register.type_article.values[0]).replace("[", "").replace("]", "").replace("  ", "")
    register.key_words = str(register.key_words.values[0]).replace("[", "").replace("]", "").replace("  ", "").replace("'", "")
    return register


laRepublica(root,sql_digital_press)
#elColombiano(root2,sql_digital_press)

cursor.execute('SELECT * FROM public."DS_DIGITAL_PRESS"')
rows = cursor.fetchall()
for row in rows:
    print("Registro"+format(row))

connection.commit()
cursor.close()
connection.close()
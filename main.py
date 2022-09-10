from bs4 import BeautifulSoup
import requests
import sqlite3
import csv
import pandas as pd

count=0;
with open('ddmmyyy_verge.csv','r') as csvfile:
    csvreader=csv.reader(csvfile)
    for line in csvreader:
        count=count+1;
    if count !=0:
        count-1;

connection=sqlite3.connect("vergedata.db")

cursor=connection.cursor()

#creating a table

command_create="""CREATE TABLE IF NOT EXISTS
DataVerge(ID INTEGER PRIMARY KEY,URL TEXT,HEADLINE TEXT,AUTHOR TEXT, DATE TEXT)""";

cursor.execute(command_create)


html=requests.get('https://www.theverge.com/').text
soup=BeautifulSoup(html,'lxml')
news_list=soup.find_all('div',class_='c-compact-river__entry')
# print(news_list);
for index,news in enumerate(news_list):
    heading=news.find('h2',class_='c-entry-box--compact__title')
    heading=heading.a.text if heading else "N/A"
    author=news.find('span',class_='c-byline__author-name')
    author=author.text if author else "N/A"
    time=news.find('time',class_='c-byline__item')
    time=time["datetime"] if time else "N/A".replace(':','/');
    url=news.find('h2',class_='c-entry-box--compact__title').a['href']
    # print(f''' 
    #     author:{author}
    #     heading:{heading}
    #     time:{time}
    #     url:{url}
    #     id:{index+count}''')

    command_add="""INSERT OR IGNORE INTO DataVerge VALUES
    (\"%d\",\"%s\",\"%s\",\"%s\",\"%s\")""";
    cursor.execute(command_add % (index,url,heading,author,time));

connection.commit();
command_query="""SELECT * FROM DataVerge""";
df=pd.read_sql_query(command_query,connection);
df.to_csv('ddmmyyy_verge.csv',index=False)

   
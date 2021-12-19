import sqlite3
import pandas as pd
import re

data = sqlite3.connect('works.sqlite')
cursor = data.cursor()
cursor.execute('drop table if exists works')
cursor.execute('create table works ('
               'ID INTEGER PRIMARY KEY AUTOINCREMENT,'
               'salary INTEGER,'
               'educationType TEXT,'
               'jobTitle TEXT,'
               'qualification TEXT,'
               'gender TEXT,'
               'dateModify TEXT,'
               'skills TEXT,'
               'otherInfo TEXT)')
data.commit()
df = pd.read_csv("works.csv")
df.to_sql("works", data, if_exists='append', index=False)
data.commit()
#Создайте отдельную таблицу с гендером, заполните ее значениями, сделайте на нее внешний ключ из таблицы works.
cursor.execute('drop table if exists genders')
cursor.execute('create table genders(id INTEGER PRIMARY KEY AUTOINCREMENT, value_gender TEXT)')
cursor.execute('INSERT INTO genders(value_gender) SELECT DISTINCT gender FROM works WHERE gender IS NOT NULL')
cursor.execute('ALTER TABLE works ADD COLUMN id_gender INTEGER REFERENCES genders(id)')
cursor.execute('UPDATE works SET id_gender = (SELECT id FROM genders WHERE value_gender = works.gender)')
cursor.execute('ALTER TABLE works DROP COLUMN gender')
data.commit()

cursor.execute('SELECT * FROM genders')
print(cursor.fetchall())

# Отдельная таблица для образования.
cursor.execute('drop table if exists education')
cursor.execute('create table education(id INTEGER PRIMARY KEY AUTOINCREMENT, value_education TEXT)')
cursor.execute('INSERT INTO education(value_education) SELECT DISTINCT educationType FROM works WHERE educationType IS NOT NULL')
cursor.execute('ALTER TABLE works ADD COLUMN id_education INTEGER REFERENCES education(id)')
cursor.execute('UPDATE works SET id_education = (SELECT id FROM education WHERE value_education = works.educationType)')
cursor.execute('ALTER TABLE works DROP COLUMN educationType')
data.commit()

cursor.execute('SELECT * FROM education')
print(cursor.fetchall())



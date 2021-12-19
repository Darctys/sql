import sqlite3
import pandas as pd
import re


def field_cleaner(field):
    return re.sub(r'\<[^>]*\>', '', str(field))


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
# Скиллы и other info
df['skills'] = df['skills'].apply(field_cleaner)
df['otherInfo'] = df['otherInfo'].apply(field_cleaner)

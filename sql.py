import os
import sqlite3

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure

data = sqlite3.connect('works.sqlite')
cursor = data.cursor()
cursor.execute('drop table if exists works')
#1. Создайте и заполните таблицу запросами, создайте техническое поле ID c параметрами INTEGER PRIMARY KEY AUTOINCREMENT.
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
#2. Добавьте индекс на поле salary. Изменится ли после этого размер файла? На сколько?
weight_no_index = os.path.getsize('works.sqlite')
cursor.execute('create index salary_index on works (salary)')
data.commit()
weight_index = os.path.getsize('works.sqlite')
delta = weight_index - weight_no_index
print("Обьем при добавлении индекса изменился на: ", delta)
#3. Выведите количество записей.
cursor.execute('SELECT COUNT(*) FROM works')
print("Количество всех записей: ", cursor.fetchall()[0][0])
cursor.execute('SELECT COUNT(*) FROM works where gender = "Мужской"')
#4. Выведите количество мужчин и женщин.
mens = cursor.fetchall()[0][0]
cursor.execute('SELECT COUNT(*) FROM works where gender = "Женский"')
womens = cursor.fetchall()[0][0]
print("Количество мужчин: ", mens, "Количество женщин:", womens)
#5. У скольки записей заполены skills?
cursor.execute('SELECT COUNT(*) FROM works where skills not null')
print("Записи у которых заполенын Skills:", cursor.fetchall()[0][0])
#6. Получить заполненные скиллы.
# cursor.execute('SELECT skills FROM works where skills not null')
# print(cursor.fetchall())
#7. Вывести зарплату только у тех, у кого в скилах есть Python.
cursor.execute('SELECT salary FROM works where skills LIKE "%Python%"')
print("Зарплаты у кого в скилах указон пайтон:", cursor.fetchall())

#8.Построить перцентили и разброс по з/п у мужчин и женщин.
men_sal = np.array([s[0] for s in cursor.execute("SELECT salary FROM works WHERE gender='Мужской';")])
women_sal = np.array([s[0] for s in cursor.execute("SELECT salary FROM works WHERE gender='Женский';")])
per = range(10, 91, 10)
men_per = np.percentile(men_sal, per, interpolation='lower')
women_per = np.percentile(women_sal, per, interpolation='lower')
figure(figsize=(10, 6))
plt.ylabel("Зарплата")
plt.xlabel("Перцентили")
plt.plot(per, men_per, 'r')
plt.plot(per, women_per, 'g')
plt.legend(["Мужчины", "Женщины"])
plt.show()

#9.Построить графики распределения по з/п мужчин и женщин
figure(figsize=(30, 10))
women_frame = women_sal[women_sal <= 160000]
men_frame = men_sal[men_sal <= 160000]
x = range(0, 160000, 10000)
y_loc = [i * 1e-6 for i in range(0, 51, 5)]
y = [round(i * 10000, 2) for i in y_loc]
plt.xticks(ticks=x, labels=x, rotation=50)
plt.yticks(ticks=y_loc, labels=y)
plt.hist([men_frame, women_frame],  int(160000 / 10000), label=['Мужчины', 'Женщины'], density=True)
plt.legend(loc='upper left')
plt.title("Распределение з/п среди мужчин и женщин")
plt.ylabel("Перцентили")
plt.xlabel("Зарплата")
plt.show()

#10.Построить графики распределения по з/п с учётом образования
statement = "SELECT salary FROM works WHERE salary <= " + str(160000) + " AND educationType = "
school = np.array([i[0] for i in cursor.execute(statement + "'Среднее';")])
suz = np.array([i[0] for i in cursor.execute(statement + "'Среднее профессиональное';")])
vuz = np.array([i[0] for i in cursor.execute(statement + "'Высшее';")])
not_full_vus = np.array([i[0] for i in cursor.execute(statement + "'Незаконченное высшее';")])
y_loc = [i * 1e-6 for i in range(0, 51, 5)]
y = [round(i * 10000, 2) for i in y_loc]
figure(figsize=(30, 10))
plt.xticks(ticks=x, labels=x, rotation=50)
plt.yticks(ticks=y_loc, labels=y)
plt.hist([school, suz, vuz, not_full_vus], int(160000 / 10000), label=['Среднее', 'Среднее профессиональное', 'Высшее', 'Незаконченное высшее'], density=True)
plt.legend(loc='upper left')
plt.title("Распределение з/п по образованию")
plt.ylabel("Перцентили")
plt.xlabel("Зарплата")
plt.show()

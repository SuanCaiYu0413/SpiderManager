from config import db
import pandas as pd
cur = db.cursor()
city_list=pd.read_excel(r'C:\Users\Administrator\Desktop\city_list.xlsx')
for i in  city_list['city']:
    print(i)
    sql_insert = "insert into city_list(city) values('{}')" .format(i)
    cur.execute(sql_insert)
    db.commit()

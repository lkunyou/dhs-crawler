# -*- coding: utf-8 -*-
import pymysql

DB_HOST = '8.163.58.109'
DB_PORT = 3306
DB_USER = 'thai_auto_parts_crm'
DB_PASSWORD = 'tDdY8NX2xJ6HpdHz'
DB_NAME = 'thai_auto_parts_crm'

conn = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME, charset='utf8mb4')
cursor = conn.cursor()

cursor.execute("SELECT id, company_name FROM p_company WHERE company_name REGEXP '^[0-9]+' LIMIT 20")
results = cursor.fetchall()

print("公司名称以数字开头的示例：")
for row in results:
    print(f"ID: {row[0]} - 名称: {row[1]}")

conn.close()
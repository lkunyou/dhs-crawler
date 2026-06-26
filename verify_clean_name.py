# -*- coding: utf-8 -*-
import pymysql

DB_HOST = '8.163.58.109'
DB_PORT = 3306
DB_USER = 'thai_auto_parts_crm'
DB_PASSWORD = 'tDdY8NX2xJ6HpdHz'
DB_NAME = 'thai_auto_parts_crm'

conn = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME, charset='utf8mb4')
cursor = conn.cursor()

cursor.execute("""
    SELECT id, company_name, email_subject, LEFT(development_email_template, 50) 
    FROM p_company 
    WHERE id IN (312, 321, 411, 412, 322) 
""")

print("验证公司名称数字前缀已去除：")
for row in cursor.fetchall():
    print(f"\nID: {row[0]}")
    print(f"原公司名称: {row[1]}")
    print(f"邮件主题: {row[2]}")
    print(f"开发信开头: {row[3]}")

conn.close()
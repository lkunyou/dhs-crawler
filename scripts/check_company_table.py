import pymysql

DB_HOST = '8.163.58.109'
DB_PORT = 3306
DB_USER = 'thai_auto_parts_crm'
DB_PASSWORD = 'tDdY8NX2xJ6HpdHz'
DB_NAME = 'thai_auto_parts_crm'

conn = pymysql.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    charset='utf8mb4'
)

cursor = conn.cursor()
cursor.execute("DESCRIBE p_company")
columns = cursor.fetchall()

print("现有 p_company 表结构:")
print("-" * 60)
for col in columns:
    print(f"  {col[0]:<20} {col[1]:<25} {col[2]}")

cursor.execute("SELECT COUNT(*) FROM p_company")
count = cursor.fetchone()[0]
print(f"\n现有记录数: {count}")

conn.close()
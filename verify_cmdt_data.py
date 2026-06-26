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

cursor.execute("SELECT COUNT(*) FROM p_cmdt_code")
total = cursor.fetchone()[0]
print(f"📊 CMDT编码总数: {total}")

cursor.execute("SELECT section_code, COUNT(*) FROM p_cmdt_code GROUP BY section_code ORDER BY section_code")
results = cursor.fetchall()
print("\n📈 大类分布:")
for row in results:
    print(f"  第{row[0]}类: {row[1]} 条")

cursor.execute("SELECT chapter_code, COUNT(*) FROM p_cmdt_code GROUP BY chapter_code ORDER BY chapter_code")
results = cursor.fetchall()
print("\n📈 中类分布:")
for row in results:
    print(f"  编码 {row[0]}: {row[1]} 条")

cursor.execute("SELECT cmdt_code, description_en, description_cn FROM p_cmdt_code ORDER BY cmdt_code LIMIT 20")
results = cursor.fetchall()
print("\n📝 前20条记录:")
print("-" * 90)
print(f"{'CMDT编码':<12} {'英文描述':<35} {'中文描述':<35}")
print("-" * 90)
for row in results:
    print(f"{row[0]:<12} {row[1][:35]:<35} {row[2][:35]:<35}")

cursor.execute("SELECT * FROM p_cmdt_code WHERE cmdt_code LIKE '%02%' LIMIT 5")
results = cursor.fetchall()
print("\n🔍 搜索示例(包含02):")
for row in results:
    print(f"  {row[5]} | {row[6]} | {row[7]}")

conn.close()

print("\n🎉 CMDT数据验证完成！")
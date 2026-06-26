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

print("=" * 80)
print("数据质量检查报告")
print("=" * 80)

cursor.execute("SELECT COUNT(*) FROM p_company")
total = cursor.fetchone()[0]
print(f"\n📊 客户总数: {total}")

cursor.execute("SELECT company_type, COUNT(*) FROM p_company GROUP BY company_type")
results = cursor.fetchall()
print("\n🏢 company_type分布:")
for row in results:
    print(f"  {row[0]}: {row[1]} 条")

cursor.execute("SELECT COUNT(*) FROM p_company WHERE phone LIKE '%xxx%'")
placeholder_phones = cursor.fetchone()[0]
print(f"\n📞 含占位符电话号码的记录: {placeholder_phones} 条")

cursor.execute("SELECT company_name, phone FROM p_company WHERE phone LIKE '%xxx%' LIMIT 5")
results = cursor.fetchall()
print("示例:")
for row in results:
    print(f"  {row[0]}: {row[1]}")

cursor.execute("SELECT COUNT(*) FROM p_company WHERE email LIKE 'info@%' OR email LIKE 'contact@%' OR email LIKE 'sales@%'")
generic_emails = cursor.fetchone()[0]
print(f"\n📧 通用邮箱地址(info@/contact@/sales@): {generic_emails} 条")

cursor.execute("SELECT COUNT(*) FROM p_company WHERE website IS NULL OR website = '' OR website = '-'")
no_website = cursor.fetchone()[0]
print(f"\n🌐 无官网的记录: {no_website} 条")

cursor.execute("""
SELECT company_name, lead_score, lead_grade, company_type, notes
FROM p_company 
WHERE notes IS NOT NULL AND notes != ''
ORDER BY lead_score DESC
""")
results = cursor.fetchall()
print(f"\n📝 有备注的客户:")
for row in results:
    print(f"  {row[0][:40]:<40} | 评分: {row[1]:<3} | 等级: {row[2]} | 类型: {row[3]:<12} | 备注: {row[4]}")

conn.close()

print("\n🎉 数据质量检查完成！")
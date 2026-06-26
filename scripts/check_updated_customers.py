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

cursor.execute("""
SELECT company_name, quality_requirement, recommended_products, recommended_channels, 
       price_sensitivity, after_sales_requirement
FROM p_company 
WHERE lead_score >= 80 AND quality_requirement IS NOT NULL 
ORDER BY lead_score DESC LIMIT 5
""")

results = cursor.fetchall()

print("前5条高质量客户的分析字段情况:")
print("=" * 80)
print(f"{'公司名称':<40} | {'质量要求':<20} | {'推荐产品':<20}")
print("-" * 80)

for row in results:
    company_name = row[0] or 'N/A'
    quality = (row[1] or '').strip()[:20]
    products = (row[2] or '').strip()[:20]
    print(f"{company_name[:40]:<40} | {quality:<20} | {products:<20}")

cursor.execute("""
SELECT company_name, quality_requirement, recommended_products, recommended_channels,
       price_sensitivity, after_sales_requirement
FROM p_company 
WHERE lead_score >= 80 AND (quality_requirement IS NULL OR quality_requirement = '')
ORDER BY lead_score DESC
""")

results = cursor.fetchall()
print(f"\n⚠️ 高质量客户中分析字段为空的数量: {len(results)}")

if results:
    print("这些客户的分析字段被覆盖了:")
    for row in results:
        print(f"  - {row[0]}")

cursor.execute("DESCRIBE p_company")
columns = cursor.fetchall()

print("\n当前数据库字段列表:")
print("=" * 60)
for col in columns:
    print(f"  {col[0]:<30} - {col[1]}")

conn.close()
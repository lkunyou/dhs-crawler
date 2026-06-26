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

cursor.execute("SHOW COLUMNS FROM p_company LIKE 'notes'")
result = cursor.fetchone()
if result:
    print("✅ notes字段已存在")
else:
    cursor.execute("ALTER TABLE p_company ADD COLUMN notes VARCHAR(500) COMMENT '备注信息'")
    print("✅ 成功添加notes字段")

companies_data = [
    {'company_name': 'SCL Motor Part Co., Ltd', 'notes': 'Top distributor'},
    {'company_name': 'DENSO Sales (Thailand) Co., Ltd', 'notes': 'Tier1 supplier'},
    {'company_name': 'Toyota Tsusho (Thailand)', 'notes': 'Toyota supply chain'},
    {'company_name': 'Honda Trading Asia', 'notes': 'OEM channel'},
    {'company_name': 'Isuzu Motors Thailand', 'notes': 'Commercial vehicle'},
    {'company_name': 'AISIN Asia Thailand', 'notes': 'OEM supplier'},
    {'company_name': 'Robert Bosch Thailand', 'notes': 'strong aftermarket'},
]

updated_count = 0
for company in companies_data:
    if company['notes']:
        cursor.execute(
            "UPDATE p_company SET notes = %s WHERE company_name = %s",
            (company['notes'], company['company_name'])
        )
        updated_count += 1

conn.commit()
print(f"✅ 更新了 {updated_count} 条记录的notes字段")

cursor.execute("SELECT company_name, notes FROM p_company WHERE notes IS NOT NULL AND notes != ''")
results = cursor.fetchall()
print("\n📝 有备注的客户:")
for row in results:
    print(f"  {row[0]}: {row[1]}")

conn.close()

print("\n🎉 完成！")
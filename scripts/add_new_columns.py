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

columns_to_add = [
    ("core_contact", "VARCHAR(200)", "核心联系人"),
    ("annual_revenue_usd", "DECIMAL(15,2)", "年营收(USD)"),
    ("purchase_potential", "VARCHAR(50)", "采购潜力"),
    ("development_priority", "VARCHAR(50)", "开发优先级"),
]

cursor.execute("DESCRIBE p_company")
existing_columns = [col[0] for col in cursor.fetchall()]

for col_name, col_type, comment in columns_to_add:
    if col_name not in existing_columns:
        try:
            sql = f"ALTER TABLE p_company ADD COLUMN {col_name} {col_type} COMMENT '{comment}'"
            cursor.execute(sql)
            print(f"✅ 新增字段: {col_name} ({col_type})")
        except Exception as e:
            print(f"❌ 添加字段 {col_name} 失败: {e}")
    else:
        print(f"⚠️ 字段 {col_name} 已存在")

conn.commit()

cursor.execute("DESCRIBE p_company")
columns = cursor.fetchall()

print("\n更新后的字段列表:")
print("=" * 60)
for col in columns:
    if col[0] in [c[0] for c in columns_to_add]:
        print(f"  {col[0]:<30} - {col[1]} *新字段")
    else:
        print(f"  {col[0]:<30} - {col[1]}")

conn.close()

print("\n🎉 字段添加完成！")
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
print("客户数据验证报告")
print("=" * 80)

cursor.execute("SELECT COUNT(*) as total FROM p_company")
total = cursor.fetchone()[0]
print(f"\n📊 客户总数: {total}")

cursor.execute("SELECT lead_grade, COUNT(*) as count FROM p_company GROUP BY lead_grade ORDER BY lead_grade")
grades = cursor.fetchall()
print("\n📈 客户等级分布:")
for grade, count in grades:
    print(f"  {grade}: {count} 条")

cursor.execute("SELECT COUNT(*) FROM p_company WHERE core_contact IS NOT NULL AND core_contact != ''")
contact_count = cursor.fetchone()[0]
print(f"\n📧 有核心联系人: {contact_count} 条")

cursor.execute("SELECT COUNT(*) FROM p_company WHERE annual_revenue_usd IS NOT NULL")
revenue_count = cursor.fetchone()[0]
print(f"💰 有年营收记录: {revenue_count} 条")

cursor.execute("SELECT COUNT(*) FROM p_company WHERE quality_requirement IS NOT NULL AND quality_requirement != ''")
analysis_count = cursor.fetchone()[0]
print(f"📋 有分析字段记录: {analysis_count} 条")

cursor.execute("SELECT COUNT(*) FROM p_company WHERE purchase_potential IS NOT NULL AND purchase_potential != ''")
potential_count = cursor.fetchone()[0]
print(f"🎯 有采购潜力记录: {potential_count} 条")

cursor.execute("SELECT COUNT(*) FROM p_company WHERE development_priority IS NOT NULL AND development_priority != ''")
priority_count = cursor.fetchone()[0]
print(f"⭐ 有开发优先级记录: {priority_count} 条")

cursor.execute("""
SELECT company_name, core_contact, annual_revenue_usd, purchase_potential, development_priority
FROM p_company 
WHERE annual_revenue_usd IS NOT NULL
ORDER BY annual_revenue_usd DESC
LIMIT 5
""")
results = cursor.fetchall()

print("\n🏆 前5大客户（按年营收）:")
print("-" * 80)
print(f"{'公司名称':<35} | {'联系人':<20} | {'年营收(USD)':<15} | {'采购潜力'} | {'优先级'}")
print("-" * 80)
for row in results:
    revenue_str = str(row[2])
    if float(row[2]) >= 10000000:
        revenue_str = f"{float(row[2])/10000000:.1f}千万"
    elif float(row[2]) >= 10000:
        revenue_str = f"{float(row[2])/10000:.0f}万"
    print(f"{row[0][:35]:<35} | {(row[1] or '')[:20]:<20} | {revenue_str:<15} | {row[3] or '-':<8} | {row[4] or '-'}")

cursor.execute("""
SELECT company_name, quality_requirement, recommended_products, recommended_channels
FROM p_company 
WHERE lead_grade = 'S'
ORDER BY lead_score DESC
LIMIT 3
""")
results = cursor.fetchall()

print("\n👑 S级客户分析字段示例:")
print("-" * 80)
for row in results:
    print(f"\n公司: {row[0]}")
    print(f"质量要求: {row[1][:60] if row[1] else '-'}")
    print(f"推荐产品: {row[2][:60] if row[2] else '-'}")
    print(f"推荐渠道: {row[3] if row[3] else '-'}")

conn.close()

print("\n🎉 数据验证完成！")
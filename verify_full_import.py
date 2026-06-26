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
print("完整版客户数据验证报告")
print("=" * 80)

cursor.execute("SELECT COUNT(*) as total FROM p_company")
total = cursor.fetchone()[0]
print(f"\n📊 客户总数: {total}")

cursor.execute("SELECT lead_grade, COUNT(*) as count FROM p_company GROUP BY lead_grade ORDER BY lead_grade")
grades = cursor.fetchall()
print("\n📈 客户等级分布:")
for grade, count in grades:
    print(f"  {grade}: {count} 条")

cursor.execute("SELECT COUNT(*) FROM p_company WHERE first_email_strategy IS NOT NULL AND first_email_strategy != ''")
strategy_count = cursor.fetchone()[0]
print(f"\n📝 有首封开发信策略: {strategy_count} 条")

cursor.execute("SELECT COUNT(*) FROM p_company WHERE development_email IS NOT NULL AND development_email != ''")
email_count = cursor.fetchone()[0]
print(f"📧 有开发信内容: {email_count} 条")

cursor.execute("SELECT COUNT(*) FROM p_company WHERE follow_up_immediately IS NOT NULL AND follow_up_immediately != ''")
follow_up_count = cursor.fetchone()[0]
print(f"🔔 有立即跟进标记: {follow_up_count} 条")

cursor.execute("SELECT COUNT(*) FROM p_company WHERE supply_chain_pain_points IS NOT NULL AND supply_chain_pain_points != ''")
pain_count = cursor.fetchone()[0]
print(f"🎯 有供应链痛点: {pain_count} 条")

cursor.execute("""
SELECT company_name, lead_score, lead_grade, first_email_strategy, recommended_channels
FROM p_company 
WHERE first_email_strategy IS NOT NULL
ORDER BY lead_score DESC
LIMIT 5
""")
results = cursor.fetchall()

print("\n🏆 高评分客户及开发策略:")
print("-" * 80)
for row in results:
    print(f"\n公司: {row[0]}")
    print(f"评分: {row[1]} | 等级: {row[2]}")
    print(f"开发策略: {row[3][:80]}..." if len(row[3]) > 80 else f"开发策略: {row[3]}")
    print(f"推荐渠道: {row[4]}")

cursor.execute("""
SELECT company_name, development_email
FROM p_company 
WHERE development_email IS NOT NULL AND development_email != ''
ORDER BY lead_score DESC
LIMIT 2
""")
results = cursor.fetchall()

print("\n📧 开发信内容示例:")
print("-" * 80)
for row in results:
    print(f"\n公司: {row[0]}")
    print(f"开发信预览:\n{row[1][:150]}...")

cursor.execute("""
SELECT COUNT(*) FROM p_company WHERE 
    quality_requirement IS NOT NULL AND quality_requirement != '' AND
    price_sensitivity IS NOT NULL AND price_sensitivity != '' AND
    delivery_requirement IS NOT NULL AND delivery_requirement != '' AND
    recommended_products IS NOT NULL AND recommended_products != ''
""")
full_analysis = cursor.fetchone()[0]
print(f"\n📋 完整分析字段的客户: {full_analysis} 条")

conn.close()

print("\n🎉 数据验证完成！")
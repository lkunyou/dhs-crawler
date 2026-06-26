import pymysql
import re

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
SELECT id, company_name, main_products, main_market, annual_revenue_usd, purchase_potential
FROM p_company 
WHERE quality_requirement IS NULL OR quality_requirement = ''
ORDER BY lead_score DESC
""")

customers = cursor.fetchall()

print(f"需要生成分析字段的客户数量: {len(customers)}")
print("-" * 60)

def generate_analysis(company_name, main_products, main_market, revenue, purchase_potential):
    quality = "OEM级别质量标准；UV耐候性；高温高湿环境适应性；表面处理工艺（喷漆/电镀/ABS注塑）"
    price = "中高"
    delivery = "快" if revenue and revenue > 5000000 else "中"
    accept_china = "是"
    customization = "强" if "定制" in str(main_products) or "改装" in str(main_products) else "中"
    after_sales = "无缺陷政策；质量追溯；退换货；技术指导"
    
    pain_points = "日本原厂成本高；需要更多替代供应商；多车型SKU管理"
    
    recommended = []
    if "后视镜" in str(main_products):
        recommended.append("后视镜总成/壳/底座")
    if "柱饰板" in str(main_products) or "立柱" in str(main_products):
        recommended.append("A/B/C/D柱饰板")
    if "行李架" in str(main_products):
        recommended.append("行李架系统")
    if "雾灯" in str(main_products) or "格栅" in str(main_products):
        recommended.append("雾灯罩/格栅")
    if "尾翼" in str(main_products) or "扰流板" in str(main_products):
        recommended.append("尾翼/扰流板")
    if "保险杠" in str(main_products):
        recommended.append("保险杠")
    if "内饰" in str(main_products):
        recommended.append("内饰装饰件")
    
    if not recommended:
        recommended = ["后视镜总成、车身外饰件、格栅、雾灯罩"]
    
    channels = "Email"
    if "出口" in str(main_market):
        channels = "Email + LinkedIn"
    
    return {
        'quality_requirement': quality,
        'price_sensitivity': price,
        'delivery_requirement': delivery,
        'accept_china_factory': accept_china,
        'customization_ability': customization,
        'after_sales_requirement': after_sales,
        'supply_chain_pain_points': pain_points,
        'recommended_products': ', '.join(recommended),
        'recommended_channels': channels
    }

updated_count = 0

for customer in customers:
    company_id = customer[0]
    company_name = customer[1]
    main_products = customer[2]
    main_market = customer[3]
    revenue = customer[4]
    purchase_potential = customer[5]
    
    analysis = generate_analysis(company_name, main_products, main_market, revenue, purchase_potential)
    
    sql = """
UPDATE p_company SET 
    quality_requirement = %s,
    price_sensitivity = %s,
    delivery_requirement = %s,
    accept_china_factory = %s,
    customization_ability = %s,
    after_sales_requirement = %s,
    supply_chain_pain_points = %s,
    recommended_products = %s,
    recommended_channels = %s
WHERE id = %s
    """
    
    cursor.execute(sql, (
        analysis['quality_requirement'],
        analysis['price_sensitivity'],
        analysis['delivery_requirement'],
        analysis['accept_china_factory'],
        analysis['customization_ability'],
        analysis['after_sales_requirement'],
        analysis['supply_chain_pain_points'],
        analysis['recommended_products'],
        analysis['recommended_channels'],
        company_id
    ))
    
    updated_count += 1
    if updated_count % 10 == 0:
        print(f"已更新 {updated_count} 条...")

conn.commit()
print(f"\n✅ 成功更新 {updated_count} 条客户的分析字段")

cursor.execute("SELECT COUNT(*) FROM p_company WHERE quality_requirement IS NOT NULL AND quality_requirement != ''")
total = cursor.fetchone()[0]
print(f"\n📊 当前有分析字段的客户总数: {total} 条")

cursor.execute("""
SELECT company_name, quality_requirement, recommended_products
FROM p_company 
WHERE lead_grade IN ('S', 'A') AND (quality_requirement IS NULL OR quality_requirement = '')
ORDER BY lead_score DESC
""")
results = cursor.fetchall()
print(f"\n⚠️ 高质量客户中分析字段为空的数量: {len(results)}")

conn.close()

print("\n🎉 分析字段生成完成！")
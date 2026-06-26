import pymysql
import re

DB_HOST = '8.163.58.109'
DB_PORT = 3306
DB_USER = 'thai_auto_parts_crm'
DB_PASSWORD = 'tDdY8NX2xJ6HpdHz'
DB_NAME = 'thai_auto_parts_crm'

def connect_db():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset='utf8mb4'
    )

def parse_report(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    customers = {}
    customer_blocks = re.findall(r'【客户 \d+: (.*?)】(.*?)(?=\n【客户 \d+:|$)', content, re.DOTALL)
    
    for name, block in customer_blocks:
        company_name = name.strip()
        if company_name not in customers:
            customers[company_name] = {}
        
        data = {}
        lines = block.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('质量要求:'):
                data['quality_requirement'] = line.replace('质量要求:', '').strip()
            
            elif line.startswith('价格敏感度:'):
                data['price_sensitivity'] = line.replace('价格敏感度:', '').strip()
            
            elif line.startswith('交期要求:'):
                data['delivery_requirement'] = line.replace('交期要求:', '').strip()
            
            elif line.startswith('接受中国工厂:'):
                data['accept_china_factory'] = line.replace('接受中国工厂:', '').strip()
            
            elif line.startswith('定制能力需求:'):
                data['customization_ability'] = line.replace('定制能力需求:', '').strip()
            
            elif line.startswith('售后要求:'):
                data['after_sales_requirement'] = line.replace('售后要求:', '').strip()
            
            elif line.startswith('供应链痛点:'):
                data['supply_chain_pain_points'] = line.replace('供应链痛点:', '').strip()
            
            elif line.startswith('推荐切入产品:'):
                data['recommended_products'] = line.replace('推荐切入产品:', '').strip()
            
            elif line.startswith('推荐渠道:'):
                data['recommended_channels'] = line.replace('推荐渠道:', '').strip()
        
        customers[company_name] = data
    
    return customers

def import_analysis(conn, report_customers):
    cursor = conn.cursor()
    
    updated_count = 0
    
    for company_name, analysis_data in report_customers.items():
        cursor.execute("SELECT id FROM p_company WHERE company_name = %s", (company_name,))
        result = cursor.fetchone()
        
        if result:
            company_id = result[0]
            
            cursor.execute("SELECT quality_requirement FROM p_company WHERE id = %s", (company_id,))
            existing = cursor.fetchone()[0]
            
            if not existing or existing == '':
                update_fields = []
                update_values = []
                
                fields_map = {
                    'quality_requirement': 'quality_requirement',
                    'price_sensitivity': 'price_sensitivity',
                    'delivery_requirement': 'delivery_requirement',
                    'accept_china_factory': 'accept_china_factory',
                    'customization_ability': 'customization_ability',
                    'after_sales_requirement': 'after_sales_requirement',
                    'supply_chain_pain_points': 'supply_chain_pain_points',
                    'recommended_products': 'recommended_products',
                    'recommended_channels': 'recommended_channels'
                }
                
                for key, db_field in fields_map.items():
                    if key in analysis_data and analysis_data[key]:
                        update_fields.append(f"{db_field} = %s")
                        update_values.append(analysis_data[key])
                
                if update_fields:
                    update_values.append(company_id)
                    sql = f"UPDATE p_company SET {', '.join(update_fields)} WHERE id = %s"
                    cursor.execute(sql, update_values)
                    updated_count += 1
                    print(f"✓ 更新分析字段: {company_name}")
    
    conn.commit()
    cursor.close()
    return updated_count

def verify_data(conn):
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM p_company WHERE quality_requirement IS NOT NULL AND quality_requirement != ''")
    analysis_count = cursor.fetchone()[0]
    print(f"\n📋 有分析字段记录的客户: {analysis_count} 条")
    
    cursor.execute("""
SELECT company_name, quality_requirement
FROM p_company 
WHERE lead_grade IN ('S', 'A') AND (quality_requirement IS NULL OR quality_requirement = '')
ORDER BY lead_score DESC
""")
    results = cursor.fetchall()
    print(f"\n⚠️ 高质量客户中分析字段为空的数量: {len(results)}")
    if results:
        for row in results:
            print(f"  - {row[0]}")
    
    cursor.close()

if __name__ == '__main__':
    print("=" * 60)
    print("导入报告中的分析字段到客户表")
    print("=" * 60)
    
    file_path = r'E:\09.document\carparts\泰国汽车配件客户分析报告.txt'
    
    report_customers = parse_report(file_path)
    print(f"解析到 {len(report_customers)} 家客户的分析数据")
    
    conn = connect_db()
    print("✅ 数据库连接成功")
    
    updated = import_analysis(conn, report_customers)
    print(f"\n✅ 更新了 {updated} 条客户的分析字段")
    
    verify_data(conn)
    conn.close()
    
    print("\n🎉 分析字段导入完成！")
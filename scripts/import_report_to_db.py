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
    
    customers = []
    customer_blocks = re.findall(r'【客户 \d+: (.*?)】(.*?)(?=\n【客户 \d+:|$)', content, re.DOTALL)
    
    for name, block in customer_blocks:
        company_name = name.strip()
        
        data = {}
        lines = block.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('等级:'):
                parts = line.split('|')
                data['lead_grade'] = parts[0].replace('等级:', '').strip()
                if len(parts) > 1:
                    data['lead_score'] = int(parts[1].replace('评分:', '').strip())
            
            elif line.startswith('官网:'):
                data['website'] = line.replace('官网:', '').strip()
            
            elif line.startswith('地址:'):
                data['address'] = line.replace('地址:', '').strip()
            
            elif line.startswith('电话:'):
                data['phone'] = line.replace('电话:', '').strip()
            
            elif line.startswith('邮箱:'):
                data['email'] = line.replace('邮箱:', '').strip()
            
            elif line.startswith('主营产品:'):
                data['main_products'] = line.replace('主营产品:', '').strip()
            
            elif line.startswith('销售市场:'):
                data['main_market'] = line.replace('销售市场:', '').strip()
            
            elif line.startswith('质量要求:'):
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
        
        data['company_name'] = company_name
        customers.append(data)
    
    return customers

def update_customers(conn, customers):
    cursor = conn.cursor()
    
    updated_count = 0
    inserted_count = 0
    
    for customer in customers:
        company_name = customer['company_name']
        
        cursor.execute("SELECT id FROM p_company WHERE company_name = %s", (company_name,))
        result = cursor.fetchone()
        
        if result:
            company_id = result[0]
            
            update_fields = []
            update_values = []
            
            fields_map = {
                'website': 'website',
                'address': 'address',
                'phone': 'phone',
                'email': 'email',
                'main_products': 'main_products',
                'main_market': 'main_market',
                'lead_score': 'lead_score',
                'lead_grade': 'lead_grade',
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
                if key in customer and customer[key]:
                    update_fields.append(f"{db_field} = %s")
                    update_values.append(customer[key])
            
            if update_fields:
                update_values.append(company_id)
                sql = f"UPDATE p_company SET {', '.join(update_fields)} WHERE id = %s"
                cursor.execute(sql, update_values)
                updated_count += 1
                print(f"✓ 更新: {company_name}")
        
        else:
            insert_fields = ['company_name', 'country', 'status', 'source', 'is_auto_parts_core', 'is_importer_distributor']
            insert_values = [company_name, 'Thailand', 'New', 'Manual', 1, 1]
            
            fields_map = {
                'website': 'website',
                'address': 'address',
                'phone': 'phone',
                'email': 'email',
                'main_products': 'main_products',
                'main_market': 'main_market',
                'lead_score': 'lead_score',
                'lead_grade': 'lead_grade',
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
                if key in customer and customer[key]:
                    insert_fields.append(db_field)
                    insert_values.append(customer[key])
            
            placeholders = ', '.join(['%s'] * len(insert_values))
            sql = f"INSERT INTO p_company ({', '.join(insert_fields)}) VALUES ({placeholders})"
            cursor.execute(sql, insert_values)
            inserted_count += 1
            print(f"✓ 新增: {company_name}")
    
    conn.commit()
    cursor.close()
    
    return updated_count, inserted_count

def verify_data(conn):
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM p_company")
    total = cursor.fetchone()[0]
    print(f"\n📊 数据库中共有 {total} 条客户记录")
    
    cursor.execute("SELECT lead_grade, COUNT(*) FROM p_company GROUP BY lead_grade")
    grades = cursor.fetchall()
    print("\n客户等级分布:")
    for grade, count in grades:
        print(f"  {grade}: {count} 条")
    
    cursor.execute("SELECT COUNT(*) FROM p_company WHERE quality_requirement IS NOT NULL AND quality_requirement != ''")
    qual_count = cursor.fetchone()[0]
    print(f"\n有质量要求记录的客户: {qual_count} 条")
    
    cursor.execute("SELECT COUNT(*) FROM p_company WHERE recommended_products IS NOT NULL AND recommended_products != ''")
    rec_count = cursor.fetchone()[0]
    print(f"有推荐产品记录的客户: {rec_count} 条")
    
    cursor.close()

if __name__ == '__main__':
    print("=" * 60)
    print("从报告文件导入客户数据到数据库")
    print("=" * 60)
    
    file_path = r'E:\09.document\carparts\泰国汽车配件客户分析报告.txt'
    
    customers = parse_report(file_path)
    print(f"解析到 {len(customers)} 家客户")
    
    conn = connect_db()
    print("✅ 数据库连接成功")
    
    updated, inserted = update_customers(conn, customers)
    
    print(f"\n✅ 更新完成")
    print(f"  更新记录: {updated} 条")
    print(f"  新增记录: {inserted} 条")
    
    verify_data(conn)
    conn.close()
    
    print("\n🎉 全部完成！")
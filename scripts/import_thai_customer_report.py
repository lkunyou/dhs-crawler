# -*- coding: utf-8 -*-
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

def parse_phone(phone_str):
    if not phone_str:
        return None
    phone_str = str(phone_str).strip()
    if phone_str in ['-', '待确认', '未提供', '网站询盘', '网站/业务邮箱', '客户服务热线', '客户服务', '业务联系', '业务联系邮箱', '***']:
        return None
    phone_str = phone_str.replace(' ', '')
    if phone_str.startswith('+66'):
        return phone_str
    if phone_str.startswith('0') and len(phone_str) >= 9:
        return '+66' + phone_str[1:]
    return phone_str

def parse_email(email_str):
    if not email_str:
        return None
    email_str = str(email_str).strip()
    if email_str in ['-', '待确认', '未提供', '网站询盘系统', '客户服务热线', '客户服务', '业务联系', '业务联系邮箱']:
        return None
    if '@' in email_str:
        email = re.search(r'[\w.-]+@[\w.-]+\.\w+', email_str)
        if email:
            return email.group(0)
    return None

def parse_company_type(main_products):
    if not main_products:
        return 'Other'
    main_products = str(main_products).lower()
    if '制造商' in main_products or 'manufacturer' in main_products:
        return 'Manufacturer'
    if '进口' in main_products or 'importer' in main_products:
        return 'Importer'
    if '经销' in main_products or 'distributor' in main_products or '批发' in main_products or '贸易' in main_products:
        return 'Distributor'
    if '零售' in main_products or 'retail' in main_products:
        return 'Retailer'
    return 'Importer'

def parse_boolean(value):
    if not value:
        return None
    value = str(value).strip()
    if value == '是':
        return True
    if value == '否':
        return False
    return None

def parse_accept_china_factory(value):
    if not value:
        return 'Unknown'
    value = str(value).strip()
    if value == '是':
        return '是'
    if value == '否':
        return '否'
    return 'Unknown'

def parse_customization_ability(value):
    if not value:
        return '中'
    value = str(value).strip()
    if value == '强':
        return '强'
    if value == '中':
        return '中'
    if value == '弱':
        return '弱'
    return '中'

def parse_price_sensitivity(value):
    if not value:
        return '中'
    value = str(value).strip()
    if value == '高':
        return '高'
    if value == '极高':
        return '极高'
    if value == '中':
        return '中'
    if value == '低':
        return '低'
    return '中'

def parse_delivery_requirement(value):
    if not value:
        return '中'
    value = str(value).strip()
    if value == '快':
        return '快'
    if value == '中':
        return '中'
    return '中'

def parse_score(value):
    if not value:
        return None
    try:
        return int(value)
    except:
        return None

def parse_report(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    customers = []
    customer_sections = re.findall(r'【客户\s*(\d+):\s*(.+?)】\s*(.*?)(?=【客户|====================================================================================================|报告结束)', content, re.DOTALL)
    
    for idx, name, details in customer_sections:
        company = {
            'company_name': name.strip(),
            'country': 'Thailand',
            'lead_score': None,
            'lead_grade': 'C',
            'website': None,
            'address': None,
            'phone': None,
            'email': None,
            'main_products': None,
            'main_market': None,
            'quality_requirement': None,
            'price_sensitivity': None,
            'delivery_requirement': None,
            'accept_china_factory': None,
            'customization_ability': None,
            'after_sales_requirement': None,
            'supply_chain_pain_points': None,
            'recommended_products': None,
            'recommended_channels': None,
            'source': 'Manual'
        }
        
        lines = details.strip().split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if line.startswith('等级:'):
                match = re.search(r'等级:\s*(\w)', line)
                if match:
                    company['lead_grade'] = match.group(1)
            elif line.startswith('评分:'):
                match = re.search(r'评分:\s*(\d+)', line)
                if match:
                    company['lead_score'] = int(match.group(1))
            elif line.startswith('官网:'):
                company['website'] = line.replace('官网:', '').strip()
                if company['website'] == '博客/社交媒体为主':
                    company['website'] = None
            elif line.startswith('地址:'):
                company['address'] = line.replace('地址:', '').strip()
                if '待查' in company['address']:
                    company['address'] = None
            elif line.startswith('电话:'):
                phone_part = line.replace('电话:', '').strip()
                company['phone'] = parse_phone(phone_part)
            elif line.startswith('邮箱:'):
                email_part = line.replace('邮箱:', '').strip()
                company['email'] = parse_email(email_part)
            elif line.startswith('主营产品:'):
                company['main_products'] = line.replace('主营产品:', '').strip()[:500]
            elif line.startswith('销售市场:'):
                company['main_market'] = line.replace('销售市场:', '').strip()[:200]
            elif line.startswith('质量要求:'):
                company['quality_requirement'] = line.replace('质量要求:', '').strip()[:500]
            elif line.startswith('价格敏感度:'):
                company['price_sensitivity'] = parse_price_sensitivity(line.replace('价格敏感度:', '').strip())
            elif line.startswith('交期要求:'):
                company['delivery_requirement'] = parse_delivery_requirement(line.replace('交期要求:', '').strip())
            elif line.startswith('接受中国工厂:'):
                company['accept_china_factory'] = parse_accept_china_factory(line.replace('接受中国工厂:', '').strip())
            elif line.startswith('定制能力需求:'):
                company['customization_ability'] = parse_customization_ability(line.replace('定制能力需求:', '').strip())
            elif line.startswith('售后要求:'):
                company['after_sales_requirement'] = line.replace('售后要求:', '').strip()[:500]
            elif line.startswith('供应链痛点:'):
                company['supply_chain_pain_points'] = line.replace('供应链痛点:', '').strip()[:500]
            elif line.startswith('推荐切入产品:'):
                company['recommended_products'] = line.replace('推荐切入产品:', '').strip()[:500]
            elif line.startswith('推荐渠道:'):
                company['recommended_channels'] = line.replace('推荐渠道:', '').strip()[:100]
        
        company['company_type'] = parse_company_type(company['main_products'])
        
        if company['company_name'] == '鼎和盛公司':
            company['country'] = 'China'
        
        customers.append(company)
    
    return customers

def import_to_db(customers):
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        for company in customers:
            cursor.execute("SELECT id FROM p_company WHERE company_name = %s LIMIT 1", (company['company_name'],))
            existing = cursor.fetchone()
            
            if existing:
                print(f"已存在: {company['company_name']}")
                update_sql = """
                    UPDATE p_company SET 
                        company_type = %s, 
                        website = %s, 
                        address = %s, 
                        phone = %s, 
                        email = %s, 
                        lead_score = %s, 
                        lead_grade = %s, 
                        main_products = %s, 
                        main_market = %s, 
                        quality_requirement = %s, 
                        price_sensitivity = %s, 
                        delivery_requirement = %s, 
                        accept_china_factory = %s, 
                        customization_ability = %s, 
                        after_sales_requirement = %s, 
                        supply_chain_pain_points = %s, 
                        recommended_products = %s, 
                        recommended_channels = %s,
                        source = %s,
                        country = %s
                    WHERE id = %s
                """
                cursor.execute(update_sql, (
                    company['company_type'],
                    company['website'],
                    company['address'],
                    company['phone'],
                    company['email'],
                    company['lead_score'],
                    company['lead_grade'],
                    company['main_products'],
                    company['main_market'],
                    company['quality_requirement'],
                    company['price_sensitivity'],
                    company['delivery_requirement'],
                    company['accept_china_factory'],
                    company['customization_ability'],
                    company['after_sales_requirement'],
                    company['supply_chain_pain_points'],
                    company['recommended_products'],
                    company['recommended_channels'],
                    company['source'],
                    company['country'],
                    existing[0]
                ))
                print(f"更新成功: {company['company_name']}")
            else:
                insert_sql = """
                    INSERT INTO p_company (
                        company_name, company_type, website, address, phone, email,
                        lead_score, lead_grade, main_products, main_market,
                        quality_requirement, price_sensitivity, delivery_requirement,
                        accept_china_factory, customization_ability, after_sales_requirement,
                        supply_chain_pain_points, recommended_products, recommended_channels,
                        source, country, status
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_sql, (
                    company['company_name'],
                    company['company_type'],
                    company['website'],
                    company['address'],
                    company['phone'],
                    company['email'],
                    company['lead_score'],
                    company['lead_grade'],
                    company['main_products'],
                    company['main_market'],
                    company['quality_requirement'],
                    company['price_sensitivity'],
                    company['delivery_requirement'],
                    company['accept_china_factory'],
                    company['customization_ability'],
                    company['after_sales_requirement'],
                    company['supply_chain_pain_points'],
                    company['recommended_products'],
                    company['recommended_channels'],
                    company['source'],
                    company['country'],
                    'New'
                ))
                print(f"插入成功: {company['company_name']}")
        
        conn.commit()
        print(f"\n完成！共处理 {len(customers)} 家公司")
        
    except Exception as e:
        conn.rollback()
        print(f"错误: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    file_path = r'E:\09.document\carparts\客户资料\泰国汽车配件客户分析报告.txt'
    customers = parse_report(file_path)
    print(f"解析到 {len(customers)} 家公司")
    import_to_db(customers)
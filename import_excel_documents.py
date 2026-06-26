# -*- coding: utf-8 -*-
import pymysql
import pandas as pd
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

def parse_priority_to_grade(priority):
    if priority is None or pd.isna(priority):
        return 'C'
    priority = str(priority).strip()
    if priority == 'A' or '★★★★★' in priority or '极高' in priority:
        return 'A'
    if priority == 'B' or '★★★★' in priority or '高' in priority:
        return 'B'
    if priority == 'C' or '★★★' in priority or '中等' in priority:
        return 'C'
    if '★★' in priority or '低' in priority or '一般' in priority:
        return 'C'
    return 'C'

def parse_company_type(type_str):
    if type_str is None or pd.isna(type_str):
        return 'Other'
    type_str = str(type_str).strip().lower()
    if 'manufacturer' in type_str or '制造商' in type_str:
        return 'Manufacturer'
    if 'importer' in type_str or '进口商' in type_str:
        return 'Importer'
    if 'distributor' in type_str or '经销商' in type_str or '批发商' in type_str or '批发' in type_str or '贸易' in type_str:
        return 'Distributor'
    if 'retail' in type_str or '零售商' in type_str:
        return 'Retailer'
    if 'oem' in type_str:
        return 'OEM'
    return 'Other'

def parse_phone(phone_str):
    if phone_str is None or pd.isna(phone_str):
        return None
    phone_str = str(phone_str).strip()
    if phone_str in ['-', '待确认', '未提供', '网站询盘', 'nan']:
        return None
    phone_str = phone_str.replace(' ', '')
    if phone_str.startswith('+66'):
        return phone_str
    if phone_str.startswith('0') and len(phone_str) >= 9:
        return '+66' + phone_str[1:]
    return phone_str

def parse_email(email_str):
    if email_str is None or pd.isna(email_str):
        return None
    email_str = str(email_str).strip()
    if email_str in ['-', '待确认', '未提供', '网站询盘系统', 'nan']:
        return None
    if '@' in email_str:
        return email_str
    return None

def parse_revenue(revenue_str):
    if revenue_str is None or pd.isna(revenue_str):
        return None
    revenue_str = str(revenue_str).strip()
    match = re.search(r'(\d[\d,]*)\s*(万?)', revenue_str)
    if match:
        num = float(match.group(1).replace(',', ''))
        if match.group(2) == '万':
            return num * 10000
        return num
    return None

def parse_website(url):
    if url is None or pd.isna(url):
        return None
    url = str(url).strip()
    if url in ['-', 'nan']:
        return None
    if not url.startswith('http'):
        return 'https://' + url
    return url

def parse_full_excel():
    df = pd.read_excel(r'E:\09.document\carparts\客户资料\泰国汽车配件客户开发清单_完整版.xlsx')
    companies = []
    
    for _, row in df.iterrows():
        company_name = row.get('公司名称')
        if company_name is None or pd.isna(company_name):
            continue
        
        contact_col = row.get('核心联系人/邮箱', '')
        email = None
        core_contact = None
        
        if contact_col and not pd.isna(contact_col):
            contact_str = str(contact_col)
            if '@' in contact_str:
                email_match = re.search(r'([\w.-]+@[\w.-]+\.\w+)', contact_str)
                if email_match:
                    email = email_match.group(1)
                    core_contact = contact_str.replace(email, '').strip()[:200]
                else:
                    core_contact = contact_str[:200]
            else:
                core_contact = contact_str[:200]
        
        company = {
            'company_name': str(company_name).strip(),
            'website': parse_website(row.get('官网')),
            'address': str(row.get('地址')).strip() if row.get('地址') and not pd.isna(row.get('地址')) else None,
            'phone': parse_phone(row.get('联系电话')),
            'email': email,
            'core_contact': core_contact,
            'company_type': parse_company_type(row.get('公司类型')),
            'main_products': str(row.get('主营产品')).strip()[:500] if row.get('主营产品') and not pd.isna(row.get('主营产品')) else None,
            'main_market': str(row.get('主要销售市场')).strip()[:200] if row.get('主要销售市场') and not pd.isna(row.get('主要销售市场')) else None,
            'lead_score': int(row.get('总评分')) if row.get('总评分') and not pd.isna(row.get('总评分')) else 60,
            'lead_grade': parse_priority_to_grade(row.get('开发优先级')),
            'purchase_potential': str(row.get('采购潜力')).strip() if row.get('采购潜力') and not pd.isna(row.get('采购潜力')) else None,
            'import_ability': int(row.get('进口能力(0-25)')) if row.get('进口能力(0-25)') and not pd.isna(row.get('进口能力(0-25)')) else 0,
            'purchase_scale': int(row.get('采购规模(0-25)')) if row.get('采购规模(0-25)') and not pd.isna(row.get('采购规模(0-25)')) else 0,
            'china_supplier_acceptance': int(row.get('中国供应商接受度(0-20)')) if row.get('中国供应商接受度(0-20)') and not pd.isna(row.get('中国供应商接受度(0-20)')) else 0,
            'oem_aftermarket_match': int(row.get('OEM/Aftermarket匹配度(0-15)')) if row.get('OEM/Aftermarket匹配度(0-15)') and not pd.isna(row.get('OEM/Aftermarket匹配度(0-15)')) else 0,
            'export_ability': int(row.get('出口能力(0-10)')) if row.get('出口能力(0-10)') and not pd.isna(row.get('出口能力(0-10)')) else 0,
            'customization_match': int(row.get('定制需求匹配度(0-5)')) if row.get('定制需求匹配度(0-5)') and not pd.isna(row.get('定制需求匹配度(0-5)')) else 0,
            'quality_requirement': str(row.get('质量要求')).strip()[:100] if row.get('质量要求') and not pd.isna(row.get('质量要求')) else None,
            'price_sensitivity': str(row.get('价格敏感度')).strip()[:100] if row.get('价格敏感度') and not pd.isna(row.get('价格敏感度')) else None,
            'delivery_requirement': str(row.get('交期要求')).strip()[:100] if row.get('交期要求') and not pd.isna(row.get('交期要求')) else None,
            'accept_china_factory': str(row.get('接受中国工厂')).strip() if row.get('接受中国工厂') and not pd.isna(row.get('接受中国工厂')) else None,
            'customization_ability': str(row.get('定制能力需求')).strip()[:200] if row.get('定制能力需求') and not pd.isna(row.get('定制能力需求')) else None,
            'after_sales_requirement': str(row.get('售后要求')).strip()[:200] if row.get('售后要求') and not pd.isna(row.get('售后要求')) else None,
            'supply_chain_pain_points': str(row.get('当前供应链痛点')).strip()[:500] if row.get('当前供应链痛点') and not pd.isna(row.get('当前供应链痛点')) else None,
            'recommended_products': str(row.get('推荐切入产品')).strip()[:500] if row.get('推荐切入产品') and not pd.isna(row.get('推荐切入产品')) else None,
            'recommended_channels': str(row.get('推荐渠道')).strip()[:200] if row.get('推荐渠道') and not pd.isna(row.get('推荐渠道')) else None,
            'first_email_strategy': str(row.get('首封开发信策略')).strip()[:500] if row.get('首封开发信策略') and not pd.isna(row.get('首封开发信策略')) else None,
            'development_email': str(row.get('开发信(英文)')).strip() if row.get('开发信(英文)') and not pd.isna(row.get('开发信(英文)')) else None,
            'country': 'Thailand',
            'source': 'Industry_Directory',
            'source_url': '泰国汽车配件客户开发清单_完整版.xlsx',
            'is_auto_parts_core': 1,
            'is_importer_distributor': 1 if 'Importer' in str(row.get('公司类型')) or '进口商' in str(row.get('公司类型')) or 'Distributor' in str(row.get('公司类型')) or '经销商' in str(row.get('公司类型')) else 0
        }
        companies.append(company)
    
    return companies

def parse_kehu_excel():
    df = pd.read_excel(r'E:\09.document\carparts\客户资料\客户资料.xlsx')
    companies = []
    
    for _, row in df.iterrows():
        company_name = row.get('公司全称')
        if company_name is None or pd.isna(company_name):
            continue
        
        company = {
            'company_name': str(company_name).strip(),
            'website': parse_website(row.get('官网')),
            'address': str(row.get('详细地址')).strip() if row.get('详细地址') and not pd.isna(row.get('详细地址')) else None,
            'phone': parse_phone(row.get('联系电话')),
            'core_contact': str(row.get('核心联系人')).strip()[:200] if row.get('核心联系人') and not pd.isna(row.get('核心联系人')) else None,
            'main_products': str(row.get('主营匹配产品')).strip()[:500] if row.get('主营匹配产品') and not pd.isna(row.get('主营匹配产品')) else None,
            'main_market': str(row.get('核心销售市场')).strip()[:200] if row.get('核心销售市场') and not pd.isna(row.get('核心销售市场')) else None,
            'annual_revenue_usd': parse_revenue(row.get('年营收 USD')),
            'purchase_potential': str(row.get('采购潜力')).strip() if row.get('采购潜力') and not pd.isna(row.get('采购潜力')) else None,
            'lead_grade': parse_priority_to_grade(row.get('开发优先级')),
            'lead_score': parse_priority_to_score(row.get('开发优先级')),
            'country': 'Thailand',
            'source': 'Industry_Directory',
            'source_url': '客户资料.xlsx',
            'is_auto_parts_core': 1,
            'is_importer_distributor': 1
        }
        companies.append(company)
    
    return companies

def parse_priority_to_score(priority):
    grade = parse_priority_to_grade(priority)
    if grade == 'A':
        return 90
    if grade == 'B':
        return 75
    return 60

def parse_thai_companies_excel():
    df = pd.read_excel(r'E:\09.document\carparts\客户资料\thailand_auto_parts_companies.xlsx')
    companies = []
    
    for _, row in df.iterrows():
        company_name = row.get('name')
        if company_name is None or pd.isna(company_name):
            continue
        
        company = {
            'company_name': str(company_name).strip(),
            'company_type': parse_company_type(row.get('category')),
            'address': str(row.get('address')).strip() if row.get('address') and not pd.isna(row.get('address')) else None,
            'phone': parse_phone(row.get('phone')),
            'email': parse_email(row.get('email')),
            'website': parse_website(row.get('website')),
            'main_products': str(row.get('description')).strip()[:500] if row.get('description') and not pd.isna(row.get('description')) else None,
            'country': 'Thailand',
            'source': 'Industry_Directory',
            'source_url': 'thailand_auto_parts_companies.xlsx',
            'is_auto_parts_core': 1,
            'is_importer_distributor': 1 if 'Wholesale' in str(row.get('category')) or 'Importer' in str(row.get('category')) else 0
        }
        companies.append(company)
    
    return companies

def deduplicate_companies(companies):
    seen = set()
    unique = []
    for company in companies:
        name = company['company_name'].strip().lower().replace(' ', '')
        if name not in seen:
            seen.add(name)
            unique.append(company)
    return unique

def import_companies(conn, companies):
    cursor = conn.cursor()
    
    insert_sql = """
    INSERT INTO p_company (
        company_name, website, address, phone, email,
        company_type, main_products, main_market,
        lead_score, lead_grade, core_contact,
        annual_revenue_usd, purchase_potential,
        import_ability, purchase_scale, china_supplier_acceptance,
        oem_aftermarket_match, export_ability, customization_match,
        quality_requirement, price_sensitivity, delivery_requirement,
        accept_china_factory, customization_ability, after_sales_requirement,
        supply_chain_pain_points, recommended_products, recommended_channels,
        first_email_strategy, development_email,
        country, status, source, source_url,
        is_auto_parts_core, is_importer_distributor
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        website = IFNULL(VALUES(website), website),
        address = IFNULL(VALUES(address), address),
        phone = IFNULL(VALUES(phone), phone),
        email = IFNULL(VALUES(email), email),
        company_type = IFNULL(VALUES(company_type), company_type),
        main_products = IFNULL(VALUES(main_products), main_products),
        main_market = IFNULL(VALUES(main_market), main_market),
        lead_score = GREATEST(VALUES(lead_score), lead_score),
        lead_grade = CASE WHEN VALUES(lead_score) > lead_score THEN VALUES(lead_grade) ELSE lead_grade END,
        core_contact = IFNULL(VALUES(core_contact), core_contact),
        annual_revenue_usd = IFNULL(VALUES(annual_revenue_usd), annual_revenue_usd),
        purchase_potential = IFNULL(VALUES(purchase_potential), purchase_potential),
        import_ability = IFNULL(VALUES(import_ability), import_ability),
        purchase_scale = IFNULL(VALUES(purchase_scale), purchase_scale),
        china_supplier_acceptance = IFNULL(VALUES(china_supplier_acceptance), china_supplier_acceptance),
        oem_aftermarket_match = IFNULL(VALUES(oem_aftermarket_match), oem_aftermarket_match),
        export_ability = IFNULL(VALUES(export_ability), export_ability),
        customization_match = IFNULL(VALUES(customization_match), customization_match),
        quality_requirement = IFNULL(VALUES(quality_requirement), quality_requirement),
        price_sensitivity = IFNULL(VALUES(price_sensitivity), price_sensitivity),
        delivery_requirement = IFNULL(VALUES(delivery_requirement), delivery_requirement),
        accept_china_factory = IFNULL(VALUES(accept_china_factory), accept_china_factory),
        customization_ability = IFNULL(VALUES(customization_ability), customization_ability),
        after_sales_requirement = IFNULL(VALUES(after_sales_requirement), after_sales_requirement),
        supply_chain_pain_points = IFNULL(VALUES(supply_chain_pain_points), supply_chain_pain_points),
        recommended_products = IFNULL(VALUES(recommended_products), recommended_products),
        recommended_channels = IFNULL(VALUES(recommended_channels), recommended_channels),
        first_email_strategy = IFNULL(VALUES(first_email_strategy), first_email_strategy),
        development_email = IFNULL(VALUES(development_email), development_email),
        source_url = CONCAT_WS('; ', source_url, VALUES(source_url)),
        updated_at = CURRENT_TIMESTAMP
    """
    
    inserted = 0
    updated = 0
    
    for company in companies:
        try:
            cursor.execute(insert_sql, (
                company.get('company_name'),
                company.get('website'),
                company.get('address'),
                company.get('phone'),
                company.get('email'),
                company.get('company_type', 'Other'),
                company.get('main_products'),
                company.get('main_market'),
                company.get('lead_score', 60),
                company.get('lead_grade', 'C'),
                company.get('core_contact'),
                company.get('annual_revenue_usd'),
                company.get('purchase_potential'),
                company.get('import_ability', 0),
                company.get('purchase_scale', 0),
                company.get('china_supplier_acceptance', 0),
                company.get('oem_aftermarket_match', 0),
                company.get('export_ability', 0),
                company.get('customization_match', 0),
                company.get('quality_requirement'),
                company.get('price_sensitivity'),
                company.get('delivery_requirement'),
                company.get('accept_china_factory'),
                company.get('customization_ability'),
                company.get('after_sales_requirement'),
                company.get('supply_chain_pain_points'),
                company.get('recommended_products'),
                company.get('recommended_channels'),
                company.get('first_email_strategy'),
                company.get('development_email'),
                company.get('country', 'Thailand'),
                'New',
                company.get('source', 'Industry_Directory'),
                company.get('source_url', ''),
                company.get('is_auto_parts_core', 1),
                company.get('is_importer_distributor', 0)
            ))
            if cursor.rowcount == 1:
                inserted += 1
            else:
                updated += 1
        except Exception as e:
            print(f"  ❌ 导入失败 [{company.get('company_name')}]: {e}")
    
    conn.commit()
    cursor.close()
    return inserted, updated

def verify_data(conn):
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM p_company")
    total = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT lead_grade, COUNT(*) as cnt 
        FROM p_company 
        GROUP BY lead_grade 
        ORDER BY FIELD(lead_grade, 'S', 'A', 'B', 'C')
    """)
    grade_dist = cursor.fetchall()
    
    cursor.execute("""
        SELECT company_type, COUNT(*) as cnt 
        FROM p_company 
        GROUP BY company_type
    """)
    type_dist = cursor.fetchall()
    
    cursor.execute("""
        SELECT company_name, lead_grade, lead_score, main_products 
        FROM p_company 
        ORDER BY lead_score DESC 
        LIMIT 20
    """)
    top_companies = cursor.fetchall()
    
    cursor.close()
    return total, grade_dist, type_dist, top_companies

if __name__ == '__main__':
    print("=" * 70)
    print("从Excel文件导入公司数据到数据库")
    print("=" * 70)
    
    print("\n📥 正在解析各Excel文件数据...")
    
    full_data = parse_full_excel()
    print(f"   泰国汽车配件客户开发清单_完整版.xlsx: {len(full_data)} 条")
    
    kehu_data = parse_kehu_excel()
    print(f"   客户资料.xlsx: {len(kehu_data)} 条")
    
    thai_data = parse_thai_companies_excel()
    print(f"   thailand_auto_parts_companies.xlsx: {len(thai_data)} 条")
    
    all_data = full_data + kehu_data + thai_data
    print(f"\n📊 原始数据总数: {len(all_data)} 条")
    
    all_data = deduplicate_companies(all_data)
    print(f"✅ 去重后数据总数: {len(all_data)} 条")
    
    try:
        conn = connect_db()
        print("✅ 数据库连接成功")
        
        print("\n🚀 正在导入数据...")
        inserted, updated = import_companies(conn, all_data)
        
        print(f"\n✅ 导入完成")
        print(f"   新增: {inserted} 条")
        print(f"   更新: {updated} 条")
        
        total, grade_dist, type_dist, top_companies = verify_data(conn)
        
        print(f"\n📊 数据库中共有 {total} 条客户记录")
        
        print("\n📈 客户等级分布:")
        for grade, cnt in grade_dist:
            print(f"  {grade}: {cnt} 条")
        
        print("\n📈 公司类型分布:")
        for comp_type, cnt in type_dist:
            print(f"  {comp_type}: {cnt} 条")
        
        print("\n🏆 顶级客户（按评分排序）:")
        print("-" * 80)
        print(f"{'公司名称':<35} {'等级':<4} {'评分':<6} {'主营产品':<40}")
        print("-" * 80)
        for row in top_companies:
            print(f"{row[0][:35]:<35} {row[1]:<4} {row[2]:<6} {row[3][:40]:<40}")
        
        conn.close()
        print("\n🎉 所有Excel数据导入完成！")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
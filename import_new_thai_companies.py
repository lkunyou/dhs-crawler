import pymysql

DB_HOST = '8.163.58.109'
DB_PORT = 3306
DB_USER = 'thai_auto_parts_crm'
DB_PASSWORD = 'tDdY8NX2xJ6HpdHz'
DB_NAME = 'thai_auto_parts_crm'

companies_data = [
    {
        'company_name': 'CNC Multiventures Co., Ltd.',
        'website': 'https://thailand-autoparts.com/en',
        'address': 'Nakhon Pathom',
        'phone': '+66 99 442 9456',
        'email': None,
        'core_contact': 'WhatsApp/电话联系人',
        'main_products': 'OEM/Aftermarket汽车配件及车身件（外饰/内饰）',
        'main_market': '出口/贸易',
        'company_type_cn': '贸易公司/进口商',
        'purchase_potential': '中高',
        'development_priority': 'B',
        'notes': '偏贸易进口，适合做外饰/内饰定制与批量供货；重点问交期与售后索赔流程',
        'revenue_usd': 1500,
        'company_size': '中型'
    },
    {
        'company_name': 'Rich Trade Co., Ltd.',
        'website': 'https://www.japanesecartrade.com/richtrade/',
        'address': 'Bangkok',
        'phone': None,
        'email': None,
        'core_contact': '询盘表单联系人',
        'main_products': '汽车配件/用于进口贸易（外饰/内饰）',
        'main_market': '多国家进口',
        'company_type_cn': '贸易公司/进口商',
        'purchase_potential': '中',
        'development_priority': 'C',
        'notes': '适合做试单与MOQ测试；重点用样件+报价阶梯拿到首单',
        'revenue_usd': 800,
        'company_size': '小型'
    },
    {
        'company_name': 'PTAP Intertrade Co., Ltd.',
        'website': 'https://ptapintertrade.com/',
        'address': 'Bangkok',
        'phone': '+66 89 4545444',
        'email': None,
        'core_contact': '销售/询盘联系人',
        'main_products': 'Genuine/OEM/REM汽车配件（外饰/内饰）',
        'main_market': '国际市场',
        'company_type_cn': '贸易公司/进口商',
        'purchase_potential': '中高',
        'development_priority': 'B',
        'notes': '更可能接受工厂供货与质量文件；重点给耐候/安装一致性资料',
        'revenue_usd': 1800,
        'company_size': '中型'
    }
]

def connect_db():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset='utf8mb4'
    )

def parse_company_type(type_cn):
    if '制造商' in type_cn:
        return 'Manufacturer'
    if '进口商' in type_cn:
        return 'Importer'
    if '贸易' in type_cn or '经销商' in type_cn or '分销商' in type_cn:
        return 'Distributor'
    if '零售商' in type_cn:
        return 'Retailer'
    return 'Other'

def parse_employee_count(size_cn):
    if size_cn == '大型':
        return '500+'
    if size_cn == '中型':
        return '100-500'
    if size_cn == '小型':
        return '1-100'
    return '-'

def calc_lead_score(priority):
    if priority == 'A':
        return 90
    if priority == 'B':
        return 75
    if priority == 'C':
        return 60
    return 50

def import_companies(conn):
    cursor = conn.cursor()
    
    inserted_count = 0
    updated_count = 0
    
    for company in companies_data:
        company_name = company['company_name']
        
        cursor.execute("SELECT id FROM p_company WHERE company_name = %s", (company_name,))
        existing = cursor.fetchone()
        
        company_type_en = parse_company_type(company['company_type_cn'])
        employee_count = parse_employee_count(company['company_size'])
        lead_score = calc_lead_score(company['development_priority'])
        
        if company['main_market'] in ['出口/贸易', '国际市场', '多国家进口']:
            export_ability = 18
            import_ability = 24
            purchase_scale = 22
        else:
            export_ability = 10
            import_ability = 18
            purchase_scale = 18
        
        china_supplier_acceptance = 20
        oem_aftermarket_match = 18
        customization_match = 8
        
        if existing:
            company_id = existing[0]
            
            update_sql = """
UPDATE p_company SET 
    website = IFNULL(%s, website),
    address = IFNULL(%s, address),
    phone = IFNULL(%s, phone),
    email = IFNULL(%s, email),
    company_type = %s,
    main_products = IFNULL(%s, main_products),
    main_market = IFNULL(%s, main_market),
    lead_score = %s,
    lead_grade = %s,
    core_contact = IFNULL(%s, core_contact),
    import_ability = %s,
    purchase_scale = %s,
    china_supplier_acceptance = %s,
    oem_aftermarket_match = %s,
    export_ability = %s,
    customization_match = %s,
    employee_count = %s,
    annual_revenue_usd = %s,
    purchase_potential = %s,
    development_priority = %s,
    notes = %s,
    status = 'New',
    source = 'Industry_Directory',
    source_url = 'https://thailand-autoparts.com/ / https://www.japanesecartrade.com/ / https://ptapintertrade.com/',
    is_auto_parts_core = 1,
    is_importer_distributor = 1
WHERE id = %s
            """
            
            cursor.execute(update_sql, (
                company['website'], company['address'], company['phone'], company['email'],
                company_type_en, company['main_products'], company['main_market'],
                lead_score, company['development_priority'],
                company['core_contact'],
                import_ability, purchase_scale, china_supplier_acceptance,
                oem_aftermarket_match, export_ability, customization_match,
                employee_count,
                company['revenue_usd'] * 10000,
                company['purchase_potential'],
                company['development_priority'],
                company['notes'],
                company_id
            ))
            updated_count += 1
        
        else:
            insert_sql = """
INSERT INTO p_company (
    company_name, website, address, phone, email,
    company_type, main_products, main_market,
    lead_score, lead_grade,
    core_contact,
    import_ability, purchase_scale, china_supplier_acceptance,
    oem_aftermarket_match, export_ability, customization_match,
    employee_count, annual_revenue_usd,
    purchase_potential, development_priority, notes,
    country, status, source, source_url,
    is_auto_parts_core, is_importer_distributor
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_sql, (
                company_name, company['website'], company['address'], company['phone'], company['email'],
                company_type_en, company['main_products'], company['main_market'],
                lead_score, company['development_priority'],
                company['core_contact'],
                import_ability, purchase_scale, china_supplier_acceptance,
                oem_aftermarket_match, export_ability, customization_match,
                employee_count,
                company['revenue_usd'] * 10000,
                company['purchase_potential'],
                company['development_priority'],
                company['notes'],
                'Thailand', 'New', 'Industry_Directory', 'https://thailand-autoparts.com/ / https://www.japanesecartrade.com/ / https://ptapintertrade.com/',
                1, 1
            ))
            inserted_count += 1
    
    conn.commit()
    print(f"\n✅ 共处理 {inserted_count + updated_count} 条客户数据")
    print(f"   新增: {inserted_count} 条")
    print(f"   更新: {updated_count} 条")
    cursor.close()

def verify_data(conn):
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as total FROM p_company")
    total = cursor.fetchone()[0]
    print(f"\n📊 数据库中共有 {total} 条客户记录")
    
    cursor.execute("""
SELECT company_name, website, phone, main_products, lead_grade, purchase_potential, notes
FROM p_company 
WHERE company_name IN ('CNC Multiventures Co., Ltd.', 'Rich Trade Co., Ltd.', 'PTAP Intertrade Co., Ltd.')
ORDER BY lead_grade
""")
    results = cursor.fetchall()
    print("\n📋 新导入客户详情:")
    print("-" * 100)
    print(f"{'公司名称':<30} {'等级':<4} {'采购潜力':<6} {'主营产品':<40}")
    print("-" * 100)
    for row in results:
        print(f"{row[0][:30]:<30} {row[4]:<4} {row[5]:<6} {row[3][:40]:<40}")
    
    cursor.close()

if __name__ == '__main__':
    print("=" * 60)
    print("导入新泰国汽车配件公司到数据库")
    print("=" * 60)
    print(f"📥 待导入公司数量: {len(companies_data)}")
    
    try:
        conn = connect_db()
        print("✅ 数据库连接成功")
        
        import_companies(conn)
        verify_data(conn)
        
        conn.close()
        print("\n🎉 客户数据导入完成！")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
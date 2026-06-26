import pymysql

DB_HOST = '8.163.58.109'
DB_PORT = 3306
DB_USER = 'thai_auto_parts_crm'
DB_PASSWORD = 'tDdY8NX2xJ6HpdHz'
DB_NAME = 'thai_auto_parts_crm'

companies_data = [
    {'company_name': 'SCL Motor Part Co., Ltd', 'company_type': 'Distributor', 'lead_grade': 'A', 'website': 'https://www.sclmotorpart.com', 'phone': '+66-2-xxx-xxxx', 'email': 'info@sclmotorpart.com', 'address': 'Bangkok', 'core_contact': 'Purchasing Manager', 'main_products': 'engine parts, chassis', 'main_market': 'Thailand', 'lead_score': 98, 'notes': 'Top distributor'},
    {'company_name': 'DENSO Sales (Thailand) Co., Ltd', 'company_type': 'OEM/Distributor', 'lead_grade': 'A', 'website': 'https://www.denso.com', 'phone': '+66-2-xxx-xxxx', 'email': 'contact@denso.com', 'address': 'Bangkok', 'core_contact': 'Procurement Manager', 'main_products': 'filters, ignition, AC', 'main_market': 'Thailand', 'lead_score': 99, 'notes': 'Tier1 supplier'},
    {'company_name': 'Toyota Tsusho (Thailand)', 'company_type': 'Trading/Distributor', 'lead_grade': 'A', 'website': 'https://www.toyota-tsusho.com', 'phone': '+66-2-xxx-xxxx', 'email': 'info@toyota-tsusho.com', 'address': 'Bangkok', 'core_contact': 'Sourcing Manager', 'main_products': 'OEM parts', 'main_market': 'ASEAN', 'lead_score': 99, 'notes': 'Toyota supply chain'},
    {'company_name': 'Honda Trading Asia', 'company_type': 'OEM Distributor', 'lead_grade': 'A', 'website': 'https://www.honda.co.th', 'phone': '+66-2-xxx-xxxx', 'email': 'contact@honda.co.th', 'address': 'Bangkok', 'core_contact': 'Parts Manager', 'main_products': 'OEM parts', 'main_market': 'ASEAN', 'lead_score': 98, 'notes': 'OEM channel'},
    {'company_name': 'Isuzu Motors Thailand', 'company_type': 'OEM', 'lead_grade': 'A', 'website': 'https://www.isuzu.co.th', 'phone': '+66-2-xxx-xxxx', 'email': 'info@isuzu.co.th', 'address': 'Bangkok', 'core_contact': 'Procurement', 'main_products': 'truck parts', 'main_market': 'ASEAN', 'lead_score': 98, 'notes': 'Commercial vehicle'},
    {'company_name': 'AISIN Asia Thailand', 'company_type': 'Tier1', 'lead_grade': 'A', 'website': 'https://www.aisin.com', 'phone': '+66-2-xxx-xxxx', 'email': 'info@aisin.com', 'address': 'Samut Prakan', 'core_contact': 'Purchasing', 'main_products': 'drivetrain', 'main_market': 'ASEAN', 'lead_score': 97, 'notes': 'OEM supplier'},
    {'company_name': 'Robert Bosch Thailand', 'company_type': 'Distributor', 'lead_grade': 'A', 'website': 'https://www.bosch.co.th', 'phone': '+66-2-xxx-xxxx', 'email': 'contact@bosch.com', 'address': 'Bangkok', 'core_contact': 'Category Manager', 'main_products': 'brake, filter', 'main_market': 'Thailand', 'lead_score': 98, 'notes': 'strong aftermarket'},
    {'company_name': 'YonMing Auto Thailand', 'company_type': 'Wholesaler', 'lead_grade': 'B', 'website': '-', 'phone': '+66-2-xxx-xxxx', 'email': 'sales@yonming.co.th', 'address': 'Bangkok', 'core_contact': 'Sales Manager', 'main_products': 'truck parts', 'main_market': 'Thailand', 'lead_score': 85, 'notes': ''},
    {'company_name': 'Bangkok Auto Parts Co., Ltd', 'company_type': 'Wholesaler', 'lead_grade': 'B', 'website': '-', 'phone': '+66-2-xxx-xxxx', 'email': 'info@bangkokautoparts.co.th', 'address': 'Bangkok', 'core_contact': 'Procurement', 'main_products': 'suspension, body parts', 'main_market': 'Thailand', 'lead_score': 83, 'notes': ''},
    {'company_name': 'Chin Seng Huat Auto Parts', 'company_type': 'Importer', 'lead_grade': 'B', 'website': '-', 'phone': '+66-2-xxx-xxxx', 'email': 'info@cshauto.co.th', 'address': 'Bangkok', 'core_contact': 'Buyer', 'main_products': 'Japanese car parts', 'main_market': 'Thailand', 'lead_score': 84, 'notes': ''},
    {'company_name': 'Vichien Auto Parts', 'company_type': 'Wholesaler', 'lead_grade': 'B', 'website': '-', 'phone': '+66-2-xxx-xxxx', 'email': 'info@vichienauto.co.th', 'address': 'Bangkok', 'core_contact': 'Owner', 'main_products': 'used parts', 'main_market': 'Thailand', 'lead_score': 80, 'notes': ''},
    {'company_name': 'Bangkok Unity Auto Parts', 'company_type': 'Distributor', 'lead_grade': 'B', 'website': '-', 'phone': '+66-2-xxx-xxxx', 'email': 'sales@buauto.co.th', 'address': 'Bangkok', 'core_contact': 'Purchasing', 'main_products': 'aftermarket parts', 'main_market': 'Thailand', 'lead_score': 82, 'notes': ''},
    {'company_name': 'Chavalit Auto Part LP', 'company_type': 'Wholesaler', 'lead_grade': 'C', 'website': 'yellowpages', 'phone': '+66-2-xxx-xxxx', 'email': 'chavalit@gmail.com', 'address': 'Bangkok', 'core_contact': 'Owner', 'main_products': 'mixed parts', 'main_market': 'Bangkok', 'lead_score': 75, 'notes': ''},
    {'company_name': 'Tani Part Co., Ltd', 'company_type': 'Wholesaler', 'lead_grade': 'C', 'website': 'yellowpages', 'phone': '+66-2-xxx-xxxx', 'email': 'tanipart@gmail.com', 'address': 'Bangkok', 'core_contact': 'Buyer', 'main_products': 'aftermarket', 'main_market': 'Bangkok', 'lead_score': 74, 'notes': ''},
    {'company_name': 'Central Auto Parts LP', 'company_type': 'Retail/Wholesaler', 'lead_grade': 'C', 'website': 'yellowpages', 'phone': '+66-2-xxx-xxxx', 'email': 'centralauto@gmail.com', 'address': 'Bangkok', 'core_contact': 'Manager', 'main_products': 'EU/Japan parts', 'main_market': 'Bangkok', 'lead_score': 73, 'notes': ''},
    {'company_name': 'Ek Chai Auto Parts', 'company_type': 'Wholesaler', 'lead_grade': 'C', 'website': 'yellowpages', 'phone': '+66-2-xxx-xxxx', 'email': 'ekchai@gmail.com', 'address': 'Bangkok', 'core_contact': 'Purchasing', 'main_products': 'full range parts', 'main_market': 'Bangkok', 'lead_score': 76, 'notes': ''},
    {'company_name': 'Kitti Yontr Spare Parts', 'company_type': 'Retail/Wholesale', 'lead_grade': 'C', 'website': 'yellowpages', 'phone': '+66-2-xxx-xxxx', 'email': 'kitti@gmail.com', 'address': 'Bangkok', 'core_contact': 'Owner', 'main_products': 'engine parts', 'main_market': 'Bangkok', 'lead_score': 72, 'notes': ''},
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

def parse_company_type(type_str):
    if 'OEM' in type_str:
        return 'OEM'
    if 'Importer' in type_str:
        return 'Importer'
    if 'Distributor' in type_str or 'Trading' in type_str:
        return 'Distributor'
    if 'Wholesaler' in type_str:
        return 'Distributor'
    if 'Retail' in type_str:
        return 'Retailer'
    if 'Tier1' in type_str:
        return 'OEM'
    return 'Distributor'

def import_companies(conn):
    cursor = conn.cursor()
    
    inserted_count = 0
    updated_count = 0
    
    for company in companies_data:
        company_name = company['company_name']
        
        cursor.execute("SELECT id FROM p_company WHERE company_name = %s", (company_name,))
        existing = cursor.fetchone()
        
        company_type_en = parse_company_type(company['company_type'])
        website = None if company['website'] == '-' else company['website']
        
        if 'ASEAN' in company['main_market']:
            export_ability = 9
            import_ability = 25
            purchase_scale = 25
        else:
            export_ability = 5
            import_ability = 20
            purchase_scale = 20
        
        china_supplier_acceptance = 18
        oem_aftermarket_match = 14
        customization_match = 4
        
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
    status = 'New',
    source = 'Manual',
    is_auto_parts_core = 1,
    is_importer_distributor = %s
WHERE id = %s
            """
            
            is_importer = 1 if 'Importer' in company['company_type'] or 'Distributor' in company['company_type'] or 'Trading' in company['company_type'] else 0
            
            cursor.execute(update_sql, (
                website, company['address'], company['phone'], company['email'],
                company_type_en, company['main_products'], company['main_market'],
                company['lead_score'], company['lead_grade'],
                company['core_contact'],
                import_ability, purchase_scale, china_supplier_acceptance,
                oem_aftermarket_match, export_ability, customization_match,
                is_importer,
                company_id
            ))
            updated_count += 1
        
        else:
            is_importer = 1 if 'Importer' in company['company_type'] or 'Distributor' in company['company_type'] or 'Trading' in company['company_type'] else 0
            
            insert_sql = """
INSERT INTO p_company (
    company_name, website, address, phone, email,
    company_type, main_products, main_market,
    lead_score, lead_grade,
    core_contact,
    import_ability, purchase_scale, china_supplier_acceptance,
    oem_aftermarket_match, export_ability, customization_match,
    country, status, source,
    is_auto_parts_core, is_importer_distributor
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_sql, (
                company_name, website, company['address'], company['phone'], company['email'],
                company_type_en, company['main_products'], company['main_market'],
                company['lead_score'], company['lead_grade'],
                company['core_contact'],
                import_ability, purchase_scale, china_supplier_acceptance,
                oem_aftermarket_match, export_ability, customization_match,
                'Thailand', 'New', 'Manual',
                1, is_importer
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
    
    cursor.execute("SELECT lead_grade, COUNT(*) as count FROM p_company GROUP BY lead_grade ORDER BY lead_grade")
    grades = cursor.fetchall()
    print("\n📈 客户等级分布:")
    for grade, count in grades:
        print(f"  {grade}: {count} 条")
    
    cursor.execute("""
SELECT company_name, lead_score, lead_grade, company_type, core_contact
FROM p_company 
WHERE lead_score >= 95
ORDER BY lead_score DESC
""")
    results = cursor.fetchall()
    print(f"\n🏆 顶级客户（评分>=95）:")
    for row in results:
        print(f"  {row[0][:40]:<40} | 评分: {row[1]:<3} | 等级: {row[2]} | 类型: {row[3]} | 联系人: {row[4]}")
    
    cursor.close()

if __name__ == '__main__':
    print("=" * 60)
    print("导入新公司列表到数据库")
    print("=" * 60)
    
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
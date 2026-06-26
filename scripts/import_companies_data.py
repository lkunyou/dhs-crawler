import pymysql

DB_HOST = '8.163.58.109'
DB_PORT = 3306
DB_USER = 'thai_auto_parts_crm'
DB_PASSWORD = 'tDdY8NX2xJ6HpdHz'
DB_NAME = 'thai_auto_parts_crm'

companies_data = [
    {"company_name": "PTAP Intertrade Co., Ltd.", "website": "ptapintertrade.com", "address": "Bangkok", "phone": "+66 89 4545444", "core_contact": "Sales Team", "main_products": "Genuine/OEM/REM spare parts", "company_type": "Distributor/Importer", "purchase_potential": "高"},
    {"company_name": "CNC Multiventures Co., Ltd.", "website": "thailand-autoparts.com", "address": "Nakhon Pathom", "phone": "+66 994429456", "core_contact": "Export Manager", "main_products": "Genuine/OEM/Aftermarket parts", "company_type": "Distributor/Exporter", "purchase_potential": "高"},
    {"company_name": "Siam Motors Parts Co., Ltd.", "website": "", "address": "Bangkok", "phone": "", "core_contact": "", "main_products": "Auto body parts", "company_type": "Distributor", "purchase_potential": "中"},
    {"company_name": "Thai Summit Group", "website": "thaisummitgroup.com", "address": "Bangkok", "phone": "", "core_contact": "", "main_products": "Automotive parts manufacturing", "company_type": "Manufacturer/OEM", "purchase_potential": "很高"},
    {"company_name": "AAPICO Hitech Public Co., Ltd.", "website": "aapico.com", "address": "Bangkok", "phone": "", "core_contact": "", "main_products": "Stamped parts, die-casting", "company_type": "Manufacturer", "purchase_potential": "很高"},
    {"company_name": "Bangkok Autopart Co., Ltd.", "website": "", "address": "Bangkok", "phone": "", "core_contact": "", "main_products": "Auto spare parts distribution", "company_type": "Distributor", "purchase_potential": "中"},
    {"company_name": "SCL Motor Part Public Co., Ltd.", "website": "sclmotor.com", "address": "Bangkok", "phone": "02-2261909", "core_contact": "", "main_products": "Motor parts", "company_type": "Distributor", "purchase_potential": "中"},
    {"company_name": "President Automobile Industries Public Co., Ltd.", "website": "paco.co.th", "address": "Bangkok", "phone": "02-810-9900", "core_contact": "Mr. Tanest Lenkajomkitti", "main_products": "Auto air-conditioning parts", "company_type": "Manufacturer/Distributor", "purchase_potential": "中"},
    {"company_name": "Fortune Parts Industry Public Co., Ltd.", "website": "koolearn.com", "address": "Bangkok", "phone": "02-993-4970", "core_contact": "Ms. Natiita Klinchan", "main_products": "Body parts (bumper, grille, panel)", "company_type": "Manufacturer/Distributor", "purchase_potential": "中高"},
    {"company_name": "Pro Automotive Corporation Co., Ltd.", "website": "proautomotive.co.th", "address": "Bangkok", "phone": "", "core_contact": "", "main_products": "Automotive distribution", "company_type": "Distributor", "purchase_potential": "中"},
    {"company_name": "Pro Part Distributor Co., Ltd.", "website": "propartdistributor.com", "address": "Bangkok", "phone": "02-225-5620", "core_contact": "Ms. Pitchada Tangchua", "main_products": "Filters, clutch kit, shock absorber", "company_type": "Distributor", "purchase_potential": "中"},
    {"company_name": "Premier Multipart Co., Ltd.", "website": "premiermultipart.com", "address": "Bangkok", "phone": "02-789-4565", "core_contact": "Mr. Krit Previousatrul", "main_products": "Engine mounting, suspension parts", "company_type": "Distributor", "purchase_potential": "中"},
    {"company_name": "Prime Standard Manufacturing Co., Ltd.", "website": "prime-standard.com", "address": "Bangkok", "phone": "", "core_contact": "Ms. Preswwanit Lettsajornkitl", "main_products": "Automotive rubber parts", "company_type": "Manufacturer/Distributor", "purchase_potential": "中"},
    {"company_name": "Sri Thai Thana Auto Parts Co., Ltd.", "website": "stautopart.com", "address": "Samut Prakan", "phone": "035-361-306", "core_contact": "Ms. Punnadar Asavalapnirundon", "main_products": "Auto body spare parts (pickup trucks)", "company_type": "Manufacturer/Distributor", "purchase_potential": "中"},
    {"company_name": "Unicom Auto Parts Co., Ltd.", "website": "unicomthailand.com", "address": "Bangkok", "phone": "", "core_contact": "Mr. Ashley Thita", "main_products": "Rubber suspension parts", "company_type": "Manufacturer/Distributor", "purchase_potential": "中"},
    {"company_name": "Rubber Intertrade Co., Ltd.", "website": "rbi.co.th", "address": "Bangkok", "phone": "02-752-0643", "core_contact": "Ms. Thipawan Karunkam", "main_products": "Automotive rubber parts", "company_type": "Manufacturer", "purchase_potential": "中"},
    {"company_name": "S.B.-Cera Co., Ltd.", "website": "sb-cera.co.th", "address": "Samut Prakan", "phone": "034-406-699", "core_contact": "Mr. Yongut Techathamikomol", "main_products": "Suspension parts (ball joint, tie rod)", "company_type": "Manufacturer/Distributor", "purchase_potential": "中"},
    {"company_name": "Goodrubber International Co., Ltd.", "website": "goodrubberthailand.com", "address": "Bangkok", "phone": "02-808-5212", "core_contact": "Mr. Paiboon Supasanya", "main_products": "Rubber parts", "company_type": "Manufacturer", "purchase_potential": "中"},
    {"company_name": "Imperial Cable Industry Co., Ltd.", "website": "imperialcable.co.th", "address": "Bangkok", "phone": "02-810-2437", "core_contact": "Mr. Saokhai", "main_products": "Automotive control cables", "company_type": "Manufacturer", "purchase_potential": "中"},
    {"company_name": "Pioneer Engineering International Co., Ltd.", "website": "explorenshox.com", "address": "Bangkok", "phone": "082-960-4440", "core_contact": "Mr. Xensfaye Anayan", "main_products": "Shock absorbers, 4x4 accessories", "company_type": "Distributor", "purchase_potential": "中"},
]

def parse_company_type(type_str):
    if not type_str:
        return 'Other'
    type_str = type_str.strip()
    if 'Manufacturer' in type_str:
        return 'Manufacturer'
    elif 'OEM' in type_str:
        return 'OEM'
    elif 'Importer' in type_str:
        return 'Importer'
    elif 'Distributor' in type_str:
        return 'Distributor'
    elif 'Exporter' in type_str:
        return 'Distributor'
    return 'Distributor'

def parse_purchase_potential(potential):
    map_dict = {'很高': '极高', '高': '高', '中高': '高', '中': '中', '低': '低'}
    return map_dict.get(potential, '中')

def get_lead_score(potential):
    map_dict = {'很高': 85, '高': 70, '中高': 65, '中': 50, '低': 30}
    return map_dict.get(potential, 50)

def get_lead_grade(potential):
    map_dict = {'很高': 'S', '高': 'A', '中高': 'A', '中': 'B', '低': 'C'}
    return map_dict.get(potential, 'B')

def connect_db():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset='utf8mb4'
    )

def import_companies(conn):
    cursor = conn.cursor()
    
    inserted_count = 0
    skipped_count = 0
    
    for idx, company in enumerate(companies_data, 1):
        company_name = company['company_name']
        website = company['website']
        address = company['address']
        phone = company['phone']
        core_contact = company['core_contact']
        main_products = company['main_products']
        company_type_str = company['company_type']
        purchase_potential = company['purchase_potential']
        
        if website and not website.startswith('http'):
            website = 'https://' + website
        
        company_type = parse_company_type(company_type_str)
        purchase_potential_norm = parse_purchase_potential(purchase_potential)
        lead_score = get_lead_score(purchase_potential)
        lead_grade = get_lead_grade(purchase_potential)
        
        city = address
        
        is_importer_distributor = 1 if company_type in ['Importer', 'Distributor'] else 0
        
        cursor.execute("SELECT id FROM p_company WHERE company_name = %s", (company_name,))
        existing = cursor.fetchone()
        
        if existing:
            print(f"⚠️  跳过重复 ({idx}): {company_name}")
            skipped_count += 1
            continue
        
        try:
            sql = """
INSERT INTO p_company (
    company_name, company_name_en, website, address, city, phone,
    company_type, main_products, core_contact,
    purchase_potential, lead_score, lead_grade,
    country, status, source,
    is_auto_parts_core, is_importer_distributor,
    import_ability, purchase_scale, china_supplier_acceptance,
    oem_aftermarket_match, export_ability, customization_match
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                company_name, company_name, website, address, city, phone,
                company_type, main_products, core_contact,
                purchase_potential_norm, lead_score, lead_grade,
                'Thailand', 'New', 'Manual',
                1, is_importer_distributor,
                20, 20 if purchase_potential in ['很高', '高', '中高'] else 15,
                18, 12, 5, 5
            )
            cursor.execute(sql, values)
            inserted_count += 1
            print(f"✅ 已导入 ({idx}): {company_name}")
            
            if inserted_count % 5 == 0:
                conn.commit()
                
        except Exception as e:
            print(f"❌ 导入失败 ({idx}): {company_name} - {e}")
            skipped_count += 1
    
    conn.commit()
    print(f"\n✅ 共导入 {inserted_count} 条客户数据")
    print(f"⚠️  跳过 {skipped_count} 条数据")
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
    
    cursor.execute("SELECT company_type, COUNT(*) as count FROM p_company GROUP BY company_type")
    types = cursor.fetchall()
    print("\n🏢 公司类型分布:")
    for ct, count in types:
        print(f"  {ct}: {count} 条")
    
    cursor.close()

if __name__ == '__main__':
    print("=" * 60)
    print("正在导入公司数据到客户表...")
    print("=" * 60)
    
    try:
        conn = connect_db()
        print("✅ 数据库连接成功")
        
        import_companies(conn)
        verify_data(conn)
        
        conn.close()
        print("\n🎉 公司数据导入完成！")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
import pymysql

DB_HOST = '8.163.58.109'
DB_PORT = 3306
DB_USER = 'thai_auto_parts_crm'
DB_PASSWORD = 'tDdY8NX2xJ6HpdHz'
DB_NAME = 'thai_auto_parts_crm'

SENDER_NAME = '佛山市鼎和盛汽车配件有限公司'
WEBSITE_URL = 'https://www.carparts-land.com/zh'

def connect_db():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset='utf8mb4'
    )

def add_columns(conn):
    cursor = conn.cursor()
    
    try:
        cursor.execute("ALTER TABLE p_company ADD COLUMN email_subject VARCHAR(255) AFTER development_email")
        print("✅ 已添加 email_subject 字段")
    except Exception as e:
        if 'Duplicate column' in str(e):
            print("⚠️  email_subject 字段已存在")
        else:
            raise e
    
    try:
        cursor.execute("ALTER TABLE p_company ADD COLUMN development_email_template TEXT AFTER email_subject")
        print("✅ 已添加 development_email_template 字段")
    except Exception as e:
        if 'Duplicate column' in str(e):
            print("⚠️  development_email_template 字段已存在")
        else:
            raise e
    
    conn.commit()
    cursor.close()

def get_products_keywords(products):
    keywords = []
    if not products:
        return keywords
    
    products = products.lower()
    
    keyword_mapping = {
        'body': ['body', 'bumper', 'grille', 'panel', 'door', 'fender', 'hood'],
        'engine': ['engine', 'mounting', 'filter', 'clutch', 'motor'],
        'suspension': ['suspension', 'shock', 'absorber', 'ball joint', 'tie rod', 'spring'],
        'rubber': ['rubber'],
        'ac': ['air-conditioning', 'air conditioning', 'ac'],
        'electrical': ['cable', 'wire', 'electrical', 'sensor'],
        'oem': ['oem'],
        'stamped': ['stamped', 'stamping'],
        'casting': ['casting', 'die-cast'],
        'aftermarket': ['aftermarket'],
        '4x4': ['4x4', 'accessory'],
    }
    
    for category, terms in keyword_mapping.items():
        for term in terms:
            if term in products:
                keywords.append(category)
                break
    
    return keywords if keywords else ['auto_parts']

def generate_email_subject(company_name, company_type, products):
    keywords = get_products_keywords(products)
    keyword_str = ', '.join(keywords[:2])
    
    company_type = company_type or ''
    if 'OEM' in company_type or 'Manufacturer' in company_type:
        return f"Quality {keyword_str} Supplier - {SENDER_NAME}"
    else:
        return f"Premium {keyword_str} Wholesale Supply - {SENDER_NAME}"

def generate_email_body(company_name, company_type, main_products, core_contact, website):
    keywords = get_products_keywords(main_products)
    
    greeting = f"Dear {core_contact}," if core_contact else "Dear Sir/Madam,"
    
    product_lines = {
        'body': "auto body parts including bumpers, grilles, panels, doors, fenders, hoods, and more",
        'engine': "engine components including engine mountings, filters, clutch kits, and motor parts",
        'suspension': "suspension parts including shock absorbers, ball joints, tie rods, and springs",
        'rubber': "automotive rubber parts including seals, gaskets, bushings, and vibration dampers",
        'ac': "auto air-conditioning parts including compressors, condensers, evaporators, and blower motors",
        'electrical': "automotive electrical parts including control cables, wiring harnesses, sensors, and switches",
        'oem': "OEM-grade automotive spare parts meeting original equipment manufacturer standards",
        'stamped': "precision stamped metal parts and assemblies for automotive applications",
        'casting': "die-casting and casting parts for engine and chassis components",
        'aftermarket': "high-quality aftermarket automotive parts for various vehicle models",
        '4x4': "4x4 accessories and off-road vehicle components",
        'auto_parts': "a wide range of automotive spare parts for various vehicle systems",
    }
    
    product_desc = product_lines.get(keywords[0], product_lines['auto_parts']) if keywords else product_lines['auto_parts']
    
    company_type = company_type or ''
    if 'OEM' in company_type or 'Manufacturer' in company_type:
        business_type = "manufacturing"
        specialization = "OEM manufacturing capabilities"
        advantage = "provide OEM services with competitive pricing"
    elif 'Importer' in company_type or 'Distributor' in company_type:
        business_type = "distributing"
        specialization = "wholesale distribution"
        advantage = "offer competitive wholesale prices and flexible MOQs"
    else:
        business_type = "supplying"
        specialization = "comprehensive automotive parts supply"
        advantage = "provide a complete range of auto parts"
    
    email_body = f"""{greeting}

We are writing to introduce {SENDER_NAME}, a leading China-based automotive parts manufacturer and exporter. With years of experience in {business_type}, we specialize in {product_desc}.

We understand that {company_name} is engaged in {main_products or 'automotive parts business'}. As a reliable partner, we can {advantage} for your {specialization}.

Our advantages include:
- Competitive pricing with direct factory supply
- High-quality products meeting international standards
- Flexible MOQ and fast delivery
- {specialization}

Please visit our website {WEBSITE_URL} to explore our full product catalog.

We would be delighted to discuss how we can support your business needs. Could you kindly share your current sourcing requirements or any specific products you are interested in?

Looking forward to your reply.

Best regards,
{SENDER_NAME}
{WEBSITE_URL}"""
    
    return email_body

def update_companies(conn):
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, company_name, company_type, main_products, core_contact, website 
        FROM p_company 
        WHERE email_subject IS NULL OR email_subject = ''
    """)
    
    companies = cursor.fetchall()
    print(f"\n需要更新 {len(companies)} 条记录")
    
    updated_count = 0
    for company in companies:
        id, company_name, company_type, main_products, core_contact, website = company
        
        try:
            subject = generate_email_subject(company_name, company_type, main_products)
            body = generate_email_body(company_name, company_type, main_products, core_contact, website)
            
            cursor.execute("""
                UPDATE p_company 
                SET email_subject = %s, development_email_template = %s
                WHERE id = %s
            """, (subject, body, id))
            
            updated_count += 1
            if updated_count % 20 == 0:
                conn.commit()
                print(f"已更新 {updated_count} 条记录...")
                
        except Exception as e:
            print(f"❌ 更新失败 (ID:{id}): {company_name} - {e}")
    
    conn.commit()
    print(f"\n✅ 共更新 {updated_count} 条记录")
    cursor.close()

def verify_update(conn):
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM p_company WHERE email_subject IS NOT NULL AND email_subject != ''")
    count_with_subject = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM p_company WHERE development_email_template IS NOT NULL AND development_email_template != ''")
    count_with_template = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT id, company_name, email_subject 
        FROM p_company 
        WHERE email_subject IS NOT NULL 
        LIMIT 5
    """)
    sample_data = cursor.fetchall()
    
    print(f"\n📊 验证结果:")
    print(f"  已设置邮件标题: {count_with_subject} 条")
    print(f"  已设置开发信模板: {count_with_template} 条")
    
    print("\n📝 示例数据:")
    for id, name, subject in sample_data:
        print(f"  ID:{id} | {name[:40]}...")
        print(f"     标题: {subject}")
    
    cursor.close()

if __name__ == '__main__':
    print("=" * 60)
    print("正在为 p_company 表添加邮件字段并生成开发信...")
    print("=" * 60)
    
    try:
        conn = connect_db()
        print("✅ 数据库连接成功")
        
        add_columns(conn)
        update_companies(conn)
        verify_update(conn)
        
        conn.close()
        print("\n🎉 邮件字段添加与开发信生成完成！")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
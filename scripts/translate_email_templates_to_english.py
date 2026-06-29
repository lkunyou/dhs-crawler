# -*- coding: utf-8 -*-
import pymysql

DB_HOST = '8.163.58.109'
DB_PORT = 3306
DB_USER = 'thai_auto_parts_crm'
DB_PASSWORD = 'tDdY8NX2xJ6HpdHz'
DB_NAME = 'thai_auto_parts_crm'

SENDER_COMPANY_EN = 'Foshan Dinghesheng Auto Parts Co., Ltd.'
SENDER_DOMAIN = 'https://www.carparts-land.com/'
SENDER_PHONE = '+86 180-7886-5445'
SENDER_EMAIL = 'market@carparts-land.com'

BLOCK_FOOTER = """Best regards,

Sales Team

Business Development Manager

Foshan Dinghesheng Auto Parts Co., Ltd.

market@carparts-land.com

+86 180-7886-5445

https://www.carparts-land.com/"""

def connect_db():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset='utf8mb4'
    )

def contains_chinese(text):
    if not text:
        return False
    for char in text:
        if '\u4e00' <= char <= '\u9fff':
            return True
    return False

PRODUCT_TRANSLATIONS = {
    '未提供': 'Not specified',
    '后视镜总成': 'mirror assemblies',
    '后视镜': 'mirrors',
    '车身外饰件': 'body exterior parts',
    '外饰件': 'exterior parts',
    '车身': 'body parts',
    '保险杠': 'bumpers',
    '格栅': 'grilles',
    '雾灯罩': 'fog lamp covers',
    '翼子板': 'fenders',
    '引擎盖': 'hoods',
    '车门': 'doors',
    '灯具': 'lighting',
    '大灯': 'headlights',
    '尾灯': 'taillights',
    '车身面板': 'body panels',
    '车身套件': 'body kits',
    '内翼子板': 'inner fenders',
    '中网格栅': 'front grilles',
    '后视镜壳': 'mirror housings',
    '行李架': 'roof racks',
    '侧裙': 'side skirts',
    '柱饰板': 'pillar trims',
    '发动机': 'engine parts',
    '传动': 'transmission parts',
    '悬挂': 'suspension parts',
    '电气': 'electrical parts',
    '底盘': 'chassis parts',
    '皮卡': 'pickup trucks',
    '乘用车': 'passenger vehicles',
    '商用车': 'commercial vehicles',
    '农机': 'agricultural machinery',
    '全品类配件': 'full range parts',
    '全车件': 'complete vehicle parts',
    '配件': 'parts',
    '零件': 'parts',
    '总成': 'assemblies',
    '空调': 'air conditioning',
    '润滑油': 'lubricants',
    '橡胶': 'rubber parts',
    '冲压件': 'stamped parts',
    '铸造件': 'casting parts',
    '售后件': 'aftermarket parts',
    '原装件': 'genuine parts',
    'OEM件': 'OEM parts',
    '及': ' and ',
    '、': ', ',
    '：': ': ',
    '等': 'etc.',
    '全': 'full',
    'SKU': 'SKU',
    '覆盖': 'coverage',
    '匹配度': 'matching degree',
    '质量': 'quality',
    '标准': 'standards',
    '出口': 'export',
    '供应': 'supply',
    '制造': 'manufacturing',
    '批发': 'wholesale',
    '进口': 'import',
    '分销': 'distribution',
    '销售': 'sales',
    '丰田': 'Toyota',
    'Hilux': 'Hilux',
    '4x4': '4x4',
    '三菱': 'Mitsubishi',
    '日欧': 'Japanese and European',
    '品牌': 'brands',
    '型号': 'models',
}

MARKET_TRANSLATIONS = {
    '未提供': 'Not specified',
    '泰国': 'Thailand',
    '东南亚': 'Southeast Asia',
    '中东': 'Middle East',
    '非洲': 'Africa',
    '南美': 'South America',
    '全球': 'global',
    '美国': 'USA',
    '迪拜': 'Dubai',
    '欧洲': 'Europe',
    '及': ' and ',
    '、': ', ',
}

QUALITY_TRANSLATIONS = {
    '标准': 'Standard quality requirements',
    'JIS/BS标准': 'JIS/BS standards',
    'OEM匹配度高': 'high OEM matching degree',
    'UV耐候': 'UV weather resistance',
    '高温高湿适应': 'high temperature and humidity resistance',
    '100%原厂件': '100% genuine parts',
    'OEM件': 'OEM parts',
    '可靠替代件': 'reliable alternative parts',
    '出口标准': 'export standards',
    'Aftermarket': 'Aftermarket quality',
    '出口品质': 'export quality',
    'OEM标准': 'OEM standards',
    'HTS 8708.29.90': 'HTS 8708.29.90 compliance',
    '高': 'High quality standards',
    '中': 'Medium quality standards',
    '低': 'Basic quality requirements',
}

PAIN_POINT_TRANSLATIONS = {
    '未提供': 'Not provided',
    '日本原厂成本高': 'High cost of Japanese original parts',
    '需要更多替代供应商': 'need more alternative suppliers',
    '多车型SKU管理': 'multi-model SKU management',
    '替代件供应链稳定性': 'supply chain stability for alternative parts',
    '多品牌覆盖': 'multi-brand coverage',
    '出口包装': 'export packaging',
    '需要持续低价供应商': 'need continuous low-cost suppliers',
    '出口美国需稳定供货': 'stable supply for US export',
    '多车型模具开发成本高': 'high mold development cost for multiple models',
    '成本高': 'high cost',
    '稳定性': 'stability',
    '管理': 'management',
    '开发': 'development',
    '配合': 'coordination',
    '物流': 'logistics',
    '一致性': 'consistency',
}

PRICE_SENSITIVITY_MAP = {
    '极高': 'Very High',
    '高': 'High',
    '中': 'Medium',
    '低': 'Low',
}

DELIVERY_REQUIREMENT_MAP = {
    '快': 'Fast',
    '中': 'Medium',
    '慢': 'Flexible',
}

CUSTOMIZATION_MAP = {
    '强': 'High',
    '中': 'Medium',
    '弱': 'Low',
}

ACCEPT_CHINA_MAP = {
    '是': 'Yes',
    '否': 'No',
    '待确认': 'Unknown',
}

AFTER_SALES_TRANSLATIONS = {
    '标准': 'Standard after-sales support',
    '无缺陷政策': 'zero defect policy',
    '质量追溯': 'quality traceability',
    '退换货': 'return and exchange',
    '技术指导': 'technical guidance',
    '100%原厂质保': '100% genuine warranty',
    '替代件质量保证': 'alternative parts quality guarantee',
    '出口文件支持': 'export documentation support',
    '大批量一致性': 'large batch consistency',
    '出口包装': 'export packaging',
    '物流配合': 'logistics coordination',
    '批次一致性': 'batch consistency',
    '质量追溯': 'quality traceability',
    '技术支持': 'technical support',
    '产品培训': 'product training',
}

COMPANY_TYPE_MAP = {
    '制造商': 'Manufacturer',
    'OEM': 'OEM Manufacturer',
    '进口商': 'Importer',
    '经销商': 'Distributor',
    '零售商': 'Retailer',
    '贸易商': 'Trader',
    '批发商': 'Wholesaler',
}

def translate_text(text, translations):
    if not text:
        return ''
    text = str(text).strip()
    if not contains_chinese(text):
        return text
    
    result = text
    for chinese, english in translations.items():
        if chinese in result:
            result = result.replace(chinese, english)
    
    if contains_chinese(result):
        result = result.replace('；', '. ')
        result = result.replace('，', ', ')
        result = result.replace('。', '. ')
    
    return result.strip()

def translate_main_products(products):
    return translate_text(products, PRODUCT_TRANSLATIONS)

def translate_market(market):
    return translate_text(market, MARKET_TRANSLATIONS)

def translate_quality(requirement):
    return translate_text(requirement, QUALITY_TRANSLATIONS)

def translate_pain_points(pain_points):
    return translate_text(pain_points, PAIN_POINT_TRANSLATIONS)

def translate_recommended_products(products):
    return translate_text(products, PRODUCT_TRANSLATIONS)

def translate_after_sales(requirement):
    return translate_text(requirement, AFTER_SALES_TRANSLATIONS)

def build_pain_point_section(pain_points):
    if not pain_points or pain_points.strip() == 'None' or pain_points.strip() == 'nan' or pain_points.strip() == 'Not provided':
        return ''
    pain_points = pain_points.strip()
    return f"\nWe've analyzed the supply chain landscape and understand {pain_points}. Our solutions are specifically designed to address these challenges effectively.\n"

def build_quality_section(quality_requirement):
    if not quality_requirement or quality_requirement.strip() == 'None' or quality_requirement.strip() == 'nan':
        return ''
    if 'High' in quality_requirement or 'high' in quality_requirement:
        return "\n🔹 OEM-grade quality with IATF 16949 certification\n"
    elif 'Medium' in quality_requirement or 'medium' in quality_requirement:
        return "\n🔹 Consistent quality with ISO 9001 standards\n"
    else:
        return "\n🔹 Reliable quality at competitive pricing\n"

def build_price_section(price_sensitivity):
    if not price_sensitivity or price_sensitivity.strip() == 'None' or price_sensitivity.strip() == 'nan':
        return ''
    if price_sensitivity == 'Very High' or price_sensitivity == 'High':
        return "\n✅ 30-40% cost reduction vs. Japanese/European suppliers\n"
    elif price_sensitivity == 'Medium':
        return "\n✅ Competitive pricing with volume discounts\n"
    else:
        return "\n✅ Premium quality at fair market prices\n"

def build_delivery_section(delivery_requirement):
    if not delivery_requirement or delivery_requirement.strip() == 'None' or delivery_requirement.strip() == 'nan':
        return ''
    if delivery_requirement == 'Fast':
        return "\n🚀 25-35 days production lead time for standard items\n"
    else:
        return "\n🚀 30-45 days production lead time\n"

def build_china_acceptance_section(accept_china_factory):
    if not accept_china_factory or accept_china_factory.strip() == 'None' or accept_china_factory.strip() == 'nan':
        return ''
    if accept_china_factory == 'Yes':
        return "\n✅ Already working with Chinese suppliers? We understand your quality standards and can seamlessly integrate into your supply chain.\n"
    elif accept_china_factory == 'No':
        return "\n✅ New to Chinese suppliers? We provide full transparency with factory tours, video inspections, and third-party quality verification.\n"
    return ''

def build_customization_section(customization_ability):
    if not customization_ability or customization_ability.strip() == 'None' or customization_ability.strip() == 'nan':
        return ''
    if customization_ability == 'High':
        return "\n🔹 Full custom design and tooling support for OEM projects\n"
    elif customization_ability == 'Medium':
        return "\n🔹 Custom branding and packaging options available\n"
    return ''

def build_after_sales_section(after_sales_requirement):
    if not after_sales_requirement or after_sales_requirement.strip() == 'None' or after_sales_requirement.strip() == 'nan' or after_sales_requirement.strip() == 'Not provided':
        return ''
    return "\n✅ Comprehensive after-sales support including product training and technical assistance\n"

def build_market_section(main_market):
    if not main_market or main_market.strip() == 'None' or main_market.strip() == 'nan' or main_market.strip() == 'Not provided':
        return ''
    return f"\nWith your focus on {main_market}, our products are well-positioned to meet local market demands.\n"

def truncate_for_subject(text, max_len=30):
    if not text:
        return "Auto Parts"
    text = str(text).strip()
    if len(text) <= max_len:
        return text
    return text[:max_len].rsplit(' ', 1)[0] + "..."

def generate_oem_email(company):
    company_id, company_name, company_type, main_products, lead_grade, \
    supply_chain_pain_points, recommended_products, quality_requirement, \
    price_sensitivity, delivery_requirement, customization_ability, \
    after_sales_requirement, accept_china_factory, main_market = company
    
    company_name = str(company_name) if company_name else "Valued Partner"
    main_products_en = translate_main_products(main_products)
    
    subject = f"OEM Quality {truncate_for_subject(main_products_en)} Supplier - {SENDER_COMPANY_EN} | Enhance Your Production"
    
    email_body = f"""Dear {company_name} Team,

Greetings from {SENDER_COMPANY_EN}! We are a professional automotive exterior parts manufacturer based in Foshan, China, with over 10 years of experience serving global OEM clients.

We specialize in manufacturing high-quality components that complement your production line:
• {translate_recommended_products(recommended_products) or 'Mirror assemblies, pillar trims, roof racks, grilles, fog lamp covers'}

{build_pain_point_section(translate_pain_points(supply_chain_pain_points))}

Our OEM Partnership Advantages:
{build_quality_section(translate_quality(quality_requirement))}
{build_customization_section(customization_ability)}
🔹 Custom tooling development in 30-45 days
🔹 Flexible MOQ: 50 sets per model for trial production
{build_price_section(price_sensitivity)}
{build_delivery_section(delivery_requirement)}
🔹 Stable batch consistency with full traceability
{build_after_sales_section(translate_after_sales(after_sales_requirement))}

{build_china_acceptance_section(accept_china_factory)}
{build_market_section(translate_market(main_market))}

Would you be interested in reviewing our product catalog and discussing how we can support your manufacturing operations?

Please visit our website: {SENDER_DOMAIN}

{BLOCK_FOOTER}"""
    return subject, email_body

def generate_distributor_email(company):
    company_id, company_name, company_type, main_products, lead_grade, \
    supply_chain_pain_points, recommended_products, quality_requirement, \
    price_sensitivity, delivery_requirement, customization_ability, \
    after_sales_requirement, accept_china_factory, main_market = company
    
    company_name = str(company_name) if company_name else "Valued Partner"
    main_products_en = translate_main_products(main_products)
    
    subject = f"Competitive {truncate_for_subject(main_products_en)} Supply - {SENDER_COMPANY_EN} | Boost Your Margins"
    
    email_body = f"""Dear {company_name} Team,

Hope this email finds you well! My name is Leo Leung from {SENDER_COMPANY_EN}, a leading Chinese auto parts factory specializing in exterior components for pickup trucks, SUVs, and passenger vehicles.

With your strong presence in {main_products_en}, we believe we can be your ideal supplier for:
• {translate_recommended_products(recommended_products) or 'Mirror assemblies, body parts, grilles, fog lamp covers'}

{build_pain_point_section(translate_pain_points(supply_chain_pain_points))}

Why partner with us:
✅ OEM-grade quality at competitive prices
✅ MOQ as low as 50 sets per model
{build_price_section(price_sensitivity)}
{build_delivery_section(delivery_requirement)}
✅ Full export support: packaging, documentation, logistics
✅ Custom branding and packaging available
✅ Sample support for quality verification
{build_after_sales_section(translate_after_sales(after_sales_requirement))}

{build_china_acceptance_section(accept_china_factory)}
{build_market_section(translate_market(main_market))}

As a distributor focused on {main_products_en}, adding our cost-effective exterior parts can significantly boost your margins while maintaining quality standards for your customers.

We'd love to send you our product catalog and sample pricing. Would you be available for a brief call next week to discuss your specific needs?

Visit us: {SENDER_DOMAIN}

{BLOCK_FOOTER}"""
    return subject, email_body

def generate_importer_email(company):
    company_id, company_name, company_type, main_products, lead_grade, \
    supply_chain_pain_points, recommended_products, quality_requirement, \
    price_sensitivity, delivery_requirement, customization_ability, \
    after_sales_requirement, accept_china_factory, main_market = company
    
    company_name = str(company_name) if company_name else "Valued Partner"
    main_products_en = translate_main_products(main_products)
    
    subject = f"Direct China {truncate_for_subject(main_products_en)} Sourcing - {SENDER_COMPANY_EN} | Import Simplified"
    
    email_body = f"""Dear {company_name} Team,

Greetings from {SENDER_COMPANY_EN}! As a professional automotive parts importer, you understand the importance of reliable suppliers and smooth logistics. We'd like to introduce ourselves as your direct sourcing partner from China.

We specialize in:
• {translate_recommended_products(recommended_products) or 'Mirror assemblies, body parts, grilles, fog lamp covers'}

{build_pain_point_section(translate_pain_points(supply_chain_pain_points))}

Our Import-Friendly Services:
🚢 Direct factory pricing - eliminate middlemen
📦 Full container load (FCL) and less than container load (LCL) options
📋 Complete documentation support: commercial invoice, packing list, CO, CIQ
✅ Quality inspection before shipment
{build_delivery_section(delivery_requirement)}
{build_price_section(price_sensitivity)}
✅ Dedicated account manager for your imports
{build_after_sales_section(translate_after_sales(after_sales_requirement))}

{build_china_acceptance_section(accept_china_factory)}
{build_market_section(translate_market(main_market))}

Would you be interested in receiving our import pricing list and discussing how we can streamline your China sourcing?

Please visit our website: {SENDER_DOMAIN}

{BLOCK_FOOTER}"""
    return subject, email_body

def generate_retailer_email(company):
    company_id, company_name, company_type, main_products, lead_grade, \
    supply_chain_pain_points, recommended_products, quality_requirement, \
    price_sensitivity, delivery_requirement, customization_ability, \
    after_sales_requirement, accept_china_factory, main_market = company
    
    company_name = str(company_name) if company_name else "Valued Partner"
    main_products_en = translate_main_products(main_products)
    
    subject = f"Quality {truncate_for_subject(main_products_en)} for Retail - {SENDER_COMPANY_EN} | Enhance Your Product Range"
    
    email_body = f"""Dear {company_name} Team,

Hope this email finds you well! My name is Leo Leung from {SENDER_COMPANY_EN}, a trusted Chinese auto parts manufacturer.

With your retail focus on {main_products_en}, we can help you expand your product offerings with:
• {translate_recommended_products(recommended_products) or 'Mirror assemblies, body parts, grilles, fog lamp covers'}

{build_pain_point_section(translate_pain_points(supply_chain_pain_points))}

Retailer-Friendly Benefits:
✅ High-quality products that satisfy your customers
✅ Competitive pricing for healthy margins
✅ Small MOQ options - test new products without risk
✅ Attractive packaging for retail display
{build_delivery_section(delivery_requirement)}
✅ Fast replenishment for popular items
{build_after_sales_section(translate_after_sales(after_sales_requirement))}

{build_market_section(translate_market(main_market))}

Would you be interested in reviewing our retail catalog and discussing how we can support your business growth?

Visit us: {SENDER_DOMAIN}

{BLOCK_FOOTER}"""
    return subject, email_body

def generate_general_email(company):
    company_id, company_name, company_type, main_products, lead_grade, \
    supply_chain_pain_points, recommended_products, quality_requirement, \
    price_sensitivity, delivery_requirement, customization_ability, \
    after_sales_requirement, accept_china_factory, main_market = company
    
    company_name = str(company_name) if company_name else "Valued Partner"
    main_products_en = translate_main_products(main_products)
    
    subject = f"Reliable Auto Parts Source - {SENDER_COMPANY_EN} | Quality You Can Trust"
    
    email_body = f"""Dear {company_name} Team,

I hope this message reaches you in good health. My name is Leo Leung representing {SENDER_COMPANY_EN}, a trusted Chinese automotive parts manufacturer with extensive experience in serving international markets.

We specialize in manufacturing high-quality exterior auto parts including:
• {translate_recommended_products(recommended_products) or 'Mirror assemblies, body parts, grilles, fog lamp covers'}

{build_pain_point_section(translate_pain_points(supply_chain_pain_points))}

Key Benefits:
⭐ Competitive pricing - 30-40% lower than premium brands
⭐ Consistent quality - IATF 16949 certified production
⭐ Flexible ordering - Small MOQ for trial, bulk pricing available
⭐ Fast turnaround - 30-45 day production lead time
⭐ Export ready - Professional packaging and documentation
{build_after_sales_section(translate_after_sales(after_sales_requirement))}

{build_china_acceptance_section(accept_china_factory)}
{build_market_section(translate_market(main_market))}

We would welcome the opportunity to discuss how {SENDER_COMPANY_EN} can support your business growth. Could we schedule a quick call or video conference at your convenience?

More information: {SENDER_DOMAIN}

{BLOCK_FOOTER}"""
    return subject, email_body

def generate_email_by_type(company):
    company_type = str(company[2]) if company[2] else "Other"
    
    company_type_en = COMPANY_TYPE_MAP.get(company_type, company_type)
    
    if 'OEM' in company_type_en or 'Manufacturer' in company_type_en:
        return generate_oem_email(company)
    elif 'Importer' in company_type_en:
        return generate_importer_email(company)
    elif 'Distributor' in company_type_en:
        return generate_distributor_email(company)
    elif 'Retailer' in company_type_en:
        return generate_retailer_email(company)
    else:
        return generate_general_email(company)

def get_all_companies(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, company_name, company_type, main_products, lead_grade, 
               supply_chain_pain_points, recommended_products, quality_requirement,
               price_sensitivity, delivery_requirement, customization_ability,
               after_sales_requirement, accept_china_factory, main_market
        FROM p_company 
        WHERE status = 'New'
        ORDER BY lead_score DESC
    """)
    companies = cursor.fetchall()
    cursor.close()
    return companies

def save_email_to_db(conn, company_id, subject, email_body):
    cursor = conn.cursor()
    update_sql = """
    UPDATE p_company 
    SET email_subject = %s, development_email_template = %s 
    WHERE id = %s
    """
    cursor.execute(update_sql, (subject, email_body, company_id))
    conn.commit()
    cursor.close()

def save_emails_to_file(companies_with_emails):
    with open(r'E:\09.document\carparts\客户资料\开发信_批量生成_英文版.txt', 'w', encoding='utf-8') as f:
        for company_id, company_name, subject, email_body in companies_with_emails:
            f.write('='*80 + '\n')
            f.write(f"📧 Company ID: {company_id}\n")
            f.write(f"📋 Company Name: {company_name}\n")
            f.write(f"📝 Subject: {subject}\n")
            f.write('='*80 + '\n')
            f.write(email_body)
            f.write('\n\n' + '='*80 + '\n\n')

if __name__ == '__main__':
    print("=" * 70)
    print("Translate Development Emails to English")
    print(f"Sender: {SENDER_COMPANY_EN}")
    print(f"Domain: {SENDER_DOMAIN}")
    print("=" * 70)
    
    try:
        conn = connect_db()
        print("\n✅ Database connection successful")
        
        companies = get_all_companies(conn)
        print(f"\n📊 Found {len(companies)} companies")
        
        companies_with_emails = []
        
        print("\n🚀 Translating development emails...")
        for i, company in enumerate(companies, 1):
            company_id = company[0]
            company_name = str(company[1]) if company[1] else "Unknown"
            
            subject, email_body = generate_email_by_type(company)
            save_email_to_db(conn, company_id, subject, email_body)
            companies_with_emails.append((company_id, company_name, subject, email_body))
            
            if i % 10 == 0:
                print(f"  ... Processed {i} companies")
        
        save_emails_to_file(companies_with_emails)
        
        conn.close()
        
        print(f"\n🎉 Successfully translated {len(companies_with_emails)} development emails")
        print("📁 Emails saved to: E:\\09.document\\carparts\\客户资料\\开发信_批量生成_英文版.txt")
        print("💾 Email subjects and templates updated in database")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
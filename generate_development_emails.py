# -*- coding: utf-8 -*-
import pymysql

DB_HOST = '8.163.58.109'
DB_PORT = 3306
DB_USER = 'thai_auto_parts_crm'
DB_PASSWORD = 'tDdY8NX2xJ6HpdHz'
DB_NAME = 'thai_auto_parts_crm'

SENDER_COMPANY = '佛山市鼎和盛汽车配件有限公司'
SENDER_DOMAIN = 'https://www.carparts-land.com/'
SENDER_PHONE = '+86 180-7886-5445'
SENDER_EMAIL = 'market@carparts-land.com'
SENDER_NAME = 'Leo Leung'

def connect_db():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset='utf8mb4'
    )

def get_all_companies(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, company_name, company_type, main_products, lead_grade, 
               purchase_potential, supply_chain_pain_points, recommended_products,
               quality_requirement, price_sensitivity, delivery_requirement,
               accept_china_factory, main_market, annual_revenue_usd,
               first_email_strategy, customization_ability, after_sales_requirement,
               china_supplier_acceptance, import_ability, purchase_scale
        FROM p_company 
        ORDER BY lead_score DESC
    """)
    companies = cursor.fetchall()
    cursor.close()
    return companies

def build_pain_point_section(pain_points):
    if not pain_points or pain_points.strip() == 'None' or pain_points.strip() == 'nan':
        return ''
    pain_points = pain_points.strip()
    return f"\nWe've analyzed the supply chain landscape and understand {pain_points}. " \
           f"Our solutions are specifically designed to address these challenges effectively.\n"

def build_quality_section(quality_requirement):
    if not quality_requirement or quality_requirement.strip() == 'None' or quality_requirement.strip() == 'nan':
        return ''
    quality_map = {
        'High': '🔹 OEM-grade quality with IATF 16949 certification',
        'Medium': '🔹 Consistent quality with ISO 9001 standards',
        'Low': '🔹 Reliable quality at competitive pricing'
    }
    return f"\n{quality_map.get(quality_requirement.strip(), '')}\n"

def build_price_section(price_sensitivity):
    if not price_sensitivity or price_sensitivity.strip() == 'None' or price_sensitivity.strip() == 'nan':
        return ''
    price_map = {
        'High': '✅ 30-40% cost reduction vs. Japanese/European suppliers',
        'Medium': '✅ Competitive pricing with volume discounts',
        'Low': '✅ Premium quality at fair market prices'
    }
    return f"\n{price_map.get(price_sensitivity.strip(), '')}\n"

def build_delivery_section(delivery_requirement):
    if not delivery_requirement or delivery_requirement.strip() == 'None' or delivery_requirement.strip() == 'nan':
        return ''
    delivery_map = {
        'Fast': '🚀 25-35 days production lead time for standard items',
        'Medium': '🚀 30-45 days production lead time',
        'Flexible': '🚀 Flexible delivery schedules to match your production cycles'
    }
    return f"\n{delivery_map.get(delivery_requirement.strip(), '')}\n"

def build_china_acceptance_section(accept_china_factory):
    if not accept_china_factory or accept_china_factory.strip() == 'None' or accept_china_factory.strip() == 'nan':
        return ''
    if 'Yes' in accept_china_factory or 'yes' in accept_china_factory:
        return "\n✅ Already working with Chinese suppliers? We understand your quality standards and can seamlessly integrate into your supply chain.\n"
    elif 'No' in accept_china_factory or 'no' in accept_china_factory:
        return "\n✅ New to Chinese suppliers? We provide full transparency with factory tours, video inspections, and third-party quality verification.\n"
    return ''

def build_purchase_potential_section(purchase_potential, revenue):
    if not purchase_potential or purchase_potential.strip() == 'None' or purchase_potential.strip() == 'nan':
        return ''
    potential_map = {
        '极高': 'As a high-potential partner, we are prepared to offer special pricing and dedicated support.',
        '高': 'Given your strong purchasing potential, we can provide volume discounts and priority delivery.',
        '中': 'We offer flexible terms suitable for your current business scale.',
        '低': 'Our low MOQ options are perfect for testing new product lines.'
    }
    revenue_str = f" (annual revenue ~${revenue:,})" if revenue else ""
    return f"\n{potential_map.get(purchase_potential.strip(), '')}{revenue_str}\n"

def build_recommended_products_section(recommended_products):
    if not recommended_products or recommended_products.strip() == 'None' or recommended_products.strip() == 'nan':
        return '• Mirror assemblies, pillar trims, roof racks, grilles, fog lamp covers'
    return f"• {recommended_products.strip()}"

def build_market_section(main_market):
    if not main_market or main_market.strip() == 'None' or main_market.strip() == 'nan':
        return ''
    return f"\nWith your focus on {main_market}, our products are well-positioned to meet local market demands.\n"

def build_customization_section(customization_ability):
    if not customization_ability or customization_ability.strip() == 'None' or customization_ability.strip() == 'nan':
        return ''
    if 'High' in customization_ability or 'high' in customization_ability:
        return "\n🔹 Full custom design and tooling support for OEM projects\n"
    elif 'Medium' in customization_ability or 'medium' in customization_ability:
        return "\n🔹 Custom branding and packaging options available\n"
    return ''

def build_after_sales_section(after_sales_requirement):
    if not after_sales_requirement or after_sales_requirement.strip() == 'None' or after_sales_requirement.strip() == 'nan':
        return ''
    return "\n✅ Comprehensive after-sales support including product training and technical assistance\n"

def build_strategy_section(strategy):
    if not strategy or strategy.strip() == 'None' or strategy.strip() == 'nan':
        return ''
    return f"\n{strategy.strip()}\n"

def truncate_for_subject(text, max_len=30):
    if not text:
        return "Auto Parts"
    text = str(text).strip()
    if len(text) <= max_len:
        return text
    return text[:max_len].rsplit(' ', 1)[0] + "..."

def generate_oem_email(company):
    company_id, company_name, company_type, main_products, lead_grade, \
    purchase_potential, pain_points, recommended_products, \
    quality_requirement, price_sensitivity, delivery_requirement, \
    accept_china_factory, main_market, revenue, strategy, \
    customization_ability, after_sales_requirement, \
    china_acceptance, import_ability, purchase_scale = company
    
    company_name = str(company_name) if company_name else "Valued Partner"
    main_products = str(main_products) if main_products else "auto parts"
    
    subject = f"OEM Quality {truncate_for_subject(main_products)} Supplier - {SENDER_COMPANY} | Enhance Your Production"
    
    email_body = f"""Dear {company_name} Team,

Greetings from {SENDER_COMPANY}! We are a professional automotive exterior parts manufacturer based in Foshan, China, with over 10 years of experience serving global OEM clients.

We specialize in manufacturing high-quality components that complement your production line:
{build_recommended_products_section(recommended_products)}

{build_pain_point_section(pain_points)}

Our OEM Partnership Advantages:
{build_quality_section(quality_requirement)}
{build_customization_section(customization_ability)}
🔹 Custom tooling development in 30-45 days
🔹 Flexible MOQ: 50 sets per model for trial production
{build_price_section(price_sensitivity)}
{build_delivery_section(delivery_requirement)}
🔹 Stable batch consistency with full traceability
{build_after_sales_section(after_sales_requirement)}

{build_china_acceptance_section(accept_china_factory)}
{build_market_section(main_market)}
{build_purchase_potential_section(purchase_potential, revenue)}
{build_strategy_section(strategy)}

Would you be interested in reviewing our product catalog and discussing how we can support your manufacturing operations?

Please visit our website: {SENDER_DOMAIN}

Best regards,
{BLOCK_FOOTER}
"""
    return subject, email_body

def generate_distributor_email(company):
    company_id, company_name, company_type, main_products, lead_grade, \
    purchase_potential, pain_points, recommended_products, \
    quality_requirement, price_sensitivity, delivery_requirement, \
    accept_china_factory, main_market, revenue, strategy, \
    customization_ability, after_sales_requirement, \
    china_acceptance, import_ability, purchase_scale = company
    
    company_name = str(company_name) if company_name else "Valued Partner"
    main_products = str(main_products) if main_products else "auto parts"
    
    subject = f"Competitive {truncate_for_subject(main_products)} Supply - {SENDER_COMPANY} | Boost Your Margins"
    
    email_body = f"""Dear {company_name} Team,

Hope this email finds you well! My name is {SENDER_NAME} from {SENDER_COMPANY}, a leading Chinese auto parts factory specializing in exterior components for pickup trucks, SUVs, and passenger vehicles.

With your strong presence in {main_products}, we believe we can be your ideal supplier for:
{build_recommended_products_section(recommended_products)}

{build_pain_point_section(pain_points)}

Why partner with us:
✅ OEM-grade quality at competitive prices
✅ MOQ as low as 50 sets per model
{build_price_section(price_sensitivity)}
{build_delivery_section(delivery_requirement)}
✅ Full export support: packaging, documentation, logistics
✅ Custom branding and packaging available
✅ Sample support for quality verification
{build_after_sales_section(after_sales_requirement)}

{build_china_acceptance_section(accept_china_factory)}
{build_market_section(main_market)}
{build_purchase_potential_section(purchase_potential, revenue)}

As a distributor focused on {main_products}, adding our cost-effective exterior parts can significantly boost your margins while maintaining quality standards for your customers.

{build_strategy_section(strategy)}

We'd love to send you our product catalog and sample pricing. Would you be available for a brief call next week to discuss your specific needs?

Visit us: {SENDER_DOMAIN}

Best regards,
{BLOCK_FOOTER}
"""
    return subject, email_body

def generate_importer_email(company):
    company_id, company_name, company_type, main_products, lead_grade, \
    purchase_potential, pain_points, recommended_products, \
    quality_requirement, price_sensitivity, delivery_requirement, \
    accept_china_factory, main_market, revenue, strategy, \
    customization_ability, after_sales_requirement, \
    china_acceptance, import_ability, purchase_scale = company
    
    company_name = str(company_name) if company_name else "Valued Partner"
    main_products = str(main_products) if main_products else "auto parts"
    
    subject = f"Direct China {truncate_for_subject(main_products)} Sourcing - {SENDER_COMPANY} | Import Simplified"
    
    email_body = f"""Dear {company_name} Team,

Greetings from {SENDER_COMPANY}! As a professional automotive parts importer, you understand the importance of reliable suppliers and smooth logistics. We'd like to introduce ourselves as your direct sourcing partner from China.

We specialize in:
{build_recommended_products_section(recommended_products)}

{build_pain_point_section(pain_points)}

Our Import-Friendly Services:
🚢 Direct factory pricing - eliminate middlemen
📦 Full container load (FCL) and less than container load (LCL) options
📋 Complete documentation support: commercial invoice, packing list, CO, CIQ
✅ Quality inspection before shipment
{build_delivery_section(delivery_requirement)}
{build_price_section(price_sensitivity)}
✅ Dedicated account manager for your imports
{build_after_sales_section(after_sales_requirement)}

{build_china_acceptance_section(accept_china_factory)}
{build_market_section(main_market)}
{build_purchase_potential_section(purchase_potential, revenue)}

{build_strategy_section(strategy)}

Would you be interested in receiving our import pricing list and discussing how we can streamline your China sourcing?

Please visit our website: {SENDER_DOMAIN}

Best regards,
{BLOCK_FOOTER}
"""
    return subject, email_body

def generate_retailer_email(company):
    company_id, company_name, company_type, main_products, lead_grade, \
    purchase_potential, pain_points, recommended_products, \
    quality_requirement, price_sensitivity, delivery_requirement, \
    accept_china_factory, main_market, revenue, strategy, \
    customization_ability, after_sales_requirement, \
    china_acceptance, import_ability, purchase_scale = company
    
    company_name = str(company_name) if company_name else "Valued Partner"
    main_products = str(main_products) if main_products else "auto parts"
    
    subject = f"Quality {truncate_for_subject(main_products)} for Retail - {SENDER_COMPANY} | Enhance Your Product Range"
    
    email_body = f"""Dear {company_name} Team,

Hope this email finds you well! My name is {SENDER_NAME} from {SENDER_COMPANY}, a trusted Chinese auto parts manufacturer.

With your retail focus on {main_products}, we can help you expand your product offerings with:
{build_recommended_products_section(recommended_products)}

{build_pain_point_section(pain_points)}

Retailer-Friendly Benefits:
✅ High-quality products that satisfy your customers
✅ Competitive pricing for healthy margins
✅ Small MOQ options - test new products without risk
✅ Attractive packaging for retail display
{build_delivery_section(delivery_requirement)}
✅ Fast replenishment for popular items
{build_after_sales_section(after_sales_requirement)}

{build_market_section(main_market)}
{build_purchase_potential_section(purchase_potential, revenue)}

{build_strategy_section(strategy)}

Would you be interested in reviewing our retail catalog and discussing how we can support your business growth?

Visit us: {SENDER_DOMAIN}

Best regards,
{BLOCK_FOOTER}
"""
    return subject, email_body

def generate_general_email(company):
    company_id, company_name, company_type, main_products, lead_grade, \
    purchase_potential, pain_points, recommended_products, \
    quality_requirement, price_sensitivity, delivery_requirement, \
    accept_china_factory, main_market, revenue, strategy, \
    customization_ability, after_sales_requirement, \
    china_acceptance, import_ability, purchase_scale = company
    
    company_name = str(company_name) if company_name else "Valued Partner"
    main_products = str(main_products) if main_products else "auto parts"
    
    subject = f"Reliable Auto Parts Source - {SENDER_COMPANY} | Quality You Can Trust"
    
    email_body = f"""Dear {company_name} Team,

I hope this message reaches you in good health. My name is {SENDER_NAME} representing {SENDER_COMPANY}, a trusted Chinese automotive parts manufacturer with extensive experience in serving international markets.

We specialize in manufacturing high-quality exterior auto parts including:
{build_recommended_products_section(recommended_products)}

{build_pain_point_section(pain_points)}

Key Benefits:
⭐ Competitive pricing - 30-40% lower than premium brands
⭐ Consistent quality - IATF 16949 certified production
⭐ Flexible ordering - Small MOQ for trial, bulk pricing available
⭐ Fast turnaround - 30-45 day production lead time
⭐ Export ready - Professional packaging and documentation
{build_after_sales_section(after_sales_requirement)}

{build_china_acceptance_section(accept_china_factory)}
{build_market_section(main_market)}
{build_purchase_potential_section(purchase_potential, revenue)}

{build_strategy_section(strategy)}

We would welcome the opportunity to discuss how {SENDER_COMPANY} can support your business growth. Could we schedule a quick call or video conference at your convenience?

More information: {SENDER_DOMAIN}

Best regards,
{BLOCK_FOOTER}
"""
    return subject, email_body

def generate_email_by_type(company):
    company_type = str(company[2]) if company[2] else "Other"
    
    if 'OEM' in company_type:
        return generate_oem_email(company)
    elif 'Manufacturer' in company_type:
        return generate_oem_email(company)
    elif 'Importer' in company_type:
        return generate_importer_email(company)
    elif 'Distributor' in company_type:
        return generate_distributor_email(company)
    elif 'Retailer' in company_type:
        return generate_retailer_email(company)
    else:
        return generate_general_email(company)

BLOCK_FOOTER = f"""{SENDER_NAME}
Export Sales Manager
{SENDER_COMPANY}
📞 {SENDER_PHONE}
📧 {SENDER_EMAIL}
🌐 {SENDER_DOMAIN}
🏭 Foshan City, Guangdong Province, China"""

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
    with open(r'E:\09.document\carparts\客户资料\开发信_批量生成.txt', 'w', encoding='utf-8') as f:
        for company_id, company_name, subject, email_body in companies_with_emails:
            f.write('='*80 + '\n')
            f.write(f"📧 公司ID: {company_id}\n")
            f.write(f"📋 公司名称: {company_name}\n")
            f.write(f"📝 邮件主题: {subject}\n")
            f.write('='*80 + '\n')
            f.write(email_body)
            f.write('\n\n' + '='*80 + '\n\n')

if __name__ == '__main__':
    print("=" * 70)
    print(f"为所有客户批量生成深度个性化开发信")
    print(f"发件人: {SENDER_COMPANY}")
    print(f"域名: {SENDER_DOMAIN}")
    print("=" * 70)
    
    try:
        conn = connect_db()
        print("\n✅ 数据库连接成功")
        
        companies = get_all_companies(conn)
        print(f"\n📊 找到 {len(companies)} 个客户")
        
        companies_with_emails = []
        
        print("\n🚀 正在生成深度个性化开发信...")
        for i, company in enumerate(companies, 1):
            company_id = company[0]
            company_name = str(company[1]) if company[1] else "Unknown"
            company_type = str(company[2]) if company[2] else "Other"
            
            subject, email_body = generate_email_by_type(company)
            save_email_to_db(conn, company_id, subject, email_body)
            companies_with_emails.append((company_id, company_name, subject, email_body))
            
            if i % 50 == 0:
                print(f"  ... 已处理 {i} 个客户")
        
        save_emails_to_file(companies_with_emails)
        
        conn.close()
        
        print(f"\n🎉 成功为 {len(companies_with_emails)} 个客户生成深度个性化开发信")
        print(f"📁 开发信已保存到: E:\\09.document\\carparts\\客户资料\\开发信_批量生成.txt")
        print(f"💾 邮件主题和内容已更新到数据库")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
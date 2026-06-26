# -*- coding: utf-8 -*-
import pymysql
import re

DB_HOST = '8.163.58.109'
DB_PORT = 3306
DB_USER = 'thai_auto_parts_crm'
DB_PASSWORD = 'tDdY8NX2xJ6HpdHz'
DB_NAME = 'thai_auto_parts_crm'

SENDER_COMPANY = 'Foshan Dinghesheng Auto Parts Co., Ltd'
SENDER_DOMAIN = 'https://www.carparts-land.com/'
SENDER_PHONE = '+86 180-7886-5445'
SENDER_EMAIL = 'market@carparts-land.com'
SENDER_NAME = 'Leo Leung'

CHINESE_TO_ENGLISH = {
    '后视镜': 'Mirror',
    '后视镜总成': 'Mirror assemblies',
    '总成': 'assemblies',
    '车身外饰件': 'Exterior body parts',
    '外饰件': 'Exterior parts',
    '格栅': 'Grilles',
    '雾灯罩': 'Fog lamp covers',
    '保险杠': 'Bumpers',
    '翼子板': 'Fenders',
    '引擎盖': 'Hoods',
    '车门': 'Doors',
    '灯具': 'Lights/Lamps',
    '车身面板': 'Body panels',
    '立柱饰板': 'Pillar trims',
    '行李架': 'Roof racks',
    '侧裙': 'Side skirts',
    '尾翼': 'Spoilers',
    '仪表饰条': 'Instrument panel trims',
    '换挡面板': 'Gear shift panels',
    '中控': 'Center console',
    '内饰': 'Interior parts',
    '塑料外饰': 'Plastic exterior',
    '高光内饰': 'High-gloss interior',
    '包围套件': 'Body kits',
    '皮卡': 'Pickup truck',
    '乘用车': 'Passenger vehicle',
    '商用车': 'Commercial vehicle',
    '农机': 'Agricultural machinery',
    '全车件': 'Full vehicle parts',
    '发动机': 'Engine parts',
    '传动': 'Transmission',
    '悬挂': 'Suspension',
    '电气': 'Electrical',
    '底盘': 'Chassis',
    '制动': 'Brake',
    '三菱': 'Mitsubishi',
    '丰田': 'Toyota',
    'Hilux': 'Hilux',
    '4x4': '4x4',
    '全车配件': 'Full vehicle accessories',
    '高品质': 'High-quality',
    '配件': 'Parts',
    '附件': 'Accessories',
    '分销': 'Distribution',
    '日本原厂': 'Japanese OEM',
    '替代供应商': 'Alternative suppliers',
    '多车型': 'Multi-model',
    'SKU管理': 'SKU management',
    '替代件': 'Replacement parts',
    '供应链': 'Supply chain',
    '稳定性': 'Stability',
    '多品牌': 'Multi-brand',
    '出口包装': 'Export packaging',
    '低价供应商': 'Low-cost suppliers',
    '老批发商': 'Seasoned wholesaler',
    '批发商': 'Wholesaler',
    '成本': 'Cost',
    '授权': 'Authorized',
    '出口公司': 'Export company',
    '需求': 'Demand',
    '成立': 'Established',
    '全球出口': 'Global export',
    '全球最低价': 'Lowest global prices',
    '本土市场': 'Local market',
    '汽配城': 'Auto parts market',
    '柬埔寨': 'Cambodia',
    '马来西亚': 'Malaysia',
    '批量出口': 'Bulk export',
    '批发市场': 'Wholesale market',
    '老挝': 'Laos',
    '整柜采购': 'Full container procurement',
    '东南亚': 'Southeast Asia',
    '二级批发商': 'Secondary wholesalers',
    '曼谷': 'Bangkok',
    '缅甸': 'Myanmar',
    '边境贸易': 'Border trade',
    '修理厂': 'Workshops',
    '全国批发商': 'Nationwide distributors',
    '越南': 'Vietnam',
    '改装店': 'Modification shops',
    '跨境出口': 'Cross-border export',
    '全境': 'Nationwide',
    '澳洲': 'Australia',
    '中东': 'Middle East',
    '非洲': 'Africa',
    '南美': 'South America',
    '泰国': 'Thailand',
    '中国': 'China',
    '日本': 'Japan',
    '欧洲': 'Europe',
    'ASEAN': 'ASEAN',
    '未提供': 'Not specified',
    '极高': 'Very High',
    '高': 'High',
    '中': 'Medium',
    '低': 'Low',
    '壳': 'Housing',
    '底座': 'Base',
    'A/B/C/D柱': 'A/B/C/D pillars',
    '全套': 'Full set',
    '扰流板': 'Spoiler',
    '塑料饰件': 'Plastic trim parts',
    '仪表': 'Instrument cluster',
    '外壳': 'Outer shell',
    '高光': 'High-gloss',
    '装饰件': 'Decorative parts',
    '替换件': 'Replacement parts',
    '中部': 'Central',
    '东部': 'Eastern',
    '周边': 'Surrounding',
    '专注': 'Specializing in',
    '日系': 'Japanese',
    '日欧品牌': 'Japanese and European brands',
    '5000+': '5000+',
    '3000+': '3000+',
    '30年老牌': '30-year established',
    '1980年代': 'Established in 1980s',
    '以...为卖点': 'Known for',
    '最大': 'Largest',
    '整车配件': 'Complete vehicle parts',
    '内外饰': 'Interior and exterior parts',
    '全品类配件': 'Full range parts',
    '低成本': 'Cost-effective',
    '高品质': 'Premium quality',
    '批量': 'Bulk',
    '整柜': 'Full container',
    '降30%成本': '30% cost reduction',
    '供应链稳定性': 'Supply chain stability',
    '持续低价': 'Consistent low prices',
    '4x4出口商': '4x4 exporter',
    '成本高': 'high costs',
    '需要更多': 'need more',
    '可降': 'can reduce',
    '工厂': 'factory',
    '及': 'and',
    '车身': 'Body',
    '柱饰板': 'Pillar trims',
    '覆盖': 'coverage',
    '有专门': 'with dedicated',
    '大': 'high',
    '丰田Hilux': 'Toyota Hilux',
    '中网': 'Grille',
    '鲨鱼鳍': 'Shark fin antenna',
    '雾灯框': 'Fog light bezels',
    '车身套件': 'Body kits',
    '立柱': 'Pillars',
    '塑料车身外饰': 'Plastic body exterior',
    '高光内饰装饰件': 'High-gloss interior trim',
    '多国出口': 'Multi-country export',
    '本土': 'Local',
    '车身塑料外饰': 'Body plastic exterior',
    '清迈': 'Chiang Mai',
    '普吉': 'Phuket',
    '汽修连锁': 'Auto repair chain',
    '再出口': 'Re-export',
    '专修厂': 'Specialized workshop',
    '泰北': 'Northern Thailand',
    'Shopee': 'Shopee',
    'Lazada': 'Lazada',
    '头部': 'Top',
    '线下门店': 'Offline stores',
    '稳定采购': 'Stable procurement',
    '东北': 'Northeastern',
    '南部': 'Southern',
    '合艾': 'Hat Yai',
    '批发': 'Wholesale',
    '印尼': 'Indonesia',
    '工业园': 'Industrial park',
    '汽修厂': 'Auto repair shop',
    '小额': 'Small quantity',
    '小额整柜': 'Small full container',
    '内翼子板': 'Inner fenders',
    '尾灯': 'Tail lights',
    '大灯': 'Headlights',
    '雾灯': 'Fog lights',
    '尾灯框': 'Tail light bezels',
    '保险杠/格栅': 'Bumpers/Grilles',
    '供应商多元化': 'Supplier diversification',
    '专业出口商': 'Professional exporter',
    '采购意愿强': 'Strong sourcing interest',
    '日产': 'Nissan',
    '集团': 'Group',
    '直属': 'Affiliated',
    '体系': 'System',
    '售后件': 'Aftermarket parts',
    '一站式采购': 'One-stop sourcing',
    '一站式': 'One-stop',
    '制造商及领先': 'Manufacturer and leading',
    '制造': 'Manufacturing',
    '优化': 'Optimization',
    'OEM代工': 'OEM manufacturing',
    '代工': 'Manufacturing',
    '供货': 'Supply',
    '正品': 'Genuine',
    '正品件': 'Genuine parts',
    '正品车身件': 'Genuine body parts',
    '门板': 'Door panels',
    '车身结构件': 'Body structural parts',
    '供应商集中': 'Supplier concentration',
    '模具开发': 'Mold development',
    '福特': 'Ford',
    'Ranger': 'Ranger',
    'Everest': 'Everest',
    '精密件': 'Precision parts',
    '精密制造': 'Precision manufacturing',
    '外协件': 'Outsourced parts',
    '外协': 'Outsourced',
    '合作': 'Cooperation',
    '零件': 'Parts',
    '零售网络': 'Retail network',
    '多品类': 'Multi-category',
    '广泛': 'Wide',
    '车型': 'Vehicle models',
    '进口': 'Import',
    '高端市场': 'High-end market',
    '全品类': 'Full range',
    '线上': 'Online',
    '乡镇': 'Rural',
    '下沉市场': 'Lower-tier markets',
    '泰国本土及出口': 'Thailand local and export',
    '泰国本土及线上': 'Thailand local and online',
    '泰国全国': 'Nationwide Thailand',
    '五十铃': 'Isuzu',
    '本田': 'Honda',
    '及售后': 'and aftermarket',
    '主营': 'Main business',
    '产品100%匹配': '100% product match',
    '覆盖多个': 'Covering multiple',
    '新兴市场': 'Emerging markets',
    '认证': 'Certification',
    '长期战略': 'Long-term strategic',
    '价值巨大': 'Great value',
    '门槛高': 'High threshold',
    '进入门槛': 'Entry threshold',
    '意味着': 'means',
    '长期订单': 'Long-term orders',
    '品牌': 'Brand',
    'SMA品牌': 'SMA brand',
    'PQM品牌': 'PQM brand',
    '控制': 'Control',
    '明确涉及': 'Clearly involves',
    '配送': 'Delivery',
    '适合': 'Suitable for',
    '广泛分销': 'Wide distribution',
    '集团旗下': 'Group subsidiary',
    '精密件外协': 'Precision parts outsourcing',
    '福特车身件': 'Ford body parts',
    'OEM品质': 'OEM quality',
    '车身件为主营': 'Body parts as main business',
    '稳定供货': 'Stable supply',
    '模具开发成本高': 'High mold development costs',
    '上市公司': 'Listed company',
    '专业出口': 'Professional export',
    '采购意愿': 'Sourcing interest',
    '战略价值': 'Strategic value',
    '供应商认证': 'Supplier certification',
    '进入供应链': 'Entering supply chain',
    '巨大': 'Significant',
    '套件': 'kits',
    '塑料': 'Plastic',
    '网': 'Grille',
    '需要持续': 'need continuous',
    '迪拜': 'Dubai',
    '汽车': 'Auto',
    '以': 'known for',
    '为卖点': '',
    '外': 'outer',
    '部': '',
    '出口': 'export',
    '全国': 'Nationwide',
    '马来': 'Malaysia',
    '4S': '4S',
    '配套改装': 'modification',
    '大型': 'Large',
    '区域': 'regional',
    '汽配大卖家': 'auto parts seller',
    '边境': 'border',
    '小额整柜': 'Small full container',
    '区域批发': 'Regional wholesale',
    '汽配大卖家': 'Auto parts seller',
    '线下': 'Offline',
    '二级批发': 'Secondary wholesale',
    '稳定采购': 'Stable procurement',
    '边境分销': 'Border distribution',
    '本土批发': 'Local wholesale',
    '小额整柜': 'Small quantity full container',
    '汽修集群': 'Auto repair cluster',
    '工业园': 'Industrial zone',
    '清迈区域批发': 'Chiang Mai regional wholesale',
    '普吉': 'Phuket',
    '大型改装市场': 'Large modification market',
    '4S配套改装': '4S modification',
    '汽配大卖家': 'Auto parts seller',
}

def translate_chinese(text):
    if not text:
        return text
    text = str(text)
    for chinese, english in CHINESE_TO_ENGLISH.items():
        text = text.replace(chinese, english)
    text = re.sub(r'([一-龥]+)', translate_unknown, text)
    return text

def translate_unknown(match):
    chinese = match.group(1)
    if chinese in CHINESE_TO_ENGLISH:
        return CHINESE_TO_ENGLISH[chinese]
    return chinese

def clean_company_name(name):
    if not name:
        return "Valued Partner"
    name = str(name).strip()
    name = re.sub(r'^[0-9]+\s*', '', name)
    name = name.strip()
    return name if name else "Valued Partner"

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
    pain_points = translate_chinese(pain_points.strip())
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
        '极高': 'As a very high-potential partner, we are prepared to offer special pricing and dedicated support.',
        '高': 'Given your strong purchasing potential, we can provide volume discounts and priority delivery.',
        '中': 'We offer flexible terms suitable for your current business scale.',
        '低': 'Our low MOQ options are perfect for testing new product lines.',
        'Very High': 'As a very high-potential partner, we are prepared to offer special pricing and dedicated support.',
        'High': 'Given your strong purchasing potential, we can provide volume discounts and priority delivery.',
        'Medium': 'We offer flexible terms suitable for your current business scale.',
        'Low': 'Our low MOQ options are perfect for testing new product lines.'
    }
    purchase_potential = translate_chinese(purchase_potential.strip())
    revenue_str = f" (annual revenue ~${revenue:,})" if revenue else ""
    return f"\n{potential_map.get(purchase_potential, '')}{revenue_str}\n"

def build_recommended_products_section(recommended_products):
    if not recommended_products or recommended_products.strip() == 'None' or recommended_products.strip() == 'nan':
        return '• Mirror assemblies, pillar trims, roof racks, grilles, fog lamp covers'
    translated = translate_chinese(recommended_products.strip())
    return f"• {translated}"

def build_market_section(main_market):
    if not main_market or main_market.strip() == 'None' or main_market.strip() == 'nan':
        return ''
    translated = translate_chinese(main_market.strip())
    return f"\nWith your focus on {translated}, our products are well-positioned to meet local market demands.\n"

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
    translated = translate_chinese(strategy.strip())
    return f"\n{translated}\n"

def truncate_for_subject(text, max_len=30):
    if not text:
        return "Auto Parts"
    text = str(text).strip()
    text = translate_chinese(text)
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
    
    company_name = clean_company_name(company_name)
    main_products = str(main_products) if main_products else "auto parts"
    main_products = translate_chinese(main_products)
    
    subject = f"OEM Quality {truncate_for_subject(main_products)} Supplier - {SENDER_COMPANY} | Enhance Your Production"
    
    email_body = f"""Dear {company_name} Team,

Greetings from {SENDER_COMPANY}! We are a professional automotive exterior parts manufacturer based in Foshan, China, with over 10 years of experience serving global OEM clients.

With your expertise in {main_products}, we believe we can be your ideal partner for:
{build_recommended_products_section(recommended_products)}


Why partner with us:
✅ OEM-grade quality at competitive prices
✅ MOQ as low as 50 sets per model
{build_quality_section(quality_requirement)}
{build_price_section(price_sensitivity)}
{build_delivery_section(delivery_requirement)}
✅ Full export support: packaging, documentation, logistics
✅ Custom branding and packaging available
✅ Sample support for quality verification
{build_customization_section(customization_ability)}
{build_after_sales_section(after_sales_requirement)}
{build_china_acceptance_section(accept_china_factory)}

{build_pain_point_section(pain_points)}

{build_market_section(main_market)}

{build_purchase_potential_section(purchase_potential, revenue)}

{build_strategy_section(strategy)}

We'd love to discuss how we can support your OEM production needs. Would you be available for a brief call next week?

Visit us: {SENDER_DOMAIN}

{BLOCK_FOOTER}"""
    
    return subject, email_body

def generate_distributor_email(company):
    company_id, company_name, company_type, main_products, lead_grade, \
    purchase_potential, pain_points, recommended_products, \
    quality_requirement, price_sensitivity, delivery_requirement, \
    accept_china_factory, main_market, revenue, strategy, \
    customization_ability, after_sales_requirement, \
    china_acceptance, import_ability, purchase_scale = company
    
    company_name = clean_company_name(company_name)
    main_products = str(main_products) if main_products else "auto parts"
    main_products = translate_chinese(main_products)
    
    subject = f"Competitive {truncate_for_subject(main_products)} Supply - {SENDER_COMPANY} | Boost Your Margins"
    
    email_body = f"""Dear {company_name} Team,

Hope this email finds you well! My name is {SENDER_NAME} from {SENDER_COMPANY}, a leading Chinese auto parts factory specializing in exterior components for pickup trucks, SUVs, and passenger vehicles.

With your strong presence in {main_products}, we believe we can be your ideal supplier for:
{build_recommended_products_section(recommended_products)}


Why partner with us:
✅ OEM-grade quality at competitive prices
✅ MOQ as low as 50 sets per model
{build_quality_section(quality_requirement)}
{build_price_section(price_sensitivity)}
{build_delivery_section(delivery_requirement)}
✅ Full export support: packaging, documentation, logistics
✅ Custom branding and packaging available
✅ Sample support for quality verification
{build_customization_section(customization_ability)}
{build_after_sales_section(after_sales_requirement)}
{build_china_acceptance_section(accept_china_factory)}

{build_pain_point_section(pain_points)}

{build_market_section(main_market)}

As a distributor focused on {main_products}, adding our cost-effective exterior parts can significantly boost your margins while maintaining quality standards for your customers.

{build_purchase_potential_section(purchase_potential, revenue)}

{build_strategy_section(strategy)}

We'd love to send you our product catalog and sample pricing. Would you be available for a brief call next week to discuss your specific needs?

Visit us: {SENDER_DOMAIN}

{BLOCK_FOOTER}"""
    
    return subject, email_body

def generate_importer_email(company):
    company_id, company_name, company_type, main_products, lead_grade, \
    purchase_potential, pain_points, recommended_products, \
    quality_requirement, price_sensitivity, delivery_requirement, \
    accept_china_factory, main_market, revenue, strategy, \
    customization_ability, after_sales_requirement, \
    china_acceptance, import_ability, purchase_scale = company
    
    company_name = clean_company_name(company_name)
    main_products = str(main_products) if main_products else "auto parts"
    main_products = translate_chinese(main_products)
    
    subject = f"Direct China {truncate_for_subject(main_products)} Sourcing - {SENDER_COMPANY} | Import Simplified"
    
    email_body = f"""Dear {company_name} Team,

Greetings from {SENDER_COMPANY}! As a professional automotive parts importer, you understand the importance of reliable suppliers and smooth logistics. We'd like to introduce ourselves as your direct sourcing partner from China.

We specialize in:
{build_recommended_products_section(recommended_products)}


Why choose us:
✅ Direct factory pricing - no middlemen
✅ Full import documentation support
✅ Door-to-door logistics options
{build_quality_section(quality_requirement)}
{build_price_section(price_sensitivity)}
{build_delivery_section(delivery_requirement)}
✅ Low MOQ for trial orders
✅ Quality control inspections before shipment
✅ English-speaking support team
{build_customization_section(customization_ability)}
{build_after_sales_section(after_sales_requirement)}
{build_china_acceptance_section(accept_china_factory)}

{build_pain_point_section(pain_points)}

{build_market_section(main_market)}

{build_purchase_potential_section(purchase_potential, revenue)}

{build_strategy_section(strategy)}

Let us simplify your China sourcing. Would you be interested in receiving our product catalog and competitive pricing?

Visit us: {SENDER_DOMAIN}

{BLOCK_FOOTER}"""
    
    return subject, email_body

def generate_retailer_email(company):
    company_id, company_name, company_type, main_products, lead_grade, \
    purchase_potential, pain_points, recommended_products, \
    quality_requirement, price_sensitivity, delivery_requirement, \
    accept_china_factory, main_market, revenue, strategy, \
    customization_ability, after_sales_requirement, \
    china_acceptance, import_ability, purchase_scale = company
    
    company_name = clean_company_name(company_name)
    main_products = str(main_products) if main_products else "auto parts"
    main_products = translate_chinese(main_products)
    
    subject = f"Quality {truncate_for_subject(main_products)} for Retail - {SENDER_COMPANY} | Enhance Your Product Range"
    
    email_body = f"""Dear {company_name} Team,

Hope this email finds you well! My name is {SENDER_NAME} from {SENDER_COMPANY}, a trusted Chinese auto parts manufacturer.

We offer a wide range of high-quality exterior parts that can enhance your retail product range:
{build_recommended_products_section(recommended_products)}


Benefits for your retail business:
✅ Quality products with competitive pricing
✅ Fast delivery options
✅ Attractive packaging for retail display
{build_quality_section(quality_requirement)}
{build_price_section(price_sensitivity)}
{build_delivery_section(delivery_requirement)}
✅ Branded packaging available
✅ Marketing support materials
✅ Returns and exchange policy
{build_after_sales_section(after_sales_requirement)}
{build_china_acceptance_section(accept_china_factory)}

{build_pain_point_section(pain_points)}

{build_market_section(main_market)}

{build_purchase_potential_section(purchase_potential, revenue)}

{build_strategy_section(strategy)}

Would you be interested in expanding your product line with our quality exterior parts? We'd be happy to send samples and pricing.

Visit us: {SENDER_DOMAIN}

{BLOCK_FOOTER}"""
    
    return subject, email_body

def generate_general_email(company):
    company_id, company_name, company_type, main_products, lead_grade, \
    purchase_potential, pain_points, recommended_products, \
    quality_requirement, price_sensitivity, delivery_requirement, \
    accept_china_factory, main_market, revenue, strategy, \
    customization_ability, after_sales_requirement, \
    china_acceptance, import_ability, purchase_scale = company
    
    company_name = clean_company_name(company_name)
    main_products = str(main_products) if main_products else "auto parts"
    main_products = translate_chinese(main_products)
    
    subject = f"Reliable Auto Parts Source - {SENDER_COMPANY} | Quality You Can Trust"
    
    email_body = f"""Dear {company_name} Team,

Greetings from {SENDER_COMPANY}! We are a professional automotive exterior parts manufacturer based in Foshan, China.

We specialize in:
{build_recommended_products_section(recommended_products)}


Why choose us:
✅ Proven quality with global client base
✅ Competitive pricing
✅ Flexible MOQ
{build_quality_section(quality_requirement)}
{build_price_section(price_sensitivity)}
{build_delivery_section(delivery_requirement)}
✅ Full export support
✅ Dedicated customer service
{build_customization_section(customization_ability)}
{build_after_sales_section(after_sales_requirement)}
{build_china_acceptance_section(accept_china_factory)}

{build_pain_point_section(pain_points)}

{build_market_section(main_market)}

{build_purchase_potential_section(purchase_potential, revenue)}

{build_strategy_section(strategy)}

We would welcome the opportunity to discuss how we can support your business. Please let us know if you'd like to receive our product catalog.

Visit us: {SENDER_DOMAIN}

{BLOCK_FOOTER}"""
    
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
    with open(r'E:\09.document\carparts\客户资料\开发信_批量生成_英文版.txt', 'w', encoding='utf-8') as f:
        for company_id, company_name, subject, email_body in companies_with_emails:
            f.write("=" * 80 + "\n")
            f.write(f"📧 Company ID: {company_id}\n")
            f.write(f"📋 Company Name: {company_name}\n")
            f.write(f"📝 Subject: {subject}\n")
            f.write("=" * 80 + "\n")
            f.write(email_body)
            f.write("\n\n" + "=" * 80 + "\n\n")

def main():
    print("=" * 70)
    print("批量生成英文版开发信")
    print(f"Sender: {SENDER_COMPANY}")
    print(f"Domain: {SENDER_DOMAIN}")
    print("=" * 70)
    
    conn = connect_db()
    print("\n✅ Database connection successful")
    
    companies = get_all_companies(conn)
    print(f"\n📊 Found {len(companies)} companies")
    
    print("\n🚀 Generating English development emails...")
    companies_with_emails = []
    
    for i, company in enumerate(companies):
        company_id = company[0]
        company_name = str(company[1]) if company[1] else "Unknown"
        
        subject, email_body = generate_email_by_type(company)
        companies_with_emails.append((company_id, company_name, subject, email_body))
        
        save_email_to_db(conn, company_id, subject, email_body)
        
        if (i + 1) % 50 == 0:
            print(f"  ... Processed {i + 1} companies")
    
    save_emails_to_file(companies_with_emails)
    
    conn.close()
    
    print(f"\n🎉 Successfully generated English development emails for {len(companies)} companies")
    print(f"📁 Emails saved to: E:\\09.document\\carparts\\客户资料\\开发信_批量生成_英文版.txt")
    print("💾 Email subjects and content updated to database")

if __name__ == "__main__":
    main()
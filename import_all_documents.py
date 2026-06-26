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

def parse_priority_to_grade(priority):
    if priority is None:
        return 'C'
    if isinstance(priority, str):
        priority = priority.strip()
        if priority == 'A' or '★★★★★' in priority or '极高' in priority:
            return 'A'
        if priority == 'B' or '★★★★' in priority or '高' in priority:
            return 'B'
        if priority == 'C' or '★★★' in priority or '中等' in priority:
            return 'C'
        if '★★' in priority or '低' in priority or '一般' in priority:
            return 'C'
    return 'C'

def parse_priority_to_score(priority):
    grade = parse_priority_to_grade(priority)
    if grade == 'A':
        return 90
    if grade == 'B':
        return 75
    return 60

def parse_company_type(type_str):
    if type_str is None:
        return 'Other'
    type_str = str(type_str).strip().lower()
    if 'manufacturer' in type_str or '制造商' in type_str:
        return 'Manufacturer'
    if 'importer' in type_str or '进口商' in type_str:
        return 'Importer'
    if 'distributor' in type_str or '经销商' in type_str or '批发商' in type_str or '贸易' in type_str:
        return 'Distributor'
    if 'retail' in type_str or '零售商' in type_str:
        return 'Retailer'
    if 'oem' in type_str:
        return 'OEM'
    return 'Other'

def parse_revenue(revenue_str):
    if revenue_str is None:
        return None
    revenue_str = str(revenue_str).strip()
    match = re.search(r'(\d[\d,]*)\s*(万?)', revenue_str)
    if match:
        num = float(match.group(1).replace(',', ''))
        if match.group(2) == '万':
            return num * 10000
        return num
    return None

def parse_phone(phone_str):
    if phone_str is None:
        return None
    phone_str = str(phone_str).strip()
    if phone_str in ['-', '待确认', '未提供']:
        return None
    phone_str = phone_str.replace(' ', '')
    if phone_str.startswith('+66'):
        return phone_str
    if phone_str.startswith('0') and len(phone_str) >= 9:
        return '+66' + phone_str[1:]
    return phone_str

def parse_email(email_str):
    if email_str is None:
        return None
    email_str = str(email_str).strip()
    if email_str in ['-', '待确认', '未提供']:
        return None
    if '@' in email_str:
        return email_str
    return None

companies_data = []

def parse_gpt_txt():
    with open(r'E:\09.document\carparts\客户资料\gpt.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.isdigit() and i + 1 < len(lines):
            i += 1
            while i < len(lines) and lines[i].strip() == '':
                i += 1
            if i < len(lines):
                data_line = lines[i].strip()
                parts = data_line.split('|')
                if len(parts) >= 12:
                    company = {
                        'company_name': parts[0].strip(),
                        'company_type': parse_company_type(parts[1].strip()),
                        'lead_grade': parts[2].strip(),
                        'website': parts[3].strip().replace('`', '') if parts[3].strip() != '-' else None,
                        'phone': parse_phone(parts[4].strip()),
                        'email': parse_email(parts[5].strip()),
                        'address': parts[6].strip(),
                        'core_contact': parts[7].strip(),
                        'main_products': parts[8].strip(),
                        'main_market': parts[9].strip(),
                        'lead_score': int(parts[10].strip()),
                        'notes': parts[11].strip() if len(parts) > 11 else '',
                        'country': 'Thailand',
                        'source': 'Industry_Directory',
                        'source_url': 'gpt.txt',
                        'is_auto_parts_core': 1,
                        'is_importer_distributor': 1 if 'Distributor' in parts[1] or 'Importer' in parts[1] else 0
                    }
                    companies_data.append(company)
        i += 1

def parse_qianwen_txt():
    with open(r'E:\09.document\carparts\客户资料\千问.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')[2:]
    for line in lines:
        if line.startswith('|') and '公司名称' not in line:
            parts = line.split('|')
            if len(parts) >= 9:
                company_name = parts[1].strip()
                if company_name and company_name != ':---':
                    contact_info = parts[2].strip()
                    website_match = re.search(r'官网：(.+)', contact_info)
                    email_match = re.search(r'邮箱：(.+)', contact_info)
                    phone_match = re.search(r'电话：(.+)', contact_info)
                    
                    priority = parts[8].strip()
                    grade = parse_priority_to_grade(priority)
                    score = parse_priority_to_score(priority)
                    
                    company = {
                        'company_name': company_name,
                        'website': website_match.group(1).strip() if website_match else None,
                        'address': parts[3].strip(),
                        'phone': parse_phone(phone_match.group(1).strip()) if phone_match else None,
                        'email': parse_email(email_match.group(1).strip()) if email_match else None,
                        'core_contact': parts[4].strip()[:200],
                        'main_products': parts[5].strip(),
                        'main_market': parts[6].strip(),
                        'purchase_potential': parts[7].strip(),
                        'lead_grade': grade,
                        'lead_score': score,
                        'company_type': 'Distributor',
                        'country': 'Thailand',
                        'source': 'Industry_Directory',
                        'source_url': '千问.txt',
                        'is_auto_parts_core': 1,
                        'is_importer_distributor': 1
                    }
                    companies_data.append(company)

def parse_huoqu_txt():
    with open(r'E:\09.document\carparts\客户资料\获取.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')[4:]
    for line in lines:
        line_stripped = line.strip()
        if line_stripped.startswith('|') and '序号' not in line_stripped and ':-:' not in line_stripped:
            parts = line_stripped.split('|')
            if len(parts) >= 10:
                company_name = parts[2].strip().replace('**', '')
                if company_name:
                    company = {
                        'company_name': company_name,
                        'website': 'https://' + parts[3].strip().replace('**', '') if parts[3].strip() != '-' and parts[3].strip() else None,
                        'address': parts[4].strip(),
                        'phone': parse_phone(parts[5].strip()),
                        'core_contact': parts[6].strip(),
                        'main_products': parts[7].strip(),
                        'company_type': parse_company_type(parts[8].strip()),
                        'lead_grade': 'A' if parts[9].strip() == '很高' else ('B' if parts[9].strip() == '高' else ('C' if parts[9].strip() == '中' else 'C')),
                        'lead_score': 90 if parts[9].strip() == '很高' else (75 if parts[9].strip() == '高' else 60),
                        'country': 'Thailand',
                        'source': 'Industry_Directory',
                        'source_url': '获取.txt',
                        'is_auto_parts_core': 1,
                        'is_importer_distributor': 1 if 'Importer' in parts[8] or 'Distributor' in parts[8] else 0
                    }
                    companies_data.append(company)

def parse_doubao_txt():
    with open(r'E:\09.document\carparts\客户资料\豆包.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')[1:]
    for line in lines:
        line = line.strip()
        if line and not line.startswith('序号'):
            parts = line.split()
            if len(parts) >= 11:
                idx = 0
                company_name = ''
                while idx < len(parts) and not parts[idx].startswith('www.'):
                    company_name += ' ' + parts[idx]
                    idx += 1
                company_name = company_name.strip()
                
                website = None
                if idx < len(parts) and parts[idx].startswith('www.'):
                    website = 'https://' + parts[idx]
                    idx += 1
                
                address_parts = []
                while idx < len(parts) and not re.match(r'\+?\d', parts[idx]):
                    address_parts.append(parts[idx])
                    idx += 1
                address = ' '.join(address_parts)
                
                phone = None
                if idx < len(parts) and re.match(r'\+?\d', parts[idx]):
                    phone = parse_phone(parts[idx])
                    idx += 1
                
                core_contact = ''
                while idx < len(parts) and not ('后视镜' in parts[idx] or '车身' in parts[idx] or '外饰' in parts[idx] or '内饰' in parts[idx]):
                    core_contact += ' ' + parts[idx]
                    idx += 1
                core_contact = core_contact.strip()
                
                main_products = ''
                while idx < len(parts) and (('后视镜' in parts[idx]) or ('车身' in parts[idx]) or ('外饰' in parts[idx]) or ('内饰' in parts[idx]) or ('行李架' in parts[idx]) or ('尾翼' in parts[idx]) or ('格栅' in parts[idx]) or ('饰板' in parts[idx]) or ('饰条' in parts[idx]) or ('雾灯' in parts[idx]) or ('鲨鱼鳍' in parts[idx]) or ('侧裙' in parts[idx]) or ('门槛' in parts[idx]) or ('门饰' in parts[idx]) or ('中控' in parts[idx]) or ('扰流板' in parts[idx]) or ('备胎' in parts[idx]) or ('底护板' in parts[idx]) or ('立柱' in parts[idx])):
                    main_products += parts[idx] + ' '
                    idx += 1
                main_products = main_products.strip()
                
                market_parts = []
                while idx < len(parts) and not re.match(r'\d+', parts[idx]):
                    market_parts.append(parts[idx])
                    idx += 1
                main_market = ' '.join(market_parts)
                
                revenue = None
                if idx < len(parts) and re.match(r'\d+', parts[idx]):
                    revenue = parse_revenue(parts[idx])
                    idx += 1
                
                purchase_potential = ''
                while idx < len(parts) and ('极高' in parts[idx] or '高' in parts[idx] or '中等' in parts[idx] or '一般' in parts[idx] or '低' in parts[idx]):
                    purchase_potential += parts[idx]
                    idx += 1
                
                priority = ''
                while idx < len(parts):
                    priority += parts[idx]
                    idx += 1
                
                grade = parse_priority_to_grade(priority)
                score = parse_priority_to_score(priority)
                
                company = {
                    'company_name': company_name,
                    'website': website,
                    'address': address,
                    'phone': phone,
                    'core_contact': core_contact[:200],
                    'main_products': main_products[:500],
                    'main_market': main_market[:200],
                    'annual_revenue_usd': revenue,
                    'purchase_potential': purchase_potential,
                    'lead_grade': grade,
                    'lead_score': score,
                    'company_type': 'Distributor',
                    'country': 'Thailand',
                    'source': 'Industry_Directory',
                    'source_url': '豆包.txt',
                    'is_auto_parts_core': 1,
                    'is_importer_distributor': 1
                }
                companies_data.append(company)

def parse_report_txt():
    with open(r'E:\09.document\carparts\客户资料\泰国汽车配件客户分析报告.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    client_blocks = re.findall(r'【客户 \d+: ([^】]+)】(.*?)(?=【客户 \d+:|报告结束)', content, re.DOTALL)
    for company_name, details in client_blocks:
        company_name = company_name.strip()
        lines = details.strip().split('\n')
        
        website = None
        address = None
        phone = None
        email = None
        main_products = None
        main_market = None
        grade = 'C'
        score = 60
        
        for line in lines:
            line = line.strip()
            if line.startswith('等级:'):
                parts = line.split('|')
                for part in parts:
                    if '等级:' in part:
                        grade = part.split(':')[1].strip()
                    if '评分:' in part:
                        score = int(part.split(':')[1].strip())
            elif line.startswith('官网:'):
                website = line.split(':', 1)[1].strip()
            elif line.startswith('地址:'):
                address = line.split(':', 1)[1].strip()
            elif line.startswith('电话:'):
                phone = parse_phone(line.split(':', 1)[1].strip())
            elif line.startswith('邮箱:'):
                email = parse_email(line.split(':', 1)[1].strip())
            elif line.startswith('主营产品:'):
                main_products = line.split(':', 1)[1].strip()
            elif line.startswith('销售市场:'):
                main_market = line.split(':', 1)[1].strip()
        
        company = {
            'company_name': company_name,
            'website': website,
            'address': address,
            'phone': phone,
            'email': email,
            'main_products': main_products,
            'main_market': main_market,
            'lead_grade': grade,
            'lead_score': score,
            'company_type': 'Distributor',
            'country': 'Thailand',
            'source': 'Industry_Directory',
            'source_url': '泰国汽车配件客户分析报告.txt',
            'is_auto_parts_core': 1,
            'is_importer_distributor': 1
        }
        companies_data.append(company)

def deduplicate_companies():
    seen = set()
    unique = []
    for company in companies_data:
        name = company['company_name'].strip().lower().replace(' ', '')
        if name not in seen:
            seen.add(name)
            unique.append(company)
    return unique

def import_companies(conn):
    cursor = conn.cursor()
    
    insert_sql = """
    INSERT INTO p_company (
        company_name, website, address, phone, email,
        company_type, main_products, main_market,
        lead_score, lead_grade, core_contact,
        annual_revenue_usd, purchase_potential,
        country, status, source, source_url,
        is_auto_parts_core, is_importer_distributor
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
        source_url = CONCAT_WS('; ', source_url, VALUES(source_url)),
        updated_at = CURRENT_TIMESTAMP
    """
    
    inserted = 0
    updated = 0
    
    for company in companies_data:
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
    print("从客户资料文件夹导入公司数据到数据库")
    print("=" * 70)
    
    print("\n📥 正在解析各文件数据...")
    
    parse_gpt_txt()
    print(f"   gpt.txt: {len([c for c in companies_data if 'gpt.txt' in c.get('source_url', '')])} 条")
    
    parse_qianwen_txt()
    print(f"   千问.txt: {len([c for c in companies_data if '千问.txt' in c.get('source_url', '')])} 条")
    
    parse_huoqu_txt()
    print(f"   获取.txt: {len([c for c in companies_data if '获取.txt' in c.get('source_url', '')])} 条")
    
    parse_doubao_txt()
    print(f"   豆包.txt: {len([c for c in companies_data if '豆包.txt' in c.get('source_url', '')])} 条")
    
    parse_report_txt()
    print(f"   泰国汽车配件客户分析报告.txt: {len([c for c in companies_data if '分析报告' in c.get('source_url', '')])} 条")
    
    print(f"\n📊 原始数据总数: {len(companies_data)} 条")
    
    companies_data = deduplicate_companies()
    print(f"✅ 去重后数据总数: {len(companies_data)} 条")
    
    try:
        conn = connect_db()
        print("✅ 数据库连接成功")
        
        print("\n🚀 正在导入数据...")
        inserted, updated = import_companies(conn)
        
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
        print("\n🎉 所有数据导入完成！")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
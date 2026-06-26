import pymysql
import re
from urllib.parse import urlparse

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

def extract_domain(website):
    if not website:
        return None
    
    try:
        if not website.startswith('http'):
            website = 'https://' + website
        
        parsed = urlparse(website)
        domain = parsed.netloc
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain
    except:
        return None

def clean_company_name(name):
    if not name:
        return 'company'
    
    name = name.lower()
    
    suffixes = ['co., ltd.', 'co. ltd.', 'co ltd', 'co.,ltd', 'coltd', 
                'ltd.', 'ltd', 'public co., ltd.', 'public company limited',
                'plc', 'limited', 'inc.', 'inc', 'corp.', 'corp']
    
    for suffix in suffixes:
        name = name.replace(suffix, '')
    
    name = name.replace(',', '').replace('.', '')
    name = re.sub(r'\s+', ' ', name).strip()
    
    replacements = {
        ' & ': 'and',
        ' + ': 'plus',
        ' - ': '-',
        '(': '',
        ')': '',
        "'": '',
        '"': '',
    }
    for old, new in replacements.items():
        name = name.replace(old, new)
    
    name = re.sub(r'[^a-z0-9\-]', '', name.replace(' ', '-'))
    
    return name[:30]

def generate_email_from_website(website):
    domain = extract_domain(website)
    if not domain:
        return None
    
    common_prefixes = ['info', 'contact', 'sales', 'support', 'service', 'auto', 'parts']
    
    for prefix in common_prefixes:
        email = f'{prefix}@{domain}'
        return email
    
    return f'contact@{domain}'

def generate_email_from_name(name):
    clean_name = clean_company_name(name)
    if not clean_name:
        return None
    
    email_formats = [
        f'{clean_name}@gmail.com',
        f'{clean_name}@yahoo.com',
        f'{clean_name}@hotmail.com',
        f'{clean_name}@outlook.com',
        f'{clean_name}@thailand.com',
    ]
    
    return email_formats[0]

def generate_email(company_name, website):
    if website and website != '':
        email = generate_email_from_website(website)
        if email:
            return email, 'website'
    
    if company_name and company_name != '':
        email = generate_email_from_name(company_name)
        if email:
            return email, 'name'
    
    return None, 'none'

def update_emails(conn):
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, company_name, website, email 
        FROM p_company 
        WHERE email IS NULL OR email = ''
    """)
    
    companies = cursor.fetchall()
    print(f"需要生成邮箱的记录: {len(companies)}")
    
    updated_count = 0
    website_count = 0
    name_count = 0
    
    for company in companies:
        id, company_name, website, email = company
        
        generated_email, source = generate_email(company_name, website)
        
        if generated_email:
            try:
                cursor.execute("""
                    UPDATE p_company 
                    SET email = %s 
                    WHERE id = %s
                """, (generated_email, id))
                
                updated_count += 1
                if source == 'website':
                    website_count += 1
                else:
                    name_count += 1
                
                if updated_count % 20 == 0:
                    conn.commit()
                    print(f"已生成 {updated_count} 个邮箱...")
                    
            except Exception as e:
                print(f"❌ 更新失败 (ID:{id}): {company_name} - {e}")
    
    conn.commit()
    print(f"\n✅ 共生成 {updated_count} 个邮箱")
    print(f"  从网站域名生成: {website_count} 个")
    print(f"  从公司名称生成: {name_count} 个")
    cursor.close()

def verify_update(conn):
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM p_company WHERE email IS NULL OR email = ''")
    no_email = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM p_company WHERE email IS NOT NULL AND email != ''")
    has_email = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT id, company_name, website, email 
        FROM p_company 
        WHERE email IS NOT NULL AND email != '' 
        ORDER BY id DESC LIMIT 10
    """)
    recent = cursor.fetchall()
    
    print(f"\n📊 验证结果:")
    print(f"  有邮箱: {has_email} 条")
    print(f"  无邮箱: {no_email} 条")
    
    print("\n📝 新生成邮箱示例:")
    for row in recent:
        id, name, website, email = row
        print(f"  ID:{id} | {name[:35]}...")
        print(f"     网站: {website[:30] if website else '无'}")
        print(f"     邮箱: {email}")
    
    cursor.close()

if __name__ == '__main__':
    print("=" * 60)
    print("正在为无邮箱的公司生成邮箱地址...")
    print("=" * 60)
    
    try:
        conn = connect_db()
        print("✅ 数据库连接成功")
        
        update_emails(conn)
        verify_update(conn)
        
        conn.close()
        print("\n🎉 邮箱生成完成！")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
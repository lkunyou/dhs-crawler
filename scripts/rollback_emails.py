import pymysql

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

def is_auto_generated_email(email, website):
    if not email:
        return False
    
    auto_prefixes = ['info@', 'contact@', 'sales@', 'support@', 'service@', 'auto@', 'parts@']
    
    if any(email.startswith(prefix) for prefix in auto_prefixes):
        return True
    
    free_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'thailand.com']
    for domain in free_domains:
        if domain in email:
            return True
    
    if website and '@' in email:
        domain = email.split('@')[1]
        if domain in website:
            return True
    
    return False

def rollback_emails(conn):
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, company_name, website, email 
        FROM p_company 
        WHERE email IS NOT NULL AND email != ''
    """)
    
    companies = cursor.fetchall()
    
    rollback_count = 0
    keep_count = 0
    
    for company in companies:
        id, company_name, website, email = company
        
        if is_auto_generated_email(email, website):
            cursor.execute("""
                UPDATE p_company 
                SET email = NULL 
                WHERE id = %s
            """, (id,))
            rollback_count += 1
        else:
            keep_count += 1
        
        if rollback_count % 20 == 0:
            conn.commit()
            print(f"已回滚 {rollback_count} 个邮箱...")
    
    conn.commit()
    print(f"\n✅ 共回滚 {rollback_count} 个自动生成的邮箱")
    print(f"   保留原有的邮箱: {keep_count} 个")
    cursor.close()

def verify_rollback(conn):
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM p_company WHERE email IS NULL OR email = ''")
    no_email = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM p_company WHERE email IS NOT NULL AND email != ''")
    has_email = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT id, company_name, email 
        FROM p_company 
        WHERE email IS NOT NULL AND email != '' 
        LIMIT 10
    """)
    remaining = cursor.fetchall()
    
    print(f"\n📊 回滚验证结果:")
    print(f"  有邮箱: {has_email} 条")
    print(f"  无邮箱: {no_email} 条")
    
    print("\n📝 保留的原有邮箱示例:")
    for row in remaining:
        id, name, email = row
        print(f"  ID:{id} | {name[:35]}... | 邮箱:{email}")
    
    cursor.close()

if __name__ == '__main__':
    print("=" * 60)
    print("正在回滚自动生成的邮箱...")
    print("=" * 60)
    
    try:
        conn = connect_db()
        print("✅ 数据库连接成功")
        
        rollback_emails(conn)
        verify_rollback(conn)
        
        conn.close()
        print("\n🎉 邮箱回滚完成！")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
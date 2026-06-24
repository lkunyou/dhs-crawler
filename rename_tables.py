import mysql.connector
import sys

config = {
    'host': '8.163.58.109',
    'port': 3306,
    'user': 'carparts_dhs',
    'password': 'tDdY8NX2xJ6HpdHz',
    'database': 'carparts_dhs'
}

tables_to_rename = [
    ('company', 'p_company'),
    ('contact_person', 'p_contact_person'),
    ('product_interest', 'p_product_interest'),
    ('email_campaign', 'p_email_campaign'),
    ('email_template', 'p_email_template'),
    ('email_record', 'p_email_record'),
    ('whatsapp_record', 'p_whatsapp_record'),
    ('linkedin_record', 'p_linkedin_record'),
    ('follow_up_record', 'p_follow_up_record'),
    ('task', 'p_task'),
    ('quotation', 'p_quotation'),
    ('crawler_task', 'p_crawler_task'),
    ('daily_stats', 'p_daily_stats'),
    ('system_config', 'p_system_config'),
]

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    
    cursor.execute("SET FOREIGN_KEY_CHECKS=0")
    
    success = 0
    skipped = 0
    
    for old_name, new_name in tables_to_rename:
        try:
            # 检查旧表是否存在
            cursor.execute(f"SHOW TABLES LIKE '{old_name}'")
            if cursor.fetchone():
                # 检查新表是否已存在
                cursor.execute(f"SHOW TABLES LIKE '{new_name}'")
                if cursor.fetchone():
                    print(f"跳过: {new_name} 已存在")
                    skipped += 1
                else:
                    cursor.execute(f"RENAME TABLE `{old_name}` TO `{new_name}`")
                    print(f"重命名: {old_name} -> {new_name}")
                    success += 1
            else:
                print(f"跳过: {old_name} 不存在")
                skipped += 1
        except Exception as e:
            print(f"错误 [{old_name} -> {new_name}]: {e}")
    
    cursor.execute("SET FOREIGN_KEY_CHECKS=1")
    conn.commit()
    
    print(f"\n完成: 成功 {success} 个, 跳过 {skipped} 个")
    
    # 验证
    cursor.execute("SHOW TABLES LIKE 'p_%'")
    tables = cursor.fetchall()
    print(f"\np_开头的表 ({len(tables)} 个):")
    for t in tables:
        print(f"  - {t[0]}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"连接失败: {e}")
    sys.exit(1)

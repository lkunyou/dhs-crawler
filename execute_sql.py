import mysql.connector
import sys
import re

config = {
    'host': '8.163.58.109',
    'port': 3306,
    'user': 'carparts_dhs',
    'password': 'tDdY8NX2xJ6HpdHz',
    'database': 'carparts_dhs'
}

def split_sql_statements(sql_text):
    """智能分割SQL语句，处理字符串内的分号"""
    statements = []
    current = []
    in_string = False
    string_char = None
    i = 0
    
    while i < len(sql_text):
        char = sql_text[i]
        
        # 处理注释
        if not in_string and char == '-' and i + 1 < len(sql_text) and sql_text[i + 1] == '-':
            # 跳过单行注释
            while i < len(sql_text) and sql_text[i] != '\n':
                i += 1
            continue
        
        if not in_string and char == '/' and i + 1 < len(sql_text) and sql_text[i + 1] == '*':
            # 跳过多行注释
            i += 2
            while i + 1 < len(sql_text) and not (sql_text[i] == '*' and sql_text[i + 1] == '/'):
                i += 1
            i += 2
            continue
        
        if not in_string and char in ("'", '"'):
            in_string = True
            string_char = char
            current.append(char)
        elif in_string and char == string_char:
            # 检查是否是转义
            if i + 1 < len(sql_text) and sql_text[i + 1] == string_char:
                current.append(char)
                current.append(sql_text[i + 1])
                i += 2
                continue
            in_string = False
            current.append(char)
        elif not in_string and char == ';':
            stmt = ''.join(current).strip()
            if stmt:
                statements.append(stmt)
            current = []
        else:
            current.append(char)
        
        i += 1
    
    # 处理最后一条
    stmt = ''.join(current).strip()
    if stmt:
        statements.append(stmt)
    
    return statements

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    
    # 设置字符集
    cursor.execute("SET NAMES utf8mb4")
    cursor.execute("SET CHARACTER SET utf8mb4")
    cursor.execute("SET FOREIGN_KEY_CHECKS=0")
    
    with open(r'E:\01.work\13.carparts\sprider1\thai-auto-parts-crm\database\schema.sql', 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # 替换不兼容的排序规则
    sql_content = sql_content.replace('utf8mb4_0900_ai_ci', 'utf8mb4_unicode_ci')
    
    # 移除 CREATE DATABASE 和 USE 语句
    sql_content = re.sub(r'CREATE DATABASE.*?;', '', sql_content, flags=re.DOTALL)
    sql_content = re.sub(r'USE .*?;', '', sql_content)
    
    # 智能分割SQL
    statements = split_sql_statements(sql_content)
    
    success = 0
    errors = 0
    
    for idx, stmt in enumerate(statements, 1):
        stmt = stmt.strip()
        if not stmt:
            continue
        
        try:
            cursor.execute(stmt)
            success += 1
            if idx % 5 == 0:
                print(f"已执行 {idx}/{len(statements)} 条...")
        except Exception as e:
            error_msg = str(e).lower()
            if any(kw in error_msg for kw in ['already exists', 'duplicate', 'errno: 1050', 'errno: 1061', 'errno: 1007']):
                success += 1
            else:
                print(f"Error [{idx}]: {e}")
                print(f"Statement: {stmt[:200]}...")
                errors += 1
    
    cursor.execute("SET FOREIGN_KEY_CHECKS=1")
    conn.commit()
    print(f"\nSQL执行完成: 成功 {success} 条, 失败 {errors} 条")
    
    # 验证表
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print(f"\n已创建的表 ({len(tables)} 个):")
    for table in tables:
        print(f"  - {table[0]}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"连接失败: {e}")
    sys.exit(1)

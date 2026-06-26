import pymysql
import re
import difflib

DB_HOST = '8.163.58.109'
DB_PORT = 3306
DB_USER = 'thai_auto_parts_crm'
DB_PASSWORD = 'tDdY8NX2xJ6HpdHz'
DB_NAME = 'thai_auto_parts_crm'

conn = pymysql.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    charset='utf8mb4'
)

cursor = conn.cursor()

cursor.execute("SELECT company_name FROM p_company ORDER BY company_name")
db_names = [row[0] for row in cursor.fetchall()]

with open(r'E:\09.document\carparts\泰国汽车配件客户分析报告.txt', 'r', encoding='utf-8') as f:
    content = f.read()

report_names = re.findall(r'【客户 \d+: (.*?)】', content)

print("报告中的公司名称:")
print("-" * 60)
for name in report_names:
    print(f"  {name}")

print("\n数据库中的公司名称:")
print("-" * 60)
for name in db_names:
    print(f"  {name}")

print("\n尝试模糊匹配:")
print("-" * 60)

matched_pairs = []
unmatched_report = []

for report_name in report_names:
    best_match = None
    best_score = 0
    
    cleaned_report = re.sub(r'\(.*?\)', '', report_name).strip().lower()
    
    for db_name in db_names:
        cleaned_db = re.sub(r'\(.*?\)', '', db_name).strip().lower()
        
        score = difflib.SequenceMatcher(None, cleaned_report, cleaned_db).ratio()
        
        if score > best_score and score >= 0.7:
            best_score = score
            best_match = db_name
    
    if best_match:
        matched_pairs.append((report_name, best_match, best_score))
    else:
        unmatched_report.append(report_name)

print("匹配成功:")
for report, db, score in matched_pairs:
    print(f"  {score:.2f} | 报告: {report[:40]} -> 数据库: {db[:40]}")

print("\n未匹配到:")
for name in unmatched_report:
    print(f"  {name}")

conn.close()
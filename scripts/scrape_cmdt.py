import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.beiei.com/cmdt-codes-directory.html'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

data = []
current_section = ''
current_chapter = ''

for element in soup.find_all(['h3', 'h4', 'p', 'div', 'tr', 'td']):
    text = element.get_text(strip=True)
    if not text:
        continue
    
    if '类' in text and 'HS Code' in text:
        match = re.match(r'第(\d+)类\s*-\s*(.+?)\s*\(.*?\)', text)
        if match:
            current_section = text
            continue
    
    if '-' in text and ('HS Code' in text or len(text) < 50):
        match = re.match(r'(\d{2})\s*-\s*(.+?)\s*\(.*?\)', text)
        if match:
            current_chapter = text
            continue
    
    code_match = re.match(r'(\d{6})\s*-\s*(.+)$', text)
    if code_match:
        code = code_match.group(1)
        description = code_match.group(2)
        
        description_en = description.split(' - ')[0] if ' - ' in description else description
        description_cn = description.split(' - ')[1] if ' - ' in description else ''
        
        data.append({
            'section': current_section,
            'chapter': current_chapter,
            'cmdt_code': code,
            'description_en': description_en,
            'description_cn': description_cn
        })

print(f"共解析到 {len(data)} 条CMDT编码记录")
print("\n前10条示例:")
for item in data[:10]:
    print(f"  {item['cmdt_code']} | {item['description_en'][:40]} | {item['description_cn'][:30]}")

with open('cmdt_data.txt', 'w', encoding='utf-8') as f:
    for item in data:
        f.write(f"{item['section']}\t{item['chapter']}\t{item['cmdt_code']}\t{item['description_en']}\t{item['description_cn']}\n")

print(f"\n数据已保存到 cmdt_data.txt")
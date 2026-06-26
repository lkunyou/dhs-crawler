import requests
import json
import time
import random
import pymysql
from typing import List, Dict, Optional

DB_HOST = '8.163.58.109'
DB_PORT = 3306
DB_USER = 'thai_auto_parts_crm'
DB_PASSWORD = 'tDdY8NX2xJ6HpdHz'
DB_NAME = 'thai_auto_parts_crm'

SERP_API_KEY = ''
BRAVE_API_KEY = ''

search_keywords = [
    'Thailand auto parts distributor',
    'Thailand car parts importer',
    'Bangkok auto parts wholesale',
    'Thailand automotive aftermarket distributor',
    'Thai auto parts trading company',
    'Thailand car accessories distributor',
    'Thailand automotive spare parts importer',
    'Thailand auto body parts distributor',
    'Thailand Toyota parts distributor',
    'Thailand Isuzu parts distributor',
    'Thailand Mitsubishi parts distributor',
    'Thailand Honda parts distributor',
    'Thailand Ford parts distributor',
    'Thailand Nissan parts distributor',
    'Thailand pickup truck parts distributor',
    'Thailand automotive exterior parts distributor',
    'Thailand automotive interior parts distributor',
]

def search_serpapi(query: str, page: int = 1) -> List[Dict]:
    if not SERP_API_KEY:
        return []
    
    url = "https://serpapi.com/search.json"
    params = {
        "q": query,
        "api_key": SERP_API_KEY,
        "engine": "google",
        "hl": "en",
        "gl": "th",
        "start": (page - 1) * 10,
        "num": 10
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        results = []
        
        if 'organic_results' in data:
            for item in data['organic_results']:
                results.append({
                    'title': item.get('title', ''),
                    'link': item.get('link', ''),
                    'snippet': item.get('snippet', ''),
                    'source': 'SerpAPI'
                })
        
        if 'local_results' in data:
            for item in data['local_results']:
                results.append({
                    'title': item.get('title', ''),
                    'link': item.get('link', ''),
                    'snippet': item.get('description', ''),
                    'address': item.get('address', ''),
                    'phone': item.get('phone', ''),
                    'source': 'SerpAPI_Local'
                })
        
        return results
    except Exception as e:
        print(f"SerpAPI搜索失败: {e}")
        return []

def search_brave(query: str) -> List[Dict]:
    if not BRAVE_API_KEY:
        return []
    
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": BRAVE_API_KEY
    }
    params = {
        "q": query,
        "count": 10,
        "country": "TH"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        results = []
        
        if 'web' in data and 'results' in data['web']:
            for item in data['web']['results']:
                results.append({
                    'title': item.get('title', ''),
                    'link': item.get('url', ''),
                    'snippet': item.get('description', ''),
                    'source': 'Brave'
                })
        
        return results
    except Exception as e:
        print(f"Brave搜索失败: {e}")
        return []

def search_google_direct(query: str) -> List[Dict]:
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": "",
        "cx": "",
        "num": 10,
        "gl": "th"
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        results = []
        
        if 'items' in data:
            for item in data['items']:
                results.append({
                    'title': item.get('title', ''),
                    'link': item.get('link', ''),
                    'snippet': item.get('snippet', ''),
                    'source': 'Google_CSE'
                })
        
        return results
    except Exception as e:
        print(f"Google CSE搜索失败: {e}")
        return []

def extract_company_info(title: str, link: str, snippet: str) -> Dict:
    company_name = title.replace('-', ' ').replace('|', ' ').split('|')[0].split('-')[0].strip()
    company_name = company_name.replace('Thailand', '').replace('Thai', '').strip()
    
    website = link
    if 'www.' not in website and 'http' in website:
        parts = website.split('/')
        if len(parts) >= 3:
            website = f"{parts[0]}//{parts[2]}"
    
    phone = None
    for word in snippet.split():
        if word.startswith('+66') or word.startswith('+66-'):
            phone = word.replace('-', '').replace('(', '').replace(')', '')
            break
        elif word.startswith('02') and len(word) >= 8:
            phone = '+66' + word[1:]
            break
    
    email = None
    for word in snippet.split():
        if '@' in word and '.' in word:
            email = word.replace('.com,', '.com').replace('.co.th,', '.co.th').strip('.,')
            break
    
    address = None
    if 'Bangkok' in snippet or 'Thailand' in snippet:
        address = snippet[:200]
    
    main_products = ''
    if 'auto parts' in snippet.lower() or 'car parts' in snippet.lower():
        main_products = 'Auto Parts'
    if 'exterior' in snippet.lower():
        main_products += '; Exterior Parts'
    if 'interior' in snippet.lower():
        main_products += '; Interior Parts'
    if 'body parts' in snippet.lower():
        main_products += '; Body Parts'
    if 'mirror' in snippet.lower():
        main_products += '; Mirrors'
    if 'grille' in snippet.lower():
        main_products += '; Grilles'
    if 'bumper' in snippet.lower():
        main_products += '; Bumpers'
    
    main_market = 'Thailand'
    if 'Southeast Asia' in snippet or 'ASEAN' in snippet:
        main_market += ', Southeast Asia'
    if 'export' in snippet.lower() or 'global' in snippet.lower():
        main_market += ', Global'
    
    return {
        'company_name': company_name,
        'website': website,
        'phone': phone,
        'email': email,
        'address': address,
        'main_products': main_products.strip('; '),
        'main_market': main_market,
        'snippet': snippet[:300]
    }

def evaluate_company(info: Dict) -> Dict:
    score = 0
    details = {}
    
    details['import_ability'] = 20
    if 'importer' in info.get('snippet', '').lower() or 'import' in info.get('snippet', '').lower():
        details['import_ability'] = 25
    
    details['purchase_scale'] = 15
    if 'wholesale' in info.get('snippet', '').lower() or 'distributor' in info.get('snippet', '').lower():
        details['purchase_scale'] = 22
    if 'large' in info.get('snippet', '').lower() or 'big' in info.get('snippet', '').lower():
        details['purchase_scale'] = 24
    
    details['china_supplier_acceptance'] = 15
    if 'China' in info.get('snippet', '') or 'Chinese' in info.get('snippet', ''):
        details['china_supplier_acceptance'] = 18
    
    details['oem_aftermarket_match'] = 12
    if 'OEM' in info.get('snippet', '') or 'aftermarket' in info.get('snippet', '').lower():
        details['oem_aftermarket_match'] = 14
    
    details['export_ability'] = 5
    if 'export' in info.get('snippet', '').lower() or 'international' in info.get('snippet', '').lower():
        details['export_ability'] = 8
    
    details['customization_match'] = 3
    if 'custom' in info.get('snippet', '').lower() or 'OEM' in info.get('snippet', ''):
        details['customization_match'] = 4
    
    score = sum(details.values())
    
    if score >= 85:
        lead_grade = 'S'
    elif score >= 75:
        lead_grade = 'A'
    elif score >= 60:
        lead_grade = 'B'
    else:
        lead_grade = 'C'
    
    return {
        'lead_score': score,
        'lead_grade': lead_grade,
        **details
    }

def generate_analysis(info: Dict, eval_result: Dict) -> Dict:
    analysis = {}
    
    analysis['quality_requirement'] = 'OEM grade, JIS/BS standards'
    if 'OEM' in info.get('snippet', ''):
        analysis['quality_requirement'] = 'Strict OEM quality standards'
    
    analysis['price_sensitivity'] = 'Medium'
    if 'price' in info.get('snippet', '').lower() or 'cost' in info.get('snippet', '').lower():
        analysis['price_sensitivity'] = 'High'
    
    analysis['delivery_requirement'] = 'Medium'
    if 'fast' in info.get('snippet', '').lower() or 'quick' in info.get('snippet', '').lower():
        analysis['delivery_requirement'] = 'Fast'
    
    analysis['accept_china_factory'] = '是'
    if 'China' in info.get('snippet', ''):
        analysis['accept_china_factory'] = '是'
    
    analysis['customization_ability'] = 'Medium'
    if 'custom' in info.get('snippet', '').lower() or 'OEM' in info.get('snippet', ''):
        analysis['customization_ability'] = 'Strong'
    
    analysis['after_sales_requirement'] = 'Standard'
    if 'service' in info.get('snippet', '').lower() or 'support' in info.get('snippet', '').lower():
        analysis['after_sales_requirement'] = 'High'
    
    analysis['supply_chain_pain_points'] = 'Seeking reliable suppliers, cost optimization'
    
    recommended = 'Mirror housings, grilles, fog lamp covers'
    if 'exterior' in info.get('snippet', '').lower():
        recommended += ', exterior body parts'
    if 'interior' in info.get('snippet', '').lower():
        recommended += ', interior trim'
    analysis['recommended_products'] = recommended
    
    analysis['recommended_channels'] = 'Email + WhatsApp'
    analysis['first_email_strategy'] = f"Focus on {analysis['recommended_products']} with OEM quality and 30% cost savings"
    
    return analysis

def save_to_db(companies: List[Dict]):
    conn = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    
    inserted = 0
    for company in companies:
        try:
            sql = """
INSERT IGNORE INTO p_company (
    company_name, website, address, phone, email, company_type,
    main_products, main_market, lead_score, lead_grade,
    import_ability, purchase_scale, china_supplier_acceptance,
    oem_aftermarket_match, export_ability, customization_match,
    quality_requirement, price_sensitivity, delivery_requirement,
    accept_china_factory, customization_ability, after_sales_requirement,
    supply_chain_pain_points, recommended_products, recommended_channels,
    first_email_strategy, country, status, source,
    is_auto_parts_core, is_importer_distributor, employee_count
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                company.get('company_name', ''),
                company.get('website', ''),
                company.get('address', ''),
                company.get('phone', ''),
                company.get('email', ''),
                'Distributor',
                company.get('main_products', ''),
                company.get('main_market', ''),
                company.get('lead_score', 0),
                company.get('lead_grade', 'B'),
                company.get('import_ability', 0),
                company.get('purchase_scale', 0),
                company.get('china_supplier_acceptance', 0),
                company.get('oem_aftermarket_match', 0),
                company.get('export_ability', 0),
                company.get('customization_match', 0),
                company.get('quality_requirement', ''),
                company.get('price_sensitivity', ''),
                company.get('delivery_requirement', ''),
                company.get('accept_china_factory', ''),
                company.get('customization_ability', ''),
                company.get('after_sales_requirement', ''),
                company.get('supply_chain_pain_points', ''),
                company.get('recommended_products', ''),
                company.get('recommended_channels', ''),
                company.get('first_email_strategy', ''),
                'Thailand',
                'New',
                'API',
                1,
                1,
                '100-500'
            )
            cursor.execute(sql, values)
            inserted += 1
        except Exception as e:
            print(f"保存失败 {company.get('company_name')}: {e}")
    
    conn.commit()
    cursor.close()
    conn.close()
    print(f"\n✅ 成功保存 {inserted} 条记录到数据库")

def main():
    print("=" * 70)
    print("泰国汽车配件经销商搜索工具")
    print("=" * 70)
    
    all_results = []
    seen_links = set()
    
    for i, keyword in enumerate(search_keywords, 1):
        print(f"\n[{i}/{len(search_keywords)}] 搜索: {keyword}")
        
        results = search_serpapi(keyword)
        results.extend(search_brave(keyword))
        results.extend(search_google_direct(keyword))
        
        print(f"  找到 {len(results)} 条结果")
        
        for result in results:
            link = result.get('link', '')
            if link in seen_links:
                continue
            seen_links.add(link)
            
            info = extract_company_info(
                result.get('title', ''),
                result.get('link', ''),
                result.get('snippet', '')
            )
            
            if not info['company_name'] or len(info['company_name']) < 3:
                continue
            
            eval_result = evaluate_company(info)
            analysis = generate_analysis(info, eval_result)
            
            company = {**info, **eval_result, **analysis}
            all_results.append(company)
        
        time.sleep(random.uniform(2, 5))
    
    print(f"\n{'='*70}")
    print(f"共找到 {len(all_results)} 家公司")
    
    sorted_companies = sorted(all_results, key=lambda x: x['lead_score'], reverse=True)
    
    print("\n\n📋 客户分析报告")
    print("=" * 70)
    print(f"{'排名':<4} | {'公司名称':<40} | {'评分':<6} | {'等级':<4} | {'主营产品':<30}")
    print("-" * 120)
    
    for i, company in enumerate(sorted_companies[:30], 1):
        print(f"{i:<4} | {company['company_name'][:40]:<40} | {company['lead_score']:<6} | {company['lead_grade']:<4} | {company['main_products'][:30]:<30}")
    
    save_to_db(sorted_companies)
    
    print("\n\n📊 统计分析")
    print("=" * 70)
    
    grades = {'S': 0, 'A': 0, 'B': 0, 'C': 0}
    for c in sorted_companies:
        grades[c['lead_grade']] += 1
    
    print("\n客户等级分布:")
    for grade, count in grades.items():
        print(f"  {grade}: {count} 家 ({count/len(sorted_companies)*100:.1f}%)")
    
    avg_score = sum(c['lead_score'] for c in sorted_companies) / len(sorted_companies)
    print(f"\n平均评分: {avg_score:.1f}")
    
    print("\n\n🎯 采购关注点分析")
    print("=" * 70)
    print("1. 产品质量要求: OEM级别，JIS/BS标准，UV耐候性，高温高湿适应")
    print("2. 使用寿命: 原厂件同等寿命，至少2-3年质保")
    print("3. 交货周期: 快交期，常备库存，灵活MOQ")
    print("4. 定制化能力: OEM定制，模具开发，快速打样")
    print("5. 售后服务: 无缺陷政策，质量追溯，退换货，技术指导")
    print("6. 价格竞争力: 比日本原厂低30-40%，稳定批量价格")

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Maps爬虫 - 泰国汽配客户抓取
"""

import sys
import json
import time
import random
import requests
from urllib.parse import quote_plus


class GoogleMapsCrawler:
    
    def __init__(self, task_id, keywords, target_city, target_country="Thailand"):
        self.task_id = task_id
        self.keywords = keywords
        self.target_city = target_city
        self.target_country = target_country
        self.results = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    
    def search(self, keyword):
        """搜索Google Maps"""
        try:
            query = f"{keyword} {self.target_city} {self.target_country}"
            url = f"https://www.google.com/maps/search/{quote_plus(query)}"
            
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            import re
            matches = re.findall(r'"name":"([^"]+)"', response.text)
            
            companies = []
            for name in matches[:50]:
                if name and len(name) > 2:
                    companies.append({
                        'companyName': name,
                        'city': self.target_city,
                        'country': self.target_country,
                        'source': 'Google_Maps',
                        'sourceKeyword': keyword
                    })
            
            return companies
        except Exception as e:
            print(f"搜索失败 {keyword}: {e}", file=sys.stderr)
            return []
    
    def crawl(self):
        """执行完整爬取流程"""
        for i, keyword in enumerate(self.keywords):
            progress = int((i + 1) / len(self.keywords) * 50)
            print(f"PROGRESS:{progress}")
            sys.stdout.flush()
            
            companies = self.search(keyword)
            self.results.extend(companies)
            
            progress = int((i + 1) / len(self.keywords) * 100)
            print(f"PROGRESS:{progress}")
            print(f"FOUND:{len(companies)}")
            sys.stdout.flush()
            
            time.sleep(random.uniform(2, 5))
        
        total_found = len(self.results)
        new_companies = total_found
        
        print(f"FINISHED:{json.dumps({
            'totalFound': total_found,
            'newCompanies': new_companies,
            'duplicates': 0,
            'companies': self.results[:50]
        }, ensure_ascii=False)}")
        sys.stdout.flush()


def main():
    if len(sys.argv) < 2:
        print("Usage: python google_maps_crawler.py <task_id>")
        sys.exit(1)
    
    task_id = sys.argv[1]
    
    try:
        with open(f'/tmp/crawler_task_{task_id}.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        keywords = config.get('keywords', [])
        target_city = config.get('targetCity', 'Bangkok')
        target_country = config.get('targetCountry', 'Thailand')
        
        crawler = GoogleMapsCrawler(task_id, keywords, target_city, target_country)
        crawler.crawl()
        
    except Exception as e:
        print(f"爬虫执行失败: {e}", file=sys.stderr)
        print(f"FINISHED:{json.dumps({
            'totalFound': 0,
            'newCompanies': 0,
            'duplicates': 0,
            'error': str(e)
        })}")
        sys.exit(1)


if __name__ == '__main__':
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn爬虫 - 泰国汽配行业联系人抓取
"""

import sys
import json
import time
import random
import requests


class LinkedInCrawler:
    
    def __init__(self, task_id, titles, company_keywords, target_country="Thailand"):
        self.task_id = task_id
        self.titles = titles
        self.company_keywords = company_keywords
        self.target_country = target_country
        self.results = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9'
        }
    
    def search(self, title):
        """搜索LinkedIn"""
        try:
            query = f"{title} {self.target_country}"
            url = f"https://www.linkedin.com/voyager/api/search/blended?q=all&query=(keywords:{query})"
            
            response = requests.get(url, headers=self.headers, timeout=30)
            
            contacts = []
            if response.status_code == 200:
                try:
                    data = response.json()
                    elements = data.get('data', {}).get('elements', [])
                    for element in elements[:20]:
                        try:
                            profile = element.get('entityResult', {})
                            if profile:
                                contact = {
                                    'fullName': profile.get('title', {}).get('text', ''),
                                    'jobTitle': profile.get('primarySubtitle', {}).get('text', ''),
                                    'companyName': profile.get('secondarySubtitle', {}).get('text', ''),
                                    'source': 'LinkedIn',
                                    'sourceKeyword': title
                                }
                                contacts.append(contact)
                        except:
                            continue
            else:
                print(f"LinkedIn API返回状态码: {response.status_code}", file=sys.stderr)
            
            return contacts
        except Exception as e:
            print(f"搜索失败 {title}: {e}", file=sys.stderr)
            return []
    
    def crawl(self):
        """执行完整爬取流程"""
        for i, title in enumerate(self.titles):
            progress = int((i + 1) / len(self.titles) * 50)
            print(f"PROGRESS:{progress}")
            sys.stdout.flush()
            
            contacts = self.search(title)
            self.results.extend(contacts)
            
            progress = int((i + 1) / len(self.titles) * 100)
            print(f"PROGRESS:{progress}")
            print(f"FOUND:{len(contacts)}")
            sys.stdout.flush()
            
            time.sleep(random.uniform(3, 6))
        
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
        print("Usage: python linkedin_crawler.py <task_id>")
        sys.exit(1)
    
    task_id = sys.argv[1]
    
    try:
        with open(f'/tmp/crawler_task_{task_id}.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        titles = config.get('keywords', [])
        company_keywords = config.get('filters', {}).get('companyKeywords', [])
        target_country = config.get('targetCountry', 'Thailand')
        
        crawler = LinkedInCrawler(task_id, titles, company_keywords, target_country)
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
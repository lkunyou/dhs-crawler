#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google搜索爬虫 - 泰国汽配客户抓取
"""

import sys
import json
import time
import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus


class GoogleSearchCrawler:
    
    def __init__(self, task_id, keywords, target_country="Thailand", max_results=50):
        self.task_id = task_id
        self.keywords = keywords
        self.target_country = target_country
        self.max_results = max_results
        self.results = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
    def search(self, keyword):
        """执行单次搜索"""
        try:
            query = f"{keyword} {self.target_country}"
            url = f"https://www.google.com/search?q={quote_plus(query)}&num={self.max_results}"
            
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all('div', class_='g')
            
            companies = []
            for result in results[:min(self.max_results, len(results))]:
                try:
                    title_tag = result.find('h3')
                    title = title_tag.get_text(strip=True) if title_tag else ""
                    
                    link_tag = result.find('a')
                    link = link_tag['href'] if link_tag and 'href' in link_tag.attrs else ""
                    
                    snippet_tag = result.find('span', class_='aCOpRe')
                    snippet = snippet_tag.get_text(strip=True) if snippet_tag else ""
                    
                    if title and link:
                        companies.append({
                            'companyName': title,
                            'website': link,
                            'description': snippet,
                            'source': 'Google_Search',
                            'sourceKeyword': keyword
                        })
                except Exception as e:
                    continue
            
            return companies
        except Exception as e:
            print(f"搜索失败 {keyword}: {e}", file=sys.stderr)
            return []
    
    def crawl(self):
        """执行完整爬取流程"""
        total_found = 0
        new_companies = 0
        
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
        print("Usage: python google_crawler.py <task_id>")
        sys.exit(1)
    
    task_id = sys.argv[1]
    
    try:
        with open(f'/tmp/crawler_task_{task_id}.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        keywords = config.get('keywords', [])
        target_country = config.get('targetCountry', 'Thailand')
        max_results = config.get('maxResults', 50)
        
        crawler = GoogleSearchCrawler(task_id, keywords, target_country, max_results)
        crawler.crawl()
        
    except FileNotFoundError:
        print(f"配置文件未找到: /tmp/crawler_task_{task_id}.json", file=sys.stderr)
        print(f"FINISHED:{json.dumps({
            'totalFound': 0,
            'newCompanies': 0,
            'duplicates': 0,
            'error': 'Config file not found'
        })}")
        sys.exit(1)
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
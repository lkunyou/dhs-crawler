#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Maps爬虫 - 泰国汽配客户抓取
"""

import sys
import json
import time
import random
import os
import requests
from urllib.parse import quote_plus

# Disable proxy
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''
os.environ['NO_PROXY'] = '*'


class GoogleMapsCrawler:
    
    def __init__(self, task_id, keywords, target_city, target_country="Thailand"):
        self.task_id = task_id
        self.keywords = keywords
        self.target_city = target_city
        self.target_country = target_country
        self.results = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        })
        # Rate limiting config
        self.min_delay = 3  # minimum seconds between requests
        self.max_delay = 8  # maximum seconds between requests
        self.max_retries = 3
        self.retry_delay = 10  # initial retry delay in seconds
    
    def search(self, keyword, retry_count=0):
        """搜索Google Maps，带重试和速率控制"""
        try:
            query = f"{keyword} {self.target_city} {self.target_country}"
            url = f"https://www.google.com/maps/search/{quote_plus(query)}"
            
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Check if we got blocked (captcha or rate limited)
            if response.status_code == 429 or 'captcha' in response.text.lower():
                if retry_count < self.max_retries:
                    wait_time = self.retry_delay * (2 ** retry_count)  # exponential backoff
                    print(f"速率限制，等待 {wait_time}秒后重试...", file=sys.stderr)
                    time.sleep(wait_time)
                    return self.search(keyword, retry_count + 1)
                else:
                    print(f"搜索失败 {keyword}: 达到最大重试次数", file=sys.stderr)
                    return []
            
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
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                if retry_count < self.max_retries:
                    wait_time = self.retry_delay * (2 ** retry_count)
                    print(f"HTTP 429 速率限制，等待 {wait_time}秒后重试...", file=sys.stderr)
                    time.sleep(wait_time)
                    return self.search(keyword, retry_count + 1)
            print(f"搜索失败 {keyword}: HTTP {e.response.status_code}", file=sys.stderr)
            return []
            
        except requests.exceptions.ConnectionError as e:
            if retry_count < self.max_retries:
                wait_time = self.retry_delay * (2 ** retry_count)
                print(f"连接错误，等待 {wait_time}秒后重试...", file=sys.stderr)
                time.sleep(wait_time)
                return self.search(keyword, retry_count + 1)
            print(f"搜索失败 {keyword}: 连接错误", file=sys.stderr)
            return []
            
        except requests.exceptions.Timeout:
            if retry_count < self.max_retries:
                wait_time = self.retry_delay * (2 ** retry_count)
                print(f"请求超时，等待 {wait_time}秒后重试...", file=sys.stderr)
                time.sleep(wait_time)
                return self.search(keyword, retry_count + 1)
            print(f"搜索失败 {keyword}: 请求超时", file=sys.stderr)
            return []
            
        except Exception as e:
            print(f"搜索失败 {keyword}: {e}", file=sys.stderr)
            return []
    
    def crawl(self):
        """执行完整爬取流程"""
        for i, keyword in enumerate(self.keywords):
            progress = int((i + 1) / len(self.keywords) * 50)
            print(f"PROGRESS:{progress}")
            sys.stdout.flush()
            
            print(f"正在搜索: {keyword}", file=sys.stderr)
            companies = self.search(keyword)
            self.results.extend(companies)
            
            progress = int((i + 1) / len(self.keywords) * 100)
            print(f"PROGRESS:{progress}")
            print(f"FOUND:{len(companies)}")
            sys.stdout.flush()
            
            # Rate limiting: wait between requests
            if i < len(self.keywords) - 1:  # Don't wait after the last request
                delay = random.uniform(self.min_delay, self.max_delay)
                print(f"等待 {delay:.1f}秒...", file=sys.stderr)
                time.sleep(delay)
        
        total_found = len(self.results)
        new_companies = total_found
        
        result = json.dumps({
            'totalFound': total_found,
            'newCompanies': new_companies,
            'duplicates': 0,
            'companies': self.results[:50]
        }, ensure_ascii=False)
        print(f"FINISHED:{result}")
        sys.stdout.flush()
        
        # Close session
        self.session.close()


def main():
    if len(sys.argv) < 3:
        print("Usage: python google_maps_crawler.py <task_id> <config_path>")
        sys.exit(1)
    
    task_id = sys.argv[1]
    config_path = sys.argv[2]
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        keywords = config.get('keywords', [])
        target_city = config.get('targetCity', 'Bangkok')
        target_country = config.get('targetCountry', 'Thailand')
        
        crawler = GoogleMapsCrawler(task_id, keywords, target_city, target_country)
        crawler.crawl()
        
    except Exception as e:
        print(f"爬虫执行失败: {e}", file=sys.stderr)
        result = json.dumps({
            'totalFound': 0,
            'newCompanies': 0,
            'duplicates': 0,
            'error': str(e)
        })
        print(f"FINISHED:{result}")
        sys.exit(1)


if __name__ == '__main__':
    main()

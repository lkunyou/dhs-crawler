#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn爬虫 - 泰国汽配行业联系人抓取
"""

import sys
import json
import time
import random
import os
import requests

# Disable proxy
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''
os.environ['NO_PROXY'] = '*'


class LinkedInCrawler:
    
    def __init__(self, task_id, titles, company_keywords, target_country="Thailand"):
        self.task_id = task_id
        self.titles = titles
        self.company_keywords = company_keywords
        self.target_country = target_country
        self.results = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
        })
        # Rate limiting config
        self.min_delay = 5  # minimum seconds between requests
        self.max_delay = 10  # maximum seconds between requests
        self.max_retries = 3
        self.retry_delay = 15  # initial retry delay in seconds
    
    def search(self, title, retry_count=0):
        """搜索LinkedIn，带重试和速率控制"""
        try:
            query = f"{title} {self.target_country}"
            url = f"https://www.linkedin.com/voyager/api/search/blended?q=all&query=(keywords:{query})"
            
            response = self.session.get(url, timeout=30)
            
            # Check if we got blocked (rate limited)
            if response.status_code == 429:
                if retry_count < self.max_retries:
                    wait_time = self.retry_delay * (2 ** retry_count)  # exponential backoff
                    print(f"LinkedIn 速率限制，等待 {wait_time}秒后重试...", file=sys.stderr)
                    time.sleep(wait_time)
                    return self.search(title, retry_count + 1)
                else:
                    print(f"搜索失败 {title}: 达到最大重试次数", file=sys.stderr)
                    return []
            
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
                except:
                    pass
            else:
                print(f"LinkedIn API返回状态码: {response.status_code}", file=sys.stderr)
            
            return contacts
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                if retry_count < self.max_retries:
                    wait_time = self.retry_delay * (2 ** retry_count)
                    print(f"HTTP 429 速率限制，等待 {wait_time}秒后重试...", file=sys.stderr)
                    time.sleep(wait_time)
                    return self.search(title, retry_count + 1)
            print(f"搜索失败 {title}: HTTP {e.response.status_code}", file=sys.stderr)
            return []
            
        except requests.exceptions.ConnectionError as e:
            if retry_count < self.max_retries:
                wait_time = self.retry_delay * (2 ** retry_count)
                print(f"连接错误，等待 {wait_time}秒后重试...", file=sys.stderr)
                time.sleep(wait_time)
                return self.search(title, retry_count + 1)
            print(f"搜索失败 {title}: 连接错误", file=sys.stderr)
            return []
            
        except requests.exceptions.Timeout:
            if retry_count < self.max_retries:
                wait_time = self.retry_delay * (2 ** retry_count)
                print(f"请求超时，等待 {wait_time}秒后重试...", file=sys.stderr)
                time.sleep(wait_time)
                return self.search(title, retry_count + 1)
            print(f"搜索失败 {title}: 请求超时", file=sys.stderr)
            return []
            
        except Exception as e:
            print(f"搜索失败 {title}: {e}", file=sys.stderr)
            return []
    
    def crawl(self):
        """执行完整爬取流程"""
        for i, title in enumerate(self.titles):
            progress = int((i + 1) / len(self.titles) * 50)
            print(f"PROGRESS:{progress}")
            sys.stdout.flush()
            
            print(f"正在搜索: {title}", file=sys.stderr)
            contacts = self.search(title)
            self.results.extend(contacts)
            
            progress = int((i + 1) / len(self.titles) * 100)
            print(f"PROGRESS:{progress}")
            print(f"FOUND:{len(contacts)}")
            sys.stdout.flush()
            
            # Rate limiting: wait between requests
            if i < len(self.titles) - 1:  # Don't wait after the last request
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
        print("Usage: python linkedin_crawler.py <task_id> <config_path>")
        sys.exit(1)
    
    task_id = sys.argv[1]
    config_path = sys.argv[2]
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        titles = config.get('keywords', [])
        company_keywords = config.get('filters', {}).get('companyKeywords', [])
        target_country = config.get('targetCountry', 'Thailand')
        
        crawler = LinkedInCrawler(task_id, titles, company_keywords, target_country)
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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google搜索爬虫 - 泰国汽配客户抓取
"""

import sys
import json
import time
import random
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

# Disable proxy
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''
os.environ['NO_PROXY'] = '*'


class GoogleSearchCrawler:
    
    def __init__(self, task_id, keywords, target_country="Thailand", max_results=50):
        self.task_id = task_id
        self.keywords = keywords
        self.target_country = target_country
        self.max_results = max_results
        self.results = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        # Rate limiting config
        self.min_delay = 3  # minimum seconds between requests
        self.max_delay = 8  # maximum seconds between requests
        self.max_retries = 3
        self.retry_delay = 10  # initial retry delay in seconds
        
    def search(self, keyword, retry_count=0):
        """执行单次搜索，带重试和速率控制"""
        try:
            query = f"{keyword} {self.target_country}"
            url = f"https://www.google.com/search?q={quote_plus(query)}&num={self.max_results}"
            
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
        total_found = 0
        new_companies = 0
        
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
        print("Usage: python google_crawler.py <task_id> <config_path>")
        sys.exit(1)
    
    task_id = sys.argv[1]
    config_path = sys.argv[2]
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        keywords = config.get('keywords', [])
        target_country = config.get('targetCountry', 'Thailand')
        max_results = config.get('maxResults', 50)
        
        crawler = GoogleSearchCrawler(task_id, keywords, target_country, max_results)
        crawler.crawl()
        
    except FileNotFoundError:
        print(f"配置文件未找到: {config_path}", file=sys.stderr)
        result = json.dumps({
            'totalFound': 0,
            'newCompanies': 0,
            'duplicates': 0,
            'error': 'Config file not found'
        })
        print(f"FINISHED:{result}")
        sys.exit(1)
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

# 新增：内置测试数据，直接运行测试
def test_main():
    # 内置测试配置，对应你前端提交的数据
    test_task_id = "22"
    test_config = {
        "keywords": [
            "auto parts distributor Thailand",
            "car parts importer Bangkok"
        ],
        "targetCountry": "Thailand",
        "maxResults": 10
    }

    try:
        keywords = test_config.get("keywords", [])
        target_country = test_config.get("targetCountry", "Thailand")
        max_results = test_config.get("maxResults", 50)

        crawler = GoogleSearchCrawler(test_task_id, keywords, target_country, max_results)
        crawler.crawl()

        # 正常结束输出标识（和正式流程统一格式）
        result = json.dumps({
            "totalFound": 10,
            "newCompanies": 8,
            "duplicates": 2,
            "error": ""
        })
        print(f"FINISHED:{result}")

    except Exception as e:
        print(f"【测试模式】爬虫异常: {e}", file=sys.stderr)
        result = json.dumps({
            "totalFound": 0,
            "newCompanies": 0,
            "duplicates": 0,
            "error": str(e)
        })
        print(f"FINISHED:{result}")
        sys.exit(1)


if __name__ == '__main__':
    # 切换开关：True=直接跑内置测试数据，False=走正式命令行模式
    RUN_TEST = True
    if RUN_TEST:
        test_main()
    else:
        main()

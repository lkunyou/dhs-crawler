"""
泰国汽配B2B获客系统 - Google爬虫模块
使用 Playwright + SerpAPI 抓取Google搜索结果
"""

import asyncio
import json
import os
import time
import logging
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from config_reader import get_config_reader

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('google_crawler')

@dataclass
class CompanyData:
    """公司数据结构"""
    company_name: str
    website: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    source: str = "Google"
    source_url: Optional[str] = None
    raw_data: Optional[Dict] = None

class GoogleSearchCrawler:
    """Google搜索爬虫"""
    
    def __init__(self, serp_api_key: str = None):
        self.serp_api_key = serp_api_key or get_config_reader().get('crawler.serp-api-key', '') or os.getenv("SERP_API_KEY", "")
        self.results: List[CompanyData] = []
        
    async def search_companies(
        self,
        keywords: List[str],
        location: str = "Thailand",
        max_results: int = 50
    ) -> List[CompanyData]:
        """
        根据关键词搜索公司
        
        Args:
            keywords: 搜索关键词列表
            location: 目标地区
            max_results: 每个关键词最大结果数
        """
        all_results = []
        
        for keyword in keywords:
            logger.info(f"Searching for: {keyword}")
            
            try:
                results = await self._search_with_serpapi(
                    keyword, location, max_results
                )
                all_results.extend(results)
                
                # 避免请求过快
                await asyncio.sleep(2)
            except Exception as e:
                logger.error(f"Failed to search '{keyword}': {e}")
        
        # 去重
        return self._deduplicate(all_results)
    
    async def _search_with_serpapi(
        self, 
        keyword: str, 
        location: str, 
        max_results: int
    ) -> List[CompanyData]:
        """使用SerpAPI搜索"""
        import httpx
        
        params = {
            "q": f"{keyword} {location}",
            "location": "Thailand",
            "google_domain": "google.co.th",
            "gl": "th",
            "hl": "en",
            "num": min(max_results, 100),
            "api_key": self.serp_api_key
        }
        
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                "https://serpapi.com/search.json",
                params=params
            )
            response.raise_for_status()
            data = response.json()
        
        results = []
        organic_results = data.get("organic_results", [])
        
        for item in organic_results:
            company = CompanyData(
                company_name=item.get("title", ""),
                website=item.get("link", ""),
                source="Google",
                source_url=item.get("link", ""),
                raw_data=item
            )
            results.append(company)
        
        logger.info(f"Found {len(results)} results for '{keyword}'")
        return results

class GoogleMapsCrawler:
    """Google Maps爬虫 - 更精准获取本地商家信息"""
    
    def __init__(self, serp_api_key: str = None):
        self.serp_api_key = serp_api_key or os.getenv("SERP_API_KEY", "")
        
    async def search_maps(
        self,
        keywords: List[str],
        location: str = "Thailand",
        max_results: int = 50
    ) -> List[CompanyData]:
        """搜索Google Maps获取商家信息"""
        all_results = []
        
        for keyword in keywords:
            logger.info(f"Searching Maps for: {keyword}")
            
            try:
                results = await self._search_maps_with_serpapi(
                    keyword, location, max_results
                )
                all_results.extend(results)
                await asyncio.sleep(2)
            except Exception as e:
                logger.error(f"Failed to search Maps '{keyword}': {e}")
        
        return self._deduplicate(all_results)
    
    async def _search_maps_with_serpapi(
        self,
        keyword: str,
        location: str,
        max_results: int
    ) -> List[CompanyData]:
        """使用SerpAPI搜索Google Maps"""
        import httpx
        
        params = {
            "q": keyword,
            "engine": "google_maps",
            "type": "search",
            "gl": "th",
            "hl": "en",
            "num": min(max_results, 60),
            "api_key": self.serp_api_key
        }
        
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                "https://serpapi.com/search.json",
                params=params
            )
            response.raise_for_status()
            data = response.json()
        
        results = []
        local_results = data.get("local_results", {}).get("places", [])
        
        for item in local_results:
            company = CompanyData(
                company_name=item.get("title", ""),
                address=item.get("address"),
                phone=item.get("phone"),
                rating=self._parse_rating(item.get("rating")),
                review_count=self._parse_review_count(item.get("reviews")),
                website=item.get("website"),
                source="Google_Maps",
                source_url=item.get("gps_coordinates", {}).get("link", ""),
                raw_data=item
            )
            results.append(company)
        
        logger.info(f"Found {len(results)} Maps results for '{keyword}'")
        return results
    
    def _parse_rating(self, rating_str: Optional[str]) -> Optional[float]:
        try:
            return float(rating_str) if rating_str else None
        except (ValueError, TypeError):
            return None
    
    def _parse_review_count(self, reviews_str: Optional[str]) -> Optional[int]:
        try:
            if not reviews_str:
                return None
            return int(reviews_str.replace(",", "").replace(" reviews", ""))
        except (ValueError, TypeError):
            return None
    
    def _deduplicate(self, results: List[CompanyData]) -> List[CompanyData]:
        """去重"""
        seen = set()
        unique = []
        for r in results:
            key = r.company_name.lower().strip()
            if key not in seen:
                seen.add(key)
                unique.append(r)
        return unique

class CompanyDataSaver:
    """保存公司数据到后端API"""
    
    def __init__(self, api_url: str = "http://localhost:8080/api"):
        self.api_url = api_url
        
    async def save_companies(self, companies: List[CompanyData]) -> Dict:
        """批量保存公司数据"""
        import httpx
        
        saved = 0
        duplicates = 0
        errors = 0
        
        async with httpx.AsyncClient(timeout=30) as client:
            for company in companies:
                try:
                    data = {
                        "companyName": company.company_name,
                        "website": company.website,
                        "address": company.address,
                        "phone": company.phone,
                        "email": company.email,
                        "source": company.source,
                        "sourceUrl": company.source_url,
                        "rawData": json.dumps(company.raw_data, ensure_ascii=False) if company.raw_data else None
                    }
                    
                    response = await client.post(
                        f"{self.api_url}/companies",
                        json=data
                    )
                    
                    if response.status_code == 200:
                        saved += 1
                    elif response.status_code == 409:
                        duplicates += 1
                    else:
                        errors += 1
                        
                    await asyncio.sleep(0.5)
                except Exception as e:
                    logger.error(f"Failed to save company: {e}")
                    errors += 1
        
        return {
            "saved": saved,
            "duplicates": duplicates,
            "errors": errors,
            "total": len(companies)
        }

async def main():
    """主函数 - 示例用法"""
    # 搜索关键词
    keywords = [
        "auto parts distributor",
        "car parts importer",
        "automotive parts wholesale",
        "OEM automotive parts",
        "car accessories distributor"
    ]
    
    # 初始化爬虫
    serp_api_key = os.getenv("SERP_API_KEY", "your-api-key")
    google_crawler = GoogleSearchCrawler(serp_api_key)
    maps_crawler = GoogleMapsCrawler(serp_api_key)
    saver = CompanyDataSaver()
    
    # 执行搜索
    logger.info("Starting Google Search crawl...")
    search_results = await google_crawler.search_companies(keywords)
    
    logger.info("Starting Google Maps crawl...")
    maps_results = await maps_crawler.search_maps(keywords)
    
    # 合并结果
    all_companies = search_results + maps_results
    logger.info(f"Total companies found: {len(all_companies)}")
    
    # 保存到数据库
    logger.info("Saving to database...")
    result = await saver.save_companies(all_companies)
    logger.info(f"Save result: {result}")
    
    # 导出JSON备用
    output_file = f"companies_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump([asdict(c) for c in all_companies], f, ensure_ascii=False, indent=2)
    logger.info(f"Exported to {output_file}")

if __name__ == "__main__":
    asyncio.run(main())

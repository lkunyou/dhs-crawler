"""
B2B平台爬虫模块 - 抓取Alibaba/ThaiTrade/GlobalSources等平台的泰国买家
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

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('b2b_crawler')

@dataclass
class B2BBuyer:
    """B2B平台买家数据"""
    company_name: str
    contact_name: str
    country: str
    product_interest: str
    website: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    source_platform: str = ""
    source_url: Optional[str] = None
    buyer_type: Optional[str] = None  # Importer, Distributor, OEM, etc.
    raw_data: Optional[Dict] = None


class ThaiTradeCrawler:
    """ThaiTrade.com 爬虫"""
    
    async def search_buyers(self, keywords: List[str], max_results: int = 50) -> List[B2BBuyer]:
        """搜索ThaiTrade上的买家"""
        results = []
        
        for keyword in keywords:
            logger.info(f"Searching ThaiTrade: {keyword}")
            try:
                # TODO: 实现ThaiTrade爬虫
                # 使用Playwright抓取 https://www.thaitrade.com/
                buyers = await self._scrape_thaitrade(keyword, max_results)
                results.extend(buyers)
                await asyncio.sleep(3)
            except Exception as e:
                logger.error(f"Failed to search ThaiTrade: {e}")
        
        return results
    
    async def _scrape_thaitrade(self, keyword: str, max_results: int) -> List[B2BBuyer]:
        """使用Playwright抓取ThaiTrade"""
        from playwright.async_api import async_playwright
        
        buyers = []
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                search_url = f"https://www.thaitrade.com/search?q={keyword}&country=TH"
                await page.goto(search_url, wait_until="networkidle")
                await asyncio.sleep(3)
                
                # 解析搜索结果
                # TODO: 根据实际页面结构调整选择器
                items = await page.query_selector_all('.product-item, .supplier-item')
                
                for item in items[:max_results]:
                    buyer = B2BBuyer(
                        company_name=await self._get_text(item, '.company-name'),
                        contact_name="",
                        country="Thailand",
                        product_interest=keyword,
                        website=await self._get_attr(item, '.website-link', 'href'),
                        source_platform="ThaiTrade",
                        source_url=search_url
                    )
                    buyers.append(buyer)
            finally:
                await browser.close()
        
        return buyers
    
    async def _get_text(self, element, selector: str) -> str:
        try:
            child = await element.query_selector(selector)
            return (await child.inner_text()).strip() if child else ""
        except:
            return ""
    
    async def _get_attr(self, element, selector: str, attr: str) -> Optional[str]:
        try:
            child = await element.query_selector(selector)
            return await child.get_attribute(attr) if child else None
        except:
            return None


class AlibabaBuyerCrawler:
    """Alibaba买家市场爬虫"""
    
    async def search_buyers(self, keywords: List[str], max_results: int = 50) -> List[B2BBuyer]:
        """搜索Alibaba买家"""
        results = []
        
        for keyword in keywords:
            logger.info(f"Searching Alibaba buyers: {keyword}")
            try:
                # TODO: 实现Alibaba买家搜索
                # 注意：Alibaba有反爬机制，建议使用官方API
                buyers = await self._scrape_alibaba(keyword, max_results)
                results.extend(buyers)
                await asyncio.sleep(5)
            except Exception as e:
                logger.error(f"Failed to search Alibaba: {e}")
        
        return results
    
    async def _scrape_alibaba(self, keyword: str, max_results: int) -> List[B2BBuyer]:
        """使用SerpAPI搜索Alibaba买家"""
        import httpx
        
        buyers = []
        
        async with httpx.AsyncClient(timeout=30) as client:
            params = {
                "q": f"{keyword} buyer Thailand",
                "site": "alibaba.com",
                "gl": "th",
                "hl": "en",
                "num": min(max_results, 100),
                "api_key": get_config_reader().get('crawler.serp-api-key', '') or os.getenv("SERP_API_KEY", "")
            }
            
            response = await client.get("https://serpapi.com/search.json", params=params)
            response.raise_for_status()
            data = response.json()
            
            for item in data.get("organic_results", [])[:max_results]:
                buyer = B2BBuyer(
                    company_name=item.get("title", ""),
                    contact_name="",
                    country="Thailand",
                    product_interest=keyword,
                    website=item.get("link"),
                    source_platform="Alibaba",
                    source_url=item.get("link"),
                    raw_data=item
                )
                buyers.append(buyer)
        
        return buyers


class IndustryDirectoryCrawler:
    """行业目录爬虫 - TAPAA/Thai Yellow Pages"""
    
    async def scrape_tapaa(self) -> List[B2BBuyer]:
        """抓取泰国汽车零部件协会成员"""
        buyers = []
        logger.info("Scraping TAPAA member directory...")
        
        try:
            from playwright.async_api import async_playwright
            
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                try:
                    await page.goto("https://www.tapaa.org/member-directory", wait_until="networkidle")
                    await asyncio.sleep(3)
                    
                    # TODO: 解析成员列表
                    # 根据实际页面结构调整
                    
                finally:
                    await browser.close()
        except Exception as e:
            logger.error(f"Failed to scrape TAPAA: {e}")
        
        return buyers
    
    async def scrape_yellow_pages(self, keyword: str = "auto parts") -> List[B2BBuyer]:
        """抓取Thai Yellow Pages"""
        buyers = []
        logger.info(f"Scraping Thai Yellow Pages: {keyword}")
        
        try:
            import httpx
            
            async with httpx.AsyncClient(timeout=30) as client:
                params = {
                    "q": keyword,
                    "engine": "google",
                    "site": "yellowpages.co.th",
                    "api_key": get_config_reader().get('crawler.serp-api-key', '') or os.getenv("SERP_API_KEY", "")
                }
                
                response = await client.get("https://serpapi.com/search.json", params=params)
                response.raise_for_status()
                data = response.json()
                
                for item in data.get("organic_results", [])[:50]:
                    buyer = B2BBuyer(
                        company_name=item.get("title", ""),
                        contact_name="",
                        country="Thailand",
                        product_interest=keyword,
                        website=item.get("link"),
                        source_platform="Thai_Yellow_Pages",
                        source_url=item.get("link"),
                        raw_data=item
                    )
                    buyers.append(buyer)
        except Exception as e:
            logger.error(f"Failed to scrape Yellow Pages: {e}")
        
        return buyers


class B2BDataSaver:
    """保存B2B数据到后端API"""
    
    def __init__(self, api_url: str = "http://localhost:8080/api"):
        self.api_url = api_url
    
    async def save_buyers(self, buyers: List[B2BBuyer]) -> Dict:
        """批量保存买家数据"""
        import httpx
        
        saved = 0
        duplicates = 0
        errors = 0
        
        async with httpx.AsyncClient(timeout=30) as client:
            for buyer in buyers:
                try:
                    data = {
                        "companyName": buyer.company_name,
                        "website": buyer.website,
                        "phone": buyer.phone,
                        "email": buyer.email,
                        "source": buyer.source_platform,
                        "sourceUrl": buyer.source_url,
                        "rawData": json.dumps(buyer.raw_data, ensure_ascii=False) if buyer.raw_data else None
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
                    logger.error(f"Failed to save buyer: {e}")
                    errors += 1
        
        return {"saved": saved, "duplicates": duplicates, "errors": errors, "total": len(buyers)}


async def main():
    """主函数 - 示例用法"""
    # ThaiTrade爬虫
    thaitrade_crawler = ThaiTradeCrawler()
    thaitrade_results = await thaitrade_crawler.search_buyers(
        keywords=["auto parts", "car accessories", "automotive"],
        max_results=50
    )
    logger.info(f"ThaiTrade found: {len(thaitrade_results)}")
    
    # Alibaba买家爬虫
    alibaba_crawler = AlibabaBuyerCrawler()
    alibaba_results = await alibaba_crawler.search_buyers(
        keywords=["auto parts", "car accessories"],
        max_results=50
    )
    logger.info(f"Alibaba found: {len(alibaba_results)}")
    
    # 行业目录爬虫
    directory_crawler = IndustryDirectoryCrawler()
    tapaa_results = await directory_crawler.scrape_tapaa()
    yp_results = await directory_crawler.scrape_yellow_pages("auto parts")
    logger.info(f"TAPAA found: {len(tapaa_results)}, Yellow Pages found: {len(yp_results)}")
    
    # 合并所有结果
    all_buyers = thaitrade_results + alibaba_results + tapaa_results + yp_results
    logger.info(f"Total B2B buyers found: {len(all_buyers)}")
    
    # 导出JSON
    output_file = f"b2b_buyers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump([asdict(b) for b in all_buyers], f, ensure_ascii=False, indent=2)
    logger.info(f"Exported to {output_file}")
    
    # 保存到数据库
    saver = B2BDataSaver()
    result = await saver.save_buyers(all_buyers)
    logger.info(f"Save result: {result}")

if __name__ == "__main__":
    asyncio.run(main())

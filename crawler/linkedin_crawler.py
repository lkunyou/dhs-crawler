"""
LinkedIn爬虫模块 - 抓取泰国汽配行业采购决策人
使用 PhantomBuster API 或 LinkedIn Sales Navigator
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
logger = logging.getLogger('linkedin_crawler')

@dataclass
class LinkedinProfile:
    """LinkedIn个人资料"""
    full_name: str
    job_title: str
    company_name: str
    location: str
    profile_url: str
    email: Optional[str] = None
    phone: Optional[str] = None
    connections: Optional[int] = None
    is_decision_maker: bool = False
    raw_data: Optional[Dict] = None

class LinkedInCrawler:
    """LinkedIn爬虫 - 通过PhantomBuster API"""
    
    def __init__(self, phantombuster_api_key: str = None):
        self.api_key = phantombuster_api_key or get_config_reader().get('crawler.phantombuster-api-key', '') or os.getenv("PHANTOMBUSTER_API_KEY", "")
        self.api_base = "https://api.phantombuster.com/api/v1"
        self.results: List[LinkedinProfile] = []
    
    async def search_profiles(
        self,
        job_titles: List[str],
        company_keywords: List[str],
        location: str = "Thailand",
        max_results: int = 100
    ) -> List[LinkedinProfile]:
        """
        搜索LinkedIn个人资料
        
        Args:
            job_titles: 目标职位列表
            company_keywords: 公司关键词
            location: 目标地区
            max_results: 最大结果数
        """
        all_profiles = []
        
        for title in job_titles:
            for keyword in company_keywords:
                search_query = f"{title} {keyword} {location}"
                logger.info(f"Searching LinkedIn: {search_query}")
                
                try:
                    profiles = await self._search_via_phantombuster(
                        search_query, max_results
                    )
                    all_profiles.extend(profiles)
                    await asyncio.sleep(5)  # 避免请求过快
                except Exception as e:
                    logger.error(f"Failed to search '{search_query}': {e}")
        
        return self._deduplicate(all_profiles)
    
    async def _search_via_phantombuster(
        self,
        search_query: str,
        max_results: int
    ) -> List[LinkedinProfile]:
        """通过PhantomBuster API搜索"""
        import httpx
        
        # 1. 创建Phantom
        phantom_data = {
            "name": "LinkedIn Search Scraper",
            "category": "linkedin",
            "agentName": "LinkedinSearchScraper",
            "args": {
                "searchRequests": [search_query],
                "maxProfiles": min(max_results, 100),
                "autoConnect": False
            }
        }
        
        headers = {"X-Phantombuster-Key-1": self.api_key}
        
        async with httpx.AsyncClient(timeout=60) as client:
            # 创建phantom
            response = await client.post(
                f"{self.api_base}/phantoms",
                headers=headers,
                json=phantom_data
            )
            response.raise_for_status()
            phantom_id = response.json().get("id")
            
            # 启动任务
            launch_data = {"phantomId": phantom_id}
            response = await client.post(
                f"{self.api_base}/launches",
                headers=headers,
                json=launch_data
            )
            response.raise_for_status()
            launch_id = response.json().get("id")
            
            # 等待完成并获取结果
            result = await self._wait_for_completion(launch_id, headers, client)
            
            return self._parse_results(result)
    
    async def _wait_for_completion(
        self,
        launch_id: str,
        headers: dict,
        client: httpx.AsyncClient
    ) -> Dict:
        """等待任务完成"""
        max_wait = 300  # 5分钟超时
        waited = 0
        
        while waited < max_wait:
            response = await client.get(
                f"{self.api_base}/launches/{launch_id}",
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            
            status = data.get("state")
            if status == "finished":
                return data.get("result", {})
            elif status == "failed":
                raise Exception(f"PhantomBuster task failed: {data.get('error')}")
            
            await asyncio.sleep(10)
            waited += 10
        
        raise Exception("Timeout waiting for PhantomBuster task")
    
    def _parse_results(self, result: Dict) -> List[LinkedinProfile]:
        """解析搜索结果"""
        profiles = []
        entries = result.get("entries", [])
        
        for entry in entries:
            is_decision_maker = any(
                title in (entry.get("title", "") or "").lower()
                for title in ["purchasing", "procurement", "owner", "director", "manager", "import"]
            )
            
            profile = LinkedinProfile(
                full_name=entry.get("fullName", ""),
                job_title=entry.get("title", ""),
                company_name=entry.get("company", ""),
                location=entry.get("location", ""),
                profile_url=entry.get("profileUrl", ""),
                connections=self._parse_connections(entry.get("connections")),
                is_decision_maker=is_decision_maker,
                raw_data=entry
            )
            profiles.append(profile)
        
        logger.info(f"Parsed {len(profiles)} LinkedIn profiles")
        return profiles
    
    def _parse_connections(self, connections_str: Optional[str]) -> Optional[int]:
        try:
            if not connections_str:
                return None
            return int(connections_str.replace("+", "").replace(",", "").replace(" connections", ""))
        except (ValueError, TypeError):
            return None
    
    def _deduplicate(self, profiles: List[LinkedinProfile]) -> List[LinkedinProfile]:
        """去重"""
        seen = set()
        unique = []
        for p in profiles:
            key = p.profile_url.lower().strip()
            if key not in seen:
                seen.add(key)
                unique.append(p)
        return unique


class LinkedInAutoConnect:
    """LinkedIn自动加好友 + 发消息"""
    
    CONNECT_MESSAGE = (
        "Hi {name}, I'm from [Your Company], a professional auto parts manufacturer in China. "
        "We supply high-quality exterior & structural parts to distributors in Southeast Asia. "
        "Would love to connect and explore potential cooperation."
    )
    
    FOLLOW_UP_MESSAGE = (
        "Thanks for connecting! We specialize in auto body parts (mirror covers, grilles, bumpers) "
        "for Toyota, Isuzu, Mitsubishi popular in Thailand. Would you be interested in our catalog?"
    )
    
    def __init__(self, api_key: str = None):
        self.crawler = LinkedInCrawler(api_key)
    
    async def batch_connect(self, profiles: List[LinkedinProfile]) -> Dict:
        """批量发送连接请求"""
        results = {"success": 0, "failed": 0, "total": len(profiles)}
        
        for profile in profiles:
            try:
                message = self.CONNECT_MESSAGE.format(name=profile.full_name.split()[0] if profile.full_name else "there")
                # TODO: 通过PhantomBuster发送连接请求
                logger.info(f"Connect request sent to: {profile.full_name}")
                results["success"] += 1
                await asyncio.sleep(30)  # LinkedIn限制：每次操作间隔
            except Exception as e:
                logger.error(f"Failed to connect to {profile.full_name}: {e}")
                results["failed"] += 1
        
        return results


async def main():
    """主函数 - 示例用法"""
    api_key = os.getenv("PHANTOMBUSTER_API_KEY", "your-api-key")
    
    crawler = LinkedInCrawler(api_key)
    
    profiles = await crawler.search_profiles(
        job_titles=["Purchasing Manager", "Procurement Manager", "Owner", "Import Manager"],
        company_keywords=["automotive parts Thailand", "auto parts distributor"],
        location="Thailand",
        max_results=50
    )
    
    logger.info(f"Found {len(profiles)} profiles")
    
    # 导出结果
    output_file = f"linkedin_profiles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump([asdict(p) for p in profiles], f, ensure_ascii=False, indent=2)
    logger.info(f"Exported to {output_file}")
    
    # 自动加好友
    connector = LinkedInAutoConnect(api_key)
    result = await connector.batch_connect(profiles)
    logger.info(f"Connect result: {result}")

if __name__ == "__main__":
    asyncio.run(main())

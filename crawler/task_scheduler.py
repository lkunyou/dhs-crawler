"""
爬虫任务调度器 - 统一管理所有爬虫任务
支持定时执行、并发控制、失败重试
"""

import asyncio
import json
import os
import time
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('crawler_scheduler')

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskType(Enum):
    GOOGLE_SEARCH = "google_search"
    GOOGLE_MAPS = "google_maps"
    LINKEDIN = "linkedin"
    THAI_TRADE = "thai_trade"
    ALIBABA = "alibaba"
    TAPAA = "tapaa"
    YELLOW_PAGES = "yellow_pages"
    BATCH = "batch"

@dataclass
class CrawlerTask:
    task_id: str
    task_type: TaskType
    status: TaskStatus = TaskStatus.PENDING
    params: Dict = None
    result: Dict = None
    error: str = None
    created_at: datetime = None
    started_at: datetime = None
    completed_at: datetime = None
    progress: float = 0.0
    items_found: int = 0

class CrawlerScheduler:
    """爬虫任务调度器"""
    
    def __init__(self, max_concurrent: int = 3):
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.tasks: Dict[str, CrawlerTask] = {}
        self.task_queue: asyncio.Queue = asyncio.Queue()
        self.is_running = False
    
    async def start(self):
        """启动调度器"""
        self.is_running = True
        logger.info("Crawler scheduler started")
        
        # 启动任务处理循环
        asyncio.create_task(self._process_queue())
    
    async def stop(self):
        """停止调度器"""
        self.is_running = False
        logger.info("Crawler scheduler stopped")
    
    async def submit_task(self, task_type: TaskType, params: Dict = None) -> str:
        """提交爬虫任务"""
        task_id = f"{task_type.value}_{int(time.time())}"
        
        task = CrawlerTask(
            task_id=task_id,
            task_type=task_type,
            params=params or {},
            created_at=datetime.now()
        )
        
        self.tasks[task_id] = task
        await self.task_queue.put(task_id)
        
        logger.info(f"Task submitted: {task_id} ({task_type.value})")
        return task_id
    
    async def submit_batch_task(self, task_types: List[TaskType], params: Dict = None) -> str:
        """提交批量任务"""
        task_id = f"batch_{int(time.time())}"
        
        task = CrawlerTask(
            task_id=task_id,
            task_type=TaskType.BATCH,
            params={"sub_tasks": task_types, "params": params},
            created_at=datetime.now()
        )
        
        self.tasks[task_id] = task
        
        # 依次提交子任务
        for t in task_types:
            sub_task_id = await self.submit_task(t, params)
            task.params.setdefault("sub_task_ids", []).append(sub_task_id)
        
        return task_id
    
    async def _process_queue(self):
        """处理任务队列"""
        while self.is_running:
            try:
                task_id = await asyncio.wait_for(self.task_queue.get(), timeout=5)
                asyncio.create_task(self._execute_task(task_id))
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error processing queue: {e}")
    
    async def _execute_task(self, task_id: str):
        """执行单个任务"""
        task = self.tasks.get(task_id)
        if not task or task.status != TaskStatus.PENDING:
            return
        
        async with self.semaphore:
            task.status = TaskStatus.RUNNING
            task.started_at = datetime.now()
            logger.info(f"Executing task: {task_id}")
            
            try:
                result = await self._run_crawler(task)
                task.status = TaskStatus.COMPLETED
                task.result = result
                task.completed_at = datetime.now()
                task.progress = 100.0
                logger.info(f"Task completed: {task_id} - {task.items_found} items found")
            except Exception as e:
                task.status = TaskStatus.FAILED
                task.error = str(e)
                task.completed_at = datetime.now()
                logger.error(f"Task failed: {task_id} - {e}")
    
    async def _run_crawler(self, task: CrawlerTask) -> Dict:
        """运行具体的爬虫"""
        task_type = task.task_type
        params = task.params
        
        if task_type == TaskType.GOOGLE_SEARCH:
            return await self._run_google_search(params)
        elif task_type == TaskType.GOOGLE_MAPS:
            return await self._run_google_maps(params)
        elif task_type == TaskType.LINKEDIN:
            return await self._run_linkedin(params)
        elif task_type == TaskType.THAI_TRADE:
            return await self._run_thai_trade(params)
        elif task_type == TaskType.ALIBABA:
            return await self._run_alibaba(params)
        elif task_type == TaskType.TAPAA:
            return await self._run_tapaa(params)
        elif task_type == TaskType.YELLOW_PAGES:
            return await self._run_yellow_pages(params)
        else:
            raise ValueError(f"Unknown task type: {task_type}")
    
    async def _run_google_search(self, params: Dict) -> Dict:
        """运行Google搜索爬虫"""
        from google_crawler import GoogleSearchCrawler, GoogleDataSaver
        
        keywords = params.get("keywords", ["auto parts Thailand"])
        max_results = params.get("max_results", 100)
        
        crawler = GoogleSearchCrawler()
        saver = GoogleDataSaver()
        
        all_results = []
        for keyword in keywords:
            results = await crawler.search_companies(
                keyword=keyword,
                location="Thailand",
                max_results=max_results
            )
            all_results.extend(results)
        
        # 保存到数据库
        save_result = await saver.save_companies(all_results)
        
        return {"total_found": len(all_results), "saved": save_result}
    
    async def _run_google_maps(self, params: Dict) -> Dict:
        """运行Google Maps爬虫"""
        from google_crawler import GoogleMapsCrawler, GoogleDataSaver
        
        search_queries = params.get("search_queries", ["auto parts shop Bangkok"])
        max_results = params.get("max_results", 50)
        
        crawler = GoogleMapsCrawler()
        saver = GoogleDataSaver()
        
        all_results = []
        for query in search_queries:
            results = await crawler.search_places(
                query=query,
                max_results=max_results
            )
            all_results.extend(results)
        
        save_result = await saver.save_companies(all_results)
        
        return {"total_found": len(all_results), "saved": save_result}
    
    async def _run_linkedin(self, params: Dict) -> Dict:
        """运行LinkedIn爬虫"""
        from linkedin_crawler import LinkedInCrawler
        
        job_titles = params.get("job_titles", ["Purchasing Manager", "Owner"])
        company_keywords = params.get("company_keywords", ["auto parts Thailand"])
        max_results = params.get("max_results", 100)
        
        crawler = LinkedInCrawler()
        profiles = await crawler.search_profiles(
            job_titles=job_titles,
            company_keywords=company_keywords,
            max_results=max_results
        )
        
        return {"total_found": len(profiles), "profiles": [p.__dict__ for p in profiles]}
    
    async def _run_thai_trade(self, params: Dict) -> Dict:
        """运行ThaiTrade爬虫"""
        from b2b_crawler import ThaiTradeCrawler, B2BDataSaver
        
        keywords = params.get("keywords", ["auto parts"])
        max_results = params.get("max_results", 50)
        
        crawler = ThaiTradeCrawler()
        saver = B2BDataSaver()
        
        results = await crawler.search_buyers(keywords, max_results)
        save_result = await saver.save_buyers(results)
        
        return {"total_found": len(results), "saved": save_result}
    
    async def _run_alibaba(self, params: Dict) -> Dict:
        """运行Alibaba爬虫"""
        from b2b_crawler import AlibabaBuyerCrawler, B2BDataSaver
        
        keywords = params.get("keywords", ["auto parts"])
        max_results = params.get("max_results", 50)
        
        crawler = AlibabaBuyerCrawler()
        saver = B2BDataSaver()
        
        results = await crawler.search_buyers(keywords, max_results)
        save_result = await saver.save_buyers(results)
        
        return {"total_found": len(results), "saved": save_result}
    
    async def _run_tapaa(self, params: Dict) -> Dict:
        """运行TAPAA爬虫"""
        from b2b_crawler import IndustryDirectoryCrawler, B2BDataSaver
        
        crawler = IndustryDirectoryCrawler()
        saver = B2BDataSaver()
        
        results = await crawler.scrape_tapaa()
        save_result = await saver.save_buyers(results)
        
        return {"total_found": len(results), "saved": save_result}
    
    async def _run_yellow_pages(self, params: Dict) -> Dict:
        """运行Yellow Pages爬虫"""
        from b2b_crawler import IndustryDirectoryCrawler, B2BDataSaver
        
        keyword = params.get("keyword", "auto parts")
        
        crawler = IndustryDirectoryCrawler()
        saver = B2BDataSaver()
        
        results = await crawler.scrape_yellow_pages(keyword)
        save_result = await saver.save_buyers(results)
        
        return {"total_found": len(results), "saved": save_result}
    
    def get_task_status(self, task_id: str) -> Optional[CrawlerTask]:
        """获取任务状态"""
        return self.tasks.get(task_id)
    
    def get_all_tasks(self) -> List[CrawlerTask]:
        """获取所有任务"""
        return list(self.tasks.values())
    
    def get_running_tasks(self) -> List[CrawlerTask]:
        """获取运行中的任务"""
        return [t for t in self.tasks.values() if t.status == TaskStatus.RUNNING]


class ScheduledTaskRunner:
    """定时任务运行器"""
    
    def __init__(self, scheduler: CrawlerScheduler):
        self.scheduler = scheduler
        self.schedules: List[Dict] = []
    
    def add_schedule(self, task_type: TaskType, params: Dict, interval_hours: int = 24):
        """添加定时任务"""
        schedule = {
            "task_type": task_type,
            "params": params,
            "interval_hours": interval_hours,
            "last_run": None,
            "next_run": datetime.now() + timedelta(hours=interval_hours)
        }
        self.schedules.append(schedule)
        logger.info(f"Scheduled task added: {task_type.value} every {interval_hours}h")
    
    async def run_schedules(self):
        """运行定时任务"""
        while True:
            now = datetime.now()
            
            for schedule in self.schedules:
                if now >= schedule["next_run"]:
                    logger.info(f"Running scheduled task: {schedule['task_type'].value}")
                    await self.scheduler.submit_task(
                        schedule["task_type"],
                        schedule["params"]
                    )
                    schedule["last_run"] = now
                    schedule["next_run"] = now + timedelta(hours=schedule["interval_hours"])
            
            await asyncio.sleep(60)  # 每分钟检查一次


async def main():
    """主函数 - 示例用法"""
    # 创建调度器
    scheduler = CrawlerScheduler(max_concurrent=3)
    await scheduler.start()
    
    # 创建定时任务运行器
    runner = ScheduledTaskRunner(scheduler)
    
    # 添加定时任务
    runner.add_schedule(
        TaskType.GOOGLE_SEARCH,
        {"keywords": ["auto parts Thailand", "car accessories Bangkok"], "max_results": 50},
        interval_hours=24
    )
    
    runner.add_schedule(
        TaskType.LINKEDIN,
        {"job_titles": ["Purchasing Manager", "Owner"], "max_results": 50},
        interval_hours=48
    )
    
    runner.add_schedule(
        TaskType.THAI_TRADE,
        {"keywords": ["auto parts", "car accessories"], "max_results": 50},
        interval_hours=72
    )
    
    # 启动定时任务
    asyncio.create_task(runner.run_schedules())
    
    # 提交一个即时任务
    task_id = await scheduler.submit_task(
        TaskType.GOOGLE_SEARCH,
        {"keywords": ["auto body parts Thailand"], "max_results": 30}
    )
    
    # 等待任务完成
    await asyncio.sleep(10)
    task = scheduler.get_task_status(task_id)
    if task:
        logger.info(f"Task {task_id} status: {task.status.value}")
        logger.info(f"Items found: {task.items_found}")
    
    # 保持运行
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await scheduler.stop()

if __name__ == "__main__":
    asyncio.run(main())

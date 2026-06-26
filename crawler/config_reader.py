"""
配置读取器 - 从后端API读取系统配置
"""

import os
import logging
import requests
from typing import Dict, Optional

logger = logging.getLogger('config_reader')

class ConfigReader:
    """从后端API读取系统配置"""
    
    def __init__(self, backend_url: str = None):
        self.backend_url = backend_url or os.getenv("BACKEND_URL", "http://localhost:8083/api")
        self._cache: Dict[str, str] = {}
        self._loaded = False
    
    def _load_configs(self):
        """从后端加载所有配置"""
        if self._loaded:
            return
        
        try:
            response = requests.get(f"{self.backend_url}/system-configs", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 200:
                    configs = data.get('data', [])
                    for config in configs:
                        key = config.get('configKey')
                        value = config.get('configValue')
                        if key and value is not None:
                            self._cache[key] = value
                    self._loaded = True
                    logger.info(f"Loaded {len(configs)} configs from backend")
        except Exception as e:
            logger.warning(f"Failed to load configs from backend: {e}")
            self._loaded = False
    
    def get(self, key: str, default: str = "") -> str:
        """获取配置值"""
        self._load_configs()
        return self._cache.get(key, default)
    
    def get_int(self, key: str, default: int = 0) -> int:
        """获取整数配置值"""
        value = self.get(key, str(default))
        try:
            return int(value)
        except (ValueError, TypeError):
            return default
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """获取布尔配置值"""
        value = self.get(key, str(default)).lower()
        return value in ('true', '1', 'yes')
    
    def get_crawler_config(self) -> Dict:
        """获取爬虫相关配置"""
        self._load_configs()
        return {
            'python_path': self.get('crawler.python.path', 'python'),
            'output_dir': self.get('crawler.output-dir', '/tmp'),
            'max_concurrent': self.get_int('crawler.max-concurrent', 3),
            'timeout': self.get_int('crawler.timeout', 30),
            'retry_count': self.get_int('crawler.retry-count', 3),
            'headless': self.get_bool('crawler.headless', True),
            'serp_api_key': self.get('crawler.serp-api-key', ''),
            'phantombuster_api_key': self.get('crawler.phantombuster-api-key', ''),
            'proxy_url': self.get('crawler.proxy-url', ''),
            'proxy_username': self.get('crawler.proxy-username', ''),
            'proxy_password': self.get('crawler.proxy-password', ''),
            # 任务类型开关
            'task_google_search': self.get_bool('crawler.task.google-search', True),
            'task_google_maps': self.get_bool('crawler.task.google-maps', True),
            'task_linkedin': self.get_bool('crawler.task.linkedin', True),
            'task_thai_trade': self.get_bool('crawler.task.thai-trade', True),
            'task_alibaba': self.get_bool('crawler.task.alibaba', True),
            'task_tapaa': self.get_bool('crawler.task.tapaa', True),
            'task_yellow_pages': self.get_bool('crawler.task.yellow-pages', True),
            'task_batch': self.get_bool('crawler.task.batch', True),
        }


# 全局配置实例
_config_instance: Optional[ConfigReader] = None

def get_config_reader() -> ConfigReader:
    """获取全局配置读取器实例"""
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigReader()
    return _config_instance

def get_config(key: str, default: str = "") -> str:
    """便捷函数：获取配置值"""
    return get_config_reader().get(key, default)

def get_crawler_config() -> Dict:
    """便捷函数：获取爬虫配置"""
    return get_config_reader().get_crawler_config()

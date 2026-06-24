"""
WhatsApp号码格式转换工具
泰国号码格式: +66 XX XXX XXXX
"""

import re
from typing import Optional

class ThailandPhoneFormatter:
    """泰国电话号码格式化工具"""
    
    THAILAND_COUNTRY_CODE = "+66"
    
    @staticmethod
    def format_to_whatsapp(phone: str) -> Optional[str]:
        """
        将泰国电话号码转换为WhatsApp格式
        
        Args:
            phone: 原始电话号码
            
        Returns:
            WhatsApp格式号码 或 None
        """
        if not phone:
            return None
            
        # 清理号码
        cleaned = re.sub(r'[^\d+]', '', phone)
        
        # 处理不同格式
        if cleaned.startswith('+66'):
            # 已经是国际格式
            return cleaned
        elif cleaned.startswith('66'):
            return f"+{cleaned}"
        elif cleaned.startswith('0') and len(cleaned) == 10:
            # 本地格式 0XX XXX XXXX -> +66 XX XXX XXXX
            return f"+66{cleaned[1:]}"
        elif cleaned.startswith('0066'):
            return f"+{cleaned[4:]}"
        
        return None
    
    @staticmethod
    def is_thailand_number(phone: str) -> bool:
        """判断是否为泰国号码"""
        if not phone:
            return False
        cleaned = re.sub(r'[^\d+]', '', phone)
        return (cleaned.startswith('+66') or 
                cleaned.startswith('66') or 
                cleaned.startswith('0066') or
                (cleaned.startswith('0') and len(cleaned) == 10))
    
    @staticmethod
    def extract_phone_from_text(text: str) -> Optional[str]:
        """从文本中提取电话号码"""
        if not text:
            return None
            
        # 匹配泰国号码模式
        patterns = [
            r'\+66\s*\d[\s-]?\d{3}[\s-]?\d{3}[\s-]?\d{3}',
            r'0\d[\s-]?\d{3}[\s-]?\d{3}[\s-]?\d{3}',
            r'66\d{9}',
            r'\+66\d{9}',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group()
        
        return None


# 测试
if __name__ == "__main__":
    formatter = ThailandPhoneFormatter()
    
    test_numbers = [
        "+66 2 123 4567",
        "02 123 4567",
        "081-234-5678",
        "+66812345678",
        "66812345678",
        "0066812345678",
    ]
    
    for num in test_numbers:
        result = formatter.format_to_whatsapp(num)
        print(f"{num} -> {result}")

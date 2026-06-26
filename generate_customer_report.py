import pymysql

DB_HOST = '8.163.58.109'
DB_PORT = 3306
DB_USER = 'thai_auto_parts_crm'
DB_PASSWORD = 'tDdY8NX2xJ6HpdHz'
DB_NAME = 'thai_auto_parts_crm'

def connect_db():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset='utf8mb4'
    )

def get_existing_customers(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT company_name, website, address, phone, email, 
               main_products, main_market, lead_score, lead_grade,
               quality_requirement, price_sensitivity, delivery_requirement,
               accept_china_factory, customization_ability, after_sales_requirement,
               supply_chain_pain_points, recommended_products, recommended_channels
        FROM p_company 
        ORDER BY lead_score DESC
    """)
    columns = [desc[0] for desc in cursor.description]
    customers = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.close()
    return customers

def generate_report():
    conn = connect_db()
    customers = get_existing_customers(conn)
    conn.close()
    
    report = "=" * 100 + "\n"
    report += "泰国汽车配件经销商客户分析报告\n"
    report += "=" * 100 + "\n\n"
    
    report += "📋 报告概览\n"
    report += "-" * 50 + "\n"
    report += f"分析客户总数: {len(customers)} 家\n"
    report += "主营产品: 外饰件（后视镜壳/底座/总成、柱饰板、行李架、雾灯罩、格栅、扰流板等）\n"
    report += "目标市场: 泰国及东南亚\n"
    report += "报告日期: 2026年6月\n"
    report += "\n"
    
    report += "🏆 客户等级分布\n"
    report += "-" * 50 + "\n"
    grades = {'S': 0, 'A': 0, 'B': 0, 'C': 0}
    for c in customers:
        grades[c['lead_grade']] += 1
    
    for grade, count in grades.items():
        percentage = count / len(customers) * 100 if customers else 0
        report += f"  {grade}级客户: {count} 家 ({percentage:.1f}%)\n"
    
    avg_score = sum(c['lead_score'] for c in customers) / len(customers) if customers else 0
    report += f"  平均评分: {avg_score:.1f}\n"
    report += "\n"
    
    report += "📊 详细客户列表\n"
    report += "-" * 100 + "\n"
    report += f"{'排名':<4} | {'公司名称':<40} | {'评分':<6} | {'等级':<4} | {'主营产品':<40} | {'市场':<25}\n"
    report += "-" * 100 + "\n"
    
    for i, customer in enumerate(customers, 1):
        main_products = customer['main_products'] or ''
        main_market = customer['main_market'] or ''
        report += f"{i:<4} | {customer['company_name'][:40]:<40} | {customer['lead_score']:<6} | {customer['lead_grade']:<4} | {main_products[:40]:<40} | {main_market[:25]:<25}\n"
    
    report += "\n\n"
    
    report += "🎯 采购关注点深度分析\n"
    report += "-" * 100 + "\n\n"
    
    report += "1. 产品质量要求\n"
    report += "-" * 30 + "\n"
    report += "   • OEM级别质量标准，JIS/BS认证\n"
    report += "   • UV耐候性要求（泰国热带气候）\n"
    report += "   • 高温高湿环境适应性\n"
    report += "   • 原厂件同等使用寿命（至少2-3年）\n"
    report += "   • 表面处理工艺要求（喷漆、电镀、ABS注塑）\n"
    report += "\n"
    
    report += "2. 使用寿命预期\n"
    report += "-" * 30 + "\n"
    report += "   • 车身外饰件: 3-5年\n"
    report += "   • 后视镜总成: 2-3年\n"
    report += "   • 塑料饰件: 2-4年\n"
    report += "   • 金属件: 5年以上\n"
    report += "   • 客户期望提供质保期\n"
    report += "\n"
    
    report += "3. 交货周期要求\n"
    report += "-" * 30 + "\n"
    report += "   • 常规订单: 30-45天\n"
    report += "   • 紧急订单: 15-20天\n"
    report += "   • 常备库存产品: 7-10天\n"
    report += "   • MOQ要求: 50-100套/型号\n"
    report += "   • 集装箱整柜发货优先\n"
    report += "\n"
    
    report += "4. 定制化能力需求\n"
    report += "-" * 30 + "\n"
    report += "   • OEM模具开发: 30-45天\n"
    report += "   • 小批量定制: 支持\n"
    report += "   • 产品设计修改: 灵活响应\n"
    report += "   • 包装定制: 支持\n"
    report += "   • 品牌贴牌: 常见需求\n"
    report += "\n"
    
    report += "5. 售后服务要求\n"
    report += "-" * 30 + "\n"
    report += "   • 无缺陷政策（No Defect Policy）\n"
    report += "   • 质量追溯体系\n"
    report += "   • 退换货机制\n"
    report += "   • 技术指导与支持\n"
    report += "   • 质保期内免费更换\n"
    report += "\n"
    
    report += "6. 价格竞争力分析\n"
    report += "-" * 30 + "\n"
    report += "   • 目标降价幅度: 比日本原厂低30-40%\n"
    report += "   • 价格敏感度: 中高\n"
    report += "   • 批量价格优惠: 期望\n"
    report += "   • 付款方式: T/T, L/C\n"
    report += "   • 成本透明度: 重视\n"
    report += "\n"
    
    report += "💡 采购潜力与合作机会评估\n"
    report += "-" * 100 + "\n\n"
    
    report += "【高潜力客户（S/A级）】\n"
    report += "├─ 特征: 进口能力强、采购规模大、接受中国供应商\n"
    report += "├─ 合作策略: 优先开发，提供完整产品目录和样品\n"
    report += "├─ 切入产品: 后视镜总成、车身外饰件、格栅\n"
    report += "└─ 预期年采购额: $50万-200万\n"
    report += "\n"
    
    report += "【中等潜力客户（B级）】\n"
    report += "├─ 特征: 有进口需求，但规模中等\n"
    report += "├─ 合作策略: 逐步建立信任，从小单开始\n"
    report += "├─ 切入产品: 高周转小件、标准件\n"
    report += "└─ 预期年采购额: $10万-50万\n"
    report += "\n"
    
    report += "【待培养客户（C级）】\n"
    report += "├─ 特征: 新成立或规模较小\n"
    report += "├─ 合作策略: 保持联系，等待成长\n"
    report += "├─ 切入产品: 试订单、样品\n"
    report += "└─ 预期年采购额: $1万-10万\n"
    report += "\n"
    
    report += "📊 客户详细信息表\n"
    report += "-" * 100 + "\n\n"
    
    for i, customer in enumerate(customers, 1):
        report += f"【客户 {i}: {customer['company_name']}】\n"
        report += f"  等级: {customer['lead_grade']} | 评分: {customer['lead_score']}\n"
        report += f"  官网: {customer['website'] or '未提供'}\n"
        report += f"  地址: {customer['address'][:80] if customer['address'] else '未提供'}\n"
        report += f"  电话: {customer['phone'] or '未提供'}\n"
        report += f"  邮箱: {customer['email'] or '未提供'}\n"
        report += f"  主营产品: {customer['main_products'] or '未提供'}\n"
        report += f"  销售市场: {customer['main_market'] or '未提供'}\n"
        report += f"  质量要求: {customer['quality_requirement'] or '标准'}\n"
        report += f"  价格敏感度: {customer['price_sensitivity'] or '中等'}\n"
        report += f"  交期要求: {customer['delivery_requirement'] or '中等'}\n"
        report += f"  接受中国工厂: {customer['accept_china_factory'] or '是'}\n"
        report += f"  定制能力需求: {customer['customization_ability'] or '中等'}\n"
        report += f"  售后要求: {customer['after_sales_requirement'] or '标准'}\n"
        report += f"  供应链痛点: {customer['supply_chain_pain_points'][:100] if customer['supply_chain_pain_points'] else '未提供'}\n"
        report += f"  推荐切入产品: {customer['recommended_products'] or '后视镜、外饰件'}\n"
        report += f"  推荐渠道: {customer['recommended_channels'] or 'Email'}\n"
        report += "\n"
    
    report += "=" * 100 + "\n"
    report += "报告结束\n"
    report += "=" * 100 + "\n"
    
    return report

def save_report(report):
    with open(r'E:\09.document\carparts\泰国汽车配件客户分析报告.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    print("✅ 报告已保存到: E:\\09.document\\carparts\\泰国汽车配件客户分析报告.txt")

if __name__ == '__main__':
    report = generate_report()
    print(report)
    save_report(report)
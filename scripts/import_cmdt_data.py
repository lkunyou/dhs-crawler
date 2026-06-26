import pymysql
import re

DB_HOST = '8.163.58.109'
DB_PORT = 3306
DB_USER = 'thai_auto_parts_crm'
DB_PASSWORD = 'tDdY8NX2xJ6HpdHz'
DB_NAME = 'thai_auto_parts_crm'

cmdt_raw_data = """
第1类 - 活动物;动物产品 (live animals; animal products) 02 - 肉及食用杂碎 (Meat and edible meat offal) 020002 - BEEF, FROZEN 020002 - 牛肉，冷冻
第1类 - 活动物;动物产品 (live animals; animal products) 02 - 肉及食用杂碎 (Meat and edible meat offal) 020003 - MEAT, FLANK, FROZEN 020003 - 肉类，侧腹，冷冻
第1类 - 活动物;动物产品 (live animals; animal products) 02 - 肉及食用杂碎 (Meat and edible meat offal) 020004 - POULTRY, FROZEN 020004 - 家禽，冷冻
第1类 - 活动物;动物产品 (live animals; animal products) 02 - 肉及食用杂碎 (Meat and edible meat offal) 020005 - BEEF OFFALS, EDIBLE 020005 - 牛肉内脏，食用
第1类 - 活动物;动物产品 (live animals; animal products) 02 - 肉及食用杂碎 (Meat and edible meat offal) 020006 - FROZEN BEEF 020006 - 牛肉，冷冻
第1类 - 活动物;动物产品 (live animals; animal products) 02 - 肉及食用杂碎 (Meat and edible meat offal) 020008 - SEASONED PORK, GROUND, FROZEN 020008 - 已腌制或调味的猪肉，绞碎的，冷冻
第1类 - 活动物;动物产品 (live animals; animal products) 02 - 肉及食用杂碎 (Meat and edible meat offal) 020009 - PORK PATTY, FROZEN 020009 - 猪肉馅饼，冷冻
第1类 - 活动物;动物产品 (live animals; animal products) 02 - 肉及食用杂碎 (Meat and edible meat offal) 020010 - HAM, SAUSAGE 020010 - 火腿，香肠
第1类 - 活动物;动物产品 (live animals; animal products) 02 - 肉及食用杂碎 (Meat and edible meat offal) 020101 - BEEF,FRESH OR CHILLED. 020101 - 牛肉，新鲜或冷藏
第1类 - 活动物;动物产品 (live animals; animal products) 02 - 肉及食用杂碎 (Meat and edible meat offal) 020200 - MEAT, FROZEN 020200 - 鲜肉，冷冻
第1类 - 活动物;动物产品 (live animals; animal products) 02 - 肉及食用杂碎 (Meat and edible meat offal) 020300 - DELI MEAT, HOT DOGS, PORK OFFALS, FROZEN 020300 - 熟食肉制品，热狗，猪内脏，冷冻
第1类 - 活动物;动物产品 (live animals; animal products) 02 - 肉及食用杂碎 (Meat and edible meat offal) 020601 - HORSEMEAT AND OFFALS 020601 - 马肉，马内脏
第1类 - 活动物;动物产品 (live animals; animal products) 02 - 肉及食用杂碎 (Meat and edible meat offal) 020603 - PORK, FRESH OR CHILLED 020603 - 猪肉，新鲜或冷藏
第1类 - 活动物;动物产品 (live animals; animal products) 02 - 肉及食用杂碎 (Meat and edible meat offal) 020604 - PORK FAT, FAT TRIMMINGS, LIVERS, OFFALS 020604 - 猪油，脂肪碎屑，猪肝，内脏
第1类 - 活动物;动物产品 (live animals; animal products) 02 - 肉及食用杂碎 (Meat and edible meat offal) 020608 - PORK, FROZEN 020608 - 猪肉，冷冻
第1类 - 活动物;动物产品 (live animals; animal products) 02 - 肉及食用杂碎 (Meat and edible meat offal) 020700 - BEEF AND PORK FATTY TISSUE 020700 - 牛肉脂肪，猪肉脂肪
第1类 - 活动物;动物产品 (live animals; animal products) 02 - 肉及食用杂碎 (Meat and edible meat offal) 020701 - POULTRY, FRESH, CHILLED OR FROZEN AND CHICKEN PARTS, WHOLE 020701 - 新鲜、冷藏或冷冻的整只家禽和鸡块
第1类 - 活动物;动物产品 (live animals; animal products) 02 - 肉及食用杂碎 (Meat and edible meat offal) 020703 - TURKEY, WHOLE, FROZEN 020703 - 火鸡，整只，冷冻
第1类 - 活动物;动物产品 (live animals; animal products) 02 - 肉及食用杂碎 (Meat and edible meat offal) 020800 - ILLEX, FROZEN 020800 - 鱿鱼，冷冻
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030000 - FISH AND CRUSTACEANS, MOLLUSC AND OTHER AQUATIC INVERTEBRATE 030000 - 鱼类，甲壳动物，软体动物，其它水生无脊椎动物
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030001 - SEAFOOD, CANNED 030001 - 海鲜，罐头
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030002 - MONK FISH, FROZEN 030002 - 安康鱼，冷冻
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030003 - FROZEN POLLOCK FILLET 030003 - 冷冻鳕鱼片
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030004 - ROASTED EEL, FROZEN 030004 - 烤鳗，冷冻
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030005 - TUNA FISH, FROZEN 030005 - 金枪鱼，冷冻
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030009 - SALTED DRY JELLY FISH 030009 - 盐渍干海蜇
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030010 - CROAKER, FROZEN 030010 - 黄花鱼，冷冻
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030012 - FISH 030012 - 鱼类
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030015 - FROZEN FISH 030015 - 冷冻鱼
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030017 - CUCUMBER, SEA, FROZEN 030017 - 大黄花鱼，海洋，冰冻
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030023 - HAG FISH, FROZEN 030023 - 海格鱼，冷冻
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030100 - EEL, FROZEN 030100 - 鳗鱼，冷冻
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030193 - FROZEN CARP 030193 - 冻鲤鱼
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030200 - CANNED SARDINES 030200 - 沙丁鱼罐头
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030201 - CANNED TUNA 030201 - 金枪鱼罐头
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030202 - MACKEREL, SQUID, FROZEN FOR CANNING 030202 - 竹夹鱼，鱿鱼，冻罐头
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030203 - COD ROE, FROZEN 030203 - 鳕鱼子，冷冻
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030204 - POLLOCK ROE, FROZEN 030204 - 明太子鱼子，冷冻
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030207 - MULLET ROE, FROZEN 030207 - 乌鱼子，冷冻
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030208 - ROE 030208 - 鱼子
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030209 - COD AND POLLOCK 030209 - 鳕鱼，狭鳕鱼
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030210 - FROZEN ANCHOVIES 030210 - 凤尾鱼，冷冻
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030302 - HALIBUT, FROZEN 030302 - 大比目鱼，冷冻
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030303 - BLACK COD, FROZEN 030303 - 黑鳕鱼，冷冻
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030304 - SARDINES, FROZEN 030304 - 沙丁鱼，冷冻
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030400 - SALMON, FROZEN 030400 - 鲑鱼，冷冻
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030401 - SALMON, PINK, FROZEN 030401 - 鲑鱼，粉红色，冷冻
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030600 - FROZEN SHRIMP 030600 - 冷冻虾
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030602 - CANNED SHRIMP 030602 - 虾罐头
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030603 - CANNED TOPSHELLS 030603 - 贝类海产，罐装的
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030604 - CLAMS, FROZEN 030604 - 蛤，冷冻
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030606 - CONCH MEAT 030606 - 海螺肉
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030608 - CRAB MEAT, FROZEN 030608 - 蟹肉，冷冻
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030610 - LOBSTER, FROZEN 030610 - 龙虾，冷冻
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030611 - PRAWNS AND SHRIMP, FRESH, CHILLED OR FROZEN 030611 - 虾，新鲜，冷藏或冷冻
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030613 - CRABS 030613 - 螃蟹
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030702 - SQUID, DRIED 030702 - 乌贼,干的
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030704 - CUTTLEFISH, OCTOPUS AND SQUID, FROZEN 030704 - 墨鱼，章鱼，鱿鱼，冷冻
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030705 - ASSORTED FROZEN MARINE PRODUCTS 030705 - 各种冷冻海产
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030709 - SCALLOP, FROZEN 030709 - 扇贝，冷冻
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030710 - BOTTOM FISH, FROZEN 030710 - 鲶鱼、鲤鱼或比目鱼等，冷冻
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030711 - CHUM SALMON, FROZEN 030711 - 鲑鱼，冷冻
第1类 - 活动物;动物产品 (live animals; animal products) 03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates) 030799 - JELLYFISH, FRESH, REFRIGERATED, NOT FROZEN 030799 - 海蜇，新鲜，冷藏，不会冻结的
第1类 - 活动物;动物产品 (live animals; animal products) 04 - 乳品;蛋品;天然蜂蜜;其他食用动物产品 (Dairy produce; birds' eggs; natural honey; edible products of animal origin, not elsewhere specified or included) 040000 - DAIRY PRODUCE, BIRDS EGGS, NATURAL HONEY, EDIBLE PRODUCTS OF ANIMAL ORIGIN 040000 - 乳制品，禽蛋，天然蜂蜜，动物来源的食品
第1类 - 活动物;动物产品 (live animals; animal products) 04 - 乳品;蛋品;天然蜂蜜;其他食用动物产品 (Dairy produce; birds' eggs; natural honey; edible products of animal origin, not elsewhere specified or included) 040001 - HONEY 040001 - 蜂蜜
第1类 - 活动物;动物产品 (live animals; animal products) 04 - 乳品;蛋品;天然蜂蜜;其他食用动物产品 (Dairy produce; birds' eggs; natural honey; edible products of animal origin, not elsewhere specified or included) 040002 - SOY MILK 040002 - 豆奶
第1类 - 活动物;动物产品 (live animals; animal products) 04 - 乳品;蛋品;天然蜂蜜;其他食用动物产品 (Dairy produce; birds' eggs; natural honey; edible products of animal origin, not elsewhere specified or included) 040003 - BEE WAX 040003 - 蜂蜡，蜂产品
第1类 - 活动物;动物产品 (live animals; animal products) 04 - 乳品;蛋品;天然蜂蜜;其他食用动物产品 (Dairy produce; birds' eggs; natural honey; edible products of animal origin, not elsewhere specified or included) 040004 - EGGS AND EGG YOLKS, WHOLE, DRIED OR POWDERED 040004 - 鸡蛋，蛋黄，全脂的，干的或粉状的
第1类 - 活动物;动物产品 (live animals; animal products) 04 - 乳品;蛋品;天然蜂蜜;其他食用动物产品 (Dairy produce; birds' eggs; natural honey; edible products of animal origin, not elsewhere specified or included) 040005 - CREAM 040005 - 奶油
第1类 - 活动物;动物产品 (live animals; animal products) 04 - 乳品;蛋品;天然蜂蜜;其他食用动物产品 (Dairy produce; birds' eggs; natural honey; edible products of animal origin, not elsewhere specified or included) 040006 - EGGS, FROZEN 040006 - 鸡蛋，冷冻
第1类 - 活动物;动物产品 (live animals; animal products) 04 - 乳品;蛋品;天然蜂蜜;其他食用动物产品 (Dairy produce; birds' eggs; natural honey; edible products of animal origin, not elsewhere specified or included) 040007 - WHIPPED TOPPINGS, DAIRY AND NON-DAIRY, CREAM AND MILK SUBSTITUTES 040007 - 乳制品，非乳制品，奶油，代乳品等搅打配料
第1类 - 活动物;动物产品 (live animals; animal products) 04 - 乳品;蛋品;天然蜂蜜;其他食用动物产品 (Dairy produce; birds' eggs; natural honey; edible products of animal origin, not elsewhere specified or included) 040200 - SKIMMED MILK, DRIED OR POWDERED 040200 - 干的脱脂牛奶制品，或脱脂奶粉
"""

def parse_section(section_str):
    match = re.match(r'第(\d+)类', section_str)
    if match:
        return match.group(1)
    return ''

def parse_chapter(chapter_str):
    match = re.match(r'(\d{2})\s*-', chapter_str)
    if match:
        return match.group(1)
    return ''

def parse_cmdt_line(line):
    if not line.strip():
        return None
    
    section_match = re.search(r'第\d+类[^0-9]+', line)
    section = section_match.group(0).strip() if section_match else ''
    
    remaining = line.replace(section, '')
    
    chapter_match = re.search(r'(\d{2}\s*-\s*[^0-9]+)', remaining)
    chapter = chapter_match.group(1).strip() if chapter_match else ''
    
    remaining = remaining.replace(chapter, '')
    
    code_en_match = re.search(r'(\d{6})\s*-\s*([^0-9]+?)(?=\s*\d{6}\s*-)', remaining)
    if not code_en_match:
        code_en_match = re.search(r'(\d{6})\s*-\s*(.+?)(?=\s*\d{6}\s*-)', remaining)
        if not code_en_match:
            code_en_match = re.search(r'(\d{6})\s*-\s*(.+)$', remaining)
    
    if not code_en_match:
        return None
    
    cmdt_code = code_en_match.group(1)
    description_en = code_en_match.group(2).strip()
    
    cn_match = re.search(rf'{cmdt_code}\s*-\s*(.+)$', remaining)
    description_cn = cn_match.group(1).strip() if cn_match else ''
    
    return {
        'section': section,
        'section_code': parse_section(section),
        'chapter': chapter,
        'chapter_code': parse_chapter(chapter),
        'cmdt_code': cmdt_code,
        'description_en': description_en,
        'description_cn': description_cn
    }

lines = cmdt_raw_data.strip().split('\n')
parsed_data = []
for line in lines:
    result = parse_cmdt_line(line)
    if result:
        parsed_data.append(result)

print(f"共解析到 {len(parsed_data)} 条记录")

conn = pymysql.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    charset='utf8mb4'
)

cursor = conn.cursor()

insert_sql = """
INSERT INTO p_cmdt_code (section, section_code, chapter, chapter_code, cmdt_code, description_en, description_cn)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

count = 0
for item in parsed_data:
    cursor.execute(insert_sql, (
        item['section'], item['section_code'],
        item['chapter'], item['chapter_code'],
        item['cmdt_code'], item['description_en'], item['description_cn']
    ))
    count += 1
    if count % 20 == 0:
        conn.commit()
        print(f"已导入 {count} 条记录...")

conn.commit()
print(f"\n✅ 成功导入 {count} 条CMDT编码记录")

cursor.execute("SELECT COUNT(*) FROM p_cmdt_code")
total = cursor.fetchone()[0]
print(f"📊 表中共有 {total} 条记录")

cursor.execute("SELECT section_code, COUNT(*) FROM p_cmdt_code GROUP BY section_code")
results = cursor.fetchall()
print("\n📈 大类分布:")
for row in results:
    print(f"  第{row[0]}类: {row[1]} 条")

cursor.execute("SELECT * FROM p_cmdt_code LIMIT 5")
results = cursor.fetchall()
print("\n📝 前5条记录:")
for row in results:
    print(f"  {row[5]} | {row[6]} | {row[7]}")

conn.close()

print("\n🎉 CMDT编码数据导入完成！")
import pymysql
import re

DB_HOST = '8.163.58.109'
DB_PORT = 3306
DB_USER = 'thai_auto_parts_crm'
DB_PASSWORD = 'tDdY8NX2xJ6HpdHz'
DB_NAME = 'thai_auto_parts_crm'

cmdt_data = [
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '02 - 肉及食用杂碎 (Meat and edible meat offal)', 'code': '020002', 'en': 'BEEF, FROZEN', 'cn': '牛肉，冷冻'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '02 - 肉及食用杂碎 (Meat and edible meat offal)', 'code': '020003', 'en': 'MEAT, FLANK, FROZEN', 'cn': '肉类，侧腹，冷冻'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '02 - 肉及食用杂碎 (Meat and edible meat offal)', 'code': '020004', 'en': 'POULTRY, FROZEN', 'cn': '家禽，冷冻'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '02 - 肉及食用杂碎 (Meat and edible meat offal)', 'code': '020005', 'en': 'BEEF OFFALS, EDIBLE', 'cn': '牛肉内脏，食用'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '02 - 肉及食用杂碎 (Meat and edible meat offal)', 'code': '020006', 'en': 'FROZEN BEEF', 'cn': '牛肉，冷冻'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '02 - 肉及食用杂碎 (Meat and edible meat offal)', 'code': '020008', 'en': 'SEASONED PORK, GROUND, FROZEN', 'cn': '已腌制或调味的猪肉，绞碎的，冷冻'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '02 - 肉及食用杂碎 (Meat and edible meat offal)', 'code': '020009', 'en': 'PORK PATTY, FROZEN', 'cn': '猪肉馅饼，冷冻'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '02 - 肉及食用杂碎 (Meat and edible meat offal)', 'code': '020010', 'en': 'HAM, SAUSAGE', 'cn': '火腿，香肠'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '02 - 肉及食用杂碎 (Meat and edible meat offal)', 'code': '020101', 'en': 'BEEF,FRESH OR CHILLED.', 'cn': '牛肉，新鲜或冷藏'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '02 - 肉及食用杂碎 (Meat and edible meat offal)', 'code': '020200', 'en': 'MEAT, FROZEN', 'cn': '鲜肉，冷冻'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '02 - 肉及食用杂碎 (Meat and edible meat offal)', 'code': '020300', 'en': 'DELI MEAT, HOT DOGS, PORK OFFALS, FROZEN', 'cn': '熟食肉制品，热狗，猪内脏，冷冻'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '02 - 肉及食用杂碎 (Meat and edible meat offal)', 'code': '020601', 'en': 'HORSEMEAT AND OFFALS', 'cn': '马肉，马内脏'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '02 - 肉及食用杂碎 (Meat and edible meat offal)', 'code': '020603', 'en': 'PORK, FRESH OR CHILLED', 'cn': '猪肉，新鲜或冷藏'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '02 - 肉及食用杂碎 (Meat and edible meat offal)', 'code': '020604', 'en': 'PORK FAT, FAT TRIMMINGS, LIVERS, OFFALS', 'cn': '猪油，脂肪碎屑，猪肝，内脏'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '02 - 肉及食用杂碎 (Meat and edible meat offal)', 'code': '020608', 'en': 'PORK, FROZEN', 'cn': '猪肉，冷冻'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '02 - 肉及食用杂碎 (Meat and edible meat offal)', 'code': '020700', 'en': 'BEEF AND PORK FATTY TISSUE', 'cn': '牛肉脂肪，猪肉脂肪'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '02 - 肉及食用杂碎 (Meat and edible meat offal)', 'code': '020701', 'en': 'POULTRY, FRESH, CHILLED OR FROZEN AND CHICKEN PARTS, WHOLE', 'cn': '新鲜、冷藏或冷冻的整只家禽和鸡块'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '02 - 肉及食用杂碎 (Meat and edible meat offal)', 'code': '020703', 'en': 'TURKEY, WHOLE, FROZEN', 'cn': '火鸡，整只，冷冻'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '02 - 肉及食用杂碎 (Meat and edible meat offal)', 'code': '020800', 'en': 'ILLEX, FROZEN', 'cn': '鱿鱼，冷冻'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030000', 'en': 'FISH AND CRUSTACEANS, MOLLUSC AND OTHER AQUATIC INVERTEBRATE', 'cn': '鱼类，甲壳动物，软体动物，其它水生无脊椎动物'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030001', 'en': 'SEAFOOD, CANNED', 'cn': '海鲜，罐头'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030002', 'en': 'MONK FISH, FROZEN', 'cn': '安康鱼，冷冻'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030003', 'en': 'FROZEN POLLOCK FILLET', 'cn': '冷冻鳕鱼片'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030004', 'en': 'ROASTED EEL, FROZEN', 'cn': '烤鳗，冷冻'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030005', 'en': 'TUNA FISH, FROZEN', 'cn': '金枪鱼，冷冻'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030009', 'en': 'SALTED DRY JELLY FISH', 'cn': '盐渍干海蜇'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030010', 'en': 'CROAKER, FROZEN', 'cn': '黄花鱼，冷冻'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030012', 'en': 'FISH', 'cn': '鱼类'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030015', 'en': 'FROZEN FISH', 'cn': '冷冻鱼'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030017', 'en': 'CUCUMBER, SEA, FROZEN', 'cn': '大黄花鱼，海洋，冰冻'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030023', 'en': 'HAG FISH, FROZEN', 'cn': '海格鱼，冷冻'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030100', 'en': 'EEL, FROZEN', 'cn': '鳗鱼，冷冻'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030193', 'en': 'FROZEN CARP', 'cn': '冻鲤鱼'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030200', 'en': 'CANNED SARDINES', 'cn': '沙丁鱼罐头'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030201', 'en': 'CANNED TUNA', 'cn': '金枪鱼罐头'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030202', 'en': 'MACKEREL, SQUID, FROZEN FOR CANNING', 'cn': '竹夹鱼，鱿鱼，冻罐头'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030203', 'en': 'COD ROE, FROZEN', 'cn': '鳕鱼子，冷冻'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030204', 'en': 'POLLOCK ROE, FROZEN', 'cn': '明太子鱼子，冷冻'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030207', 'en': 'MULLET ROE, FROZEN', 'cn': '乌鱼子，冷冻'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030208', 'en': 'ROE', 'cn': '鱼子'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030209', 'en': 'COD AND POLLOCK', 'cn': '鳕鱼，狭鳕鱼'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030210', 'en': 'FROZEN ANCHOVIES', 'cn': '凤尾鱼，冷冻'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030302', 'en': 'HALIBUT, FROZEN', 'cn': '大比目鱼，冷冻'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030303', 'en': 'BLACK COD, FROZEN', 'cn': '黑鳕鱼，冷冻'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030304', 'en': 'SARDINES, FROZEN', 'cn': '沙丁鱼，冷冻'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030400', 'en': 'SALMON, FROZEN', 'cn': '鲑鱼，冷冻'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030401', 'en': 'SALMON, PINK, FROZEN', 'cn': '鲑鱼，粉红色，冷冻'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030600', 'en': 'FROZEN SHRIMP', 'cn': '冷冻虾'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030602', 'en': 'CANNED SHRIMP', 'cn': '虾罐头'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030603', 'en': 'CANNED TOPSHELLS', 'cn': '贝类海产，罐装的'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030604', 'en': 'CLAMS, FROZEN', 'cn': '蛤，冷冻'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030606', 'en': 'CONCH MEAT', 'cn': '海螺肉'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030608', 'en': 'CRAB MEAT, FROZEN', 'cn': '蟹肉，冷冻'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030610', 'en': 'LOBSTER, FROZEN', 'cn': '龙虾，冷冻'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030611', 'en': 'PRAWNS AND SHRIMP, FRESH, CHILLED OR FROZEN', 'cn': '虾，新鲜，冷藏或冷冻'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030613', 'en': 'CRABS', 'cn': '螃蟹'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030702', 'en': 'SQUID, DRIED', 'cn': '乌贼,干的'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030704', 'en': 'CUTTLEFISH, OCTOPUS AND SQUID, FROZEN', 'cn': '墨鱼，章鱼，鱿鱼，冷冻'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030705', 'en': 'ASSORTED FROZEN MARINE PRODUCTS', 'cn': '各种冷冻海产'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030709', 'en': 'SCALLOP, FROZEN', 'cn': '扇贝，冷冻'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030710', 'en': 'BOTTOM FISH, FROZEN', 'cn': '鲶鱼、鲤鱼或比目鱼等，冷冻'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030711', 'en': 'CHUM SALMON, FROZEN', 'cn': '鲑鱼，冷冻'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '03 - 鱼、甲壳动物,软体动物及其他水生无脊椎动物 (Fish and crustaceans, molluscs and other aquatic invertebrates)', 'code': '030799', 'en': 'JELLYFISH, FRESH, REFRIGERATED, NOT FROZEN', 'cn': '海蜇，新鲜，冷藏，不会冻结的'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '04 - 乳品;蛋品;天然蜂蜜;其他食用动物产品 (Dairy produce; birds eggs; natural honey; edible products of animal origin, not elsewhere specified or included)', 'code': '040000', 'en': 'DAIRY PRODUCE, BIRDS EGGS, NATURAL HONEY, EDIBLE PRODUCTS OF ANIMAL ORIGIN', 'cn': '乳制品，禽蛋，天然蜂蜜，动物来源的食品'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '04 - 乳品;蛋品;天然蜂蜜;其他食用动物产品 (Dairy produce; birds eggs; natural honey; edible products of animal origin, not elsewhere specified or included)', 'code': '040001', 'en': 'HONEY', 'cn': '蜂蜜'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '04 - 乳品;蛋品;天然蜂蜜;其他食用动物产品 (Dairy produce; birds eggs; natural honey; edible products of animal origin, not elsewhere specified or included)', 'code': '040002', 'en': 'SOY MILK', 'cn': '豆奶'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '04 - 乳品;蛋品;天然蜂蜜;其他食用动物产品 (Dairy produce; birds eggs; natural honey; edible products of animal origin, not elsewhere specified or included)', 'code': '040003', 'en': 'BEE WAX', 'cn': '蜂蜡，蜂产品'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '04 - 乳品;蛋品;天然蜂蜜;其他食用动物产品 (Dairy produce; birds eggs; natural honey; edible products of animal origin, not elsewhere specified or included)', 'code': '040004', 'en': 'EGGS AND EGG YOLKS, WHOLE, DRIED OR POWDERED', 'cn': '鸡蛋，蛋黄，全脂的，干的或粉状的'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '04 - 乳品;蛋品;天然蜂蜜;其他食用动物产品 (Dairy produce; birds eggs; natural honey; edible products of animal origin, not elsewhere specified or included)', 'code': '040005', 'en': 'CREAM', 'cn': '奶油'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '04 - 乳品;蛋品;天然蜂蜜;其他食用动物产品 (Dairy produce; birds eggs; natural honey; edible products of animal origin, not elsewhere specified or included)', 'code': '040006', 'en': 'EGGS, FROZEN', 'cn': '鸡蛋，冷冻'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '04 - 乳品;蛋品;天然蜂蜜;其他食用动物产品 (Dairy produce; birds eggs; natural honey; edible products of animal origin, not elsewhere specified or included)', 'code': '040007', 'en': 'WHIPPED TOPPINGS, DAIRY AND NON-DAIRY, CREAM AND MILK SUBSTITUTES', 'cn': '乳制品，非乳制品，奶油，代乳品等搅打配料'},
    {'section': '第1类 - 活动物;动物产品 (live animals; animal products)', 'chapter': '04 - 乳品;蛋品;天然蜂蜜;其他食用动物产品 (Dairy produce; birds eggs; natural honey; edible products of animal origin, not elsewhere specified or included)', 'code': '040200', 'en': 'SKIMMED MILK, DRIED OR POWDERED', 'cn': '干的脱脂牛奶制品，或脱脂奶粉'},
]

def parse_section_code(section_str):
    match = re.match(r'第(\d+)类', section_str)
    return match.group(1) if match else ''

def parse_chapter_code(chapter_str):
    match = re.match(r'(\d{2})', chapter_str)
    return match.group(1) if match else ''

conn = pymysql.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    charset='utf8mb4'
)

cursor = conn.cursor()

cursor.execute("DELETE FROM p_cmdt_code")

insert_sql = """
INSERT INTO p_cmdt_code (section, section_code, chapter, chapter_code, cmdt_code, description_en, description_cn)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

count = 0
for item in cmdt_data:
    cursor.execute(insert_sql, (
        item['section'],
        parse_section_code(item['section']),
        item['chapter'],
        parse_chapter_code(item['chapter']),
        item['code'],
        item['en'],
        item['cn']
    ))
    count += 1

conn.commit()
print(f"✅ 成功导入 {count} 条CMDT编码记录")

cursor.execute("SELECT COUNT(*) FROM p_cmdt_code")
total = cursor.fetchone()[0]
print(f"📊 表中共有 {total} 条记录")

cursor.execute("SELECT chapter_code, COUNT(*) FROM p_cmdt_code GROUP BY chapter_code ORDER BY chapter_code")
results = cursor.fetchall()
print("\n📈 中类(HS Code 二位编码)分布:")
for row in results:
    cursor.execute("SELECT chapter FROM p_cmdt_code WHERE chapter_code = %s LIMIT 1", (row[0],))
    chapter_name = cursor.fetchone()[0]
    print(f"  {row[0]} - {chapter_name[:40]}: {row[1]} 条")

cursor.execute("SELECT cmdt_code, description_en, description_cn FROM p_cmdt_code LIMIT 10")
results = cursor.fetchall()
print("\n📝 前10条记录示例:")
for row in results:
    print(f"  {row[0]} | {row[1][:30]:<30} | {row[2][:25]:<25}")

conn.close()

print("\n🎉 CMDT编码数据导入完成！")
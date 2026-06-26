import pymysql

DB_HOST = '8.163.58.109'
DB_PORT = 3306
DB_USER = 'thai_auto_parts_crm'
DB_PASSWORD = 'tDdY8NX2xJ6HpdHz'
DB_NAME = 'thai_auto_parts_crm'

companies_data = [
    {'company_name': 'Thai Summit Group', 'company_type_cn': '制造商/经销商', 'website': 'www.thaisummit.co.th', 'address': 'Bangkok', 'phone': '+66 2-325-8000', 'email': 'info@thaisummit.co.th', 'core_contact': '-', 'main_products': '底盘、线束、金属和塑料部件', 'main_market': '全球', 'company_size': '大型', 'revenue_usd': 10000, 'purchase_potential': '极高', 'cooperation_opportunity': 'OEM/ODM合作、技术支持', 'development_priority': 'A'},
    {'company_name': 'Siam Motors Parts Co., Ltd', 'company_type_cn': '经销商', 'website': 'www.smparts.co.th', 'address': 'Bangkok', 'phone': '+66 2726-8080', 'email': 'marketing@smparts.co.th', 'core_contact': '-', 'main_products': '汽车车身零部件、维修配件', 'main_market': '泰国', 'company_size': '大型', 'revenue_usd': 5000, 'purchase_potential': '高', 'cooperation_opportunity': '零部件供应、分销合作', 'development_priority': 'A'},
    {'company_name': 'JPM Automotive (Thailand)', 'company_type_cn': '经销商/进口商', 'website': 'www.jpmautomotive.com', 'address': 'Bangkok', 'phone': '+66 86-819-4050', 'email': 'jpmgroup.th@gmail.com', 'core_contact': '-', 'main_products': '发动机零部件、OEM组件、售后配件', 'main_market': '全球', 'company_size': '中型', 'revenue_usd': 1500, 'purchase_potential': '中高', 'cooperation_opportunity': '进口代理、技术合作', 'development_priority': 'B'},
    {'company_name': 'President Automobile Industries Public Co., Ltd (PACO)', 'company_type_cn': '制造商', 'website': 'www.paco.co.th', 'address': 'Bangkok', 'phone': '02-810-9900', 'email': 'paco@paco.co.th', 'core_contact': '-', 'main_products': '汽车空调冷凝器、蒸发器', 'main_market': '全球', 'company_size': '中型', 'revenue_usd': 2000, 'purchase_potential': '高', 'cooperation_opportunity': 'OEM合作、技术研发', 'development_priority': 'A'},
    {'company_name': 'CHOAKNUMCHAI AUTOPARTS 789 Co., Ltd', 'company_type_cn': '经销商/零售商', 'website': 'www.thailand-autoparts.com', 'address': 'Bangkok', 'phone': '+66 927955144', 'email': 'cncautopart789@gmail.com', 'core_contact': '-', 'main_products': '日本汽车零部件、照明系统、车身部件', 'main_market': '泰国', 'company_size': '小型', 'revenue_usd': 500, 'purchase_potential': '中', 'cooperation_opportunity': '产品供应、批发合作', 'development_priority': 'C'},
    {'company_name': 'TOYOTOMI Auto Parts (Thailand) Co., Ltd', 'company_type_cn': '制造商', 'website': 'www.toyotomi.co.th', 'address': 'Bangkok', 'phone': '+6638-989-808', 'email': 'info@toyotomi.co.th', 'core_contact': '-', 'main_products': '高精度冲压金属件、车身部件', 'main_market': '全球', 'company_size': '中型', 'revenue_usd': 2500, 'purchase_potential': '高', 'cooperation_opportunity': 'OEM零部件供应', 'development_priority': 'A'},
    {'company_name': 'PakTokyo Co., Ltd (PTC Thailand)', 'company_type_cn': '制造商/出口商', 'website': 'www.ptcthailand.com', 'address': 'Bangkok', 'phone': '+66-2 4631900', 'email': 'export@ptcthailand.com', 'core_contact': '-', 'main_products': '汽车零部件、定制化部件', 'main_market': '全球', 'company_size': '中型', 'revenue_usd': 1800, 'purchase_potential': '中高', 'cooperation_opportunity': '出口合作、定制开发', 'development_priority': 'B'},
    {'company_name': 'Kyowa NT (Thailand) Co.,Ltd', 'company_type_cn': '制造商/供应商', 'website': 'www.kwnt.co.th', 'address': 'Ayutthaya', 'phone': '+66 35-330-431', 'email': 'marketing@kwnt.co.th', 'core_contact': '-', 'main_products': '高精度CNC机械零件', 'main_market': '全球', 'company_size': '中型', 'revenue_usd': 1200, 'purchase_potential': '中高', 'cooperation_opportunity': '精密零部件供应', 'development_priority': 'B'},
    {'company_name': 'Aisin Takaoka Thailand Group (ATTG)', 'company_type_cn': '制造商/供应商', 'website': 'www.attg.co.th', 'address': 'Chon Buri', 'phone': '+66-2-529-1893', 'email': 'sales@attg.co.th', 'core_contact': '-', 'main_products': '刹车盘、刹车鼓、歧管零件', 'main_market': '全球', 'company_size': '大型', 'revenue_usd': 8000, 'purchase_potential': '极高', 'cooperation_opportunity': 'OEM零部件合作', 'development_priority': 'A'},
    {'company_name': 'S.K.E. Autopart Company Limited', 'company_type_cn': '经销商', 'website': 'www.skeautopart.com', 'address': 'Bangkok', 'phone': '02-898-5791', 'email': 'ske.autopart@gmail.com', 'core_contact': '-', 'main_products': '日本和欧洲汽车零部件', 'main_market': '泰国', 'company_size': '小型', 'revenue_usd': 600, 'purchase_potential': '中', 'cooperation_opportunity': '零部件批发', 'development_priority': 'C'},
    {'company_name': 'R.R.D. Automotive (Thailand) Co., Ltd.', 'company_type_cn': '制造商', 'website': 'www.rrd-automotive.com', 'address': 'Nong Khae', 'phone': '0-3637-4171-5', 'email': 'info@rrd-automotive.com', 'core_contact': '-', 'main_products': '金属冲压件、车身结构组件', 'main_market': '全球', 'company_size': '中型', 'revenue_usd': 1500, 'purchase_potential': '中高', 'cooperation_opportunity': 'OEM制造合作', 'development_priority': 'B'},
    {'company_name': 'Bangkok Unity Auto Parts Co.,Ltd.', 'company_type_cn': '分销商', 'website': 'www.buautoparts.com', 'address': 'Bangkok/Pathum Thani', 'phone': '+66-81-444-7024', 'email': 'support@bu-autoparts.com', 'core_contact': '-', 'main_products': '日本汽车零部件、发动机组件、涡轮增压器', 'main_market': '泰国/全球', 'company_size': '中型', 'revenue_usd': 1200, 'purchase_potential': '中高', 'cooperation_opportunity': '零部件供应、分销合作', 'development_priority': 'B'},
    {'company_name': 'Yokohama Tire (Thailand) Co., Ltd', 'company_type_cn': '经销商/制造商', 'website': 'www.yokohamathailand.com', 'address': 'Bangkok', 'phone': '02 652-6996', 'email': 'info@yokohama.co.th', 'core_contact': '-', 'main_products': '高性能轮胎、乘用车/SUV轮胎', 'main_market': '泰国/全球', 'company_size': '大型', 'revenue_usd': 6000, 'purchase_potential': '极高', 'cooperation_opportunity': '轮胎供应、技术合作', 'development_priority': 'A'},
    {'company_name': 'Bridgestone Holdings (Thailand) Co., Ltd.', 'company_type_cn': '经销商/制造商', 'website': 'www.bridgestone.co.th', 'address': 'Bangkok', 'phone': '+66 2636-1555', 'email': '-', 'core_contact': '-', 'main_products': '各类轮胎、橡胶制品', 'main_market': '泰国/全球', 'company_size': '大型', 'revenue_usd': 15000, 'purchase_potential': '极高', 'cooperation_opportunity': '轮胎供应、战略合作', 'development_priority': 'A'},
    {'company_name': 'MAXXIS International (Thailand) Co., Ltd', 'company_type_cn': '制造商/经销商', 'website': 'www.maxxis.co.th', 'address': 'Rayong', 'phone': '038 955 856', 'email': 'hr_recruit@maxxis.co.th', 'core_contact': '-', 'main_products': '乘用车轮胎、摩托车轮胎、越野车轮胎', 'main_market': '泰国/全球', 'company_size': '大型', 'revenue_usd': 8000, 'purchase_potential': '极高', 'cooperation_opportunity': '轮胎供应、OEM合作', 'development_priority': 'A'},
    {'company_name': 'N.D. Rubber Public Co., Ltd', 'company_type_cn': '制造商', 'website': 'www.ndrubber.co.th', 'address': 'Ban Bueng', 'phone': '089 131 5000', 'email': 'ndrubber@ndrubber.co.th', 'core_contact': '-', 'main_products': '摩托车轮胎、内胎', 'main_market': '泰国/东南亚', 'company_size': '中型', 'revenue_usd': 2000, 'purchase_potential': '高', 'cooperation_opportunity': '摩托车轮胎供应', 'development_priority': 'B'},
    {'company_name': 'TOYO TIRES Thailand', 'company_type_cn': '经销商', 'website': 'www.toyotires.in.th', 'address': 'Bangkok', 'phone': '+66 2-024 8091-9', 'email': 'tsiam@loxinfo.co.th', 'core_contact': '-', 'main_products': '高性能轮胎、乘用车/SUV轮胎', 'main_market': '泰国', 'company_size': '中型', 'revenue_usd': 3000, 'purchase_potential': '高', 'cooperation_opportunity': '轮胎分销合作', 'development_priority': 'B'},
    {'company_name': 'Michelin Tyres Thailand', 'company_type_cn': '制造商/经销商', 'website': 'www.michelin.co.th', 'address': 'Bangkok', 'phone': '+66 2-700-3993', 'email': '-', 'core_contact': '-', 'main_products': '乘用车轮胎、摩托车轮胎、卡车轮胎、飞机轮胎', 'main_market': '泰国/全球', 'company_size': '大型', 'revenue_usd': 12000, 'purchase_potential': '极高', 'cooperation_opportunity': '轮胎供应、战略合作', 'development_priority': 'A'},
    {'company_name': 'Goodyear Thailand', 'company_type_cn': '经销商/制造商', 'website': '-', 'address': 'Pathum Thani', 'phone': '-', 'email': '-', 'core_contact': '-', 'main_products': '各类轮胎产品', 'main_market': '泰国/全球', 'company_size': '大型', 'revenue_usd': 5000, 'purchase_potential': '极高', 'cooperation_opportunity': '轮胎供应合作', 'development_priority': 'A'},
    {'company_name': 'Dunlop Tire (Thailand) Co.,Ltd', 'company_type_cn': '制造商', 'website': '-', 'address': 'Bangkok', 'phone': '-', 'email': '-', 'core_contact': '-', 'main_products': '轮胎产品', 'main_market': '泰国/全球', 'company_size': '大型', 'revenue_usd': 4000, 'purchase_potential': '高', 'cooperation_opportunity': '轮胎供应合作', 'development_priority': 'A'},
    {'company_name': 'NEXEN TIRE Thailand', 'company_type_cn': '制造商', 'website': '-', 'address': 'Bangkok', 'phone': '-', 'email': '-', 'core_contact': '-', 'main_products': '轮胎产品', 'main_market': '泰国/全球', 'company_size': '中型', 'revenue_usd': 2500, 'purchase_potential': '高', 'cooperation_opportunity': '轮胎供应合作', 'development_priority': 'B'},
    {'company_name': 'Finixx Tire (Thailand)', 'company_type_cn': '制造商', 'website': '-', 'address': 'Bangkok', 'phone': '-', 'email': '-', 'core_contact': '-', 'main_products': '轮胎产品', 'main_market': '泰国', 'company_size': '中型', 'revenue_usd': 1500, 'purchase_potential': '中高', 'cooperation_opportunity': '轮胎供应合作', 'development_priority': 'B'},
    {'company_name': 'Ek-Chai Distribution System Co. Ltd (Lotus’s)', 'company_type_cn': '经销商/零售商', 'website': 'www.ekchai.co.th', 'address': 'Bangkok', 'phone': '+66-2-742-9362-7', 'email': 'info@ekchai.co.th', 'core_contact': '-', 'main_products': '汽车配件零售（通过Lotus超市网络）', 'main_market': '泰国', 'company_size': '大型', 'revenue_usd': 20000, 'purchase_potential': '极高', 'cooperation_opportunity': '零售渠道合作', 'development_priority': 'A'},
    {'company_name': 'Union Autoparts Manufacturing Co., Ltd. (UAM)', 'company_type_cn': '制造商', 'website': '-', 'address': 'Samut Prakan', 'phone': '-', 'email': '-', 'core_contact': '-', 'main_products': '汽车零部件', 'main_market': '全球', 'company_size': '中型', 'revenue_usd': 2000, 'purchase_potential': '高', 'cooperation_opportunity': 'OEM零部件供应', 'development_priority': 'B'},
    {'company_name': 'Thai Auto Tools And Die Public Co., Ltd', 'company_type_cn': '制造商', 'website': '-', 'address': 'Pathum Thani', 'phone': '-', 'email': '-', 'core_contact': '-', 'main_products': '汽车零部件模具、工具', 'main_market': '全球', 'company_size': '中型', 'revenue_usd': 1800, 'purchase_potential': '中高', 'cooperation_opportunity': '模具技术合作', 'development_priority': 'B'},
    {'company_name': 'Eversuccess Auto (Thailand) Limited', 'company_type_cn': '经销商/进口商', 'website': '-', 'address': 'Bangkok', 'phone': '-', 'email': '-', 'core_contact': '-', 'main_products': '汽车及汽车零部件', 'main_market': '泰国/全球', 'company_size': '中型', 'revenue_usd': 1500, 'purchase_potential': '中高', 'cooperation_opportunity': '进口代理合作', 'development_priority': 'B'},
    {'company_name': 'SEA Export Co., Ltd.', 'company_type_cn': '供应商/出口商', 'website': '-', 'address': 'Bangkok', 'phone': '-', 'email': '-', 'core_contact': '-', 'main_products': '汽车零部件', 'main_market': '全球', 'company_size': '小型', 'revenue_usd': 800, 'purchase_potential': '中', 'cooperation_opportunity': '产品供应、出口合作', 'development_priority': 'C'},
    {'company_name': 'Burson Auto Part', 'company_type_cn': '零售商', 'website': '-', 'address': 'Bangkok', 'phone': '-', 'email': '-', 'core_contact': '-', 'main_products': '汽车零部件零售', 'main_market': '泰国', 'company_size': '小型', 'revenue_usd': 500, 'purchase_potential': '中', 'cooperation_opportunity': '零售供应合作', 'development_priority': 'C'},
    {'company_name': 'Sun Trading (Thailand), Co.,Ltd', 'company_type_cn': '供应商', 'website': '-', 'address': 'Bangkok', 'phone': '-', 'email': '-', 'core_contact': '-', 'main_products': '汽车配件', 'main_market': '泰国', 'company_size': '小型', 'revenue_usd': 400, 'purchase_potential': '中', 'cooperation_opportunity': '配件供应合作', 'development_priority': 'C'},
    {'company_name': 'Nissan Trading (Thailand) Co., Ltd.', 'company_type_cn': '经销商', 'website': '-', 'address': 'Bangkok', 'phone': '-', 'email': '-', 'core_contact': '-', 'main_products': '日产汽车零部件', 'main_market': '泰国', 'company_size': '大型', 'revenue_usd': 6000, 'purchase_potential': '极高', 'cooperation_opportunity': '授权零部件供应', 'development_priority': 'A'},
    {'company_name': 'Pro Automotive Corporation Co.,Ltd', 'company_type_cn': '经销商', 'website': '-', 'address': 'Bangkok', 'phone': '-', 'email': '-', 'core_contact': '-', 'main_products': '汽车零部件分销', 'main_market': '泰国', 'company_size': '中型', 'revenue_usd': 2000, 'purchase_potential': '高', 'cooperation_opportunity': '分销合作', 'development_priority': 'B'},
    {'company_name': 'American Petrochemical (Thailand) Co.,Ltd', 'company_type_cn': '经销商', 'website': '-', 'address': 'Bangkok', 'phone': '-', 'email': '-', 'core_contact': '-', 'main_products': '润滑油产品', 'main_market': '泰国', 'company_size': '中型', 'revenue_usd': 1500, 'purchase_potential': '中高', 'cooperation_opportunity': '润滑油供应合作', 'development_priority': 'B'},
    {'company_name': 'Repsol Lubricants Thailand', 'company_type_cn': '经销商', 'website': '-', 'address': 'Bangkok', 'phone': '-', 'email': '-', 'core_contact': '-', 'main_products': '润滑油', 'main_market': '泰国', 'company_size': '中型', 'revenue_usd': 2000, 'purchase_potential': '高', 'cooperation_opportunity': '润滑油供应合作', 'development_priority': 'B'},
    {'company_name': 'Opposite Lock Thailand', 'company_type_cn': '供应商', 'website': '-', 'address': 'Bangkok', 'phone': '-', 'email': '-', 'core_contact': '-', 'main_products': '汽车电子产品', 'main_market': '泰国', 'company_size': '小型', 'revenue_usd': 600, 'purchase_potential': '中', 'cooperation_opportunity': '电子产品供应', 'development_priority': 'C'},
    {'company_name': 'Echo Autoparts (Thailand) Co., Ltd.', 'company_type_cn': '制造商', 'website': '-', 'address': 'Chachoengsao', 'phone': '-', 'email': '-', 'core_contact': '-', 'main_products': '汽车塑料零部件', 'main_market': '全球', 'company_size': '中型', 'revenue_usd': 1800, 'purchase_potential': '中高', 'cooperation_opportunity': '塑料零部件供应', 'development_priority': 'B'},
    {'company_name': 'TYREPLUS Thailand', 'company_type_cn': '零售商', 'website': '-', 'address': 'Bangkok', 'phone': '-', 'email': '-', 'core_contact': '-', 'main_products': '轮胎及配件零售', 'main_market': '泰国', 'company_size': '中型', 'revenue_usd': 1200, 'purchase_potential': '中高', 'cooperation_opportunity': '零售供应合作', 'development_priority': 'C'},
    {'company_name': 'Cockpit Thailand', 'company_type_cn': '零售商', 'website': '-', 'address': 'Bangkok', 'phone': '-', 'email': '-', 'core_contact': '-', 'main_products': '轮胎及配件', 'main_market': '泰国', 'company_size': '小型', 'revenue_usd': 500, 'purchase_potential': '中', 'cooperation_opportunity': '配件供应合作', 'development_priority': 'C'},
    {'company_name': 'TNAUTOCARE Co., Ltd', 'company_type_cn': '供应商', 'website': '-', 'address': 'Samut Prakan', 'phone': '-', 'email': '-', 'core_contact': '-', 'main_products': '发动机油、汽车配件', 'main_market': '泰国', 'company_size': '小型', 'revenue_usd': 400, 'purchase_potential': '中', 'cooperation_opportunity': '油品供应合作', 'development_priority': 'C'},
    {'company_name': 'S.P.R.Y Auto Parts Co.,Ltd', 'company_type_cn': '制造商', 'website': '-', 'address': 'Bangkok', 'phone': '-', 'email': '-', 'core_contact': '-', 'main_products': '塑料汽车零部件', 'main_market': '全球', 'company_size': '中型', 'revenue_usd': 1500, 'purchase_potential': '中高', 'cooperation_opportunity': '塑料零部件供应', 'development_priority': 'B'},
    {'company_name': 'G.P.Auto Parts Co.,Ltd.', 'company_type_cn': '供应商', 'website': '-', 'address': 'Bangkok', 'phone': '-', 'email': '-', 'core_contact': '-', 'main_products': '汽车零部件', 'main_market': '泰国', 'company_size': '小型', 'revenue_usd': 500, 'purchase_potential': '中', 'cooperation_opportunity': '零部件供应', 'development_priority': 'C'},
    {'company_name': 'YonMing Auto (Thailand) Co., Ltd', 'company_type_cn': '供应商', 'website': '-', 'address': 'Pathum Thani', 'phone': '-', 'email': '-', 'core_contact': '-', 'main_products': '汽车零部件及配件', 'main_market': '泰国', 'company_size': '小型', 'revenue_usd': 600, 'purchase_potential': '中', 'cooperation_opportunity': '零部件供应', 'development_priority': 'C'},
    {'company_name': 'CNY Import & Export Co., Ltd', 'company_type_cn': '进口商/制造商', 'website': '-', 'address': 'Bangkok', 'phone': '-', 'email': '-', 'core_contact': '-', 'main_products': '汽车制造及零部件', 'main_market': '全球', 'company_size': '中型', 'revenue_usd': 2000, 'purchase_potential': '高', 'cooperation_opportunity': '进口合作、制造合作', 'development_priority': 'B'},
    {'company_name': 'TT (I.K.I) AUTOPARTS CO., LTD', 'company_type_cn': '供应商', 'website': '-', 'address': 'Pathum Thani', 'phone': '-', 'email': '-', 'core_contact': '-', 'main_products': '汽车零部件', 'main_market': '泰国/全球', 'company_size': '中型', 'revenue_usd': 1200, 'purchase_potential': '中高', 'cooperation_opportunity': '零部件供应', 'development_priority': 'B'},
    {'company_name': 'Skyrace International Co. Ltd', 'company_type_cn': '经销商', 'website': '-', 'address': 'Bangkok', 'phone': '-', 'email': '-', 'core_contact': '-', 'main_products': '轮胎分销', 'main_market': '泰国', 'company_size': '小型', 'revenue_usd': 500, 'purchase_potential': '中', 'cooperation_opportunity': '轮胎分销合作', 'development_priority': 'C'},
    {'company_name': 'Stamford Tyres Thailand', 'company_type_cn': '经销商', 'website': '-', 'address': 'Bangkok', 'phone': '-', 'email': '-', 'core_contact': '-', 'main_products': '轮胎分销', 'main_market': '泰国', 'company_size': '中型', 'revenue_usd': 1000, 'purchase_potential': '中高', 'cooperation_opportunity': '轮胎分销合作', 'development_priority': 'B'},
    {'company_name': 'Khow Inter Business Co.,Ltd (KIB)', 'company_type_cn': '经销商', 'website': '-', 'address': 'Bangkok', 'phone': '-', 'email': '-', 'core_contact': '-', 'main_products': '轮胎分销', 'main_market': '泰国', 'company_size': '小型', 'revenue_usd': 600, 'purchase_potential': '中', 'cooperation_opportunity': '轮胎分销合作', 'development_priority': 'C'},
    {'company_name': 'Grip Thailand', 'company_type_cn': '经销商', 'website': '-', 'address': 'Bangkok', 'phone': '-', 'email': '-', 'core_contact': '-', 'main_products': '轮胎零售', 'main_market': '泰国', 'company_size': '小型', 'revenue_usd': 400, 'purchase_potential': '中', 'cooperation_opportunity': '轮胎供应合作', 'development_priority': 'C'},
    {'company_name': 'Siam Rubber Company Limited', 'company_type_cn': '制造商', 'website': '-', 'address': 'Samut Sakhon', 'phone': '-', 'email': '-', 'core_contact': '-', 'main_products': '轮胎制造', 'main_market': '泰国/全球', 'company_size': '中型', 'revenue_usd': 2000, 'purchase_potential': '高', 'cooperation_opportunity': '轮胎制造合作', 'development_priority': 'B'},
    {'company_name': 'Camel Industries Co., Ltd', 'company_type_cn': '制造商', 'website': '-', 'address': 'Bangkok', 'phone': '-', 'email': '-', 'core_contact': '-', 'main_products': '摩托车和自行车轮胎', 'main_market': '泰国/东南亚', 'company_size': '中型', 'revenue_usd': 1500, 'purchase_potential': '中高', 'cooperation_opportunity': '摩托车轮胎供应', 'development_priority': 'B'},
    {'company_name': 'OTR Tire Thailand', 'company_type_cn': '制造商', 'website': '-', 'address': 'Ban Bueng', 'phone': '-', 'email': '-', 'core_contact': '-', 'main_products': '工程机械轮胎', 'main_market': '全球', 'company_size': '中型', 'revenue_usd': 1800, 'purchase_potential': '中高', 'cooperation_opportunity': '工程机械轮胎供应', 'development_priority': 'B'},
    {'company_name': 'Archar Tyre', 'company_type_cn': '制造商', 'website': '-', 'address': 'Samut Prakan', 'phone': '-', 'email': '-', 'core_contact': '-', 'main_products': '轮胎制造', 'main_market': '泰国/全球', 'company_size': '中型', 'revenue_usd': 2000, 'purchase_potential': '高', 'cooperation_opportunity': '轮胎制造合作', 'development_priority': 'B'},
    {'company_name': 'AJ Automotive (Thailand) Co., Ltd.', 'company_type_cn': '进口商', 'website': '-', 'address': 'Bangkok', 'phone': '-', 'email': '-', 'core_contact': '-', 'main_products': '合金轮毂、汽车轮胎进口', 'main_market': '泰国', 'company_size': '小型', 'revenue_usd': 600, 'purchase_potential': '中', 'cooperation_opportunity': '进口代理合作', 'development_priority': 'C'},
]

def connect_db():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset='utf8mb4'
    )

def parse_company_type(type_cn):
    if '制造商' in type_cn:
        return 'Manufacturer'
    if '进口商' in type_cn:
        return 'Importer'
    if '经销商' in type_cn or '分销商' in type_cn or '出口商' in type_cn:
        return 'Distributor'
    if '零售商' in type_cn:
        return 'Retailer'
    if '供应商' in type_cn:
        return 'Distributor'
    return 'Other'

def parse_employee_count(size_cn):
    if size_cn == '大型':
        return '500+'
    if size_cn == '中型':
        return '100-500'
    if size_cn == '小型':
        return '1-100'
    return '-'

def calc_lead_score(priority):
    if priority == 'A':
        return 90
    if priority == 'B':
        return 75
    if priority == 'C':
        return 60
    return 50

def import_companies(conn):
    cursor = conn.cursor()
    
    inserted_count = 0
    updated_count = 0
    
    for company in companies_data:
        company_name = company['company_name']
        
        cursor.execute("SELECT id FROM p_company WHERE company_name = %s", (company_name,))
        existing = cursor.fetchone()
        
        company_type_en = parse_company_type(company['company_type_cn'])
        website = None if company['website'] == '-' else company['website']
        phone = None if company['phone'] == '-' else company['phone']
        email = None if company['email'] == '-' else company['email']
        core_contact = None if company['core_contact'] == '-' else company['core_contact']
        employee_count = parse_employee_count(company['company_size'])
        lead_score = calc_lead_score(company['development_priority'])
        
        if company['main_market'] == '全球':
            export_ability = 20
            import_ability = 25
            purchase_scale = 25
        elif '/' in company['main_market']:
            export_ability = 15
            import_ability = 22
            purchase_scale = 22
        else:
            export_ability = 10
            import_ability = 18
            purchase_scale = 18
        
        china_supplier_acceptance = 18
        oem_aftermarket_match = 14
        customization_match = 4
        
        if existing:
            company_id = existing[0]
            
            update_sql = """
UPDATE p_company SET 
    website = IFNULL(%s, website),
    address = IFNULL(%s, address),
    phone = IFNULL(%s, phone),
    email = IFNULL(%s, email),
    company_type = %s,
    main_products = IFNULL(%s, main_products),
    main_market = IFNULL(%s, main_market),
    lead_score = %s,
    lead_grade = %s,
    core_contact = IFNULL(%s, core_contact),
    import_ability = %s,
    purchase_scale = %s,
    china_supplier_acceptance = %s,
    oem_aftermarket_match = %s,
    export_ability = %s,
    customization_match = %s,
    employee_count = %s,
    annual_revenue_usd = %s,
    purchase_potential = %s,
    development_priority = %s,
    notes = IFNULL(%s, notes),
    status = 'New',
    source = 'Industry_Directory',
    source_url = 'https://www.siambusinessguide.com/',
    is_auto_parts_core = 1,
    is_importer_distributor = %s
WHERE id = %s
            """
            
            is_importer = 1 if '进口商' in company['company_type_cn'] or '经销商' in company['company_type_cn'] or '分销商' in company['company_type_cn'] else 0
            
            cursor.execute(update_sql, (
                website, company['address'], phone, email,
                company_type_en, company['main_products'], company['main_market'],
                lead_score, company['development_priority'],
                core_contact,
                import_ability, purchase_scale, china_supplier_acceptance,
                oem_aftermarket_match, export_ability, customization_match,
                employee_count,
                company['revenue_usd'] * 10000,
                company['purchase_potential'],
                company['development_priority'],
                company['cooperation_opportunity'],
                is_importer,
                company_id
            ))
            updated_count += 1
        
        else:
            is_importer = 1 if '进口商' in company['company_type_cn'] or '经销商' in company['company_type_cn'] or '分销商' in company['company_type_cn'] else 0
            
            insert_sql = """
INSERT INTO p_company (
    company_name, website, address, phone, email,
    company_type, main_products, main_market,
    lead_score, lead_grade,
    core_contact,
    import_ability, purchase_scale, china_supplier_acceptance,
    oem_aftermarket_match, export_ability, customization_match,
    employee_count, annual_revenue_usd,
    purchase_potential, development_priority, notes,
    country, status, source, source_url,
    is_auto_parts_core, is_importer_distributor
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_sql, (
                company_name, website, company['address'], phone, email,
                company_type_en, company['main_products'], company['main_market'],
                lead_score, company['development_priority'],
                core_contact,
                import_ability, purchase_scale, china_supplier_acceptance,
                oem_aftermarket_match, export_ability, customization_match,
                employee_count,
                company['revenue_usd'] * 10000,
                company['purchase_potential'],
                company['development_priority'],
                company['cooperation_opportunity'],
                'Thailand', 'New', 'Industry_Directory', 'https://www.siambusinessguide.com/',
                1, is_importer
            ))
            inserted_count += 1
    
    conn.commit()
    print(f"\n✅ 共处理 {inserted_count + updated_count} 条客户数据")
    print(f"   新增: {inserted_count} 条")
    print(f"   更新: {updated_count} 条")
    cursor.close()

def verify_data(conn):
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as total FROM p_company")
    total = cursor.fetchone()[0]
    print(f"\n📊 数据库中共有 {total} 条客户记录")
    
    cursor.execute("SELECT lead_grade, COUNT(*) as count FROM p_company GROUP BY lead_grade ORDER BY lead_grade")
    grades = cursor.fetchall()
    print("\n📈 客户等级分布:")
    for grade, count in grades:
        print(f"  {grade}: {count} 条")
    
    cursor.execute("""
SELECT company_type, COUNT(*) as count FROM p_company GROUP BY company_type ORDER BY count DESC
""")
    types = cursor.fetchall()
    print("\n📈 公司类型分布:")
    for type_name, count in types:
        print(f"  {type_name}: {count} 条")
    
    cursor.execute("""
SELECT company_name, annual_revenue_usd/10000 as revenue_usd, lead_grade, company_type
FROM p_company 
WHERE source = 'Industry_Directory'
ORDER BY annual_revenue_usd DESC
LIMIT 15
""")
    results = cursor.fetchall()
    print("\n🏆 新导入顶级客户（按营业额排序）:")
    for row in results:
        print(f"  {row[0][:40]:<40} | 营业额: {int(row[1]):<6}万$ | 等级: {row[2]} | 类型: {row[3]}")
    
    cursor.close()

if __name__ == '__main__':
    print("=" * 60)
    print("导入泰国汽车配件公司到数据库")
    print("=" * 60)
    print(f"📥 待导入公司数量: {len(companies_data)}")
    
    try:
        conn = connect_db()
        print("✅ 数据库连接成功")
        
        import_companies(conn)
        verify_data(conn)
        
        conn.close()
        print("\n🎉 客户数据导入完成！")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
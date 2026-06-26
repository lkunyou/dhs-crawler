import pymysql

DB_HOST = '8.163.58.109'
DB_PORT = 3306
DB_USER = 'thai_auto_parts_crm'
DB_PASSWORD = 'tDdY8NX2xJ6HpdHz'
DB_NAME = 'thai_auto_parts_crm'

conn = pymysql.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    charset='utf8mb4'
)

cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS p_cmdt_code")

create_table_sql = """
CREATE TABLE p_cmdt_code (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    section VARCHAR(200) COMMENT '大类(HS Code Sections)',
    section_code VARCHAR(10) COMMENT '大类编码',
    chapter VARCHAR(200) COMMENT '中类(HS Code 二位编码)',
    chapter_code VARCHAR(10) COMMENT '中类编码',
    cmdt_code VARCHAR(20) NOT NULL COMMENT '商品编码',
    description_en VARCHAR(500) COMMENT '英文描述',
    description_cn VARCHAR(500) COMMENT '中文描述',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_cmdt_code (cmdt_code),
    INDEX idx_section_code (section_code),
    INDEX idx_chapter_code (chapter_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='CMDT商品编码表'
"""

cursor.execute(create_table_sql)
print("✅ 成功创建 p_cmdt_code 表")

conn.close()
print("\n🎉 完成！")
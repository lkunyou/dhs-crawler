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

def add_columns(conn):
    cursor = conn.cursor()
    
    columns_to_add = [
        ("model", "VARCHAR(100) COMMENT '型号'"),
        ("dimensions", "VARCHAR(100) COMMENT '产品尺寸'"),
        ("pkg_length", "INT COMMENT '包装长(mm)'"),
        ("pkg_width", "INT COMMENT '包装宽(mm)'"),
        ("pkg_height", "INT COMMENT '包装高(mm)'"),
        ("qty_per_pkg", "INT COMMENT '每箱数量'"),
        ("car_model", "VARCHAR(200) COMMENT '适用车型'"),
        ("production_date", "DATE COMMENT '量产日期'"),
        ("weight", "DECIMAL(10,2) COMMENT '重量(g)'")
    ]
    
    for col_name, col_def in columns_to_add:
        try:
            sql = f"ALTER TABLE p_product ADD COLUMN {col_name} {col_def}"
            cursor.execute(sql)
            print(f"✅ 成功添加字段: {col_name}")
        except pymysql.err.OperationalError as e:
            if e.args[0] == 1060:
                print(f"⚠️ 字段 {col_name} 已存在，跳过")
            else:
                raise
    
    conn.commit()
    cursor.close()

def verify_table(conn):
    cursor = conn.cursor()
    cursor.execute("DESCRIBE p_product")
    columns = cursor.fetchall()
    print("\n📋 表结构:")
    for col in columns:
        print(f"  {col[0]}: {col[1]}")
    cursor.close()

if __name__ == '__main__':
    print("=" * 60)
    print("正在连接数据库并更新表结构...")
    print("=" * 60)
    
    try:
        conn = connect_db()
        print("✅ 数据库连接成功")
        
        add_columns(conn)
        verify_table(conn)
        
        conn.close()
        print("\n🎉 表结构更新完成！")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
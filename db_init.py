import pymysql
from config import DB_CONFIG

def init_database():
    try:
        # 连接到MySQL服务器（不指定数据库）
        connection = pymysql.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            charset=DB_CONFIG['charset']
        )
        cursor = connection.cursor()

        # 创建数据库
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['db']}")
        print(f"数据库 {DB_CONFIG['db']} 创建成功或已存在")

        # 选择数据库
        cursor.execute(f"USE {DB_CONFIG['db']}")

        # 创建图片表
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS images (
            id INT AUTO_INCREMENT PRIMARY KEY,
            filename VARCHAR(255) NOT NULL,
            filepath VARCHAR(512) NOT NULL,
            upload_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            filesize INT NOT NULL,
            filetype VARCHAR(50) NOT NULL,
            description TEXT,
            is_deleted BOOLEAN DEFAULT FALSE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        cursor.execute(create_table_sql)
        print("图片表创建成功或已存在")

        # 创建用户表
        create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(100) UNIQUE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        cursor.execute(create_users_table)
        print("用户表创建成功或已存在")

        connection.commit()
        print("数据库初始化完成")

    except Exception as e:
        print(f"数据库初始化错误: {str(e)}")
        if 'connection' in locals():
            connection.rollback()
    finally:
        if 'connection' in locals() and connection.open:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    init_database()
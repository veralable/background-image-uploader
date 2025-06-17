import os
import pymysql
from config import DB_CONFIG, UPLOAD_FOLDER

def clean_unused_files():
    """清理上传目录中未被数据库引用的文件"""
    # 获取数据库中所有已保存的文件路径
    db_files = set()
    connection = None
    
    try:
        # 连接数据库
        connection = pymysql.connect(**DB_CONFIG)
        with connection.cursor() as cursor:
            # 查询所有未删除的图片文件路径
            sql = "SELECT filepath FROM images WHERE is_deleted = FALSE"
            cursor.execute(sql)
            results = cursor.fetchall()
            db_files = {row['filepath'] for row in results}
            
        # 获取上传目录中的所有文件
        upload_files = set()
        for root, dirs, files in os.walk(UPLOAD_FOLDER):
            for file in files:
                file_path = os.path.join(root, file)
                upload_files.add(file_path)
                
        # 找出不在数据库中的文件（需要删除的文件）
        files_to_delete = upload_files - db_files
        
        # 根据用户要求，已禁用文件删除功能
        print(f"检测到 {len(files_to_delete)} 个未引用文件，但已禁用自动删除")
        # 如需手动清理，请取消以下代码注释
        # deleted_count = 0
        # for file_path in files_to_delete:
        #     try:
        #         os.remove(file_path)
        #         deleted_count += 1
        #         print(f"已删除未引用文件: {file_path}")
        #     except Exception as e:
        #         print(f"删除文件失败 {file_path}: {str(e)}")
        # 
        # print(f"清理完成，共删除 {deleted_count} 个未引用文件")
        return deleted_count
        
    except Exception as e:
        print(f"清理过程出错: {str(e)}")
        return 0
    finally:
        if connection:
            connection.close()

if __name__ == '__main__':
    clean_unused_files()
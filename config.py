import pymysql

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '123456',  # 默认密码，根据你的phpstudy设置修改
    'db': 'wallpaper_db',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# 图片上传配置
import os
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'mp4', 'avi', 'mov', 'mp3', 'wav', 'ogg'}
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB (增大以支持音视频)
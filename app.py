from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory
import os
import pymysql
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import DB_CONFIG, UPLOAD_FOLDER, ALLOWED_EXTENSIONS, MAX_CONTENT_LENGTH
import hashlib

# 初始化Flask应用
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.secret_key = 'supersecretkey'  # 用于会话管理

# 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 数据库连接函数
def get_db_connection():
    connection = pymysql.connect(**DB_CONFIG)
    return connection

# 检查文件扩展名是否允许
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 首页路由
@app.route('/')
def index():
    return render_template('index.html', title='图片上传系统')

# 上传图片路由
@app.route('/upload', methods=['POST'])
def upload_file():
    # 检查是否有文件部分
    if 'file' not in request.files:
        return jsonify({'error': '没有文件部分'}), 400
    file = request.files['file']
    # 如果用户没有选择文件
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    if file and allowed_file(file.filename):
        # 生成唯一文件名
        filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{hashlib.md5(file.filename.encode()).hexdigest()[:8]}.{file.filename.rsplit('.', 1)[1].lower()}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # 获取文件信息
        filesize = os.path.getsize(filepath)
        filetype = file.content_type
        description = request.form.get('description', '')

        # 保存到数据库
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO images (filename, filepath, filesize, filetype, description) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (filename, filepath, filesize, filetype, description))
            connection.commit()
            return jsonify({
                'success': True,
                'message': '文件上传成功',
                'filename': filename,
                'id': cursor.lastrowid
            }), 201
        except Exception as e:
            connection.rollback()
            return jsonify({'error': f'数据库错误: {str(e)}'}), 500
        finally:
            connection.close()

    return jsonify({'error': '不允许的文件类型'}), 400

# 获取所有图片路由
@app.route('/images')
def get_images():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM images WHERE is_deleted = FALSE ORDER BY upload_time DESC"
            cursor.execute(sql)
            images = cursor.fetchall()
        return jsonify(images)
    except Exception as e:
        return jsonify({'error': f'数据库错误: {str(e)}'}), 500
    finally:
        connection.close()

# 获取单个图片路由
@app.route('/images/<int:image_id>')
def get_image(image_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM images WHERE id = %s AND is_deleted = FALSE"
            cursor.execute(sql, (image_id,))
            image = cursor.fetchone()
            if image is None:
                return jsonify({'error': '图片不存在'}), 404
            return send_from_directory(os.path.dirname(image['filepath']), os.path.basename(image['filepath']))
    except Exception as e:
        return jsonify({'error': f'数据库错误: {str(e)}'}), 500
    finally:
        connection.close()

# 删除图片路由
@app.route('/images/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # 先获取图片信息
            sql = "SELECT * FROM images WHERE id = %s"
            cursor.execute(sql, (image_id,))
            image = cursor.fetchone()
            if image is None:
                return jsonify({'error': '图片不存在'}), 404

            # 逻辑删除图片
            sql = "UPDATE images SET is_deleted = TRUE WHERE id = %s"
            cursor.execute(sql, (image_id,))
            connection.commit()

            # 仅标记删除，不物理删除文件
            pass

        return jsonify({'success': True, 'message': '图片已删除'})
    except Exception as e:
        connection.rollback()
        return jsonify({'error': f'数据库错误: {str(e)}'}), 500
    finally:
        connection.close()

# 用户注册路由
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')

    if not username or not password:
        return jsonify({'error': '用户名和密码不能为空'}), 400

    # 密码哈希
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
            cursor.execute(sql, (username, hashed_password, email))
        connection.commit()
        return jsonify({'success': True, 'message': '注册成功'}), 201
    except pymysql.err.IntegrityError:
        connection.rollback()
        return jsonify({'error': '用户名或邮箱已存在'}), 400
    except Exception as e:
        connection.rollback()
        return jsonify({'error': f'数据库错误: {str(e)}'}), 500
    finally:
        connection.close()

# 运行应用
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
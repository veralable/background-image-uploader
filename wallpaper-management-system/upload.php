<?php
require 'config.php';

// 上传目录
$upload_dir = 'uploads/';

// 创建上传目录（如果不存在）
if (!file_exists($upload_dir)) {
    mkdir($upload_dir, 0777, true);
}

// 检查是否有文件上传
if (isset($_FILES['image'])) {
    $errors = [];
    $file_name = $_FILES['image']['name'];
    $file_size = $_FILES['image']['size'];
    $file_tmp = $_FILES['image']['tmp_name'];
    $file_type = $_FILES['image']['type'];
    $file_ext = strtolower(pathinfo($file_name, PATHINFO_EXTENSION));
    
    // 允许的文件扩展名
    $extensions = ["jpeg", "jpg", "png", "gif", "bmp"];
    
    // 检查文件扩展名
    if (!in_array($file_ext, $extensions)) {
        $errors[] = "不支持的文件类型，请上传JPEG、PNG、GIF或BMP格式的图片";
    }
    
    // 检查文件大小（最大10MB）
    if ($file_size > 10 * 1024 * 1024) {
        $errors[] = "文件大小超过10MB";
    }
    
    // 如果没有错误，则上传文件
    if (empty($errors)) {
        // 生成唯一文件名
        $new_file_name = uniqid() . '.' . $file_ext;
        $target_file = $upload_dir . $new_file_name;
        
        // 获取图片尺寸
        list($width, $height) = getimagesize($file_tmp);
        
        // 移动文件
        if (move_uploaded_file($file_tmp, $target_file)) {
            // 插入数据库
            try {
                $stmt = $pdo->prepare("INSERT INTO wallpapers (filename, original_name, size, type, width, height) VALUES (:filename, :original_name, :size, :type, :width, :height)");
                $stmt->execute([
                    'filename' => $new_file_name,
                    'original_name' => $file_name,
                    'size' => $file_size,
                    'type' => $file_type,
                    'width' => $width,
                    'height' => $height
                ]);
                
                $response = [
                    'status' => 'success',
                    'message' => '图片上传成功',
                    'file_path' => $target_file,
                    'id' => $pdo->lastInsertId()
                ];
            } catch(PDOException $e) {
                $response = [
                    'status' => 'error',
                    'message' => '数据库错误: ' . $e->getMessage()
                ];
                // 如果数据库插入失败，删除已上传的文件
                if (file_exists($target_file)) {
                    unlink($target_file);
                }
            }
        } else {
            $response = [
                'status' => 'error',
                'message' => '上传文件失败'
            ];
        }
    } else {
        $response = [
            'status' => 'error',
            'message' => implode(', ', $errors)
        ];
    }
    
    // 返回JSON响应
    header('Content-Type: application/json');
    echo json_encode($response);
} else {
    header('Content-Type: application/json');
    echo json_encode([
        'status' => 'error',
        'message' => '没有上传文件'
    ]);
}
?>    
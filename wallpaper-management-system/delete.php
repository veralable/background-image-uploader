<?php
require 'config.php';

// 检查是否有ID参数
if (isset($_GET['id'])) {
    $id = intval($_GET['id']);
    
    try {
        // 查询图片信息
        $stmt = $pdo->prepare("SELECT filename FROM wallpapers WHERE id = :id");
        $stmt->execute(['id' => $id]);
        $wallpaper = $stmt->fetch(PDO::FETCH_ASSOC);
        
        if ($wallpaper) {
            $filename = $wallpaper['filename'];
            $file_path = 'uploads/' . $filename;
            
            // 删除文件
            if (file_exists($file_path)) {
                unlink($file_path);
            }
            
            // 从数据库中删除记录
            $stmt = $pdo->prepare("DELETE FROM wallpapers WHERE id = :id");
            $stmt->execute(['id' => $id]);
            
            $response = [
                'status' => 'success',
                'message' => '图片已删除'
            ];
        } else {
            $response = [
                'status' => 'error',
                'message' => '找不到该图片'
            ];
        }
    } catch(PDOException $e) {
        $response = [
            'status' => 'error',
            'message' => '数据库错误: ' . $e->getMessage()
        ];
    }
} else {
    $response = [
        'status' => 'error',
        'message' => '缺少必要的参数'
    ];
}

// 返回JSON响应
header('Content-Type: application/json');
echo json_encode($response);
?>    
<?php
require 'config.php';

try {
    // 查询所有壁纸
    $stmt = $pdo->query("SELECT * FROM wallpapers ORDER BY upload_time DESC");
    $wallpapers = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
    // 添加图片URL
    foreach ($wallpapers as &$wallpaper) {
        $wallpaper['url'] = 'uploads/' . $wallpaper['filename'];
        $wallpaper['size_mb'] = round($wallpaper['size'] / (1024 * 1024), 2);
    }
    
    $response = [
        'status' => 'success',
        'data' => $wallpapers
    ];
} catch(PDOException $e) {
    $response = [
        'status' => 'error',
        'message' => '数据库错误: ' . $e->getMessage()
    ];
}

// 返回JSON响应
header('Content-Type: application/json');
echo json_encode($response);
?>    
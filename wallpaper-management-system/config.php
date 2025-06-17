<?php
// 数据库配置
define('DB_HOST', 'localhost');
define('DB_NAME', 'wallpaper_manager');
define('DB_USER', 'root');
define('DB_PASSWORD', '您的数据库密码'); // 请修改为您的phpstudy_pro MySQL密码

// 创建数据库连接
try {
    $pdo = new PDO("mysql:host=".DB_HOST.";dbname=".DB_NAME, DB_USER, DB_PASSWORD);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $pdo->exec("set names utf8mb4");
} catch(PDOException $e) {
    die("数据库连接失败: " . $e->getMessage());
}
?>    
<?php
require __DIR__ . '/bootstrap.php';

$user = require_auth($pdo);

$stmt = $pdo->prepare(
  'SELECT order_code, shipping_method, payment_method, total, status, created_at
   FROM orders WHERE user_id = ? ORDER BY created_at DESC'
);
$stmt->execute([$user['id']]);

respond(['orders' => $stmt->fetchAll()]);

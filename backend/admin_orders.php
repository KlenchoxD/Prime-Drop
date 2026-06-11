<?php
require __DIR__ . '/bootstrap.php';

$user = require_auth($pdo);
if ((int)$user['is_admin'] !== 1) fail('Acceso restringido.', 403);

// Listar todos los pedidos con sus items
$orders = $pdo->query(
  'SELECT * FROM orders ORDER BY created_at DESC LIMIT 500'
)->fetchAll();

$itemStmt = $pdo->prepare('SELECT product_name, color, unit_price, quantity FROM order_items WHERE order_id = ?');
foreach ($orders as &$o) {
  $itemStmt->execute([$o['id']]);
  $o['items'] = $itemStmt->fetchAll();
}
unset($o);

respond(['orders' => $orders]);

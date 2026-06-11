<?php
require __DIR__ . '/bootstrap.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') fail('Método no permitido.', 405);

$body = json_body();
$c = $body['customer'] ?? [];
$items = $body['items'] ?? [];

// Validación básica
foreach (['fullName', 'email', 'phone', 'address', 'department', 'city'] as $f) {
  if (empty(trim($c[$f] ?? ''))) fail("Falta el campo de envío: $f");
}
if (!is_array($items) || count($items) === 0) fail('El pedido no tiene productos.');

$shippingMethod = trim($body['shippingMethod'] ?? '');
$paymentMethod = trim($body['paymentMethod'] ?? '');
$subtotal = (int)($body['subtotal'] ?? 0);
$discount = (int)($body['discount'] ?? 0);
$shippingCost = (int)($body['shippingCost'] ?? 0);
$total = (int)($body['total'] ?? 0);

$orderCode = 'PRIME-CO-' . date('Y') . '-' . random_int(100000, 999999);
$userId = !empty($_SESSION['user_id']) ? (int)$_SESSION['user_id'] : null;

try {
  $pdo->beginTransaction();

  $stmt = $pdo->prepare(
    'INSERT INTO orders
      (order_code, user_id, full_name, email, phone, address, department, city, notes,
       shipping_method, payment_method, subtotal, discount, shipping_cost, total)
     VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
  );
  $stmt->execute([
    $orderCode, $userId,
    trim($c['fullName']), strtolower(trim($c['email'])), trim($c['phone']),
    trim($c['address']), trim($c['department']), trim($c['city']),
    trim($c['notes'] ?? '') ?: null,
    $shippingMethod, $paymentMethod, $subtotal, $discount, $shippingCost, $total,
  ]);

  $orderId = (int)$pdo->lastInsertId();

  $itemStmt = $pdo->prepare(
    'INSERT INTO order_items (order_id, product_id, product_name, color, unit_price, quantity)
     VALUES (?,?,?,?,?,?)'
  );
  foreach ($items as $it) {
    $itemStmt->execute([
      $orderId,
      (string)($it['productId'] ?? ''),
      (string)($it['productName'] ?? ''),
      isset($it['color']) ? (string)$it['color'] : null,
      (int)($it['unitPrice'] ?? 0),
      (int)($it['quantity'] ?? 1),
    ]);
  }

  $pdo->commit();
} catch (Throwable $e) {
  if ($pdo->inTransaction()) $pdo->rollBack();
  fail('No se pudo guardar el pedido.', 500);
}

respond(['orderCode' => $orderCode, 'status' => 'Pendiente'], 201);

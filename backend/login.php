<?php
require __DIR__ . '/bootstrap.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') fail('Método no permitido.', 405);

$body = json_body();
$email = strtolower(trim($body['email'] ?? ''));
$password = (string)($body['password'] ?? '');

if ($email === '' || $password === '') fail('Ingresa correo y contraseña.');

$stmt = $pdo->prepare('SELECT id, name, email, phone, password_hash, is_admin FROM users WHERE email = ?');
$stmt->execute([$email]);
$user = $stmt->fetch();

if (!$user || !password_verify($password, $user['password_hash'])) {
  fail('Correo o contraseña incorrectos.', 401);
}

$_SESSION['user_id'] = (int)$user['id'];

respond([
  'user' => [
    'id' => (int)$user['id'],
    'name' => $user['name'],
    'email' => $user['email'],
    'phone' => $user['phone'],
    'is_admin' => (int)$user['is_admin'],
  ],
]);

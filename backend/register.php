<?php
require __DIR__ . '/bootstrap.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') fail('Método no permitido.', 405);

$body = json_body();
$name = trim($body['name'] ?? '');
$email = strtolower(trim($body['email'] ?? ''));
$password = (string)($body['password'] ?? '');
$phone = trim($body['phone'] ?? '');

if ($name === '') fail('El nombre es requerido.');
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) fail('Correo electrónico inválido.');
if (strlen($password) < 6) fail('La contraseña debe tener al menos 6 caracteres.');

$stmt = $pdo->prepare('SELECT id FROM users WHERE email = ?');
$stmt->execute([$email]);
if ($stmt->fetch()) fail('Este correo ya tiene una cuenta registrada.', 409);

$hash = password_hash($password, PASSWORD_DEFAULT);
$stmt = $pdo->prepare('INSERT INTO users (name, email, password_hash, phone) VALUES (?, ?, ?, ?)');
$stmt->execute([$name, $email, $hash, $phone ?: null]);

$_SESSION['user_id'] = (int)$pdo->lastInsertId();

respond([
  'user' => [
    'id' => $_SESSION['user_id'],
    'name' => $name,
    'email' => $email,
    'phone' => $phone,
    'is_admin' => 0,
  ],
], 201);

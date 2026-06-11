<?php
require __DIR__ . '/bootstrap.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') fail('Método no permitido.', 405);

$body = json_body();
$email = strtolower(trim($body['email'] ?? ''));

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) fail('Ingresa un correo válido.');

$stmt = $pdo->prepare('SELECT id, name FROM users WHERE email = ?');
$stmt->execute([$email]);
$user = $stmt->fetch();

// Por seguridad respondemos siempre igual, exista o no la cuenta.
if ($user) {
  // Genera una contraseña temporal y la guarda.
  $temp = bin2hex(random_bytes(4)); // 8 caracteres
  $hash = password_hash($temp, PASSWORD_DEFAULT);
  $upd = $pdo->prepare('UPDATE users SET password_hash = ? WHERE id = ?');
  $upd->execute([$hash, $user['id']]);

  // Envía el correo con la contraseña temporal.
  $subject = 'Recuperación de contraseña - Prime Drop Elite';
  $message =
    "Hola {$user['name']},\n\n" .
    "Recibimos una solicitud para restablecer tu contraseña en Prime Drop Elite.\n\n" .
    "Tu contraseña temporal es: {$temp}\n\n" .
    "Ingresa con ella y cámbiala lo antes posible desde tu perfil.\n\n" .
    "Si no solicitaste esto, contáctanos de inmediato.\n\n" .
    "Prime Drop Elite\nhttps://primedropelite.com";
  $headers = 'From: no-reply@primedropelite.com' . "\r\n" .
             'Content-Type: text/plain; charset=utf-8';

  @mail($email, $subject, $message, $headers);
}

respond(['ok' => true]);

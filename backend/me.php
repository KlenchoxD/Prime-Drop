<?php
require __DIR__ . '/bootstrap.php';

$user = current_user($pdo);
if (!$user) respond(['user' => null]);

respond([
  'user' => [
    'id' => (int)$user['id'],
    'name' => $user['name'],
    'email' => $user['email'],
    'phone' => $user['phone'],
    'is_admin' => (int)$user['is_admin'],
  ],
]);

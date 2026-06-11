<?php
/**
 * Bootstrap común: carga config, abre conexión PDO, configura CORS,
 * sesión y helpers JSON. Incluido por todos los endpoints.
 */

declare(strict_types=1);

$configPath = __DIR__ . '/config.php';
if (!file_exists($configPath)) {
  http_response_code(500);
  header('Content-Type: application/json');
  echo json_encode(['error' => 'Falta config.php. Copia config.example.php como config.php.']);
  exit;
}

$config = require $configPath;

// --- CORS (mismo dominio en producción) ---
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
if ($origin === $config['allowed_origin']) {
  header('Access-Control-Allow-Origin: ' . $origin);
  header('Access-Control-Allow-Credentials: true');
}
header('Vary: Origin');
header('Content-Type: application/json; charset=utf-8');

if (($_SERVER['REQUEST_METHOD'] ?? '') === 'OPTIONS') {
  header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
  header('Access-Control-Allow-Headers: Content-Type');
  http_response_code(204);
  exit;
}

// --- Sesión ---
session_set_cookie_params([
  'lifetime' => 60 * 60 * 24 * 30, // 30 días
  'path' => '/',
  'httponly' => true,
  'samesite' => 'Lax',
  'secure' => (($_SERVER['HTTPS'] ?? '') === 'on'),
]);
session_start();

// --- Conexión PDO ---
try {
  $pdo = new PDO(
    "mysql:host={$config['db_host']};dbname={$config['db_name']};charset=utf8mb4",
    $config['db_user'],
    $config['db_pass'],
    [
      PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
      PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
      PDO::ATTR_EMULATE_PREPARES => false,
    ]
  );
} catch (Throwable $e) {
  http_response_code(500);
  echo json_encode(['error' => 'No se pudo conectar a la base de datos.']);
  exit;
}

// --- Helpers ---
function json_body(): array {
  $raw = file_get_contents('php://input');
  $data = json_decode($raw, true);
  return is_array($data) ? $data : [];
}

function respond(array $data, int $code = 200): void {
  http_response_code($code);
  echo json_encode($data);
  exit;
}

function fail(string $message, int $code = 400): void {
  respond(['error' => $message], $code);
}

function current_user(PDO $pdo): ?array {
  if (empty($_SESSION['user_id'])) return null;
  $stmt = $pdo->prepare('SELECT id, name, email, phone, is_admin FROM users WHERE id = ?');
  $stmt->execute([$_SESSION['user_id']]);
  $u = $stmt->fetch();
  return $u ?: null;
}

function require_auth(PDO $pdo): array {
  $u = current_user($pdo);
  if (!$u) fail('No autenticado.', 401);
  return $u;
}

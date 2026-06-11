<?php
/**
 * =====================================================================
 *  CONFIGURACIÓN DEL BACKEND — COPIA ESTE ARCHIVO COMO "config.php"
 *  Y RELLENA CON LOS DATOS DE TU BASE DE DATOS DE HOSTINGER.
 * =====================================================================
 *
 *  En hPanel de Hostinger:
 *   1. Ve a "Bases de datos" → "Administración de bases de datos MySQL"
 *   2. Crea una base de datos nueva y un usuario (anota la contraseña)
 *   3. Hostinger te da: nombre de BD, usuario y host (normalmente "localhost")
 *   4. Copia este archivo como  config.php  y pega los valores aquí abajo.
 */

return [
  // --- Base de datos MySQL ---
  'db_host' => 'localhost',
  'db_name' => 'TU_NOMBRE_DE_BD',
  'db_user' => 'TU_USUARIO_BD',
  'db_pass' => 'TU_CONTRASEÑA_BD',

  // --- Seguridad ---
  // Cambia esto por una frase larga y secreta (cualquier texto aleatorio).
  'app_secret' => 'cambia-esto-por-una-frase-larga-y-secreta',

  // Dominio del sitio (para CORS). En producción debe ser tu dominio exacto.
  'allowed_origin' => 'https://primedropelite.com',
];

-- =====================================================================
--  ESQUEMA DE BASE DE DATOS — Prime Drop Elite
--  Ejecuta este SQL en phpMyAdmin de Hostinger (pestaña "SQL")
--  después de crear tu base de datos.
-- =====================================================================

-- Usuarios (clientes registrados)
CREATE TABLE IF NOT EXISTS users (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  name          VARCHAR(120) NOT NULL,
  email         VARCHAR(190) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  phone         VARCHAR(40)  DEFAULT NULL,
  is_admin      TINYINT(1)   NOT NULL DEFAULT 0,
  created_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Pedidos
CREATE TABLE IF NOT EXISTS orders (
  id             INT AUTO_INCREMENT PRIMARY KEY,
  order_code     VARCHAR(40)  NOT NULL UNIQUE,
  user_id        INT          DEFAULT NULL,
  full_name      VARCHAR(120) NOT NULL,
  email          VARCHAR(190) NOT NULL,
  phone          VARCHAR(40)  NOT NULL,
  address        VARCHAR(255) NOT NULL,
  department     VARCHAR(80)  NOT NULL,
  city           VARCHAR(80)  NOT NULL,
  notes          TEXT         DEFAULT NULL,
  shipping_method VARCHAR(120) NOT NULL,
  payment_method VARCHAR(40)  NOT NULL,
  subtotal       INT          NOT NULL,
  discount       INT          NOT NULL DEFAULT 0,
  shipping_cost  INT          NOT NULL DEFAULT 0,
  total          INT          NOT NULL,
  status         VARCHAR(30)  NOT NULL DEFAULT 'Pendiente',
  created_at     DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_orders_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Items de cada pedido
CREATE TABLE IF NOT EXISTS order_items (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  order_id    INT          NOT NULL,
  product_id  VARCHAR(60)  NOT NULL,
  product_name VARCHAR(190) NOT NULL,
  color       VARCHAR(80)  DEFAULT NULL,
  unit_price  INT          NOT NULL,
  quantity    INT          NOT NULL,
  CONSTRAINT fk_items_order FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================================
--  Para convertir una cuenta en ADMINISTRADOR (ver pedidos), regístrate
--  primero en la web y luego ejecuta (cambiando el correo):
--    UPDATE users SET is_admin = 1 WHERE email = 'tucorreo@ejemplo.com';
-- =====================================================================

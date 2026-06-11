# Backend Prime Drop Elite (PHP + MySQL para Hostinger)

Backend real que corre en tu **Hostinger Business** (incluye PHP y MySQL).
Da: cuentas de clientes, login real y pedidos guardados en base de datos.

---

## Pasos de instalación (una sola vez)

### 1. Crear la base de datos
En **hPanel de Hostinger**:
1. Entra a **Bases de datos → Administración de bases de datos MySQL**.
2. Crea una base de datos nueva y un usuario. Anota: **nombre de BD, usuario, contraseña**.
3. Entra a **phpMyAdmin** de esa base de datos.
4. Abre la pestaña **SQL**, pega todo el contenido de `schema.sql` y ejecuta.

### 2. Configurar credenciales
1. Copia `config.example.php` y renómbralo a **`config.php`**.
2. Rellena `db_name`, `db_user`, `db_pass` con los datos del paso 1.
3. Cambia `app_secret` por una frase larga aleatoria.
4. Confirma que `allowed_origin` sea `https://primedropelite.com`.

### 3. Subir los archivos
Sube **toda esta carpeta `backend/`** dentro de `public_html` y renómbrala a **`api`**.
Es decir, los archivos deben quedar en:
```
public_html/api/login.php
public_html/api/register.php
public_html/api/create_order.php
...
```
Así la web los llama en `https://primedropelite.com/api/...`

### 4. Activar el backend en la web
En el código de la web, edita `src/lib/api.ts`:
```ts
export const BACKEND_ENABLED = true;   // cámbialo a true
```
Vuelve a hacer `npm run build` y sube la carpeta `dist/` a `public_html`.

### 5. Crear tu cuenta de administrador
1. Regístrate normalmente en la web con tu correo.
2. En phpMyAdmin (pestaña SQL) ejecuta:
   ```sql
   UPDATE users SET is_admin = 1 WHERE email = 'tucorreo@ejemplo.com';
   ```
Ahora ese usuario puede consultar todos los pedidos (`/api/admin_orders.php`).

---

## Endpoints
| Archivo | Qué hace |
|---|---|
| `register.php` | Crear cuenta (name, email, password, phone) |
| `login.php` | Iniciar sesión (email, password) |
| `logout.php` | Cerrar sesión |
| `me.php` | Devuelve el usuario de la sesión actual |
| `create_order.php` | Guarda un pedido (con o sin sesión) |
| `my_orders.php` | Pedidos del usuario autenticado |
| `admin_orders.php` | Todos los pedidos (solo admin) |

> **Nota:** mientras `BACKEND_ENABLED = false`, la web sigue funcionando como hasta ahora
> (sin tocar nada). El backend solo se activa cuando completes estos pasos.

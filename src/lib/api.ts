/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Cliente del backend (PHP + MySQL en Hostinger).
 *
 * Mientras BACKEND_ENABLED = false, la web funciona como antes (sin backend).
 * Cuando subas la carpeta backend/ a public_html/api y lo configures,
 * cambia BACKEND_ENABLED a true y reconstruye (npm run build).
 */

export const BACKEND_ENABLED = false;

// Ruta de los endpoints PHP. Por defecto, misma web en /api.
export const API_BASE = '/api';

export interface ApiUser {
  id: number;
  name: string;
  email: string;
  phone?: string;
  is_admin: number;
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(`${API_BASE}/${path}`, {
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });

  let data: any = null;
  try {
    data = await res.json();
  } catch {
    /* respuesta no-JSON */
  }

  if (!res.ok) {
    throw new Error(data?.error || 'Ocurrió un error. Intenta de nuevo.');
  }
  return data as T;
}

export function apiRegister(name: string, email: string, password: string, phone = '') {
  return request<{ user: ApiUser }>('register.php', {
    method: 'POST',
    body: JSON.stringify({ name, email, password, phone }),
  });
}

export function apiLogin(email: string, password: string) {
  return request<{ user: ApiUser }>('login.php', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  });
}

export function apiLogout() {
  return request<{ ok: boolean }>('logout.php', { method: 'POST' });
}

export function apiMe() {
  return request<{ user: ApiUser | null }>('me.php');
}

export interface CreateOrderPayload {
  customer: {
    fullName: string;
    email: string;
    phone: string;
    address: string;
    department: string;
    city: string;
    notes?: string;
  };
  items: Array<{
    productId: string;
    productName: string;
    color?: string;
    unitPrice: number;
    quantity: number;
  }>;
  shippingMethod: string;
  paymentMethod: string;
  subtotal: number;
  discount: number;
  shippingCost: number;
  total: number;
}

export function apiCreateOrder(payload: CreateOrderPayload) {
  return request<{ orderCode: string; status: string }>('create_order.php', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

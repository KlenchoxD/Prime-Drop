/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { PaymentMethodKey } from '../types';

/**
 * =====================================================================
 *  CONFIGURACIÓN DE PAGOS — EDITA AQUÍ CON TUS DATOS REALES
 * =====================================================================
 *
 * Cuando tengas tus cuentas de comercio, reemplaza los enlaces de abajo:
 *
 *  - WOMPI:  Crea un "Link de Pago" en tu panel de Wompi
 *            (https://comercios.wompi.co) y pega la URL aquí.
 *            Wompi cubre tarjetas, PSE, Nequi y Bancolombia.
 *
 *  - MERCADO PAGO: Crea un link de pago en tu cuenta de Mercado Pago
 *            (https://www.mercadopago.com.co) y pega la URL aquí.
 *
 *  Mientras estos enlaces estén vacíos, el checkout coordinará el pago
 *  por WhatsApp automáticamente (no se pierde ninguna venta).
 * =====================================================================
 */

export const PAYMENT_CONFIG = {
  // Link de pago de Wompi (cubre tarjetas + PSE + Nequi + Bancolombia)
  wompiLink: '',

  // Link de pago de Mercado Pago
  mercadoPagoLink: '',

  // WhatsApp de la tienda (formato internacional sin + ni espacios)
  whatsappNumber: '573160685555',
};

export interface PaymentOption {
  key: PaymentMethodKey;
  label: string;
  description: string;
}

export const PAYMENT_METHODS: PaymentOption[] = [
  {
    key: 'Wompi',
    label: 'Wompi',
    description: 'Paga con tarjeta de crédito/débito, Nequi o Bancolombia. Procesado de forma segura por Wompi (Grupo Bancolombia).',
  },
  {
    key: 'PSE',
    label: 'PSE',
    description: 'Débito directo desde tu cuenta de ahorros o corriente. Compatible con la mayoría de bancos colombianos.',
  },
  {
    key: 'MercadoPago',
    label: 'Mercado Pago',
    description: 'Paga con tu saldo de Mercado Pago, tarjetas o medios habilitados en tu cuenta.',
  },
];

/**
 * Bancos disponibles para PSE en Colombia (lista representativa).
 */
export const PSE_BANKS: string[] = [
  'Bancolombia',
  'Banco de Bogotá',
  'Davivienda',
  'BBVA Colombia',
  'Banco de Occidente',
  'Banco Popular',
  'Banco Caja Social',
  'Banco AV Villas',
  'Banco Agrario',
  'Banco GNB Sudameris',
  'Banco Falabella',
  'Banco Pichincha',
  'Bancoomeva',
  'Banco Cooperativo Coopcentral',
  'Citibank',
  'Scotiabank Colpatria',
  'Itaú',
  'Nequi',
  'Daviplata',
  'Lulo Bank',
  'Nu Colombia',
];

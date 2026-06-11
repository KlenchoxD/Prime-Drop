/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

export interface ProductColor {
  name: string;
  hex: string;
}

export interface BagProduct {
  id: string;
  name: string;
  description: string;
  longDescription: string;
  price: number;
  originalPrice?: number;
  primaryImage: string;
  secondaryImage: string;
  category: 'KARL LAGERFELD' | 'MICHAEL KORS' | 'STEVE MADDEN' | 'TOMMY HILFIGER' | string;
  materials: string[];
  features: string[];
  dimensions: string;
  colors: ProductColor[];
  rating: number;
  reviewsCount: number;
  isNew?: boolean;
  isPopular?: boolean;
  inStock: boolean;
  gender?: 'mujer' | 'hombre' | 'unisex';
  brand?: string;
}

export interface CartItem {
  id: string; // Composite ID of productId + color + engraving + hardware
  product: BagProduct;
  quantity: number;
  selectedColor: ProductColor;
  customEngraving: string; // Max 3 initials, e.g. "K.M."
  selectedHardware: 'Gold' | 'Silver' | 'Obsidian';
}

export interface PromoCode {
  code: string;
  discountPercent: number;
  description: string;
}

export interface CustomerInfo {
  fullName: string;
  email: string;
  phone: string;
  address: string;
  city: string;
  postalCode: string;
  country: string;
}

export interface ShippingMethod {
  id: string;
  name: string;
  description: string;
  price: number;
  estimatedDays: string;
}

export interface PaymentDetails {
  method: 'Card' | 'PayPal' | 'ApplePay' | 'Crypto';
  cardName?: string;
  cardNumber?: string;
  cardExpiry?: string;
  cardCvv?: string;
}

export interface Order {
  id: string;
  customerInfo: CustomerInfo;
  items: CartItem[];
  subtotal: number;
  shippingCost: number;
  discountAmount: number;
  total: number;
  shippingMethod: ShippingMethod;
  paymentDetails: PaymentDetails;
  status: 'Pending' | 'Processing' | 'Shipped' | 'Delivered';
  createdAt: string;
  trackingNumber: string;
}

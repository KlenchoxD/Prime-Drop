/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { X, ShoppingBag, Trash2, ArrowRight, ShieldCheck, Ticket, Check, Sparkles } from 'lucide-react';
import { CartItem, PromoCode } from '../types';
import { PROMO_CODES } from '../data/products';
import { motion, AnimatePresence } from 'motion/react';
import { formatCOP } from '../utils';

interface CartDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  cartItems: CartItem[];
  onUpdateQuantity: (id: string, quantity: number) => void;
  onRemoveItem: (id: string) => void;
  onStartCheckout: (discountPercent: number, promoCodeUsed: string) => void;
}

export default function CartDrawer({
  isOpen,
  onClose,
  cartItems,
  onUpdateQuantity,
  onRemoveItem,
  onStartCheckout
}: CartDrawerProps) {
  const [promoInput, setPromoInput] = useState('');
  const [appliedPromo, setAppliedPromo] = useState<PromoCode | null>(null);
  const [promoError, setPromoError] = useState('');

  const subtotal = cartItems.reduce((acc, item) => acc + item.product.price * item.quantity, 0);
  const discountAmount = appliedPromo ? (subtotal * appliedPromo.discountPercent) / 100 : 0;
  const total = Math.max(0, subtotal - discountAmount);

  // Goal amount for Free White-glove express shipping!
  const freeShippingThreshold = 1000000;
  const shippingPercent = Math.min(100, (subtotal / freeShippingThreshold) * 100);
  const missingForFreeShipping = Math.max(0, freeShippingThreshold - subtotal);

  const handleApplyPromo = () => {
    setPromoError('');
    const matched = PROMO_CODES.find(
      (p) => p.code.toLowerCase() === promoInput.trim().toLowerCase()
    );

    if (matched) {
      setAppliedPromo(matched);
      setPromoInput('');
    } else {
      setPromoError('Cupón inválido. Pruebe: PRIMEDROP o BIENVENIDOVIP');
    }
  };

  const handleRemovePromo = () => {
    setAppliedPromo(null);
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 overflow-hidden font-sans">
          
          {/* Backdrop overlay */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="absolute inset-0 bg-charcoal-900/60 backdrop-blur-xs"
          />

          {/* Drawer container align right */}
          <div className="absolute inset-y-0 right-0 max-w-full flex pl-10">
            <motion.div
              initial={{ x: '100%' }}
              animate={{ x: 0 }}
              exit={{ x: '100%' }}
              transition={{ type: 'spring', damping: 25, stiffness: 220 }}
              className="w-screen max-w-md bg-white shadow-2xl flex flex-col justify-between"
            >
              
              {/* Drawer Header */}
              <div className="p-6 border-b border-neutral-150 flex items-center justify-between bg-charcoal-900 text-white">
                <div className="flex items-center space-x-2.5">
                  <ShoppingBag className="w-5 h-5 text-gold-coulisse" />
                  <span className="font-serif text-lg font-bold tracking-wide">MI BOLSA DE COMPRAS</span>
                  <span className="text-xs bg-gold-coulisse/15 text-gold-200 border border-gold-400/30 px-2 py-0.5 rounded-md font-mono">
                    {cartItems.length}
                  </span>
                </div>
                <button
                  id="close-cart-btn"
                  onClick={onClose}
                  className="p-1.5 rounded-full hover:bg-white/10 text-charcoal-200 transition-colors"
                  aria-label="Cerrar bolsa"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              {/* Drawer Products Body Scroll */}
              <div className="flex-1 p-6 overflow-y-auto space-y-4">
                {cartItems.length === 0 ? (
                  <div className="h-full flex flex-col items-center justify-center text-center space-y-4 py-12">
                    <div className="p-5 rounded-full bg-neutral-100 text-neutral-300">
                      <ShoppingBag className="w-16 h-16 stroke-[1.2]" />
                    </div>
                    <div className="space-y-1">
                      <h4 className="font-serif text-lg font-bold text-charcoal-800">Tu bolsa está vacía</h4>
                      <p className="text-sm text-neutral-400 font-light max-w-xs mx-auto">
                        Aún no has añadido ningún bolso de lujo a tu selección exclusiva.
                      </p>
                    </div>
                    <button
                      id="continue-shopping-btn"
                      onClick={onClose}
                      className="px-6 py-2.5 text-xs tracking-wider uppercase font-semibold border border-charcoal-900 rounded-full text-charcoal-900 hover:bg-charcoal-900 hover:text-white transition-all shadow-xs"
                    >
                      Seguir explorando
                    </button>
                  </div>
                ) : (
                  cartItems.map((item) => (
                    <motion.div
                      id={`cart-item-${item.id}`}
                      key={item.id}
                      layout
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, scale: 0.9 }}
                      className="flex space-x-4 p-4 border border-neutral-150 rounded-xl bg-neutral-50/50 hover:bg-neutral-50 transition-colors relative"
                    >
                      {/* Product Thumbnail inside cart */}
                      <div className="w-20 h-24 bg-neutral-100 rounded-lg overflow-hidden flex-shrink-0 border border-neutral-200">
                        <img
                          src={item.product.primaryImage}
                          alt={item.product.name}
                          className="w-full h-full object-cover object-center"
                          referrerPolicy="no-referrer"
                        />
                      </div>

                      {/* Product text details */}
                      <div className="flex-1 flex flex-col justify-between">
                        <div>
                          <div className="flex items-start justify-between">
                            <h4 className="font-serif font-bold text-sm text-charcoal-900 tracking-wide line-clamp-1">
                              {item.product.name}
                            </h4>
                            <button
                              id={`delete-item-${item.id}`}
                              onClick={() => onRemoveItem(item.id)}
                              className="text-neutral-400 hover:text-red-500 p-0.5 transition-colors"
                              aria-label="Quitar de la bolsa"
                            >
                              <Trash2 className="w-4 h-4" />
                            </button>
                          </div>

                          {/* Attributes chosen */}
                          <div className="text-[10px] space-y-0.5 mt-1 text-charcoal-500 font-medium tracking-wide">
                            <p className="flex items-center">
                              Piel: <span className="ml-1 text-charcoal-800 font-bold">{item.selectedColor.name}</span>
                              <span className="w-1.5 h-1.5 rounded-full ml-1" style={{ backgroundColor: item.selectedColor.hex }} />
                            </p>
                            <p>
                              Herrajes: <span className="text-charcoal-800 font-bold">{item.selectedHardware}</span>
                            </p>
                            {item.customEngraving && (
                              <p className="inline-flex items-center bg-gold-100/50 text-gold-800 border border-gold-300/30 px-1.5 py-0.2 rounded mt-0.5 uppercase text-[9px] font-bold">
                                Grabado: "{item.customEngraving}"
                              </p>
                            )}
                          </div>
                        </div>

                        {/* Quantity and dynamic pricing math */}
                        <div className="flex items-center justify-between mt-2 pt-1 border-t border-neutral-200/50">
                          <div className="flex items-center border border-neutral-300 rounded-lg overflow-hidden text-xs bg-white">
                            <button
                              id={`decrease-quantity-${item.id}`}
                              onClick={() => onUpdateQuantity(item.id, Math.max(1, item.quantity - 1))}
                              className="px-2 py-0.5 text-neutral-500 hover:bg-neutral-100 font-bold"
                            >
                              -
                            </button>
                            <span className="px-2.5 font-bold text-charcoal-900 text-center w-5 select-none text-[11px]">
                              {item.quantity}
                            </span>
                            <button
                              id={`increase-quantity-${item.id}`}
                              onClick={() => onUpdateQuantity(item.id, item.quantity + 1)}
                              className="px-2 py-0.5 text-neutral-500 hover:bg-neutral-100 font-bold"
                            >
                              +
                            </button>
                          </div>

                          <div className="text-right">
                            <p className="font-serif font-black text-sm text-charcoal-900">
                              {formatCOP(item.product.price * item.quantity)}
                            </p>
                            {item.quantity > 1 && (
                              <p className="text-[9px] text-neutral-400">
                                {formatCOP(item.product.price)} cada uno
                              </p>
                            )}
                          </div>
                        </div>
                      </div>
                    </motion.div>
                  ))
                )}
              </div>

              {/* Drawer Footer and Checkout Activators */}
              <div className="p-6 border-t border-neutral-150 bg-neutral-50 space-y-4">
                
                {/* Subtotals & Math Summary */}
                <div className="space-y-2 text-sm pt-2 border-t border-neutral-200">
                  <div className="flex justify-between text-neutral-500 font-medium">
                    <span>Subtotal:</span>
                    <span className="font-semibold text-charcoal-900">{formatCOP(subtotal)}</span>
                  </div>
                  {appliedPromo && (
                    <div className="flex justify-between text-red-600 font-semibold">
                      <span>Descuento ({appliedPromo.discountPercent}%):</span>
                      <span>-{formatCOP(discountAmount)}</span>
                    </div>
                  )}
                  <div className="flex justify-between text-base font-serif font-black pt-2 border-t border-neutral-200 text-charcoal-950">
                    <span>Precio Estimado Total:</span>
                    <span className="text-lg">{formatCOP(total)}</span>
                  </div>
                </div>

                {/* Action button payments */}
                <button
                  id="checkout-drawer-trigger"
                  onClick={() => onStartCheckout(appliedPromo?.discountPercent || 0, appliedPromo?.code || '')}
                  disabled={cartItems.length === 0}
                  className={`w-full py-4 rounded-full text-xs font-semibold tracking-widest uppercase flex items-center justify-center space-x-2 transition-all duration-300 shadow-lg ${
                    cartItems.length === 0
                      ? 'bg-neutral-200 text-neutral-400 cursor-not-allowed shadow-none'
                      : 'bg-charcoal-900 text-white hover:bg-gold-coulisse hover:text-charcoal-950 hover:shadow-gold-500/10'
                  }`}
                >
                  <ShieldCheck className="w-4.5 h-4.5" />
                  <span>Proceder al Pago Seguro</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            </motion.div>
          </div>
        </div>
      )}
    </AnimatePresence>
  );
}

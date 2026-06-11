/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { X, Heart, ShoppingBag } from 'lucide-react';
import { BagProduct, ProductColor } from '../types';
import { motion, AnimatePresence } from 'motion/react';
import { formatCOP } from '../utils';

interface FavoritesModalProps {
  isOpen: boolean;
  onClose: () => void;
  products: BagProduct[];
  onSelectProduct: (product: BagProduct) => void;
  onAddToCart: (product: BagProduct, color: ProductColor) => void;
  onRemoveFavorite: (id: string, e: React.MouseEvent) => void;
}

export default function FavoritesModal({
  isOpen,
  onClose,
  products,
  onSelectProduct,
  onAddToCart,
  onRemoveFavorite,
}: FavoritesModalProps) {
  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="absolute inset-0 bg-black/60 backdrop-blur-xs"
          />

          <motion.div
            initial={{ opacity: 0, scale: 0.97, y: 12 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.97, y: 12 }}
            className="relative bg-white text-charcoal-900 w-full max-w-2xl rounded-3xl shadow-2xl border border-neutral-150 z-10 flex flex-col max-h-[85vh]"
          >
            {/* Header */}
            <div className="flex items-center justify-between p-6 border-b border-neutral-150">
              <div className="flex items-center gap-2.5">
                <Heart className="w-5 h-5 fill-charcoal-900 text-charcoal-900" />
                <h3 className="font-serif text-lg font-black tracking-wide">Mis Favoritos</h3>
                <span className="text-xs bg-neutral-100 border border-neutral-200 px-2 py-0.5 rounded-md font-mono">
                  {products.length}
                </span>
              </div>
              <button onClick={onClose} className="p-1.5 rounded-full hover:bg-neutral-100 transition-colors" aria-label="Cerrar">
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Body */}
            <div className="p-6 overflow-y-auto">
              {products.length === 0 ? (
                <div className="py-16 text-center space-y-4">
                  <div className="w-16 h-16 rounded-full bg-neutral-100 text-neutral-300 flex items-center justify-center mx-auto">
                    <Heart className="w-8 h-8 stroke-[1.2]" />
                  </div>
                  <div className="space-y-1">
                    <h4 className="font-serif text-lg font-bold text-charcoal-800">Aún no tienes favoritos</h4>
                    <p className="text-sm text-neutral-400 font-light max-w-xs mx-auto">
                      Toca el corazón en cualquier bolso para guardarlo aquí y encontrarlo fácil después.
                    </p>
                  </div>
                  <button
                    onClick={onClose}
                    className="px-6 py-2.5 text-xs tracking-wider uppercase font-semibold border border-charcoal-900 rounded-full text-charcoal-900 hover:bg-charcoal-900 hover:text-white transition-all"
                  >
                    Explorar bolsos
                  </button>
                </div>
              ) : (
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  {products.map((p) => (
                    <div key={p.id} className="flex gap-3 p-3 border border-neutral-150 rounded-2xl hover:bg-neutral-50/60 transition-colors">
                      <button
                        onClick={() => { onSelectProduct(p); onClose(); }}
                        className="w-20 h-24 bg-neutral-100 rounded-lg overflow-hidden flex-shrink-0"
                      >
                        <img src={p.primaryImage} alt={p.name} loading="lazy" decoding="async" className="w-full h-full object-cover" referrerPolicy="no-referrer" />
                      </button>
                      <div className="flex-1 flex flex-col justify-between min-w-0">
                        <div>
                          <p className="text-[10px] uppercase tracking-widest text-charcoal-400 font-semibold">{p.category}</p>
                          <button onClick={() => { onSelectProduct(p); onClose(); }} className="block text-left font-serif text-sm font-bold text-charcoal-900 hover:text-charcoal-600 line-clamp-1">
                            {p.name}
                          </button>
                          <p className="font-sans text-sm text-charcoal-900 mt-0.5">{formatCOP(p.price)}</p>
                        </div>
                        <div className="flex items-center gap-2 mt-2">
                          <button
                            onClick={() => onAddToCart(p, p.colors[0])}
                            disabled={!p.inStock}
                            className="flex-1 py-2 px-3 rounded-lg bg-charcoal-900 text-white text-[10px] uppercase tracking-wider font-semibold flex items-center justify-center gap-1.5 hover:bg-charcoal-700 transition disabled:bg-neutral-200 disabled:text-neutral-400"
                          >
                            <ShoppingBag className="w-3.5 h-3.5" />
                            {p.inStock ? 'Añadir' : 'Agotado'}
                          </button>
                          <button
                            onClick={(e) => onRemoveFavorite(p.id, e)}
                            aria-label="Quitar de favoritos"
                            className="p-2 rounded-lg border border-neutral-200 text-charcoal-700 hover:bg-neutral-100 transition"
                          >
                            <Heart className="w-3.5 h-3.5 fill-charcoal-900 text-charcoal-900" />
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}

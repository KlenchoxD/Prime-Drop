/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect } from 'react';
import { Star, Plus, Minus, ZoomIn, ChevronLeft, ShieldCheck, Truck, BadgeCheck } from 'lucide-react';
import { BagProduct } from '../types';
import { motion } from 'motion/react';
import { formatCOP } from '../utils';

interface ProductPageProps {
  product: BagProduct;
  onClose: () => void;
  onAddToCart: (product: BagProduct, quantity: number) => void;
  onBuyNow: (product: BagProduct, quantity: number) => void;
  relatedProducts: BagProduct[];
  onSelectProduct: (product: BagProduct) => void;
}

/**
 * Renders the 5-star rating following a consistent rule:
 *  - If the product has 0 reviews → show muted empty stars + "Sin valoraciones".
 *  - Otherwise → fill stars based on the rating and show the rating + reviews count.
 */
function RatingBlock({ rating, reviewsCount }: { rating: number; reviewsCount: number }) {
  const hasReviews = reviewsCount > 0;
  const rounded = Math.round(rating);

  return (
    <div className="flex items-center space-x-2">
      <div className="flex">
        {[...Array(5)].map((_, i) => {
          const filled = hasReviews && i < rounded;
          return (
            <Star
              key={i}
              className={`w-4 h-4 ${
                filled ? 'fill-charcoal-900 text-charcoal-900' : 'text-neutral-300'
              }`}
            />
          );
        })}
      </div>
      {hasReviews ? (
        <span className="text-xs text-charcoal-600 font-medium">
          {rating.toFixed(1)} · {reviewsCount} {reviewsCount === 1 ? 'reseña' : 'reseñas'}
        </span>
      ) : (
        <span className="text-xs text-charcoal-400">Sin valoraciones verificadas todavía</span>
      )}
    </div>
  );
}

export default function ProductDetailModal({
  product,
  onClose,
  onAddToCart,
  onBuyNow,
  relatedProducts,
  onSelectProduct
}: ProductPageProps) {
  const [quantity, setQuantity] = useState(1);
  const [selectedImage, setSelectedImage] = useState<string>(product.primaryImage);
  const [isDetailsOpen, setIsDetailsOpen] = useState(true);
  const [isAdditionalOpen, setIsAdditionalOpen] = useState(false);

  useEffect(() => {
    setQuantity(1);
    setSelectedImage(product.primaryImage);
    setIsDetailsOpen(true);
    setIsAdditionalOpen(false);
  }, [product]);

  // Build images array (unique, padded for thumbnail look)
  const images = Array.from(
    new Set([product.primaryImage, product.secondaryImage].filter(Boolean) as string[])
  );

  return (
    <div className="bg-white min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-10">

        {/* Breadcrumb / Back */}
        <button
          onClick={onClose}
          className="flex items-center gap-1.5 text-xs uppercase tracking-widest font-semibold text-charcoal-500 hover:text-charcoal-900 transition-colors mb-6"
        >
          <ChevronLeft className="w-4 h-4" />
          <span>Volver al catálogo</span>
        </button>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-14">

          {/* Left: Images */}
          <div className="flex flex-col-reverse sm:flex-row gap-4">
            {/* Thumbnails */}
            {images.length > 1 && (
              <div className="flex sm:flex-col gap-3 overflow-x-auto sm:overflow-visible">
                {images.map((img, idx) => (
                  <button
                    key={idx}
                    onClick={() => setSelectedImage(img)}
                    className={`w-16 h-20 sm:w-20 sm:h-24 flex-shrink-0 rounded-lg overflow-hidden border-2 transition-all ${
                      selectedImage === img ? 'border-charcoal-900' : 'border-neutral-200 hover:border-neutral-400'
                    }`}
                  >
                    <img src={img} alt={`Vista ${idx + 1}`} loading="lazy" decoding="async" className="w-full h-full object-cover" referrerPolicy="no-referrer" />
                  </button>
                ))}
              </div>
            )}

            {/* Main image */}
            <div className="flex-1 relative bg-neutral-50 rounded-2xl overflow-hidden flex items-center justify-center min-h-[360px] sm:min-h-[520px]">
              <img
                src={selectedImage}
                alt={product.name}
                decoding="async"
                className="w-full max-h-[560px] object-contain"
                referrerPolicy="no-referrer"
              />
              <div className="absolute top-4 right-4 w-10 h-10 bg-white/90 border border-neutral-200 rounded-full flex items-center justify-center text-charcoal-500 shadow-sm">
                <ZoomIn className="w-5 h-5" />
              </div>
              {product.isNew && (
                <span className="absolute top-4 left-4 bg-charcoal-900 text-white text-[10px] font-bold uppercase tracking-widest px-3 py-1.5 rounded-full">
                  Nuevo
                </span>
              )}
            </div>
          </div>

          {/* Right: Details */}
          <div className="flex flex-col">
            <p className="text-xs font-bold tracking-[0.2em] uppercase text-charcoal-500 mb-2">
              {product.brand || product.category}
            </p>
            <h1 className="font-serif text-3xl sm:text-4xl lg:text-5xl font-black text-charcoal-950 leading-tight tracking-tight mb-3">
              {product.name}
            </h1>

            <div className="mb-5">
              <RatingBlock rating={product.rating} reviewsCount={product.reviewsCount} />
            </div>

            {/* Price */}
            <div className="flex items-baseline gap-3 mb-6">
              <span className="text-3xl font-sans font-bold text-charcoal-900">{formatCOP(product.price)}</span>
              {product.originalPrice && (
                <span className="text-base line-through text-neutral-400">{formatCOP(product.originalPrice)}</span>
              )}
            </div>

            {/* Short description */}
            <p className="text-sm text-charcoal-600 leading-relaxed mb-6 font-serif">
              {product.description}
            </p>

            {/* Trust rows */}
            <div className="border border-neutral-200 rounded-xl divide-y divide-neutral-200 mb-7 text-xs">
              <div className="flex p-4 items-center gap-3">
                <BadgeCheck className="w-5 h-5 text-charcoal-700 flex-shrink-0" />
                <div><span className="font-bold text-charcoal-900">Addi disponible.</span> <span className="text-charcoal-600">Paga tu bolso en cuotas según aprobación.</span></div>
              </div>
              <div className="flex p-4 items-center gap-3">
                <Truck className="w-5 h-5 text-charcoal-700 flex-shrink-0" />
                <div><span className="font-bold text-charcoal-900">Entrega estimada.</span> <span className="text-charcoal-600">2 a 5 días hábiles tras confirmar el pago.</span></div>
              </div>
              <div className="flex p-4 items-center gap-3">
                <ShieldCheck className="w-5 h-5 text-charcoal-700 flex-shrink-0" />
                <div><span className="font-bold text-charcoal-900">100% original.</span> <span className="text-charcoal-600">Garantía de autenticidad Prime Drop Elite.</span></div>
              </div>
            </div>

            {/* Add to cart row */}
            <div className="flex gap-4 mb-4">
              <div className="flex items-center justify-between border border-charcoal-900 rounded-full px-3 w-32 h-[52px]">
                <button onClick={() => setQuantity(Math.max(1, quantity - 1))} className="text-charcoal-900 hover:text-charcoal-500 p-2"><Minus className="w-4 h-4" /></button>
                <span className="font-bold text-sm text-charcoal-900">{quantity}</span>
                <button onClick={() => setQuantity(quantity + 1)} className="text-charcoal-900 hover:text-charcoal-500 p-2"><Plus className="w-4 h-4" /></button>
              </div>
              <button
                onClick={() => onAddToCart(product, quantity)}
                disabled={!product.inStock}
                className="flex-1 bg-charcoal-900 text-white rounded-full font-bold text-xs tracking-widest uppercase hover:bg-gold-coulisse hover:text-charcoal-950 transition-colors h-[52px] flex items-center justify-center disabled:bg-neutral-200 disabled:text-neutral-400"
              >
                {product.inStock ? 'Añadir a la bolsa' : 'Agotado'}
              </button>
            </div>

            {product.inStock && (
              <button
                onClick={() => onBuyNow(product, quantity)}
                className="w-full border-2 border-charcoal-900 text-charcoal-900 rounded-full font-black text-[13px] tracking-widest uppercase hover:bg-charcoal-50 transition-colors min-h-[52px] flex items-center justify-center mb-8"
              >
                Comprar ahora
              </button>
            )}

            {/* Accordions */}
            <div className="border-t border-b border-charcoal-900 divide-y divide-neutral-200">
              <div>
                <button onClick={() => setIsDetailsOpen(!isDetailsOpen)} className="w-full py-5 flex items-center justify-between font-bold text-xs tracking-widest uppercase text-charcoal-900">
                  Detalles del producto
                  {isDetailsOpen ? <Minus className="w-4 h-4" /> : <Plus className="w-4 h-4" />}
                </button>
                <div className={`overflow-hidden transition-all duration-300 ${isDetailsOpen ? 'max-h-96 pb-4' : 'max-h-0'}`}>
                  <div className="text-sm text-charcoal-600 leading-relaxed font-serif">{product.longDescription}</div>
                </div>
              </div>
              <div>
                <button onClick={() => setIsAdditionalOpen(!isAdditionalOpen)} className="w-full py-5 flex items-center justify-between font-bold text-xs tracking-widest uppercase text-charcoal-900">
                  Información adicional
                  {isAdditionalOpen ? <Minus className="w-4 h-4" /> : <Plus className="w-4 h-4" />}
                </button>
                <div className={`overflow-hidden transition-all duration-300 ${isAdditionalOpen ? 'max-h-96 pb-4' : 'max-h-0'}`}>
                  <ul className="list-disc pl-4 space-y-1 text-sm text-charcoal-600">
                    <li>Dimensiones: {product.dimensions}</li>
                    {product.materials.map((m, idx) => <li key={idx}>{m}</li>)}
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Related products */}
        {relatedProducts.length > 0 && (
          <section className="mt-16 sm:mt-24">
            <div className="text-center mb-8">
              <h2 className="font-serif text-2xl sm:text-3xl font-black text-charcoal-900">También te puede gustar</h2>
              <p className="text-xs text-charcoal-500 mt-1 uppercase tracking-widest">Productos relacionados</p>
            </div>
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
              {relatedProducts.map((rel) => (
                <motion.button
                  key={rel.id}
                  onClick={() => onSelectProduct(rel)}
                  whileHover={{ y: -4 }}
                  className="group text-left bg-[#fdfdfc] rounded-2xl overflow-hidden shadow-sm hover:shadow-xl transition-all"
                >
                  <div className="aspect-[4/5] bg-neutral-100 overflow-hidden">
                    <img
                      src={rel.primaryImage}
                      alt={rel.name}
                      loading="lazy"
                      decoding="async"
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                      referrerPolicy="no-referrer"
                    />
                  </div>
                  <div className="p-4 space-y-1">
                    <p className="text-[10px] uppercase tracking-widest text-charcoal-400 font-semibold">{rel.category}</p>
                    <h3 className="font-serif text-sm font-bold text-charcoal-900 line-clamp-1 group-hover:text-gold-600 transition-colors">{rel.name}</h3>
                    <p className="font-sans text-sm text-charcoal-900">{formatCOP(rel.price)}</p>
                  </div>
                </motion.button>
              ))}
            </div>
          </section>
        )}
      </div>
    </div>
  );
}

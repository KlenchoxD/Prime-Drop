/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { ArrowRight, Heart } from 'lucide-react';
import { BagProduct, ProductColor } from '../types';
import { motion } from 'motion/react';

interface ProductCardProps {
  key?: string;
  product: BagProduct;
  onSelectProduct: (product: BagProduct) => void;
  onAddToCartDirect: (product: BagProduct, selectedColor: ProductColor) => void;
  isFavorite: boolean;
  onToggleFavorite: (id: string, e: React.MouseEvent) => void;
}

export default function ProductCard({
  product,
  onSelectProduct,
  onAddToCartDirect,
  isFavorite,
  onToggleFavorite
}: ProductCardProps) {
  const [hovered, setHovered] = useState(false);
  const [selectedColor, setSelectedColor] = useState<ProductColor>(product.colors[0]);

  const handleCardClick = () => {
    onSelectProduct(product);
  };

  const handleDirectAdd = (e: React.MouseEvent) => {
    e.stopPropagation();
    onAddToCartDirect(product, selectedColor);
  };

  return (
    <motion.article
      id={`product-card-${product.id}`}
      className="group relative bg-[#fdfdfc] rounded-2xl overflow-hidden shadow-sm hover:shadow-xl transition-all duration-500 flex flex-col cursor-pointer"
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      onClick={handleCardClick}
      whileHover={{ y: -5 }}
    >
      
      {/* Product Image Stage */}
      <div className="relative aspect-[4/5] bg-neutral-100 overflow-hidden select-none">
        {/* Dynamic Image Overlay (fading secondary view on hover) */}
        <div className="absolute inset-0">
          <img
            src={product.primaryImage}
            alt={`${product.name} primario`}
            loading="lazy"
            decoding="async"
            className={`w-full h-full object-cover object-center transition-all duration-700 transform scale-100 group-hover:scale-105 ${
              hovered && product.secondaryImage ? 'opacity-0 scale-95' : 'opacity-100'
            }`}
            referrerPolicy="no-referrer"
          />
          {product.secondaryImage && (
            <img
              src={product.secondaryImage}
              alt={`${product.name} secundario`}
              loading="lazy"
              decoding="async"
              className={`absolute inset-0 w-full h-full object-cover object-center transition-all duration-700 transform ${
                hovered ? 'opacity-100 scale-105' : 'opacity-0 scale-100'
              }`}
              referrerPolicy="no-referrer"
            />
          )}
        </div>

        {/* Quick View Tint Gradient */}
        <div className="absolute inset-0 bg-gradient-to-t from-charcoal-950/20 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />

        {/* Favorite (wishlist) toggle */}
        <button
          id={`favorite-toggle-${product.id}`}
          onClick={(e) => onToggleFavorite(product.id, e)}
          aria-label={isFavorite ? 'Quitar de favoritos' : 'Guardar en favoritos'}
          className="absolute top-3 right-3 z-10 w-9 h-9 rounded-full bg-white/90 backdrop-blur flex items-center justify-center shadow-sm hover:bg-white transition-colors"
        >
          <Heart className={`w-4.5 h-4.5 transition-colors ${isFavorite ? 'fill-charcoal-900 text-charcoal-900' : 'text-charcoal-500'}`} />
        </button>
      </div>

      {/* Details Area */}
      <div className="p-5 flex-1 flex flex-col justify-between space-y-4">
        
        {/* Title, Category and Rating */}
        <div className="space-y-1.5">
          <div className="flex items-center justify-between text-xs text-charcoal-400 font-medium uppercase tracking-widest">
            <span>{product.category}</span>
          </div>

          <h3 className="font-serif text-lg font-bold text-charcoal-900 tracking-wide group-hover:text-gold-600 transition-colors text-center">
            {product.name}
          </h3>

          <p className="text-xs text-charcoal-500 font-light line-clamp-2 h-8 leading-relaxed">
            {product.description}
          </p>
        </div>

        {/* Action Button: always visible so the card looks complete */}
        <div className="pt-1">
          <button
            id={`quick-add-${product.id}`}
            onClick={handleDirectAdd}
            disabled={!product.inStock}
            className={`w-full py-3 px-4 rounded-xl text-xs tracking-wider font-semibold uppercase flex items-center justify-center space-x-2 transition-all duration-300 ${
              !product.inStock
                ? 'bg-neutral-200 text-neutral-400 cursor-not-allowed border-none'
                : 'bg-charcoal-900 text-white hover:bg-gold-coulisse hover:text-charcoal-950 hover:shadow-md'
            }`}
          >
            <span>{product.inStock ? 'Añadir a la Bolsa' : 'Agotado'}</span>
            <ArrowRight className="w-3.5 h-3.5 transition-transform group-hover:translate-x-1" />
          </button>
        </div>
      </div>
    </motion.article>
  );
}

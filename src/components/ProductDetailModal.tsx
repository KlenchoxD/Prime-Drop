/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect } from 'react';
import { X, Star, Heart, Plus, Minus, ZoomIn } from 'lucide-react';
import { BagProduct, ProductColor } from '../types';
import { motion, AnimatePresence } from 'motion/react';
import { formatCOP } from '../utils';

interface ProductDetailModalProps {
  product: BagProduct | null;
  onClose: () => void;
  onAddToCart: (
    product: BagProduct,
    quantity: number,
    selectedColor: ProductColor,
    customEngraving: string,
    selectedHardware: 'Gold' | 'Silver' | 'Obsidian'
  ) => void;
}

export default function ProductDetailModal({
  product,
  onClose,
  onAddToCart
}: ProductDetailModalProps) {
  const [quantity, setQuantity] = useState(1);
  const [activeTab, setActiveTab] = useState<'details' | 'additional'>('details');
  const [selectedImage, setSelectedImage] = useState<string>('');
  
  // States for accordions
  const [isDetailsOpen, setIsDetailsOpen] = useState(true);
  const [isAdditionalOpen, setIsAdditionalOpen] = useState(false);

  useEffect(() => {
    if (product) {
      setQuantity(1);
      setSelectedImage(product.primaryImage);
      setIsDetailsOpen(true);
      setIsAdditionalOpen(false);
    }
  }, [product]);

  if (!product) return null;

  const handleAddToCartSubmit = () => {
    onAddToCart(product, quantity, product.colors[0], '', 'Gold');
    onClose();
  };

  const handleBuyNow = () => {
    onAddToCart(product, quantity, product.colors[0], '', 'Gold');
    onClose();
  };

  // Build images array
  const images = [product.primaryImage];
  if (product.secondaryImage) images.push(product.secondaryImage);
  // Just pad with some repeats for the thumbnail look if there's only 1 or 2
  while (images.length < 5) {
    images.push(product.secondaryImage || product.primaryImage);
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6">
      
      {/* Backdrop (Removed blur for performance) */}
      <div
        onClick={onClose}
        className="fixed inset-0 bg-black/60 cursor-pointer"
      />

      {/* Modal Container */}
      <div
        className="relative bg-white w-full max-w-5xl rounded-2xl shadow-2xl z-10 flex flex-col md:flex-row max-h-[90vh] overflow-hidden"
      >
        {/* Close button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 z-20 p-2 rounded-full hover:bg-neutral-100 text-charcoal-900 transition-colors cursor-pointer"
        >
          <X className="w-6 h-6" />
        </button>

        {/* Left Column: Images (Thumbnails + Main) */}
        <div className="w-full md:w-[55%] flex flex-col sm:flex-row p-6 lg:p-10 gap-6 bg-white overflow-y-auto [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none]">
          
          {/* Thumbnails */}
          <div className="flex sm:flex-col gap-3 order-2 sm:order-1 overflow-x-auto sm:overflow-y-auto [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none]">
            {images.map((img, idx) => (
              <button
                key={idx}
                onClick={() => setSelectedImage(img)}
                className={`w-16 h-20 sm:w-20 sm:h-24 flex-shrink-0 border-2 transition-all cursor-pointer ${selectedImage === img ? 'border-charcoal-900' : 'border-transparent hover:border-neutral-300'}`}
              >
                <img src={img} alt={`Thumbnail ${idx}`} className="w-full h-full object-cover" />
              </button>
            ))}
          </div>

          {/* Main Image */}
          <div className="flex-1 relative order-1 sm:order-2 flex items-center justify-center bg-white min-h-[400px]">
            <img src={selectedImage} alt={product.name} className="w-full max-h-[500px] object-contain transition-opacity duration-300" />
            <button className="absolute top-4 right-4 w-10 h-10 bg-white border border-neutral-200 rounded-full flex items-center justify-center text-charcoal-600 hover:text-charcoal-900 hover:border-charcoal-900 transition-colors shadow-sm cursor-pointer">
              <ZoomIn className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Right Column: Product Details */}
        <div className="w-full md:w-[45%] p-6 lg:p-10 lg:pl-0 flex flex-col overflow-y-auto [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none]">
          
          {/* Title & Brand */}
          <h1 className="font-serif text-3xl sm:text-4xl lg:text-5xl font-black text-charcoal-950 leading-tight tracking-tight mb-2">
            {product.name}
          </h1>
          <p className="text-xs font-bold tracking-[0.2em] uppercase text-charcoal-500 mb-4">
            {product.category}
          </p>

          {/* Rating */}
          <div className="flex items-center space-x-2 mb-6">
            <div className="flex text-gold-coulisse">
              {[...Array(5)].map((_, i) => (
                <Star key={i} className="w-4 h-4 fill-gold-coulisse text-gold-coulisse" />
              ))}
            </div>
            <span className="text-xs text-charcoal-500">Valoraciones de clientes</span>
          </div>

          {/* Price */}
          <div className="mb-6">
            <span className="text-3xl font-sans font-bold text-charcoal-900">
              {formatCOP(product.price)}
            </span>
          </div>

          {/* Info Boxes (Color & Brand) */}
          <div className="flex gap-4 mb-6">
            <div className="flex items-center space-x-3 border border-neutral-200 rounded-md px-4 py-2.5 flex-1">
              <div className="w-5 h-5 rounded-full border border-neutral-300" style={{ backgroundColor: product.colors[0]?.hex || '#121212' }}></div>
              <div className="flex flex-col">
                <span className="text-[10px] text-charcoal-400 font-medium">Color</span>
                <span className="text-xs font-bold text-charcoal-900">{product.colors[0]?.name || 'Negro'}</span>
              </div>
            </div>
            <div className="flex items-center space-x-3 border border-neutral-200 rounded-md px-4 py-2.5 flex-1">
              <svg className="w-5 h-5 text-charcoal-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path><line x1="3" y1="6" x2="21" y2="6"></line><path d="M16 10a4 4 0 0 1-8 0"></path></svg>
              <div className="flex flex-col">
                <span className="text-[10px] text-charcoal-400 font-medium">Marca</span>
                <span className="text-xs font-bold text-charcoal-900">{product.category}</span>
              </div>
            </div>
          </div>

          {/* Feature Rows */}
          <div className="border border-neutral-200 rounded-md divide-y divide-neutral-200 mb-8 text-xs">
            <div className="flex p-4 items-center">
              <div className="font-bold w-24 flex-shrink-0 text-charcoal-900">Addi<br/>disponible</div>
              <div className="text-charcoal-600">Paga tu bolso en cuotas según<br/>aprobación.</div>
            </div>
            <div className="flex p-4 items-center">
              <div className="font-bold w-24 flex-shrink-0 text-charcoal-900">Entrega<br/>estimada</div>
              <div className="text-charcoal-600">2 a 5 días hábiles después de confirmar<br/>el pago.</div>
            </div>
          </div>

          {/* Add to Cart Row */}
          <div className="flex gap-4 mb-4">
            {/* Quantity */}
            <div className="flex items-center justify-between border border-charcoal-900 rounded-full px-4 w-28 h-[52px]">
              <button onClick={() => setQuantity(Math.max(1, quantity - 1))} className="text-charcoal-900 hover:text-charcoal-500 cursor-pointer p-2"><Minus className="w-4 h-4" /></button>
              <span className="font-bold text-sm text-charcoal-900">{quantity}</span>
              <button onClick={() => setQuantity(quantity + 1)} className="text-charcoal-900 hover:text-charcoal-500 cursor-pointer p-2"><Plus className="w-4 h-4" /></button>
            </div>
            {/* Add to bag button */}
            <button 
              onClick={handleAddToCartSubmit}
              className="flex-1 bg-charcoal-900 text-white rounded-full font-bold text-xs tracking-widest uppercase hover:bg-charcoal-800 transition-colors h-[52px] flex items-center justify-center cursor-pointer"
            >
              Añadir a la bolsa
            </button>
          </div>

          {/* Buy Now Button */}
          <button 
            onClick={handleBuyNow}
            className="w-full border-2 border-charcoal-900 text-charcoal-900 rounded-full font-black text-[13px] tracking-widest uppercase hover:bg-charcoal-50 transition-colors min-h-[52px] flex items-center justify-center mb-8 cursor-pointer"
          >
            Comprar Ahora
          </button>

          {/* Accordions */}
          <div className="border-t border-b border-charcoal-900 divide-y divide-neutral-200 mt-auto">
            
            {/* Detalles */}
            <div className="">
              <button 
                onClick={() => setIsDetailsOpen(!isDetailsOpen)}
                className="w-full py-5 flex items-center justify-between font-bold text-xs tracking-widest uppercase text-charcoal-900 cursor-pointer"
              >
                Detalles del producto
                {isDetailsOpen ? <Minus className="w-4 h-4" /> : <Plus className="w-4 h-4" />}
              </button>
              <div className={`overflow-hidden transition-all duration-300 ease-in-out ${isDetailsOpen ? 'max-h-96 pb-4' : 'max-h-0'}`}>
                <div className="text-xs text-charcoal-600 leading-relaxed font-serif">
                  {product.longDescription}
                </div>
              </div>
            </div>

            {/* Informacion Adicional */}
            <div className="">
              <button 
                onClick={() => setIsAdditionalOpen(!isAdditionalOpen)}
                className="w-full py-5 flex items-center justify-between font-bold text-xs tracking-widest uppercase text-charcoal-900 cursor-pointer"
              >
                Información adicional
                {isAdditionalOpen ? <Minus className="w-4 h-4" /> : <Plus className="w-4 h-4" />}
              </button>
              <div className={`overflow-hidden transition-all duration-300 ease-in-out ${isAdditionalOpen ? 'max-h-96 pb-4' : 'max-h-0'}`}>
                <div className="text-xs text-charcoal-600 leading-relaxed">
                  <ul className="list-disc pl-4 space-y-1">
                    <li>Dimensiones: {product.dimensions}</li>
                    {product.materials.map((m, idx) => <li key={idx}>{m}</li>)}
                  </ul>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
  );
}

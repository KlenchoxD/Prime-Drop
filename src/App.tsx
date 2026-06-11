/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useRef } from 'react';
import { BagProduct, CartItem, ProductColor } from './types';
import { BAG_PRODUCTS } from './data/products';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import ProductCard from './components/ProductCard';
import ProductDetailModal from './components/ProductDetailModal';
import CartDrawer from './components/CartDrawer';
import CheckoutFlow from './components/CheckoutFlow';
import MundoPrime from './components/MundoPrime';
import AuthModal from './components/AuthModal';
import FavoritesModal from './components/FavoritesModal';
import { BACKEND_ENABLED, apiMe, apiLogout } from './lib/api';
import { TERMS_CONTENT, PRIVACY_CONTENT, REFUND_CONTENT, WARRANTY_CONTENT } from './data/policies';

import {
  Search,
  ArrowUpDown,
  Sparkles,
  X,
  Mail,
  Instagram,
  ChevronLeft,
  ChevronRight
} from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';

export default function App() {
  const [activeTab, setActiveTab] = useState<'inicio' | 'bolsos' | 'prime'>('inicio');
  const [cart, setCart] = useState<CartItem[]>([]);
  const [selectedProduct, setSelectedProduct] = useState<BagProduct | null>(null);
  const [cartOpen, setCartOpen] = useState(false);
  const [checkoutOpen, setCheckoutOpen] = useState(false);
  const [isPrimeMember, setIsPrimeMember] = useState(false);
  const [favorites, setFavorites] = useState<string[]>(() => {
    try { return JSON.parse(localStorage.getItem('prime_favorites') || '[]'); }
    catch { return []; }
  });
  const [favoritesOpen, setFavoritesOpen] = useState(false);
  const [authOpen, setAuthOpen] = useState(false);
  const [currentUserEmail, setCurrentUserEmail] = useState('');
  const [currentUsername, setCurrentUsername] = useState('Socio Elite');

  // Filtering states
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('Todos');
  const [sortOption, setSortOption] = useState<'default' | 'price-asc' | 'price-desc' | 'popular'>('default');

  // Checkout tracker state (carried from cart drawer discounts)
  const [appliedDiscountPercent, setAppliedDiscountPercent] = useState(0);
  const [promoCodeUsed, setPromoCodeUsed] = useState('');

  // Tendencias carousel state
  const [carouselIndex, setCarouselIndex] = useState(0);
  const carouselRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const CAROUSEL_VISIBLE = 3;

  useEffect(() => {
    return () => { if (carouselRef.current) clearInterval(carouselRef.current); };
  }, []);

  // Persistir favoritos
  useEffect(() => {
    localStorage.setItem('prime_favorites', JSON.stringify(favorites));
  }, [favorites]);

  const handleCarouselPrev = () => {
    setCarouselIndex(prev => Math.max(0, prev - 1));
  };
  const handleCarouselNext = () => {
    setCarouselIndex(prev => Math.min(BAG_PRODUCTS.length - CAROUSEL_VISIBLE, prev + 1));
  };
  const carouselVisible = BAG_PRODUCTS.slice(carouselIndex, carouselIndex + CAROUSEL_VISIBLE);

  // Modales de políticas de la tienda
  const [policyModal, setPolicyModal] = useState<{ isOpen: boolean; title: string; content: string }>({
    isOpen: false,
    title: '',
    content: ''
  });

  // Small floating toast notifications state
  const [notifications, setNotifications] = useState<Array<{ id: string; message: string; type: 'success' | 'info' | 'gold' }>>([]);

  // Trigger floating notifications
  const triggerNotification = (message: string, type: 'success' | 'info' | 'gold' = 'success') => {
    const freshId = Date.now().toString();
    setNotifications((prev) => [...prev, { id: freshId, message, type }]);
    setTimeout(() => {
      setNotifications((prev) => prev.filter((n) => n.id !== freshId));
    }, 3500);
  };

  // 1. Direct Add to cart from listing (uses default first leather color configuration)
  const handleAddToCartDirect = (product: BagProduct, selectedColor: ProductColor) => {
    const compositeId = `${product.id}-${selectedColor.name.toLowerCase().replace(/\s/g, '-')}-none-gold`;
    
    setCart((prevCart) => {
      const match = prevCart.find((item) => item.id === compositeId);
      if (match) {
        triggerNotification(`Aumentado: ${product.name} (${selectedColor.name}) en tu bolsa.`, 'success');
        return prevCart.map((item) =>
          item.id === compositeId ? { ...item, quantity: item.quantity + 1 } : item
        );
      } else {
        triggerNotification(`Añadido: ${product.name} (${selectedColor.name}) a tu bolsa.`, 'success');
        return [
          ...prevCart,
          {
            id: compositeId,
            product,
            quantity: 1,
            selectedColor,
            customEngraving: '',
            selectedHardware: 'Gold'
          }
        ];
      }
    });
  };

  // 2. Custom Add to cart from Detailed Modal (with engraved initials and metal locks)
  const handleAddToCartCustom = (
    product: BagProduct,
    quantity: number,
    selectedColor: ProductColor,
    customEngraving: string,
    selectedHardware: 'Gold' | 'Silver' | 'Obsidian'
  ) => {
    const engravingKey = customEngraving ? customEngraving.toLowerCase() : 'none';
    const compositeId = `${product.id}-${selectedColor.name.toLowerCase().replace(/\s/g, '-')}-${engravingKey}-${selectedHardware.toLowerCase()}`;

    setCart((prevCart) => {
      const match = prevCart.find((item) => item.id === compositeId);
      if (match) {
        triggerNotification(`Cantidad coordinada para ${product.name}!`, 'success');
        return prevCart.map((item) =>
          item.id === compositeId ? { ...item, quantity: item.quantity + quantity } : item
        );
      } else {
        triggerNotification(`Reservados ${quantity} unidades de ${product.name} en tu bolsa.`, 'gold');
        return [
          ...prevCart,
          {
            id: compositeId,
            product,
            quantity,
            selectedColor,
            customEngraving,
            selectedHardware
          }
        ];
      }
    });
  };

  const handleUpdateCartQuantity = (id: string, quantity: number) => {
    setCart((prevCart) =>
      prevCart.map((item) => (item.id === id ? { ...item, quantity } : item))
    );
  };

  const handleRemoveItem = (id: string) => {
    setCart((prevCart) => {
      const match = prevCart.find((item) => item.id === id);
      if (match) {
        triggerNotification(`Removido: ${match.product.name} de la selección.`, 'info');
      }
      return prevCart.filter((item) => item.id !== id);
    });
  };

  const handleToggleFavorite = (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    setFavorites((prev) => {
      const exists = prev.includes(id);
      if (exists) {
        triggerNotification('Removido de favoritos', 'info');
        return prev.filter((fid) => fid !== id);
      } else {
        triggerNotification('Bolso guardado en favoritos ❤️', 'success');
        return [...prev, id];
      }
    });
  };

  // Open a product page (scrolls to top, professional product view instead of modal)
  const handleSelectProduct = (product: BagProduct) => {
    setSelectedProduct(product);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleCloseProductPage = () => {
    setSelectedProduct(null);
  };

  // Add to cart from the product page (default config: first color, no engraving, gold hardware)
  const handleAddFromPage = (product: BagProduct, quantity: number) => {
    handleAddToCartCustom(product, quantity, product.colors[0], '', 'Gold');
  };

  // Buy now from the product page → add then open cart
  const handleBuyNowFromPage = (product: BagProduct, quantity: number) => {
    handleAddToCartCustom(product, quantity, product.colors[0], '', 'Gold');
    setSelectedProduct(null);
    setCartOpen(true);
  };

  // Related products: same category first, then fill with others, excluding current
  const relatedProducts = selectedProduct
    ? (() => {
        const sameCategory = BAG_PRODUCTS.filter(
          (p) => p.id !== selectedProduct.id && p.category === selectedProduct.category
        );
        const others = BAG_PRODUCTS.filter(
          (p) => p.id !== selectedProduct.id && p.category !== selectedProduct.category
        );
        return [...sameCategory, ...others].slice(0, 4);
      })()
    : [];

  // Switch to checkout state
  const handleStartCheckout = (discountPercent: number, promoCodeUsed: string) => {
    setAppliedDiscountPercent(discountPercent);
    setPromoCodeUsed(promoCodeUsed);
    setCartOpen(false);
    setCheckoutOpen(true);
  };

  // Complete checkout process
  const handleOrderCompleted = () => {
    setCart([]);
    setAppliedDiscountPercent(0);
    setPromoCodeUsed('');
    triggerNotification('¡Gracias por tu compra! Revisa WhatsApp para finalizar tu pedido.', 'gold');
  };

  useEffect(() => {
    if (BACKEND_ENABLED) {
      // Restaurar sesión real desde el backend
      apiMe()
        .then(({ user }) => {
          if (user) {
            setCurrentUsername(user.name);
            setCurrentUserEmail(user.email);
            setIsPrimeMember(true);
          }
        })
        .catch(() => { /* sin sesión */ });
    } else {
      const savedName = localStorage.getItem('prime_user_name');
      const savedEmail = localStorage.getItem('prime_user_email');
      if (savedName && savedEmail) {
        setCurrentUsername(savedName);
        setCurrentUserEmail(savedEmail);
        setIsPrimeMember(true);
      }
    }

    // Listen for category selection from Navbar dropdown
    const handleSelectCategory = (e: Event) => {
      const customEvent = e as CustomEvent;
      setSelectedCategory(customEvent.detail);
    };
    window.addEventListener('selectCategory', handleSelectCategory);
    return () => window.removeEventListener('selectCategory', handleSelectCategory);
  }, []);

  const handleLoginSuccess = (name: string, email: string) => {
    setCurrentUsername(name);
    setCurrentUserEmail(email);
    setIsPrimeMember(true);
    triggerNotification(`¡Sesión iniciada! Bienvenido ${name}.`, 'gold');
  };

  const handleLogout = () => {
    if (BACKEND_ENABLED) {
      apiLogout().catch(() => { /* ignorar */ });
    }
    localStorage.removeItem('prime_user_name');
    localStorage.removeItem('prime_user_email');
    setCurrentUsername('Socio Elite');
    setCurrentUserEmail('');
    setIsPrimeMember(false);
    triggerNotification('Sesión finalizada.', 'info');
  };

  // Open VIP modal trigger from navbar
  const handleNavbarOpenVip = () => {
    setActiveTab('prime');
    window.scrollTo({ top: 350, behavior: 'smooth' });
    triggerNotification('Accediendo al panel de acceso y registro privado.', 'gold');
  };

  // Products filters math calculation
  const filteredProducts = BAG_PRODUCTS.filter((product) => {
    // 1. Search term match
    const matchesSearch =
      product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      product.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
      product.category.toLowerCase().includes(searchTerm.toLowerCase());

    // 2. Category match
    const matchesCategory =
      selectedCategory === 'Todos' || product.category === selectedCategory;

    return matchesSearch && matchesCategory;
  }).sort((a, b) => {
    if (sortOption === 'price-asc') return a.price - b.price;
    if (sortOption === 'price-desc') return b.price - a.price;
    if (sortOption === 'popular') return b.reviewsCount - a.reviewsCount;
    return 0; // Default ID sort
  });

  const cartItemsCount = cart.reduce((acc, item) => acc + item.quantity, 0);

  return (
    <div className="min-h-screen bg-[#faf9f6] text-charcoal-900 flex flex-col justify-between selection:bg-gold-200 selection:text-charcoal-950 font-serif relative antialiased">
      
      {/* Floating Notifications Toast Stack */}
      <div id="toast-wrapper" className="fixed bottom-24 right-6 z-[60] flex flex-col space-y-3 max-w-sm pointer-events-none">
        <AnimatePresence>
          {notifications.map((notif) => (
            <motion.div
              key={notif.id}
              initial={{ opacity: 0, y: 20, scale: 0.9 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, scale: 0.85, x: 50 }}
              className={`p-4 rounded-2xl shadow-xl flex items-center space-x-3 pointer-events-auto border ${
                notif.type === 'gold'
                  ? 'bg-charcoal-900 border-gold-400 text-gold-200'
                  : notif.type === 'info'
                  ? 'bg-charcoal-800 border-charcoal-750 text-white'
                  : 'bg-white border-neutral-200 text-charcoal-900'
              }`}
            >
              <div className="p-1 rounded-full bg-black/10 shrink-0">
                <Sparkles className="w-4 h-4" />
              </div>
              <p className="text-xs font-semibold tracking-wide leading-normal">{notif.message}</p>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>

      {/* Main Header navigation link bar */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={(tab) => { setSelectedProduct(null); setActiveTab(tab); }}
        cartCount={cartItemsCount}
        onOpenCart={() => setCartOpen(true)}
        isPrimeMember={isPrimeMember}
        onOpenVipModal={handleNavbarOpenVip}
        onOpenAuth={() => setAuthOpen(true)}
        onOpenFavorites={() => setFavoritesOpen(true)}
        favoriteCount={favorites.length}
        currentUserEmail={currentUserEmail}
      />

      {/* Favoritos */}
      <FavoritesModal
        isOpen={favoritesOpen}
        onClose={() => setFavoritesOpen(false)}
        products={BAG_PRODUCTS.filter((p) => favorites.includes(p.id))}
        onSelectProduct={handleSelectProduct}
        onAddToCart={handleAddToCartDirect}
        onRemoveFavorite={handleToggleFavorite}
      />

      {/* Main Sections */}
      <main className="flex-grow pt-[156px] md:pt-[172px]">

        {/* PRODUCT PAGE — replaces tab content when a product is selected */}
        {selectedProduct && (
          <ProductDetailModal
            product={selectedProduct}
            onClose={handleCloseProductPage}
            onAddToCart={handleAddFromPage}
            onBuyNow={handleBuyNowFromPage}
            relatedProducts={relatedProducts}
            onSelectProduct={handleSelectProduct}
          />
        )}

        {/* TAB 1: INICIO (HOME PAGE) */}
        {!selectedProduct && activeTab === 'inicio' && (
          <div className="space-y-0">

            {/* Elegant Parallax introduction Hero */}
            <Hero
              onExploreProducts={() => setActiveTab('bolsos')}
              onJoinPrime={() => {
                setActiveTab('prime');
                window.scrollTo({ top: 0, behavior: 'smooth' });
              }}
            />

            {/* Instagram Section just below the Hero/Vision */}
            <section id="instagram-vogue-section" className="w-full py-1 bg-white">
              <div className="flex flex-col sm:flex-row w-full justify-between gap-1 px-0">
                {[
                  'https://www.instagram.com/p/DOURt7rD71p/embed',
                  'https://www.instagram.com/p/DRZ7kpsEcdK/embed',
                  'https://www.instagram.com/p/DRVHe_AjzaM/embed'
                ].map((src, i) => (
                  <div key={i} className="flex-1 relative overflow-hidden bg-white" style={{ aspectRatio: '0.76 / 1' }}>
                    <iframe
                      src={src}
                      className="absolute top-0 left-0 w-full border-none"
                      style={{ height: 'calc(100% + 46px)' }}
                      scrolling="no"
                      loading="lazy"
                      allowTransparency={true}
                      title={`Instagram Post ${i + 1}`}
                    />
                  </div>
                ))}
              </div>
            </section>
            {/* Tendencias - Manual Carousel */}
            <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 border-t border-neutral-200">
              <div className="flex items-center justify-center gap-6 mb-10">
                <button
                  id="carousel-prev-btn"
                  onClick={handleCarouselPrev}
                  disabled={carouselIndex === 0}
                  className="w-11 h-11 rounded-full border border-neutral-300 bg-white flex items-center justify-center hover:bg-charcoal-900 hover:text-white hover:border-charcoal-900 disabled:opacity-25 disabled:cursor-not-allowed transition-all shadow-sm"
                >
                  <ChevronLeft className="w-5 h-5" />
                </button>
                <h3 className="font-serif text-3xl sm:text-4xl font-black text-charcoal-900 tracking-tight text-center">Tendencias</h3>
                <button
                  id="carousel-next-btn"
                  onClick={handleCarouselNext}
                  disabled={carouselIndex >= BAG_PRODUCTS.length - CAROUSEL_VISIBLE}
                  className="w-11 h-11 rounded-full border border-neutral-300 bg-white flex items-center justify-center hover:bg-charcoal-900 hover:text-white hover:border-charcoal-900 disabled:opacity-25 disabled:cursor-not-allowed transition-all shadow-sm"
                >
                  <ChevronRight className="w-5 h-5" />
                </button>
              </div>

              <AnimatePresence mode="wait">
                <motion.div
                  key={carouselIndex}
                  initial={{ opacity: 0, x: 40 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -40 }}
                  transition={{ duration: 0.4 }}
                  className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8"
                >
                  {carouselVisible.map((bag) => (
                    <ProductCard
                      key={bag.id}
                      product={bag}
                      onSelectProduct={handleSelectProduct}
                      onAddToCartDirect={handleAddToCartDirect}
                      isFavorite={favorites.includes(bag.id)}
                      onToggleFavorite={handleToggleFavorite}
                    />
                  ))}
                </motion.div>
              </AnimatePresence>
            </section>

            {/* Socios Comerciales — logos reales */}
            <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 border-t border-neutral-200">
              <div className="text-center mb-6">
                <h3 className="font-serif text-2xl sm:text-3xl font-black text-charcoal-900">Nuestros Socios Comerciales</h3>
              </div>
              <div className="flex flex-wrap items-center justify-center w-full max-w-5xl mx-auto gap-6 sm:gap-10">
                {/* Nequi — gris, revela su color al pasar el mouse */}
                <div className="flex items-center justify-center shrink-0 group">
                  <svg viewBox="0 0 120 40" className="h-8 sm:h-10 w-auto transition-all duration-300" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <text x="0" y="32" fontFamily="Arial Black, sans-serif" fontWeight="900" fontSize="34" className="transition-all duration-300 group-hover:fill-[#9B1FC1]" fill="#bbb">nequi</text>
                  </svg>
                </div>
                {/* Bancolombia — revela amarillo al pasar el mouse */}
                <div className="flex items-center justify-center shrink-0 group">
                  <svg viewBox="0 0 220 40" className="h-8 sm:h-10 w-auto transition-all duration-300" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="0" y="4" width="32" height="32" rx="4" className="transition-all duration-300 group-hover:fill-[#FDDA24]" fill="#ccc"/>
                    <text x="38" y="30" fontFamily="Arial, sans-serif" fontWeight="700" fontSize="22" className="transition-all duration-300 group-hover:fill-[#1A1A1A]" fill="#bbb">Bancolombia</text>
                  </svg>
                </div>
                {/* PSE — revela azul al pasar el mouse */}
                <div className="flex items-center justify-center shrink-0 group">
                  <svg viewBox="0 0 80 40" className="h-8 sm:h-10 w-auto transition-all duration-300" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="0" y="4" width="80" height="32" rx="6" className="transition-all duration-300 group-hover:fill-[#003DA5]" fill="#ccc"/>
                    <text x="40" y="27" textAnchor="middle" fontFamily="Arial Black, sans-serif" fontWeight="900" fontSize="18" className="transition-all duration-300 group-hover:fill-white" fill="#888">PSE</text>
                  </svg>
                </div>
                {/* Wompi — gris, revela color al pasar el mouse */}
                <div className="flex items-center justify-center shrink-0">
                  <img
                    src="/images/socio_wompi.png"
                    alt="Wompi"
                    loading="lazy"
                    decoding="async"
                    className="h-8 sm:h-10 w-auto object-contain opacity-60 hover:opacity-100 transition-all duration-300 grayscale hover:grayscale-0"
                  />
                </div>
                {/* Addi — gris, revela color al pasar el mouse */}
                <div className="flex items-center justify-center shrink-0">
                  <img
                    src="/images/socio_addi.png"
                    alt="Addi"
                    loading="lazy"
                    decoding="async"
                    className="h-8 sm:h-10 w-auto object-contain opacity-60 hover:opacity-100 transition-all duration-300 grayscale hover:grayscale-0"
                  />
                </div>
                {/* Mercado Pago — gris, revela color al pasar el mouse */}
                <div className="flex items-center justify-center shrink-0">
                  <img
                    src="/images/socio_mercadopago.png"
                    alt="Mercado Pago"
                    loading="lazy"
                    decoding="async"
                    className="h-8 sm:h-10 w-auto object-contain opacity-60 hover:opacity-100 transition-all duration-300 grayscale hover:grayscale-0"
                  />
                </div>
              </div>
            </section>


          </div>
        )}

        {/* TAB 2: BOLSOS (CATALOG SHOP PAGE) */}
        {!selectedProduct && activeTab === 'bolsos' && (
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-10">
            {/* Catalog header */}
            <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4 pb-2">
              <div>
                <h2 className="font-serif text-3xl sm:text-4xl font-black text-charcoal-950 tracking-tight">
                  {selectedCategory === 'Todos' ? 'Todos los bolsos' : selectedCategory}
                </h2>
                <p className="text-xs text-charcoal-500 mt-1 tracking-wide">
                  {filteredProducts.length} {filteredProducts.length === 1 ? 'producto disponible' : 'productos disponibles'}
                </p>
              </div>

              {/* Search + Sort controls */}
              <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 w-full sm:w-auto">
                {/* Search box */}
                <div className="relative flex-1 sm:w-72">
                  <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-neutral-400 pointer-events-none" />
                  <input
                    id="catalog-search-textbox"
                    type="text"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    placeholder="Buscar bolso, material…"
                    className="w-full pl-11 pr-10 py-3 rounded-full border border-neutral-200 bg-white text-sm text-charcoal-800 placeholder-neutral-400 focus:outline-none focus:border-charcoal-900 focus:ring-2 focus:ring-charcoal-900/5 transition-all"
                  />
                  {searchTerm && (
                    <button
                      id="clear-search-btn"
                      onClick={() => setSearchTerm('')}
                      className="absolute right-4 top-1/2 -translate-y-1/2 text-neutral-400 hover:text-charcoal-900"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  )}
                </div>

                {/* Sort dropdown */}
                <div className="relative shrink-0">
                  <ArrowUpDown className="absolute left-4 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-neutral-400 pointer-events-none" />
                  <select
                    id="catalog-sort-dropdown"
                    value={sortOption}
                    onChange={(e: any) => setSortOption(e.target.value)}
                    className="appearance-none pl-10 pr-10 py-3 rounded-full border border-neutral-200 bg-white text-sm text-charcoal-700 font-medium focus:outline-none focus:border-charcoal-900 focus:ring-2 focus:ring-charcoal-900/5 cursor-pointer transition-all"
                  >
                    <option value="default">Ordenar por</option>
                    <option value="price-asc">Precio: menor a mayor</option>
                    <option value="price-desc">Precio: mayor a menor</option>
                    <option value="popular">Más populares</option>
                  </select>
                  <ChevronRight className="absolute right-4 top-1/2 -translate-y-1/2 w-4 h-4 text-neutral-400 rotate-90 pointer-events-none" />
                </div>
              </div>
            </div>

            {/* Catalog Grid Cards display */}
            {filteredProducts.length === 0 ? (
              <div className="py-24 text-center space-y-4 bg-white rounded-3xl border border-[#ecebe6]">
                <div className="p-4 rounded-full bg-neutral-50 text-neutral-300 w-16 h-16 flex items-center justify-center mx-auto">
                  <Search className="w-8 h-8 stroke-[1.2]" />
                </div>
                <div>
                  <h3 className="font-serif text-lg font-black text-charcoal-800">No encontramos resultados</h3>
                  <p className="text-xs text-neutral-450 mt-1 max-w-sm mx-auto font-light">
                    Prueba a limpiar los filtros de búsqueda o cambia de categoría para ver otros finos bolsos marroquineros.
                  </p>
                </div>
                <button
                  id="reset-filters-btn"
                  onClick={() => {
                    setSearchTerm('');
                    setSelectedCategory('Todos');
                    setSortOption('default');
                  }}
                  className="px-6 py-2.5 bg-charcoal-900 text-white rounded-full text-xs font-semibold uppercase tracking-wider hover:bg-gold-coulisse hover:text-charcoal-950 transition"
                >
                  Restaurar Filtros
                </button>
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredProducts.map((bag) => (
                  <ProductCard
                    key={bag.id}
                    product={bag}
                    onSelectProduct={handleSelectProduct}
                    onAddToCartDirect={handleAddToCartDirect}
                    isFavorite={favorites.includes(bag.id)}
                    onToggleFavorite={handleToggleFavorite}
                  />
                ))}
              </div>
            )}
          </div>
        )}

        {/* TAB 3: MUNDO PRIME (historia de la marca) */}
        {!selectedProduct && activeTab === 'prime' && (
          <MundoPrime
            onOpenAuth={() => setAuthOpen(true)}
          />
        )}
      </main>

      {/* Elegant Editorial Footer block (Vogue aesthetic) */}
      <footer id="editorial-footer" className="bg-[#121212] border-t border-charcoal-800 text-white py-10 mt-8 font-serif">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-1 md:grid-cols-12 gap-8 font-sans text-xs">
          {/* Column 1: PRIME DROP */}
          <div className="md:col-span-5 space-y-4 text-left">
            <span className="font-serif text-2xl font-black tracking-[0.25em] text-white">PRIME DROP</span>
            <p className="text-[#999] leading-relaxed font-light max-w-sm">
              Bolsos exclusivos, originales y seleccionados para elevar tu estilo diario con marcas internacionales.
            </p>
          </div>

          {/* Column 2: REDES SOCIALES */}
          <div className="md:col-span-3 text-left space-y-4">
            <h4 className="font-sans font-extrabold text-xs tracking-widest text-[#ecebe6] uppercase">REDES SOCIALES</h4>
            <div className="flex flex-wrap gap-3">
              <a
                href="mailto:primedropelite@gmail.com"
                className="w-10 h-10 rounded-full bg-charcoal-900 border border-charcoal-800 flex items-center justify-center text-neutral-300 hover:bg-white hover:text-black hover:border-white transition-all"
                title="Email"
              >
                <Mail className="w-4 h-4" />
              </a>
              <a
                href="https://instagram.com/primedrop_elite"
                target="_blank"
                rel="noreferrer"
                className="w-10 h-10 rounded-full bg-charcoal-900 border border-charcoal-800 flex items-center justify-center text-neutral-300 hover:bg-white hover:text-black hover:border-white transition-all"
                title="Instagram"
              >
                <Instagram className="w-4 h-4" />
              </a>
              <a
                href="https://tiktok.com/@primedrop_elite"
                target="_blank"
                rel="noreferrer"
                className="w-10 h-10 rounded-full bg-charcoal-900 border border-charcoal-800 flex items-center justify-center text-neutral-300 hover:bg-white hover:text-black hover:border-white transition-all"
                title="TikTok"
              >
                <svg className="w-4 h-4 fill-current" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64 2.93 2.93 0 0 1 .8.11v-3.5a6.39 6.39 0 0 0-3.32-.23c-3.1.64-5.32 3.53-5.32 6.87A6.38 6.38 0 0 0 8 22c3.5 0 6.38-2.88 6.38-6.38V7.78a8.31 8.31 0 0 0 5.21 1.74V6.69z" />
                </svg>
              </a>
              <a
                href="https://facebook.com/primedrop_elite"
                target="_blank"
                rel="noreferrer"
                className="w-10 h-10 rounded-full bg-charcoal-900 border border-charcoal-800 flex items-center justify-center text-neutral-300 hover:bg-white hover:text-black hover:border-white transition-all"
                title="Facebook"
              >
                <svg className="w-4 h-4 fill-current" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z" />
                </svg>
              </a>
            </div>
          </div>
          {/* Column 3: ÚNETE A NOSOTROS */}
          <div className="md:col-span-4 text-left space-y-4">
            <h4 className="font-sans font-extrabold text-xs tracking-widest text-[#ecebe6] uppercase">ÚNETE A NOSOTROS</h4>
            <p className="text-[#999] leading-relaxed font-light">
              Recibe ofertas exclusivas y novedades.
            </p>
            <div className="space-y-2 max-w-sm">
              <input
                id="footer-join-email"
                type="email"
                placeholder="Ingresa tu correo"
                className="w-full bg-charcoal-900 border border-charcoal-800 text-xs px-4 py-3 rounded-xl focus:outline-none focus:border-gold-coulisse focus:ring-1 focus:ring-gold-coulisse text-white"
              />
              <button
                id="footer-join-submit"
                onClick={() => {
                  const inputVal = (document.getElementById('footer-join-email') as HTMLInputElement)?.value;
                  if (inputVal && inputVal.includes('@')) {
                    triggerNotification('¡Bienvenido! Te hemos registrado para recibir drops privados.', 'gold');
                    (document.getElementById('footer-join-email') as HTMLInputElement).value = '';
                  } else {
                    triggerNotification('Por favor, ingresa un correo electrónico válido.', 'info');
                  }
                }}
                className="w-full bg-white hover:bg-neutral-200 text-black font-extrabold uppercase tracking-widest text-[10px] py-3 rounded-xl transition-all shadow-md"
              >
                REGISTRARSE
              </button>
            </div>
          </div>

        </div>

        {/* ===== POLICIES FOOTER ===== */}
        <div className="border-t border-neutral-200 pt-8 pb-10 mt-10">

          {/* Row 1 — primary policy links */}
          <div className="flex flex-wrap justify-center gap-x-6 gap-y-2 mb-4">
            {[
              { label: 'Términos de uso', key: 'terminos' },
              { label: 'Política de privacidad', key: 'privacidad' },
              { label: 'Política de devoluciones', key: 'devoluciones' },
              { label: 'Garantía de autenticidad', key: 'garantia' },
            ].map((link) => (
              <button
                key={link.key}
                onClick={() => setPolicyModal({
                  isOpen: true,
                  title: link.label,
                  content: link.key === 'terminos'
                    ? TERMS_CONTENT
                    : link.key === 'privacidad'
                    ? PRIVACY_CONTENT
                    : link.key === 'devoluciones'
                    ? REFUND_CONTENT
                    : WARRANTY_CONTENT
                })}
                className="font-serif text-[10px] sm:text-[11px] uppercase tracking-[0.15em] text-charcoal-500 hover:text-charcoal-900 transition-colors duration-200"
              >
                {link.label}
              </button>
            ))}
          </div>

          {/* Row 2 — secondary links */}
          <div className="flex flex-wrap justify-center gap-x-6 gap-y-2 mb-6">
            {[
              { label: 'Atención al cliente', key: 'atencion' },
              { label: 'Métodos de pago', key: 'pago' },
              { label: 'Envíos', key: 'envios' },
              { label: 'Protección de datos', key: 'datos' },
              { label: 'Mapa del sitio', key: 'mapa' },
            ].map((link) => (
              <button
                key={link.key}
                onClick={() => setPolicyModal({
                  isOpen: true,
                  title: link.label,
                  content: link.key === 'atencion'
                    ? 'Nuestro equipo está disponible de lunes a sábado de 8am a 7pm. Podés contactarnos por WhatsApp al 316 068 5555 o al correo primedropelite@gmail.com. Respondemos en menos de 2 horas en horario hábil.'
                    : link.key === 'pago'
                    ? 'Aceptamos pagos por Nequi, Bancolombia, Daviplata y Bold. Todos los pagos son procesados de forma segura con encriptación SSL. No guardamos información de tarjetas ni cuentas bancarias.'
                    : link.key === 'envios'
                    ? 'Realizamos envíos a todo Colombia a través de transportadoras certificadas. El tiempo de entrega es de 3 a 5 días hábiles para ciudades principales y de 5 a 8 días para municipios. El envío estándar es gratuito en compras mayores a $200.000 COP.'
                    : link.key === 'datos'
                    ? 'Cumplimos con la Ley 1581 de 2012 de Protección de Datos Personales de Colombia. Tenés derecho a conocer, actualizar, rectificar y suprimir tu información personal. Para ejercer estos derechos escribinos a primedropelite@gmail.com.'
                    : 'Inicio · Bolsos · Mundo Prime · Contacto · Políticas · Términos'
                })}
                className="font-serif text-[10px] sm:text-[11px] uppercase tracking-[0.15em] text-charcoal-500 hover:text-charcoal-900 transition-colors duration-200"
              >
                {link.label}
              </button>
            ))}
          </div>

          {/* Divider */}
          <div className="w-16 h-px bg-neutral-300 mx-auto mb-5" />

          {/* Copyright */}
          <p className="font-serif text-[10px] tracking-[0.15em] uppercase text-charcoal-400 text-center">
            © 2026 Prime Drop Elite. Todos los derechos reservados.
          </p>

        </div>
      </footer>

      {/* Cart Sidebar drawer slide-out overlay component */}
      <CartDrawer
        isOpen={cartOpen}
        onClose={() => setCartOpen(false)}
        cartItems={cart}
        onUpdateQuantity={handleUpdateCartQuantity}
        onRemoveItem={handleRemoveItem}
        onStartCheckout={handleStartCheckout}
      />

      {/* Floating WhatsApp fixed action button */}
      <a
        href="https://wa.me/573160685555"
        target="_blank"
        rel="noreferrer"
        className="fixed bottom-6 right-6 z-[55] w-14 h-14 rounded-full bg-black flex items-center justify-center text-white shadow-2xl hover:scale-110 transition-transform duration-300"
        title="WhatsApp"
      >
        <svg className="w-8 h-8 fill-current" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a12.8 12.8 0 0 0-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413Z"/>
        </svg>
      </a>

      {/* Multi-step Payment Gate & Receipt details */}
      <CheckoutFlow
        isOpen={checkoutOpen}
        onClose={() => setCheckoutOpen(false)}
        cartItems={cart}
        appliedDiscountPercent={appliedDiscountPercent}
        promoCodeUsed={promoCodeUsed}
        onOrderCompleted={handleOrderCompleted}
      />

      {/* Elegant login/register portal modal */}
      <AuthModal
        isOpen={authOpen}
        onClose={() => setAuthOpen(false)}
        onLoginSuccess={handleLoginSuccess}
        onLogout={handleLogout}
        isPrimeMember={isPrimeMember}
        currentUserEmail={currentUserEmail}
        currentUsername={currentUsername}
      />

      {/* Dynamic interactive Policies details popup dialog */}
      <AnimatePresence>
        {policyModal.isOpen && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setPolicyModal({ ...policyModal, isOpen: false })}
              className="absolute inset-0 bg-black/60 backdrop-blur-xs"
            />
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: 15 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 15 }}
              className="relative bg-[#fdfdfc] text-charcoal-900 w-full max-w-lg p-8 sm:p-10 rounded-[32px] border border-[#ecebe6] shadow-2xl space-y-6 text-left z-10"
            >
              <button
                id="close-policy-btn"
                onClick={() => setPolicyModal({ ...policyModal, isOpen: false })}
                className="absolute top-6 right-6 p-2 rounded-full hover:bg-neutral-100 transition-colors"
                aria-label="Cerrar políticas"
              >
                <X className="w-5 h-5 text-neutral-550" />
              </button>
              
              <div className="space-y-2">
                <span className="text-[10px] tracking-[0.3em] uppercase font-extrabold text-gold-600 block">Prime Drop Elite • Colombia</span>
                <h3 className="font-serif text-2xl sm:text-3xl font-black text-charcoal-950">{policyModal.title}</h3>
              </div>
              
              <div className="text-sm font-light text-charcoal-600 leading-relaxed pt-2 whitespace-pre-line max-h-[60vh] overflow-y-auto pr-2">
                {policyModal.content}
              </div>
              
              <div className="pt-4 text-right">
                <button
                  id="confirm-policy-btn"
                  onClick={() => setPolicyModal({ ...policyModal, isOpen: false })}
                  className="bg-charcoal-950 hover:bg-neutral-800 text-white text-xs font-bold tracking-widest uppercase py-3.5 px-8 rounded-full shadow-sm transition-all"
                >
                  Entendido
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
}

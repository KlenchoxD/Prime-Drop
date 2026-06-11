/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { ShoppingBag, Menu, X, Shield, Crown, User, Search, Instagram, Facebook, Heart } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';

const ROTATING_TEXTS = [
  "BOLSOS 100% ORIGINALES",
  "GARANTÍA DE AUTENTICIDAD",
  "ENVÍOS A TODA COLOMBIA | RÁPIDO Y SEGURO"
];

interface NavbarProps {
  activeTab: 'inicio' | 'bolsos' | 'prime';
  setActiveTab: (tab: 'inicio' | 'bolsos' | 'prime') => void;
  cartCount: number;
  onOpenCart: () => void;
  isPrimeMember: boolean;
  onOpenVipModal: () => void;
  onOpenAuth: () => void;
  favoriteCount: number;
  onOpenFavorites?: () => void;
  currentUserEmail?: string;
}

export default function Navbar({
  activeTab,
  setActiveTab,
  cartCount,
  onOpenCart,
  isPrimeMember,
  onOpenVipModal,
  onOpenAuth,
  favoriteCount,
  onOpenFavorites,
  currentUserEmail
}: NavbarProps) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [currentTextIndex, setCurrentTextIndex] = useState(0);
  const [isBolsosHovered, setIsBolsosHovered] = useState(false);

  React.useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTextIndex((prev) => (prev + 1) % ROTATING_TEXTS.length);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  const handleNavClick = (tab: 'inicio' | 'bolsos' | 'prime') => {
    setActiveTab(tab);
    setMobileMenuOpen(false);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <header
      id="main-navbar"
      className="absolute top-0 left-0 right-0 z-50 bg-white border-b border-[#ecebe6] shadow-xs"
    >
      {/* Top Bar - Black background with white text */}
      <div className="bg-black text-white py-2.5 px-4 sm:px-6 lg:px-8 text-[11px] font-serif flex items-center justify-between">
        <div className="hidden md:block w-1/3 text-left">
          {currentUserEmail && (
            <span className="text-neutral-300 font-semibold">{currentUserEmail}</span>
          )}
        </div>
        
        <div className="w-full md:w-1/3 text-center relative h-4 overflow-hidden flex items-center justify-center">
          <AnimatePresence mode="wait">
            <motion.span
              key={currentTextIndex}
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              exit={{ y: -20, opacity: 0 }}
              transition={{ duration: 0.5, ease: "easeInOut" }}
              className="absolute font-bold tracking-widest text-[9px] sm:text-[10px] uppercase w-full text-center"
            >
              {ROTATING_TEXTS[currentTextIndex]}
            </motion.span>
          </AnimatePresence>
        </div>

        <div className="hidden md:flex w-1/3 justify-end items-center gap-3.5">
          <span className="text-neutral-400 uppercase tracking-[0.2em] text-[10px] font-semibold">Síguenos</span>
          <div className="flex items-center gap-1">
            <a href="https://facebook.com/primedrop_elite" target="_blank" rel="noreferrer" aria-label="Facebook" className="w-8 h-8 rounded-full flex items-center justify-center text-neutral-300 hover:text-white hover:bg-white/10 transition-colors duration-200">
              <Facebook className="w-[17px] h-[17px]" strokeWidth={1.6} />
            </a>
            <a href="https://tiktok.com/@primedrop_elite" target="_blank" rel="noreferrer" aria-label="TikTok" className="w-8 h-8 rounded-full flex items-center justify-center text-neutral-300 hover:text-white hover:bg-white/10 transition-colors duration-200">
              <svg className="w-[16px] h-[16px] fill-current" viewBox="0 0 24 24" aria-hidden="true">
                <path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64 2.93 2.93 0 0 1 .8.11v-3.5a6.39 6.39 0 0 0-3.32-.23c-3.1.64-5.32 3.53-5.32 6.87A6.38 6.38 0 0 0 8 22c3.5 0 6.38-2.88 6.38-6.38V7.78a8.31 8.31 0 0 0 5.21 1.74V6.69z" />
              </svg>
            </a>
            <a href="https://instagram.com/primedrop_elite" target="_blank" rel="noreferrer" aria-label="Instagram" className="w-8 h-8 rounded-full flex items-center justify-center text-neutral-300 hover:text-white hover:bg-white/10 transition-colors duration-200">
              <Instagram className="w-[17px] h-[17px]" strokeWidth={1.6} />
            </a>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        
        {/* Top brand bar for Title and Mobile layout */}
        <div className="relative flex flex-col items-center justify-center">
          
          {/* Mobile layout handler */}
          <div className="flex md:hidden items-center justify-between h-12 w-full">
            {/* Mobile hamburger menu */}
            <button
              id="mobile-menu-toggle"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 -ml-2 text-charcoal-800 hover:text-black focus:outline-none"
              aria-label="Abrir menú"
            >
              {mobileMenuOpen ? <X className="h-6 w-6 stroke-[1.5]" /> : <Menu className="h-6 w-6 stroke-[1.5]" />}
            </button>

            {/* Mobile centered logo */}
            <button
              id="brand-logo-mobile"
              onClick={() => handleNavClick('inicio')}
              className="font-serif text-lg font-normal tracking-[0.2em] text-[#0a1128] uppercase select-none"
            >
              PRIME DROP
            </button>

            {/* Mobile cart icon */}
            <button
              id="navbar-cart-trigger-mobile"
              onClick={onOpenCart}
              className="p-2 -mr-2 text-charcoal-800 hover:text-black relative"
              aria-label="Ver bolsa"
            >
              <ShoppingBag className="h-5.5 w-5.5 stroke-[1.5]" />
              {cartCount > 0 && (
                <span className="absolute top-1 right-1 h-4 w-4 bg-black text-white text-[9px] font-bold rounded-full flex items-center justify-center">
                  {cartCount}
                </span>
              )}
            </button>
          </div>

          {/* Desktop Logo: centered beautifully at the top */}
          <div className="hidden md:block text-center mt-2 mb-4">
            <button
              id="brand-logo-desktop"
              onClick={() => handleNavClick('inicio')}
              className="focus:outline-none group"
            >
              <h1 className="font-serif text-[28px] font-light tracking-[0.3em] text-[#1a1a1a] uppercase transition-colors duration-300 group-hover:text-charcoal-500">
                PRIME DROP
              </h1>
            </button>
          </div>

          {/* Desktop Row containing Sub-navigation links centered + Right items (like cart, VIP) aligned inline */}
          <div className="hidden md:flex items-center justify-between w-full border-t border-[#f3f2ee] pt-3.5 pb-1">
            
            {/* Left side: Pure symmetrical offset placeholder matching the size of the right container */}
            <div className="w-48"></div>

            {/* Center: Main navigation links */}
            <nav className="flex items-center justify-center space-x-12">
              <button
                id="nav-link-inicio"
                onClick={() => handleNavClick('inicio')}
                className={`text-[13px] tracking-[0.1em] font-serif font-bold transition-all relative pb-2 px-1 ${
                  activeTab === 'inicio'
                    ? 'text-black border-b-[2px] border-black'
                    : 'text-neutral-700 hover:text-black'
                }`}
              >
                INICIO
              </button>
              
              <div 
                className="relative"
                onMouseEnter={() => setIsBolsosHovered(true)}
                onMouseLeave={() => setIsBolsosHovered(false)}
              >
                <button
                  id="nav-link-bolsos"
                  onClick={() => handleNavClick('bolsos')}
                  className={`text-[13px] tracking-[0.1em] font-serif font-bold transition-all relative pb-2 px-1 ${
                    activeTab === 'bolsos'
                      ? 'text-black border-b-[2px] border-black'
                      : 'text-neutral-700 hover:text-black'
                  }`}
                >
                  BOLSOS
                </button>
                <AnimatePresence>
                  {isBolsosHovered && (
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: 10 }}
                      className="absolute top-full left-1/2 -translate-x-1/2 mt-1 bg-white border border-neutral-100 shadow-xl rounded-xl py-3 px-4 w-48 z-50"
                    >
                      <div className="flex flex-col space-y-2">
                        {['Todos', 'KARL LAGERFELD', 'MICHAEL KORS', 'STEVE MADDEN', 'TOMMY HILFIGER'].map((cat) => (
                          <button
                            key={cat}
                            onClick={() => {
                              handleNavClick('bolsos');
                              // Dispatch event so App.tsx can select category (hacky but works since state is in App)
                              window.dispatchEvent(new CustomEvent('selectCategory', { detail: cat }));
                            }}
                            className="text-left text-xs font-serif text-charcoal-700 hover:text-black hover:bg-neutral-50 px-2 py-1.5 rounded transition-colors uppercase tracking-wider"
                          >
                            {cat}
                          </button>
                        ))}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>

              <button
                id="nav-link-prime"
                onClick={() => handleNavClick('prime')}
                className={`text-[13px] tracking-[0.1em] font-serif font-bold transition-all relative pb-2 px-1 flex items-center space-x-1 ${
                  activeTab === 'prime'
                    ? 'text-black border-b-[2px] border-black'
                    : 'text-neutral-700 hover:text-black'
                }`}
              >
                <span>MUNDO PRIME</span>
              </button>
            </nav>

            {/* Right side: Symmetrical container holding Cart & VIP login */}
            <div className="flex items-center justify-end space-x-4 w-48">
              
              {/* Lupa (Search) Icon */}
              <button
                onClick={() => handleNavClick('bolsos')}
                className="text-neutral-500 hover:text-black transition-colors"
                title="Buscar"
              >
                <Search className="w-5 h-5 stroke-[1.5]" />
              </button>

              {/* Favoritos */}
              <button
                id="navbar-favorites-trigger"
                onClick={onOpenFavorites}
                className="relative text-neutral-500 hover:text-black transition-colors"
                title="Mis favoritos"
                aria-label="Mis favoritos"
              >
                <Heart className="w-5 h-5 stroke-[1.5]" />
                {favoriteCount > 0 && (
                  <span className="absolute -top-2 -right-2 h-4 w-4 bg-black text-white text-[9px] font-bold rounded-full flex items-center justify-center">
                    {favoriteCount}
                  </span>
                )}
              </button>

              {/* VIP Auth / Session button - Simple silhouette */}
              <button
                id="vip-status-btn"
                onClick={onOpenAuth}
                className="flex items-center justify-center transition-colors duration-300 text-charcoal-800 hover:text-black"
                title={isPrimeMember ? "Socio VIP Activo" : "Acceso de Socios"}
              >
                {isPrimeMember ? (
                  <>
                    <Shield className="w-5 h-5 text-gold-400" />
                  </>
                ) : (
                  <>
                    <svg className="w-6 h-6 fill-current text-neutral-400" viewBox="0 0 24 24">
                      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/>
                    </svg>
                  </>
                )}
              </button>

              {/* Shopping Bag Icon with elegant count count badge */}
              <button
                id="navbar-cart-trigger"
                onClick={onOpenCart}
                className="p-1.5 h-9 w-9 rounded-full relative transition-all duration-300 hover:bg-neutral-100 text-charcoal-900"
                aria-label="Ver bolsa"
              >
                <ShoppingBag className="h-5.5 w-5.5 stroke-[1.5] mx-auto" />
                <AnimatePresence>
                  {cartCount > 0 && (
                    <motion.span
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      exit={{ scale: 0 }}
                      className="absolute -top-1 -right-1 h-4.5 w-4.5 bg-black text-white text-[9px] font-bold rounded-full flex items-center justify-center shadow-md font-sans"
                    >
                      {cartCount}
                    </motion.span>
                  )}
                </AnimatePresence>
              </button>
            </div>

          </div>

        </div>
      </div>

      {/* Mobile Menu Drawer */}
      <AnimatePresence>
        {mobileMenuOpen && (
          <motion.div
            id="mobile-navigation-drawer"
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
            className="md:hidden absolute top-full left-0 right-0 bg-white border-b border-neutral-200 shadow-2xl py-6 px-4 space-y-4"
          >
            <div className="flex flex-col space-y-3">
              <button
                id="mob-nav-inicio"
                onClick={() => handleNavClick('inicio')}
                className={`text-left py-2 px-4 rounded-lg text-sm tracking-wider uppercase font-serif font-medium ${
                  activeTab === 'inicio' ? 'bg-neutral-100 text-black font-semibold' : 'text-charcoal-700 hover:bg-neutral-50'
                }`}
              >
                Inicio
              </button>
              <button
                id="mob-nav-bolsos"
                onClick={() => handleNavClick('bolsos')}
                className={`text-left py-2 px-4 rounded-lg text-sm tracking-wider uppercase font-serif font-medium ${
                  activeTab === 'bolsos' ? 'bg-neutral-100 text-black font-semibold' : 'text-charcoal-700 hover:bg-neutral-50'
                }`}
              >
                Bolsos
              </button>
              <button
                id="mob-nav-prime"
                onClick={() => handleNavClick('prime')}
                className={`text-left py-2 px-4 rounded-lg text-sm tracking-wider uppercase font-serif font-medium flex items-center justify-between ${
                  activeTab === 'prime' ? 'bg-neutral-100 text-black font-semibold' : 'text-charcoal-700 hover:bg-neutral-50'
                }`}
              >
                <span>Mundo Prime</span>
                <span className="text-xs bg-gold-600/10 text-gold-700 px-2.5 py-0.5 rounded font-serif font-semibold">CLUB VIP</span>
              </button>
            </div>

            <div className="pt-4 border-t border-neutral-200 flex flex-col space-y-3">
              <button
                id="mob-vip-badge-btn"
                onClick={() => {
                  onOpenAuth();
                  setMobileMenuOpen(false);
                }}
                className={`flex items-center justify-center space-x-2 w-full py-2.5 rounded-lg border text-xs tracking-wider uppercase font-semibold transition-all ${
                  isPrimeMember
                    ? 'bg-neutral-900 border-neutral-900 text-white'
                    : 'border-neutral-800 text-neutral-800 hover:bg-neutral-50'
                }`}
              >
                {isPrimeMember ? (
                  <>
                    <Shield className="w-4 h-4 text-gold-400" />
                    <span>MIEMBRO GOLD ACTIVO</span>
                  </>
                ) : (
                  <>
                    <User className="w-4 h-4 text-neutral-600" />
                    <span>LOGUEARSE / REGISTRARSE</span>
                  </>
                )}
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
}

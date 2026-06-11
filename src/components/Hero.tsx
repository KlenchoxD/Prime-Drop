/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { Shield } from 'lucide-react';
import { motion } from 'motion/react';

interface HeroProps {
  onExploreProducts: () => void;
  onJoinPrime: () => void;
}

export default function Hero({ onExploreProducts, onJoinPrime }: HeroProps) {
  return (
    <>
      {/* ===== HERO SECTION — video de fondo, texto izquierda ===== */}
      <section
        id="hero-banner"
        className="relative w-full overflow-hidden h-[460px] sm:h-[520px] lg:h-[560px]"
      >
        {/* ── Video de fondo ── */}
        <video
          src="/hero-video.mp4"
          autoPlay
          loop
          muted
          playsInline
          className="absolute inset-0 w-full h-full object-cover object-center select-none"
        />

        {/* ── Overlay oscuro gradiente hacia la izquierda ── */}
        <div className="absolute inset-0 bg-gradient-to-r from-black/75 via-black/40 to-black/10" />

        {/* ── Contenido: alineado a la izquierda ── */}
        <div className="relative z-10 h-full w-full flex items-center">
          <div className="max-w-7xl mx-auto px-6 sm:px-10 lg:px-16 w-full">
            {/* Columna izquierda — máximo la mitad del ancho */}
            <div className="max-w-[520px] space-y-5">

              {/* Título principal */}
              <motion.h1
                initial={{ opacity: 0, y: 24 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.7 }}
                className="font-serif font-black text-white leading-[1.05] text-5xl sm:text-6xl lg:text-7xl"
                style={{ letterSpacing: '-0.01em' }}
              >
                Prime Drop
              </motion.h1>

              {/* Descripción */}
              <motion.p
                initial={{ opacity: 0, y: 18 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.7, delay: 0.18 }}
                className="font-serif text-white/90 leading-relaxed text-sm sm:text-base max-w-[440px]"
              >
                Armá el outfit perfecto con las mejores marcas. En PRIME DROP ELITE,
                vas a encontrar esa prenda que completará tu estilo. Vestir de lujo
                nunca fue tan fácil.
              </motion.p>

              {/* Botón VER MÁS — estilo borde blanco redondeado */}
              <motion.div
                initial={{ opacity: 0, y: 16 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.7, delay: 0.34 }}
              >
                <button
                  id="hero-explore-products-btn"
                  onClick={onExploreProducts}
                  className="mt-2 px-8 py-3 rounded-full border-2 border-white text-white font-serif font-bold uppercase tracking-widest text-xs hover:bg-white hover:text-charcoal-900 transition-all duration-300"
                >
                  VER MÁS
                </button>
              </motion.div>

            </div>
          </div>
        </div>
      </section>

      {/* ===== VISION / ABOUT SECTION ===== */}
      <section className="bg-white py-14 sm:py-20">
        <div className="max-w-6xl mx-auto px-6 sm:px-8 lg:px-12">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 md:gap-12 items-center">

            {/* Left Column */}
            <div className="flex flex-col items-center gap-8">
              <p className="text-[17px] sm:text-[18px] leading-[1.6] text-charcoal-800 tracking-tight text-center md:text-left">
                Prime Drop Elite nace con una visión clara:
                Acercar las mejores marcas del mundo a quienes
                realmente saben de estilo. Nos especializamos en
                traer prendas 100% originales, sin
                intermediarios, sin sobreprecios. Solo moda
                auténtica, exclusiva y al mejor precio.
              </p>

              {/* Logo HTML */}
              <div className="text-center select-none">
                <div className="text-[72px] sm:text-[88px] leading-[0.85] font-black text-black tracking-tighter">
                  <div>PRIME</div>
                  <div className="h-[4px] bg-black w-full my-2" />
                  <div>DROP</div>
                </div>
              </div>
            </div>

            {/* Right Column */}
            <div className="flex flex-col items-center gap-8">
              {/* Bag Image */}
              <div className="rounded-[20px] overflow-hidden shadow-md w-full max-w-[300px]">
                <img
                  src="/images/STEVEMADDEN_HANDBAGS_BPREPPY_BROWN_01.webp"
                  alt="Bolso Steve Madden Preppy Brown"
                  className="w-full h-auto object-cover block"
                />
              </div>

              {/* Bottom Texts */}
              <div className="space-y-4 text-[16px] sm:text-[17px] leading-[1.6] text-charcoal-800 tracking-tight text-center md:text-left">
                <p>
                  No somos solo una tienda de bolsos, somos el puente entre el lujo internacional y tu clóset.
                </p>
                <p>
                  En Prime Drop Elite creemos que vestir bien no debe ser un privilegio, sino una posibilidad real para quienes quieren destacar.
                </p>
              </div>
            </div>

          </div>
        </div>
      </section>

      {/* ===== BENEFITS BAR — card style matching reference ===== */}
      <section className="bg-white border-y border-neutral-200 py-0">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-2 lg:grid-cols-4 divide-x divide-neutral-200">

            {/* 1. Soporte */}
            <div className="flex flex-col items-center justify-center gap-2 py-6 px-4 hover:bg-neutral-50 transition-colors duration-200">
              <svg className="w-8 h-8 text-charcoal-700 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.3" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
              </svg>
              <span className="font-serif text-[11px] font-bold tracking-[0.12em] text-charcoal-900 uppercase text-center">
                Soporte
              </span>
              <span className="text-[10px] text-charcoal-500 font-light tracking-wide">3160685555</span>
            </div>

            {/* 2. Envíos */}
            <div className="flex flex-col items-center justify-center gap-2 py-6 px-4 hover:bg-neutral-50 transition-colors duration-200">
              <svg className="w-8 h-8 text-charcoal-700 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.3"
                  d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 01-1 1H9m4-1V8a1 1 0 011-1h2.586a1 1 0 01.707.293l3.414 3.414a1 1 0 01.293.707V16a1 1 0 01-1 1h-1m-6-1a1 1 0 001 1h1M5 17a2 2 0 104 0m-4 0a2 2 0 114 0m6 0a2 2 0 104 0m-4 0a2 2 0 114 0" />
              </svg>
              <span className="font-serif text-[11px] font-bold tracking-[0.12em] text-charcoal-900 uppercase text-center">
                Envíos a toda Colombia
              </span>
              <span className="text-[10px] text-charcoal-500 font-light tracking-wide">Rápido y seguro</span>
            </div>

            {/* 3. Garantía */}
            <div className="flex flex-col items-center justify-center gap-2 py-6 px-4 hover:bg-neutral-50 transition-colors duration-200">
              <svg className="w-8 h-8 text-charcoal-700 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.3" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span className="font-serif text-[11px] font-bold tracking-[0.12em] text-charcoal-900 uppercase text-center">
                Garantía de autenticidad
              </span>
              <span className="text-[10px] text-charcoal-500 font-light tracking-wide">Bolsos 100% originales</span>
            </div>

            {/* 4. Compras seguras */}
            <div className="flex flex-col items-center justify-center gap-2 py-6 px-4 hover:bg-neutral-50 transition-colors duration-200">
              <svg className="w-8 h-8 text-charcoal-700 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.3"
                  d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              <span className="font-serif text-[11px] font-bold tracking-[0.12em] text-charcoal-900 uppercase text-center">
                Compras seguras
              </span>
              <span className="text-[10px] text-charcoal-500 font-light tracking-wide">Supervisado por la SIC</span>
            </div>

          </div>
        </div>
      </section>
    </>
  );
}

/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { Crown, ShieldCheck, Sparkles, Truck, Gem, Globe2 } from 'lucide-react';
import { motion } from 'motion/react';

interface MundoPrimeProps {
  isPrimeMember: boolean;
  onJoinPrime: (guestName: string, guestEmail: string) => void;
  onAddCustomBagToCart: (customBagItem: any) => void;
  onOpenAuth: () => void;
}

const PILLARS = [
  {
    icon: ShieldCheck,
    title: '100% Originales',
    text: 'Cada bolso es auténtico, importado directamente de distribuidores autorizados. Sin réplicas, sin excepciones.',
  },
  {
    icon: Gem,
    title: 'Selección Curada',
    text: 'No vendemos todo. Elegimos pieza por pieza las referencias que mejor representan estilo y calidad.',
  },
  {
    icon: Truck,
    title: 'Envíos a toda Colombia',
    text: 'Despachamos con transportadoras certificadas y seguimiento de guía a cualquier ciudad del país.',
  },
  {
    icon: Globe2,
    title: 'Lujo Internacional',
    text: 'Acercamos las mejores marcas del mundo a tu clóset, sin intermediarios ni sobreprecios.',
  },
];

const STATS = [
  { value: '4', label: 'Marcas internacionales' },
  { value: '100%', label: 'Productos originales' },
  { value: '32', label: 'Departamentos cubiertos' },
  { value: '24/7', label: 'Atención por WhatsApp' },
];

const BRANDS = ['MICHAEL KORS', 'KARL LAGERFELD', 'STEVE MADDEN', 'TOMMY HILFIGER'];

export default function MundoPrime({ onOpenAuth }: MundoPrimeProps) {
  return (
    <div
      id="mundo-prime-section"
      className="bg-[#faf9f6] text-charcoal-900 min-h-screen selection:bg-gold-200 selection:text-charcoal-950 font-serif antialiased"
    >
      {/* 1. BLACK HEADER BANNER */}
      <header id="prime-header" className="bg-black py-16 sm:py-24 text-center relative overflow-hidden">
        <div className="absolute inset-0 opacity-[0.07] pointer-events-none"
          style={{ backgroundImage: 'radial-gradient(circle at 50% 0%, #ffea79 0%, transparent 60%)' }} />
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7 }}
          className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col items-center space-y-6 relative z-10"
        >
          <Crown className="w-14 h-14 sm:w-16 sm:h-16 text-gold-coulisse stroke-[1]" />
          <div className="space-y-3">
            <h1 className="font-serif text-5xl sm:text-7xl font-bold tracking-[0.15em] text-white uppercase leading-none">
              MUNDO PRIME
            </h1>
            <p className="font-serif text-xs sm:text-sm text-neutral-400 italic tracking-[2px] uppercase">
              La historia detrás de Prime Drop Elite
            </p>
          </div>
        </motion.div>
      </header>

      {/* 2. EDITORIAL INTRO */}
      <section className="py-16 sm:py-24">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-6">
          <h2 className="font-serif text-3xl sm:text-4xl font-bold text-charcoal-950 leading-tight">
            Moda auténtica, elegida para Colombia
          </h2>
          <p className="font-serif text-base sm:text-[17px] text-charcoal-700 leading-relaxed font-light">
            Prime Drop Elite nace con una visión clara: acercar las mejores marcas del mundo a quienes
            realmente saben de estilo. Nos especializamos en traer productos 100% originales de Michael Kors,
            Steve Madden, Karl Lagerfeld y Tommy Hilfiger. Sin intermediarios, sin sobreprecios. Solo moda
            auténtica, exclusiva y al mejor precio para Colombia.
          </p>
        </div>
      </section>

      {/* 3. STATS STRIP */}
      <section className="bg-black text-white py-12">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          {STATS.map((s) => (
            <div key={s.label} className="space-y-1">
              <p className="font-serif text-4xl sm:text-5xl font-black text-gold-coulisse">{s.value}</p>
              <p className="text-[11px] uppercase tracking-widest text-neutral-400 font-sans">{s.label}</p>
            </div>
          ))}
        </div>
      </section>

      {/* 4. PILLARS */}
      <section className="py-16 sm:py-24">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <span className="text-[11px] uppercase tracking-[0.25em] text-gold-600 font-bold font-sans">Nuestra promesa</span>
            <h2 className="font-serif text-3xl sm:text-4xl font-bold text-charcoal-950 mt-2">Por qué Prime Drop Elite</h2>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {PILLARS.map((p) => {
              const Icon = p.icon;
              return (
                <motion.div
                  key={p.title}
                  whileHover={{ y: -5 }}
                  className="bg-white rounded-2xl p-7 border border-neutral-150 shadow-sm space-y-4"
                >
                  <div className="w-12 h-12 rounded-full bg-charcoal-900 flex items-center justify-center">
                    <Icon className="w-6 h-6 text-gold-coulisse stroke-[1.5]" />
                  </div>
                  <h3 className="font-serif text-lg font-bold text-charcoal-950">{p.title}</h3>
                  <p className="text-sm text-charcoal-600 font-light leading-relaxed font-sans">{p.text}</p>
                </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* 5. BRANDS */}
      <section className="border-y border-neutral-200 bg-white py-12">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-8">
          <span className="text-[11px] uppercase tracking-[0.25em] text-charcoal-400 font-bold font-sans">Marcas que trabajamos</span>
          <div className="flex flex-wrap items-center justify-center gap-x-10 gap-y-4">
            {BRANDS.map((b) => (
              <span key={b} className="font-serif text-lg sm:text-2xl font-black text-charcoal-800 tracking-[0.15em]">
                {b}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* 6. CTA */}
      <section className="py-16 sm:py-24">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-black rounded-3xl p-10 sm:p-14 text-center space-y-6 relative overflow-hidden">
            <Sparkles className="w-8 h-8 text-gold-coulisse mx-auto" />
            <h2 className="font-serif text-2xl sm:text-3xl font-bold text-white leading-snug">
              Sé el primero en conocer cada nuevo drop
            </h2>
            <p className="text-sm text-neutral-400 font-light font-sans max-w-md mx-auto">
              Crea tu cuenta y recibe acceso anticipado a las nuevas colecciones, ofertas exclusivas y novedades de Prime Drop Elite.
            </p>
            <button
              onClick={onOpenAuth}
              className="inline-flex items-center gap-2 px-8 py-3.5 bg-gold-coulisse text-charcoal-950 rounded-full text-xs font-bold uppercase tracking-widest hover:bg-white transition-colors shadow-lg"
            >
              <Crown className="w-4 h-4" />
              Únete a Prime Drop
            </button>
          </div>
        </div>
      </section>
    </div>
  );
}

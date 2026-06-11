/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { Crown } from 'lucide-react';

interface MundoPrimeProps {
  isPrimeMember: boolean;
  onJoinPrime: (guestName: string, guestEmail: string) => void;
  onAddCustomBagToCart: (customBagItem: any) => void;
  onOpenAuth: () => void;
}

export default function MundoPrime({
}: MundoPrimeProps) {
  
  return (
    <div 
      id="mundo-prime-section" 
      className="bg-[#faf9f6] text-charcoal-900 min-h-screen flex flex-col justify-between selection:bg-gold-200 selection:text-charcoal-950 font-serif antialiased"
    >
      
      {/* 1. SOLID BLACK HEADER BANNER - MATCHING IMAGE 4 */}
      <header id="prime-header" className="bg-black py-16 sm:py-24 text-center relative z-10 flex flex-col items-center justify-center">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col items-center justify-center space-y-6">
          <div className="flex flex-col items-center justify-center">
            {/* Elegant luxury Crown without bulky bubble wrapper, slim gold stroke for premium boutique feel */}
            <Crown className="w-14 h-14 sm:w-16 sm:h-16 text-gold-coulisse stroke-[1] mb-2" />
          </div>
          <div className="space-y-3 flex flex-col items-center">
            <h1 id="prime-h1" className="font-serif text-5xl sm:text-7xl font-bold tracking-[0.15em] text-white uppercase leading-none">
              MUNDO PRIME
            </h1>
            <p id="prime-p" className="font-serif text-xs sm:text-sm text-neutral-400 italic tracking-[2px] uppercase">
              La historia detrás de Prime Drop Elite
            </p>
          </div>
        </div>
      </header>

      {/* 2. MAIN QUALITY CONTENT - MATCHING ELEGANT EDITORIAL CONCEPT */}
      <main id="prime-core-content" className="flex-grow py-16 sm:py-24 bg-[#faf9f6]">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 space-y-16">
          
          {/* Brand Editorial Paragraph matching layout from Image 4 */}
          <div id="brand-editorial-wrapper" className="text-center space-y-6 max-w-3xl mx-auto col-span-full">
            <h2 id="editorial-title" className="font-serif text-3xl sm:text-4.5xl font-bold text-charcoal-950 tracking-normal leading-tight">
              Moda auténtica, elegida para Colombia
            </h2>
            <p id="editorial-desc" className="font-serif text-base sm:text-[17px] text-charcoal-700 leading-relaxed font-light max-w-2xl mx-auto">
              Prime Drop Elite nace con una visión clara: Acercar las mejores marcas del mundo a quienes realmente saben de estilo. Nos especializamos en traer productos 100% originales de Michael Kors, Steve Madden y Tommy Hilfiger. Sin intermediarios, sin sobreprecios. Solo moda auténtica, exclusiva y al mejor precio para Colombia.
            </p>
          </div>

        </div>
      </main>

    </div>
  );
}

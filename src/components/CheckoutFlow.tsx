/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { X, CreditCard, ShieldCheck, Truck, CheckCircle2, Ticket, ArrowLeft, Loader2, Sparkles, AlertCircle, Printer, Download } from 'lucide-react';
import { CartItem, CustomerInfo, ShippingMethod, PaymentDetails } from '../types';
import { SHIPPING_METHODS } from '../data/products';
import { motion, AnimatePresence } from 'motion/react';
import { formatCOP } from '../utils';

interface CheckoutFlowProps {
  isOpen: boolean;
  onClose: () => void;
  cartItems: CartItem[];
  appliedDiscountPercent: number;
  promoCodeUsed: string;
  onOrderCompleted: () => void; // Clears the cart, etc.
}

export default function CheckoutFlow({
  isOpen,
  onClose,
  cartItems,
  appliedDiscountPercent,
  promoCodeUsed,
  onOrderCompleted
}: CheckoutFlowProps) {
  if (!isOpen) return null;

  const [step, setStep] = useState<1 | 2 | 3 | 4>(1);
  const [processing, setProcessing] = useState(false);

  // Form states: Customer Info
  const [customerInfo, setCustomerInfo] = useState<CustomerInfo>({
    fullName: '',
    email: '',
    phone: '',
    address: '',
    city: '',
    postalCode: '',
    country: 'Colombia'
  });
  const [infoErrors, setInfoErrors] = useState<Partial<CustomerInfo>>({});

  // Form states: Shipping selection
  const [selectedShipping, setSelectedShipping] = useState<ShippingMethod>(SHIPPING_METHODS[0]);

  // Form states: Payment Method & Card Details
  const [paymentMethod, setPaymentMethod] = useState<'Card' | 'PayPal' | 'ApplePay' | 'Crypto'>('Card');
  const [cardDetails, setCardDetails] = useState({
    name: '',
    number: '',
    expiry: '',
    cvv: ''
  });
  const [paymentErrors, setPaymentErrors] = useState<Record<string, string>>({});

  // Math totals
  const subtotal = cartItems.reduce((acc, item) => acc + item.product.price * item.quantity, 0);
  const discountAmount = (subtotal * appliedDiscountPercent) / 100;
  const deliveryCost = selectedShipping.price;
  const total = Math.max(0, subtotal - discountAmount + deliveryCost);

  // Handlers: Info inputs
  const handleInfoChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setCustomerInfo((prev) => ({ ...prev, [name]: value }));
    if (infoErrors[name as keyof CustomerInfo]) {
      setInfoErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  // Validators: Info form
  const validateInfoStep = () => {
    const errors: Partial<CustomerInfo> = {};
    if (!customerInfo.fullName.trim()) errors.fullName = 'El nombre completo es requerido';
    if (!customerInfo.email.trim() || !/\S+@\S+\.\S+/.test(customerInfo.email))
      errors.email = 'Ingrese un correo electrónico válido';
    if (!customerInfo.phone.trim()) errors.phone = 'El número de teléfono es requerido';
    if (!customerInfo.address.trim()) errors.address = 'La dirección de entrega es requerida';
    if (!customerInfo.city.trim()) errors.city = 'La ciudad es requerida';
    if (!customerInfo.postalCode.trim()) errors.postalCode = 'El código postal es requerido';

    setInfoErrors(errors);
    return Object.keys(errors).length === 0;
  };

  // Card Inputs validation and formatting
  const handleCardChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    let { name, value } = e.target;

    if (name === 'number') {
      // Format: 4444 4444 4444 4444
      value = value.replace(/\D/g, '').substring(0, 16);
      value = value.match(/.{1,4}/g)?.join(' ') || value;
    } else if (name === 'expiry') {
      // Format: MM/YY
      value = value.replace(/\D/g, '').substring(0, 4);
      if (value.length >= 2) {
        value = value.slice(0, 2) + '/' + value.slice(2);
      }
    } else if (name === 'cvv') {
      value = value.replace(/\D/g, '').substring(0, 3);
    }

    setCardDetails((prev) => ({ ...prev, [name]: value }));
    setPaymentErrors((prev) => ({ ...prev, [name]: '' }));
  };

  const validatePaymentStep = () => {
    if (paymentMethod !== 'Card') return true;

    const errors: Record<string, string> = {};
    if (!cardDetails.name.trim()) errors.name = 'Titular heraldo requerido';
    if (cardDetails.number.replace(/\s/g, '').length !== 16)
      errors.number = 'Número de tarjeta inválido (requiere 16 dígitos)';
    if (!cardDetails.expiry.includes('/') || cardDetails.expiry.length !== 5)
      errors.expiry = 'Fecha incorrecta (MM/AA)';
    if (cardDetails.cvv.length !== 3) errors.cvv = 'CVV inválido (3 dígitos)';

    setPaymentErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleNextStep = () => {
    if (step === 1 && validateInfoStep()) {
      setStep(2);
    } else if (step === 2) {
      setStep(3);
    }
  };

  const handleProcessPy = () => {
    if (!validatePaymentStep()) return;

    setProcessing(true);
    // Simulate luxury merchant payment delay
    setTimeout(() => {
      setProcessing(false);
      setStep(4);
    }, 2800);
  };

  const handleFinishAndExit = () => {
    onOrderCompleted();
    onClose();
  };

  // Determine card provider based on first digit
  const getCardType = () => {
    const num = cardDetails.number.trim();
    if (num.startsWith('4')) return 'Visa';
    if (num.startsWith('5')) return 'Mastercard';
    if (num.startsWith('3')) return 'American Express';
    return 'Premium Elite Gold';
  };

  const generatedTrackingId = `PRIME-ES-2026-${Math.floor(100000 + Math.random() * 900000)}`;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-charcoal-900/70 backdrop-blur-md overflow-y-auto">
      
      {/* Container Card */}
      <div className="bg-white rounded-3xl w-full max-w-4xl shadow-2xl relative grid grid-cols-1 lg:grid-cols-12 overflow-hidden max-h-[92vh]">
        
        {/* Close Button top-right (unless on step 4 recipe screen) */}
        {step !== 4 && (
          <button
            id="close-checkout"
            onClick={onClose}
            className="absolute top-5 right-5 z-20 p-2. rounded-full bg-neutral-100 hover:bg-neutral-200 text-charcoal-700 transition"
          >
            <X className="w-5 h-5" />
          </button>
        )}

        {/* Left Side: Dynamic steps progress info & Cart preview */}
        <div className="lg:col-span-5 bg-charcoal-950 p-6 sm:p-8 text-white flex flex-col justify-between border-r border-charcoal-800">
          <div className="space-y-6">
            <div className="flex items-center space-x-1">
              <span className="font-serif text-xl tracking-[0.25em] font-extrabold text-white">PRIME</span>
              <span className="text-[9px] tracking-widest font-light text-gold-coulisse uppercase bg-gold-400/10 px-1.5 py-0.5 rounded border border-gold-400/25">SECURE PAY</span>
            </div>

            {/* Steps Progress Visualizer */}
            {step < 4 ? (
              <div className="space-y-4 pt-4">
                {[
                  { n: 1, label: 'Datos de Despacho' },
                  { n: 2, label: 'Distribución & Courier' },
                  { n: 3, label: 'Suscripción de Fondos' }
                ].map((s) => (
                  <div key={s.n} className="flex items-center space-x-3.5">
                    <div
                      className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold font-sans transition-all duration-300 ${
                        step === s.n
                          ? 'bg-gold-coulisse text-charcoal-950 ring-4 ring-gold-coulisse/20 scale-110'
                          : step > s.n
                          ? 'bg-green-600 text-white'
                          : 'bg-charcoal-800 text-charcoal-400'
                      }`}
                    >
                      {step > s.n ? '✓' : s.n}
                    </div>
                    <span
                      className={`text-xs uppercase tracking-wider font-semibold transition-colors duration-300 ${
                        step === s.n ? 'text-gold-200 font-bold' : 'text-charcoal-450'
                      }`}
                    >
                      {s.label}
                    </span>
                  </div>
                ))}
              </div>
            ) : (
              <div id="recipe-success-visual" className="pt-6 text-center space-y-3 bg-gold-500/10 p-5 rounded-2xl border border-gold-500/20">
                <CheckCircle2 className="w-12 h-12 text-gold-coulisse mx-auto animate-bounce" />
                <div>
                  <h4 className="font-serif font-black text-gold-300 tracking-wider">COMPRA CON PALCO ROYAL</h4>
                  <p className="text-[10px] text-charcoal-350">Acreditación aprobada por Maison Madrid</p>
                </div>
              </div>
            )}

            {/* Cart overview mini invoice list */}
            <div className="pt-6 border-t border-charcoal-800 space-y-4">
              <h5 className="text-[10px] text-charcoal-400 uppercase tracking-widest font-bold">Resumen del Pedido</h5>
              <div className="space-y-3.5 max-h-[160px] overflow-y-auto pr-2">
                {cartItems.map((item) => (
                  <div key={item.id} className="flex items-center justify-between text-xs font-sans">
                    <div className="flex items-center space-x-2.5">
                      <div className="w-8 h-10 bg-charcoal-900 rounded overflow-hidden flex-shrink-0">
                        <img src={item.product.primaryImage} className="w-full h-full object-cover" referrerPolicy="no-referrer" />
                      </div>
                      <div>
                        <p className="font-serif font-bold text-white max-w-[120px] truncate">{item.product.name}</p>
                        <p className="text-[9px] text-[#999]">Piel {item.selectedColor.name} • {item.quantity} ud.</p>
                      </div>
                    </div>
                    <span className="font-semibold text-charcoal-200 font-sans">{formatCOP(item.product.price * item.quantity)}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Checkout Totals Math Box */}
          <div className="pt-6 border-t border-charcoal-800 space-y-2">
            <div className="flex justify-between text-xs text-charcoal-400 font-sans">
              <span>Subtotal:</span>
              <span>{formatCOP(subtotal)}</span>
            </div>
            {appliedDiscountPercent > 0 && (
              <div className="flex justify-between text-xs text-red-400 font-semibold font-sans">
                <span>Descuento ({appliedDiscountPercent}%):</span>
                <span>-{formatCOP(discountAmount)}</span>
              </div>
            )}
            <div className="flex justify-between text-xs text-charcoal-400 font-sans">
              <span>Entrega ({selectedShipping.name}):</span>
              <span>{deliveryCost === 0 ? 'Gratis' : formatCOP(deliveryCost)}</span>
            </div>
            <div className="flex justify-between text-sm pt-2.5 border-t border-charcoal-800 text-white font-serif font-black">
              <span>Total Final:</span>
              <span className="text-base text-gold-coulisse">{formatCOP(total)}</span>
            </div>
          </div>
        </div>

        {/* Right Side: Step Contents */}
        <div className="lg:col-span-7 p-6 sm:p-8 flex flex-col justify-between overflow-y-auto max-h-[92vh] bg-white">
          
          <AnimatePresence mode="wait">
            
            {/* Step 1: Customer Details */}
            {step === 1 && (
              <motion.div
                key="step1"
                initial={{ opacity: 0, x: 15 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -15 }}
                className="space-y-6"
              >
                <div>
                  <h3 className="font-serif text-lg font-bold text-charcoal-900 uppercase tracking-wider">1. Datos de Despacho Postal</h3>
                  <p className="text-xs text-neutral-500">Ingrese la dirección exacta donde nuestro courier de guante blanco entregará.</p>
                </div>

                <div className="space-y-3">
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    <div className="space-y-1">
                      <label id="full-name-field" className="block text-[10px] uppercase font-bold text-charcoal-700">Nombre Completo</label>
                      <input
                        type="text"
                        name="fullName"
                        value={customerInfo.fullName}
                        onChange={handleInfoChange}
                        className={`w-full text-xs py-3 px-4 border rounded-xl focus:outline-none focus:ring-1 focus:ring-gold-coulisse ${
                          infoErrors.fullName ? 'border-red-500 bg-red-50/20' : 'border-neutral-250 bg-neutral-50/50'
                        }`}
                        placeholder="Ej. Manuel Benitez"
                      />
                      {infoErrors.fullName && <p className="text-[10px] text-red-500">{infoErrors.fullName}</p>}
                    </div>

                    <div className="space-y-1">
                      <label id="email-field" className="block text-[10px] uppercase font-bold text-charcoal-700">Correo Electrónico</label>
                      <input
                        type="email"
                        name="email"
                        value={customerInfo.email}
                        onChange={handleInfoChange}
                        className={`w-full text-xs py-3 px-4 border rounded-xl focus:outline-none focus:ring-1 focus:ring-gold-coulisse ${
                          infoErrors.email ? 'border-red-500 bg-red-50/20' : 'border-neutral-250 bg-neutral-50/50'
                        }`}
                        placeholder="manuel@gmail.com"
                      />
                      {infoErrors.email && <p className="text-[10px] text-red-500">{infoErrors.email}</p>}
                    </div>
                  </div>

                  <div className="space-y-1">
                    <label id="phone-field" className="block text-[10px] uppercase font-bold text-charcoal-700">Teléfono de Contacto (SMS Courier)</label>
                    <input
                      type="text"
                      name="phone"
                      value={customerInfo.phone}
                      onChange={handleInfoChange}
                      className={`w-full text-xs py-3 px-4 border rounded-xl focus:outline-none focus:ring-1 focus:ring-gold-coulisse ${
                        infoErrors.phone ? 'border-red-500 bg-red-50/20' : 'border-neutral-250 bg-neutral-50/50'
                      }`}
                      placeholder="+34 600 000 000"
                    />
                    {infoErrors.phone && <p className="text-[10px] text-red-500">{infoErrors.phone}</p>}
                  </div>

                  <div className="space-y-1">
                    <label id="address-field" className="block text-[10px] uppercase font-bold text-charcoal-700">Dirección y Piso</label>
                    <input
                      type="text"
                      name="address"
                      value={customerInfo.address}
                      onChange={handleInfoChange}
                      className={`w-full text-xs py-3 px-4 border rounded-xl focus:outline-none focus:ring-1 focus:ring-gold-coulisse ${
                        infoErrors.address ? 'border-red-500 bg-red-50/20' : 'border-neutral-250 bg-neutral-50/50'
                      }`}
                      placeholder="Calle Gran Vía 42, Piso 4B"
                    />
                    {infoErrors.address && <p className="text-[10px] text-red-500">{infoErrors.address}</p>}
                  </div>

                  <div className="grid grid-cols-2 gap-3">
                    <div className="space-y-1">
                      <label id="city-field" className="block text-[10px] uppercase font-bold text-charcoal-700">Ciudad</label>
                      <input
                        type="text"
                        name="city"
                        value={customerInfo.city}
                        onChange={handleInfoChange}
                        className={`w-full text-xs py-3 px-4 border rounded-xl focus:outline-none focus:ring-1 focus:ring-gold-coulisse ${
                          infoErrors.city ? 'border-red-500 bg-red-50/20' : 'border-neutral-250 bg-neutral-50/50'
                        }`}
                        placeholder="Madrid"
                      />
                      {infoErrors.city && <p className="text-[10px] text-red-500">{infoErrors.city}</p>}
                    </div>

                    <div className="space-y-1">
                      <label id="postal-code-field" className="block text-[10px] uppercase font-bold text-charcoal-700">Código Postal</label>
                      <input
                        type="text"
                        name="postalCode"
                        value={customerInfo.postalCode}
                        onChange={handleInfoChange}
                        className={`w-full text-xs py-3 px-4 border rounded-xl focus:outline-none focus:ring-1 focus:ring-gold-coulisse ${
                          infoErrors.postalCode ? 'border-red-500 bg-red-50/20' : 'border-neutral-250 bg-neutral-50/50'
                        }`}
                        placeholder="28013"
                      />
                      {infoErrors.postalCode && <p className="text-[10px] text-red-500">{infoErrors.postalCode}</p>}
                    </div>
                  </div>
                </div>

                <div className="pt-6 border-t border-neutral-100 flex justify-end">
                  <button
                    id="info-step-submit"
                    onClick={handleNextStep}
                    className="px-8 py-3 bg-charcoal-900 hover:bg-gold-coulisse hover:text-charcoal-950 text-white rounded-full text-xs uppercase tracking-widest font-semibold flex items-center space-x-2 transition-all shadow-md"
                  >
                    <span>Continuar al Envío</span>
                    <Truck className="w-4 h-4" />
                  </button>
                </div>
              </motion.div>
            )}

            {/* Step 2: Courier & Shipping selection */}
            {step === 2 && (
              <motion.div
                key="step2"
                initial={{ opacity: 0, x: 15 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -15 }}
                className="space-y-6"
              >
                <div>
                  <h3 className="font-serif text-lg font-bold text-charcoal-900 uppercase tracking-wider">2. Distribución y Courier Premium</h3>
                  <p className="text-xs text-neutral-500">Ofrecemos empaques acondicionados térmicamente para resguardar las finas carteras marroquineras.</p>
                </div>

                <div className="space-y-3">
                  {SHIPPING_METHODS.map((method) => {
                    const isSelected = selectedShipping.id === method.id;
                    return (
                      <button
                        id={`shipping-option-${method.id}`}
                        key={method.id}
                        onClick={() => setSelectedShipping(method)}
                        className={`w-full text-left p-4 rounded-2xl border flex items-start justify-between transition-all ${
                          isSelected
                            ? 'border-gold-coulisse bg-gold-50/15 ring-1 ring-gold-coulisse shadow-sm'
                            : 'border-neutral-200 hover:bg-neutral-50/50'
                        }`}
                      >
                        <div className="flex items-start space-x-3 max-w-[80%]">
                          <input
                            type="radio"
                            checked={isSelected}
                            onChange={() => setSelectedShipping(method)}
                            className="mt-1 accent-gold-coulisse h-4 w-4"
                          />
                          <div>
                            <p className="font-serif font-extrabold text-sm text-charcoal-900 uppercase tracking-wide">{method.name}</p>
                            <p className="text-xs text-[#666] font-light mt-0.5 leading-relaxed">{method.description}</p>
                            <span className="text-[10px] bg-charcoal-900/10 text-charcoal-700 font-semibold uppercase px-2 py-0.5 rounded mt-1.5 inline-block font-mono">
                              Estimado: {method.estimatedDays}
                            </span>
                          </div>
                        </div>
                        <span className="font-serif font-black text-sm text-charcoal-950 flex-shrink-0">
                          {method.price === 0 ? 'GRATIS' : formatCOP(method.price)}
                        </span>
                      </button>
                    );
                  })}
                </div>

                <div className="pt-6 border-t border-neutral-100 flex justify-between items-center">
                  <button
                    id="back-to-info-step"
                    onClick={() => setStep(1)}
                    className="flex items-center space-x-1.5 text-xs uppercase tracking-wider text-charcoal-500 font-bold hover:text-charcoal-900"
                  >
                    <ArrowLeft className="w-4 h-4" />
                    <span>Volver</span>
                  </button>

                  <button
                    id="shipping-step-submit"
                    onClick={handleNextStep}
                    className="px-8 py-3 bg-charcoal-900 hover:bg-gold-coulisse hover:text-charcoal-950 text-white rounded-full text-xs uppercase tracking-widest font-semibold flex items-center space-x-2 transition-all shadow-md"
                  >
                    <span>Proceder al Pago</span>
                    <CreditCard className="w-4 h-4" />
                  </button>
                </div>
              </motion.div>
            )}

            {/* Step 3: Payment Method with LIVE CARD GRAPHIC */}
            {step === 3 && (
              <motion.div
                key="step3"
                initial={{ opacity: 0, x: 15 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -15 }}
                className="space-y-6"
              >
                <div>
                  <h3 className="font-serif text-lg font-bold text-charcoal-900 uppercase tracking-wider">3. Acreditación de Fondos</h3>
                  <p className="text-xs text-neutral-500">Su pago se transfiere bajo encriptación SSL de grado bancario militar de 256 bits.</p>
                </div>

                {/* Tab switch of custom payment channels */}
                <div className="grid grid-cols-4 gap-2 border-b border-neutral-100 pb-3">
                  {[
                    { key: 'Card', label: 'T. Crédito' },
                    { key: 'PayPal', label: 'PayPal' },
                    { key: 'ApplePay', label: 'Apple Pay' },
                    { key: 'Crypto', label: 'Crypto' }
                  ].map((p) => (
                    <button
                      id={`pay-method-${p.key}`}
                      key={p.key}
                      onClick={() => setPaymentMethod(p.key as any)}
                      className={`py-2 px-1 text-center border rounded-xl text-xs font-semibold uppercase tracking-wider transition-all ${
                        paymentMethod === p.key
                          ? 'bg-charcoal-900 text-white border-charcoal-900 shadow-sm'
                          : 'border-neutral-200 text-charcoal-500 hover:bg-neutral-50'
                      }`}
                    >
                      {p.label}
                    </button>
                  ))}
                </div>

                {/* Render corresponding form */}
                {paymentMethod === 'Card' ? (
                  <div className="space-y-4">
                    
                    {/* LIVE SIMULATED CREDIT CARD COMPONENT (Mind-blowing visual touch) */}
                    <motion.div
                      id="card-simulator-graphic"
                      whileHover={{ scale: 1.02 }}
                      className="aspect-[1.58/1] w-full max-w-sm mx-auto rounded-2xl bg-gradient-to-tr from-charcoal-950 via-charcoal-900 to-[#1e140d] p-5 text-white flex flex-col justify-between shadow-xl relative overflow-hidden border border-charcoal-800"
                    >
                      {/* Gold card chip and antenna lines */}
                      <div className="flex items-start justify-between">
                        <div className="space-y-3">
                          <div className="w-10 h-8 rounded bg-gradient-to-tr from-[#FFD700] via-[#ffd700]/70 to-[#DAA520] border border-[#d4af37]/60 relative overflow-hidden flex items-center justify-center">
                            <span className="text-[5px] text-charcoal-800 font-mono">EMV CHIP</span>
                          </div>
                          <span className="text-[7px] uppercase tracking-[0.25em] font-sans text-gold-200 font-bold block">
                            {getCardType()}
                          </span>
                        </div>
                        <span className="font-serif text-lg font-black italic text-gold-coulisse tracking-widest uppercase">
                          PRIME
                        </span>
                      </div>

                      {/* Hard stamped number fields */}
                      <div className="py-2">
                        <p className="font-mono text-base sm:text-lg text-gold-100 tracking-widest text-center shadow-xs">
                          {cardDetails.number || '•••• •••• •••• ••••'}
                        </p>
                      </div>

                      {/* Expiry and holder names */}
                      <div className="flex justify-between items-end">
                        <div className="space-y-0.5">
                          <span className="text-[8px] uppercase tracking-wider text-charcoal-400 font-sans">Socio Credencial</span>
                          <p className="font-sans font-bold text-[11px] truncate w-40 tracking-wider text-white uppercase">
                            {cardDetails.name || 'MANUEL BENITEZ'}
                          </p>
                        </div>
                        <div className="space-y-0.5 text-right flex-shrink-0">
                          <span className="text-[8px] uppercase tracking-wider text-charcoal-400 font-sans block">Caducidad</span>
                          <p className="font-mono text-[11px] text-white">
                            {cardDetails.expiry || 'MM/AA'}
                          </p>
                        </div>
                      </div>

                      {/* Luxury gold circle background graphics */}
                      <div className="absolute top-1/2 -right-12 w-32 h-32 border border-gold-400/5 rounded-full pointer-events-none" />
                      <div className="absolute top-1/4 -right-12 w-20 h-20 bg-gold-400/5 rounded-full pointer-events-none" />
                    </motion.div>

                    {/* Inputs panel for the Card */}
                    <div className="space-y-3">
                      <div className="space-y-1">
                        <label id="card-holder-label" className="block text-[10px] uppercase font-bold text-charcoal-700">Titular de la Tarjeta</label>
                        <input
                          type="text"
                          name="name"
                          value={cardDetails.name}
                          onChange={handleCardChange}
                          className={`w-full text-xs py-3 px-4 border rounded-xl focus:outline-none focus:ring-1 focus:ring-gold-coulisse ${
                            paymentErrors.name ? 'border-red-500 bg-red-50/20' : 'border-neutral-250 bg-neutral-50/50'
                          }`}
                          placeholder="Ej. Manuel Benitez"
                        />
                        {paymentErrors.name && <p className="text-[10px] text-red-500">{paymentErrors.name}</p>}
                      </div>

                      <div className="space-y-1">
                        <label id="card-num-label" className="block text-[10px] uppercase font-bold text-charcoal-700">Número de la Tarjeta (Sin Guiones)</label>
                        <input
                          type="text"
                          name="number"
                          value={cardDetails.number}
                          onChange={handleCardChange}
                          className={`w-full text-xs py-3 px-4 border rounded-xl focus:outline-none focus:ring-1 focus:ring-gold-coulisse font-mono tracking-wider ${
                            paymentErrors.number ? 'border-red-500 bg-red-50/20' : 'border-neutral-250 bg-neutral-50/50'
                          }`}
                          placeholder="4540 1200 4500 8900"
                        />
                        {paymentErrors.number && <p className="text-[10px] text-red-500">{paymentErrors.number}</p>}
                      </div>

                      <div className="grid grid-cols-2 gap-3">
                        <div className="space-y-1">
                          <label id="card-expiry-label" className="block text-[10px] uppercase font-bold text-charcoal-700">Vencimiento</label>
                          <input
                            type="text"
                            name="expiry"
                            value={cardDetails.expiry}
                            onChange={handleCardChange}
                            maxLength={5}
                            className={`w-full text-xs py-3 px-4 border rounded-xl focus:outline-none focus:ring-1 focus:ring-gold-coulisse font-mono ${
                              paymentErrors.expiry ? 'border-red-500 bg-red-50/20' : 'border-neutral-250 bg-neutral-50/50'
                            }`}
                            placeholder="MM/AA"
                          />
                          {paymentErrors.expiry && <p className="text-[10px] text-red-500">{paymentErrors.expiry}</p>}
                        </div>

                        <div className="space-y-1">
                          <label id="card-cvv-label" className="block text-[10px] uppercase font-bold text-charcoal-700">CVV / Firma posterior</label>
                          <input
                            type="password"
                            name="cvv"
                            value={cardDetails.cvv}
                            onChange={handleCardChange}
                            maxLength={3}
                            className={`w-full text-xs py-3 px-4 border rounded-xl focus:outline-none focus:ring-1 focus:ring-gold-coulisse font-mono ${
                              paymentErrors.cvv ? 'border-red-500 bg-red-50/20' : 'border-neutral-250 bg-neutral-50/50'
                            }`}
                            placeholder="3 dígitos"
                          />
                          {paymentErrors.cvv && <p className="text-[10px] text-red-500">{paymentErrors.cvv}</p>}
                        </div>
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="py-12 text-center space-y-4 bg-neutral-50 rounded-2xl border border-neutral-150 p-6">
                    <CheckCircle2 className="w-10 h-10 text-green-600 mx-auto" />
                    <div>
                      <h4 className="font-serif font-black text-charcoal-900">Método de terceros: {paymentMethod}</h4>
                      <p className="text-xs text-[#777] max-w-sm mx-auto leading-relaxed">
                        Al pulsar "Confirmar pedido", abriremos de forma segura el pop-up de acreditación certificado de {paymentMethod}.
                      </p>
                    </div>
                  </div>
                )}

                {/* Security badges */}
                <div className="bg-green-50/40 p-4 rounded-xl border border-green-200/50 text-xs flex items-start space-x-3 text-charcoal-700 font-sans leading-relaxed">
                  <ShieldCheck className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                  <div>
                    <strong>Pago de Encriptación Segura:</strong> Sus credenciales se procesan como un Hash tokenizado directo y nunca se registran en repositorios físicos.
                  </div>
                </div>

                {/* Back / Pay Actions Buttons */}
                <div className="pt-6 border-t border-neutral-100 flex justify-between items-center">
                  <button
                    id="back-to-shipping-step"
                    onClick={() => setStep(2)}
                    className="flex items-center space-x-1.5 text-xs uppercase tracking-wider text-charcoal-500 font-bold hover:text-charcoal-900"
                  >
                    <ArrowLeft className="w-4 h-4" />
                    <span>Volver</span>
                  </button>

                  <button
                    id="trigger-payment-btn"
                    onClick={handleProcessPy}
                    disabled={processing}
                    className="group px-8 py-3.5 bg-charcoal-900 hover:bg-gold-coulisse hover:text-charcoal-950 text-white rounded-full text-xs uppercase tracking-widest font-semibold flex items-center justify-center space-x-2 transition-all shadow-md min-w-[160px]"
                  >
                    {processing ? (
                      <>
                        <Loader2 className="w-4.5 h-4.5 animate-spin" />
                        <span>Acreditando...</span>
                      </>
                    ) : (
                      <>
                        <span>Confirmar & Pagar {formatCOP(total)}</span>
                        <ArrowLeft className="w-4 h-4 transform rotate-180" />
                      </>
                    )}
                  </button>
                </div>
              </motion.div>
            )}

            {/* Step 4: Invoice Receipt Success Screen */}
            {step === 4 && (
              <motion.div
                key="step4"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="space-y-6 pt-2 text-center"
              >
                <div className="space-y-2">
                  <span className="bg-gold-500/10 border border-gold-400/30 text-gold-600 text-[10px] font-bold tracking-widest uppercase px-3.5 py-1.5 rounded-full inline-block font-sans">
                    ★ ADQUISICIÓN CONFIRMADA DE ARCHIVO
                  </span>
                  <h3 className="font-serif text-2xl font-extrabold text-charcoal-950">¡Gracias por su Compra, Excelencia!</h3>
                  <p className="text-xs text-neutral-500 max-w-sm mx-auto">
                    Su pedido ha sido asignado al despachador. Se despachará de inmediato según la agenda establecida.
                  </p>
                </div>

                {/* Printable Invoice detail sheet (factura) */}
                <div className="border border-neutral-250 rounded-2xl bg-[#fafafa] p-5 text-left text-xs font-sans space-y-4 shadow-sm relative">
                  {/* Decorative stamp decoration */}
                  <div className="absolute top-4 right-4 border-2 border-dashed border-gold-coulisse/50 rounded-full px-2.5 py-1 text-[8px] font-mono font-bold tracking-widest text-gold-600 uppercase select-none opacity-55">
                    Maison Aprobado
                  </div>

                  <div className="border-b border-neutral-200 pb-3 space-y-1">
                    <p className="text-neutral-400 font-semibold uppercase text-[9px] tracking-wider">Maison Factura No.</p>
                    <p className="font-bold text-charcoal-800 text-[11px]">{generatedTrackingId}</p>
                    <div className="flex justify-between text-[10px] text-neutral-500 pt-1">
                      <span>Emisor: PRIME DROP SL, Madrid</span>
                      <span>Fecha: {new Date().toLocaleDateString('es-ES')}</span>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <p className="font-bold text-charcoal-800 text-[10px] uppercase tracking-wider">Detalles de Entrega:</p>
                    <div className="text-neutral-500 text-[11px] space-y-0.5 font-light">
                      <p><strong className="font-medium text-charcoal-800">Destinatario:</strong> {customerInfo.fullName}</p>
                      <p><strong className="font-medium text-charcoal-800">Dirección:</strong> {customerInfo.address}, {customerInfo.city}, {customerInfo.postalCode}</p>
                      <p><strong className="font-medium text-charcoal-800">Método de Envío:</strong> {selectedShipping.name}</p>
                    </div>
                  </div>

                  <div className="border-t border-neutral-200 pt-3 flex justify-between items-center text-charcoal-900 font-serif">
                    <span className="font-medium uppercase text-[10px] tracking-wider">Monto Total Acreditado:</span>
                    <strong className="font-black text-sm text-gold-700">{formatCOP(total)}</strong>
                  </div>
                </div>

                {/* Tracking status visualizer bar */}
                <div className="bg-[#121212] rounded-xl p-4 text-left border border-neutral-800">
                  <div className="flex justify-between text-[9px] text-charcoal-400 uppercase tracking-widest font-bold">
                    <span>Estado del Tránsito Courier</span>
                    <span className="text-gold-200">{selectedShipping.price === 0 ? 'DESPACHO PRIORITARIO' : 'EXPRESS DE GUANTE BLANCO'}</span>
                  </div>
                  <div className="flex items-center space-x-2.5 mt-3.5">
                    <span className="relative flex h-2 w-2">
                      <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-gold-400 opacity-75"></span>
                      <span className="relative inline-flex rounded-full h-2 w-2 bg-gold-coulisse"></span>
                    </span>
                    <p className="text-xs text-white font-medium">Asignando Courier en Central de Madrid...</p>
                  </div>
                  <p className="text-[10px] text-charcoal-400 mt-2">
                    Código de Rastreo: <strong className="font-mono text-white text-[11px]">{generatedTrackingId}</strong>
                  </p>
                </div>

                {/* Print bill / Continue shopping buttons */}
                <div className="flex flex-col sm:flex-row gap-3 pt-4">
                  <button
                    id="on-print-recipe"
                    onClick={() => window.print()}
                    className="flex-1 py-3 px-4 rounded-xl border border-neutral-200 font-semibold text-xs uppercase tracking-wider text-charcoal-700 hover:bg-neutral-50 flex items-center justify-center space-x-1.5"
                  >
                    <Printer className="w-4 h-4" />
                    <span>Imprimir Recibo de Compra</span>
                  </button>

                  <button
                    id="finish-checkout-btn"
                    onClick={handleFinishAndExit}
                    className="flex-1 py-3 px-4 rounded-xl bg-charcoal-900 hover:bg-gold-coulisse hover:text-charcoal-950 text-white font-semibold text-xs uppercase tracking-wider leading-relaxed flex items-center justify-center space-x-1.5 shadow-md"
                  >
                    <span>Volver a la Tienda</span>
                  </button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
}

/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo } from 'react';
import { X, ShieldCheck, Truck, CheckCircle2, ArrowLeft, Loader2, Printer, MessageCircle, ExternalLink, MapPin, CreditCard, Building2, Wallet } from 'lucide-react';
import { CartItem, CustomerInfo, ShippingMethod, PaymentMethodKey } from '../types';
import { SHIPPING_METHODS } from '../data/products';
import { COLOMBIA_DEPARTMENTS, COLOMBIA_LOCATIONS } from '../data/colombia';
import { PAYMENT_METHODS, PAYMENT_CONFIG, PSE_BANKS } from '../data/payment';
import { BACKEND_ENABLED, apiCreateOrder } from '../lib/api';
import { REFUND_CONTENT, TERMS_CONTENT } from '../data/policies';
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
    department: '',
    city: '',
    notes: '',
    country: 'Colombia'
  });
  const [infoErrors, setInfoErrors] = useState<Record<string, string>>({});

  // Form states: Shipping selection
  const [selectedShipping, setSelectedShipping] = useState<ShippingMethod>(SHIPPING_METHODS[0]);

  // Form states: Payment Method
  const [paymentMethod, setPaymentMethod] = useState<PaymentMethodKey>('Wompi');
  const [pseBank, setPseBank] = useState('');
  const [paymentErrors, setPaymentErrors] = useState<Record<string, string>>({});
  const [acceptedTerms, setAcceptedTerms] = useState(false);
  const [policyView, setPolicyView] = useState<'terms' | 'refund' | null>(null);

  // Cities available for the selected department
  const availableCities = useMemo(
    () => (customerInfo.department ? COLOMBIA_LOCATIONS[customerInfo.department] || [] : []),
    [customerInfo.department]
  );

  // Math totals
  const subtotal = cartItems.reduce((acc, item) => acc + item.product.price * item.quantity, 0);
  const discountAmount = (subtotal * appliedDiscountPercent) / 100;
  const deliveryCost = selectedShipping.price;
  const total = Math.max(0, subtotal - discountAmount + deliveryCost);

  const localOrderId = useMemo(
    () => `PRIME-CO-2026-${Math.floor(100000 + Math.random() * 900000)}`,
    []
  );
  // Código de pedido mostrado (lo reemplaza el backend si está activo)
  const [generatedOrderId, setGeneratedOrderId] = useState(localOrderId);

  // Handlers: Info inputs
  const handleInfoChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setCustomerInfo((prev) => {
      // Reset city if department changes
      if (name === 'department') {
        return { ...prev, department: value, city: '' };
      }
      return { ...prev, [name]: value };
    });
    if (infoErrors[name]) {
      setInfoErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  // Validators: Info form
  const validateInfoStep = () => {
    const errors: Record<string, string> = {};
    if (!customerInfo.fullName.trim()) errors.fullName = 'El nombre completo es requerido';
    if (!customerInfo.email.trim() || !/\S+@\S+\.\S+/.test(customerInfo.email))
      errors.email = 'Ingresa un correo electrónico válido';
    if (!/^\d{10}$/.test(customerInfo.phone.replace(/\D/g, '')))
      errors.phone = 'Ingresa un celular válido de 10 dígitos';
    if (!customerInfo.address.trim()) errors.address = 'La dirección de entrega es requerida';
    if (!customerInfo.department) errors.department = 'Selecciona tu departamento';
    if (!customerInfo.city) errors.city = 'Selecciona tu ciudad o municipio';

    setInfoErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const validatePaymentStep = () => {
    const errors: Record<string, string> = {};
    if (paymentMethod === 'PSE' && !pseBank) {
      errors.pseBank = 'Selecciona tu banco para continuar con PSE';
    }
    if (!acceptedTerms) {
      errors.terms = 'Debes aceptar los términos y la política de reembolso para continuar.';
    }
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

  // Build a readable WhatsApp order message
  const buildWhatsappMessage = () => {
    const lines = cartItems
      .map(
        (item) =>
          `• ${item.product.name} (${item.selectedColor.name}) x${item.quantity} — ${formatCOP(
            item.product.price * item.quantity
          )}`
      )
      .join('\n');

    const msg =
      `¡Hola Prime Drop Elite! 🛍️\n\n` +
      `Quiero confirmar mi pedido *${generatedOrderId}*:\n\n${lines}\n\n` +
      `Subtotal: ${formatCOP(subtotal)}\n` +
      (appliedDiscountPercent > 0 ? `Descuento (${appliedDiscountPercent}%): -${formatCOP(discountAmount)}\n` : '') +
      `Envío (${selectedShipping.name}): ${deliveryCost === 0 ? 'Gratis' : formatCOP(deliveryCost)}\n` +
      `*Total: ${formatCOP(total)}*\n\n` +
      `Método de pago: ${paymentMethod}${paymentMethod === 'PSE' && pseBank ? ` (${pseBank})` : ''}\n\n` +
      `*Datos de envío:*\n` +
      `${customerInfo.fullName}\n` +
      `${customerInfo.address}\n` +
      `${customerInfo.city}, ${customerInfo.department}\n` +
      `Cel: ${customerInfo.phone}\n` +
      (customerInfo.notes ? `Notas: ${customerInfo.notes}\n` : '');

    return encodeURIComponent(msg);
  };

  const openWhatsapp = () => {
    const url = `https://wa.me/${PAYMENT_CONFIG.whatsappNumber}?text=${buildWhatsappMessage()}`;
    window.open(url, '_blank', 'noopener');
  };

  // Guarda el pedido en el backend (si está activo). No bloquea la venta si falla.
  const saveOrderToBackend = async () => {
    if (!BACKEND_ENABLED) return;
    try {
      const { orderCode } = await apiCreateOrder({
        customer: {
          fullName: customerInfo.fullName,
          email: customerInfo.email,
          phone: customerInfo.phone,
          address: customerInfo.address,
          department: customerInfo.department,
          city: customerInfo.city,
          notes: customerInfo.notes,
        },
        items: cartItems.map((it) => ({
          productId: it.product.id,
          productName: it.product.name,
          color: it.selectedColor?.name,
          unitPrice: it.product.price,
          quantity: it.quantity,
        })),
        shippingMethod: selectedShipping.name,
        paymentMethod: paymentMethod + (paymentMethod === 'PSE' && pseBank ? ` (${pseBank})` : ''),
        subtotal,
        discount: discountAmount,
        shippingCost: deliveryCost,
        total,
      });
      if (orderCode) setGeneratedOrderId(orderCode);
    } catch {
      /* Si el backend falla, seguimos con el código local y el flujo de pago. */
    }
  };

  const handleProcessPayment = async () => {
    if (!validatePaymentStep()) return;

    setProcessing(true);

    // Determine the redirect target for the selected method
    let redirectUrl = '';
    if (paymentMethod === 'MercadoPago') {
      redirectUrl = PAYMENT_CONFIG.mercadoPagoLink;
    } else {
      // Wompi & PSE are both handled by the Wompi gateway
      redirectUrl = PAYMENT_CONFIG.wompiLink;
    }

    // Guardar el pedido antes de redirigir/confirmar
    await saveOrderToBackend();

    setTimeout(() => {
      setProcessing(false);
      // If a real payment link is configured, open the secure gateway.
      // Otherwise, coordinate the payment via WhatsApp so no sale is lost.
      if (redirectUrl) {
        window.open(redirectUrl, '_blank', 'noopener');
      } else {
        openWhatsapp();
      }
      setStep(4);
    }, 1800);
  };

  const handleFinishAndExit = () => {
    onOrderCompleted();
    onClose();
  };

  const paymentLinkConfigured =
    paymentMethod === 'MercadoPago' ? !!PAYMENT_CONFIG.mercadoPagoLink : !!PAYMENT_CONFIG.wompiLink;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-charcoal-900/70 backdrop-blur-md overflow-y-auto">

      {/* Container Card */}
      <div className="bg-white rounded-3xl w-full max-w-4xl shadow-2xl relative grid grid-cols-1 lg:grid-cols-12 overflow-hidden max-h-[92vh]">

        {/* Close Button top-right (unless on step 4 receipt screen) */}
        {step !== 4 && (
          <button
            id="close-checkout"
            onClick={onClose}
            className="absolute top-5 right-5 z-20 p-2 rounded-full bg-neutral-100 hover:bg-neutral-200 text-charcoal-700 transition"
          >
            <X className="w-5 h-5" />
          </button>
        )}

        {/* Left Side: Steps progress + order summary */}
        <div className="lg:col-span-5 bg-charcoal-950 p-6 sm:p-8 text-white flex flex-col justify-between border-r border-charcoal-800">
          <div className="space-y-6">
            <div className="flex items-center space-x-2">
              <span className="font-serif text-xl tracking-[0.25em] font-extrabold text-white">PRIME</span>
              <span className="text-[9px] tracking-widest font-light text-gold-coulisse uppercase bg-gold-400/10 px-1.5 py-0.5 rounded border border-gold-400/25">PAGO SEGURO</span>
            </div>

            {/* Steps Progress Visualizer */}
            {step < 4 ? (
              <div className="space-y-4 pt-4">
                {[
                  { n: 1, label: 'Datos de envío' },
                  { n: 2, label: 'Método de entrega' },
                  { n: 3, label: 'Pago' }
                ].map((s) => (
                  <div key={s.n} className="flex items-center space-x-3.5">
                    <div
                      className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold font-sans transition-all duration-300 ${
                        step === s.n
                          ? 'bg-gold-coulisse text-charcoal-950 ring-4 ring-gold-coulisse/20 scale-110'
                          : step > s.n
                          ? 'bg-charcoal-900 text-white'
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
              <div id="success-visual" className="pt-6 text-center space-y-3 bg-gold-500/10 p-5 rounded-2xl border border-gold-500/20">
                <CheckCircle2 className="w-12 h-12 text-gold-coulisse mx-auto" />
                <div>
                  <h4 className="font-serif font-black text-gold-300 tracking-wider">PEDIDO REGISTRADO</h4>
                  <p className="text-[10px] text-charcoal-350">Completa tu pago para despachar</p>
                </div>
              </div>
            )}

            {/* Cart overview mini list */}
            <div className="pt-6 border-t border-charcoal-800 space-y-4">
              <h5 className="text-[10px] text-charcoal-400 uppercase tracking-widest font-bold">Resumen del pedido</h5>
              <div className="space-y-3.5 max-h-[160px] overflow-y-auto pr-2">
                {cartItems.map((item) => (
                  <div key={item.id} className="flex items-center justify-between text-xs font-sans">
                    <div className="flex items-center space-x-2.5">
                      <div className="w-8 h-10 bg-charcoal-900 rounded overflow-hidden flex-shrink-0">
                        <img src={item.product.primaryImage} loading="lazy" decoding="async" className="w-full h-full object-cover" referrerPolicy="no-referrer" />
                      </div>
                      <div>
                        <p className="font-serif font-bold text-white max-w-[120px] truncate">{item.product.name}</p>
                        <p className="text-[9px] text-[#999]">{item.selectedColor.name} • {item.quantity} ud.</p>
                      </div>
                    </div>
                    <span className="font-semibold text-charcoal-200 font-sans">{formatCOP(item.product.price * item.quantity)}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Totals box */}
          <div className="pt-6 border-t border-charcoal-800 space-y-2">
            <div className="flex justify-between text-xs text-charcoal-400 font-sans">
              <span>Subtotal:</span>
              <span>{formatCOP(subtotal)}</span>
            </div>
            {appliedDiscountPercent > 0 && (
              <div className="flex justify-between text-xs text-charcoal-600 font-semibold font-sans">
                <span>Descuento ({appliedDiscountPercent}%{promoCodeUsed ? ` · ${promoCodeUsed}` : ''}):</span>
                <span>-{formatCOP(discountAmount)}</span>
              </div>
            )}
            <div className="flex justify-between text-xs text-charcoal-400 font-sans">
              <span>Envío ({selectedShipping.name}):</span>
              <span>{deliveryCost === 0 ? 'Gratis' : formatCOP(deliveryCost)}</span>
            </div>
            <div className="flex justify-between text-sm pt-2.5 border-t border-charcoal-800 text-white font-serif font-black">
              <span>Total:</span>
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
                  <h3 className="font-serif text-lg font-bold text-charcoal-900 uppercase tracking-wider">1. Datos de envío</h3>
                  <p className="text-xs text-neutral-500">Ingresa la dirección exacta donde quieres recibir tu pedido.</p>
                </div>

                <div className="space-y-3">
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    <div className="space-y-1">
                      <label className="block text-[10px] uppercase font-bold text-charcoal-700">Nombre completo</label>
                      <input
                        type="text"
                        name="fullName"
                        value={customerInfo.fullName}
                        onChange={handleInfoChange}
                        className={`w-full text-xs py-3 px-4 border rounded-xl focus:outline-none focus:ring-1 focus:ring-charcoal-400 ${
                          infoErrors.fullName ? 'border-charcoal-800 bg-neutral-100/20' : 'border-neutral-250 bg-neutral-50/50'
                        }`}
                        placeholder="Ej. Valentina Restrepo"
                      />
                      {infoErrors.fullName && <p className="text-[10px] text-charcoal-800">{infoErrors.fullName}</p>}
                    </div>

                    <div className="space-y-1">
                      <label className="block text-[10px] uppercase font-bold text-charcoal-700">Correo electrónico</label>
                      <input
                        type="email"
                        name="email"
                        value={customerInfo.email}
                        onChange={handleInfoChange}
                        className={`w-full text-xs py-3 px-4 border rounded-xl focus:outline-none focus:ring-1 focus:ring-charcoal-400 ${
                          infoErrors.email ? 'border-charcoal-800 bg-neutral-100/20' : 'border-neutral-250 bg-neutral-50/50'
                        }`}
                        placeholder="valentina@gmail.com"
                      />
                      {infoErrors.email && <p className="text-[10px] text-charcoal-800">{infoErrors.email}</p>}
                    </div>
                  </div>

                  <div className="space-y-1">
                    <label className="block text-[10px] uppercase font-bold text-charcoal-700">Celular (WhatsApp)</label>
                    <input
                      type="tel"
                      name="phone"
                      value={customerInfo.phone}
                      onChange={handleInfoChange}
                      className={`w-full text-xs py-3 px-4 border rounded-xl focus:outline-none focus:ring-1 focus:ring-charcoal-400 ${
                        infoErrors.phone ? 'border-charcoal-800 bg-neutral-100/20' : 'border-neutral-250 bg-neutral-50/50'
                      }`}
                      placeholder="300 123 4567"
                    />
                    {infoErrors.phone && <p className="text-[10px] text-charcoal-800">{infoErrors.phone}</p>}
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    <div className="space-y-1">
                      <label className="block text-[10px] uppercase font-bold text-charcoal-700">Departamento</label>
                      <select
                        name="department"
                        value={customerInfo.department}
                        onChange={handleInfoChange}
                        className={`w-full text-xs py-3 px-4 border rounded-xl focus:outline-none focus:ring-1 focus:ring-charcoal-400 bg-neutral-50/50 ${
                          infoErrors.department ? 'border-charcoal-800 bg-neutral-100/20' : 'border-neutral-250'
                        }`}
                      >
                        <option value="">Selecciona…</option>
                        {COLOMBIA_DEPARTMENTS.map((dep) => (
                          <option key={dep} value={dep}>{dep}</option>
                        ))}
                      </select>
                      {infoErrors.department && <p className="text-[10px] text-charcoal-800">{infoErrors.department}</p>}
                    </div>

                    <div className="space-y-1">
                      <label className="block text-[10px] uppercase font-bold text-charcoal-700">Ciudad / Municipio</label>
                      <select
                        name="city"
                        value={customerInfo.city}
                        onChange={handleInfoChange}
                        disabled={!customerInfo.department}
                        className={`w-full text-xs py-3 px-4 border rounded-xl focus:outline-none focus:ring-1 focus:ring-charcoal-400 bg-neutral-50/50 disabled:opacity-50 disabled:cursor-not-allowed ${
                          infoErrors.city ? 'border-charcoal-800 bg-neutral-100/20' : 'border-neutral-250'
                        }`}
                      >
                        <option value="">{customerInfo.department ? 'Selecciona…' : 'Elige departamento primero'}</option>
                        {availableCities.map((c) => (
                          <option key={c} value={c}>{c}</option>
                        ))}
                      </select>
                      {infoErrors.city && <p className="text-[10px] text-charcoal-800">{infoErrors.city}</p>}
                    </div>
                  </div>

                  <div className="space-y-1">
                    <label className="block text-[10px] uppercase font-bold text-charcoal-700">Dirección</label>
                    <div className="relative">
                      <MapPin className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-neutral-400" />
                      <input
                        type="text"
                        name="address"
                        value={customerInfo.address}
                        onChange={handleInfoChange}
                        className={`w-full text-xs py-3 pl-10 pr-4 border rounded-xl focus:outline-none focus:ring-1 focus:ring-charcoal-400 ${
                          infoErrors.address ? 'border-charcoal-800 bg-neutral-100/20' : 'border-neutral-250 bg-neutral-50/50'
                        }`}
                        placeholder="Ej. Cra 43A # 18-95, Apto 502, Torre 2"
                      />
                    </div>
                    {infoErrors.address && <p className="text-[10px] text-charcoal-800">{infoErrors.address}</p>}
                  </div>

                  <div className="space-y-1">
                    <label className="block text-[10px] uppercase font-bold text-charcoal-700">Notas de entrega (opcional)</label>
                    <textarea
                      name="notes"
                      value={customerInfo.notes}
                      onChange={handleInfoChange}
                      rows={2}
                      className="w-full text-xs py-3 px-4 border border-neutral-250 bg-neutral-50/50 rounded-xl focus:outline-none focus:ring-1 focus:ring-charcoal-400 resize-none"
                      placeholder="Punto de referencia, horario preferido, conjunto residencial…"
                    />
                  </div>
                </div>

                <div className="pt-6 border-t border-neutral-100 flex justify-end">
                  <button
                    id="info-step-submit"
                    onClick={handleNextStep}
                    className="px-8 py-3 bg-charcoal-900 hover:bg-gold-coulisse hover:text-charcoal-950 text-white rounded-full text-xs uppercase tracking-widest font-semibold flex items-center space-x-2 transition-all shadow-md"
                  >
                    <span>Continuar al envío</span>
                    <Truck className="w-4 h-4" />
                  </button>
                </div>
              </motion.div>
            )}

            {/* Step 2: Shipping selection */}
            {step === 2 && (
              <motion.div
                key="step2"
                initial={{ opacity: 0, x: 15 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -15 }}
                className="space-y-6"
              >
                <div>
                  <h3 className="font-serif text-lg font-bold text-charcoal-900 uppercase tracking-wider">2. Método de entrega</h3>
                  <p className="text-xs text-neutral-500">Enviamos a toda Colombia con transportadoras certificadas y seguimiento de guía.</p>
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
                            ? 'border-charcoal-900 bg-neutral-50 ring-1 ring-charcoal-900 shadow-sm'
                            : 'border-neutral-200 hover:bg-neutral-50/50'
                        }`}
                      >
                        <div className="flex items-start space-x-3 max-w-[80%]">
                          <input
                            type="radio"
                            checked={isSelected}
                            onChange={() => setSelectedShipping(method)}
                            className="mt-1 accent-black h-4 w-4"
                          />
                          <div>
                            <p className="font-serif font-extrabold text-sm text-charcoal-900 uppercase tracking-wide">{method.name}</p>
                            <p className="text-xs text-[#666] font-light mt-0.5 leading-relaxed">{method.description}</p>
                            <span className="text-[10px] bg-charcoal-900/10 text-charcoal-700 font-semibold uppercase px-2 py-0.5 rounded mt-1.5 inline-block font-mono">
                              {method.estimatedDays}
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
                    <span>Ir al pago</span>
                    <CreditCard className="w-4 h-4" />
                  </button>
                </div>
              </motion.div>
            )}

            {/* Step 3: Payment Method (Colombia) */}
            {step === 3 && (
              <motion.div
                key="step3"
                initial={{ opacity: 0, x: 15 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -15 }}
                className="space-y-6"
              >
                <div>
                  <h3 className="font-serif text-lg font-bold text-charcoal-900 uppercase tracking-wider">3. Pago</h3>
                  <p className="text-xs text-neutral-500">Elige cómo quieres pagar. Tu pago se procesa de forma segura por la pasarela seleccionada.</p>
                </div>

                {/* Payment method tabs */}
                <div className="grid grid-cols-3 gap-2">
                  {PAYMENT_METHODS.map((p) => {
                    const Icon = p.key === 'Wompi' ? Wallet : p.key === 'PSE' ? Building2 : CreditCard;
                    return (
                      <button
                        id={`pay-method-${p.key}`}
                        key={p.key}
                        onClick={() => setPaymentMethod(p.key)}
                        className={`py-3 px-1 text-center border rounded-xl text-xs font-semibold uppercase tracking-wider transition-all flex flex-col items-center gap-1.5 ${
                          paymentMethod === p.key
                            ? 'bg-charcoal-900 text-white border-charcoal-900 shadow-sm'
                            : 'border-neutral-200 text-charcoal-500 hover:bg-neutral-50'
                        }`}
                      >
                        <Icon className="w-4 h-4" />
                        {p.label}
                      </button>
                    );
                  })}
                </div>

                {/* Selected method description */}
                <div className="bg-neutral-50 rounded-2xl border border-neutral-150 p-5 space-y-3">
                  <p className="text-xs text-charcoal-700 leading-relaxed">
                    {PAYMENT_METHODS.find((p) => p.key === paymentMethod)?.description}
                  </p>

                  {/* PSE bank selector */}
                  {paymentMethod === 'PSE' && (
                    <div className="space-y-1 pt-1">
                      <label className="block text-[10px] uppercase font-bold text-charcoal-700">Selecciona tu banco</label>
                      <select
                        value={pseBank}
                        onChange={(e) => {
                          setPseBank(e.target.value);
                          setPaymentErrors((prev) => ({ ...prev, pseBank: '' }));
                        }}
                        className={`w-full text-xs py-3 px-4 border rounded-xl focus:outline-none focus:ring-1 focus:ring-charcoal-400 bg-white ${
                          paymentErrors.pseBank ? 'border-charcoal-800 bg-neutral-100/20' : 'border-neutral-250'
                        }`}
                      >
                        <option value="">Selecciona tu banco…</option>
                        {PSE_BANKS.map((b) => (
                          <option key={b} value={b}>{b}</option>
                        ))}
                      </select>
                      {paymentErrors.pseBank && <p className="text-[10px] text-charcoal-800">{paymentErrors.pseBank}</p>}
                    </div>
                  )}

                  <div className="flex items-center gap-2 text-[10px] text-charcoal-500 pt-1">
                    <ExternalLink className="w-3.5 h-3.5" />
                    <span>
                      {paymentLinkConfigured
                        ? 'Te redirigiremos a la pasarela segura para completar el pago.'
                        : 'Confirmaremos tu pedido y coordinaremos el pago por WhatsApp.'}
                    </span>
                  </div>
                </div>

                {/* Security badge */}
                <div className="bg-neutral-100/40 p-4 rounded-xl border border-neutral-300/50 text-xs flex items-start space-x-3 text-charcoal-700 font-sans leading-relaxed">
                  <ShieldCheck className="w-5 h-5 text-charcoal-900 flex-shrink-0 mt-0.5" />
                  <div>
                    <strong>Pago 100% seguro.</strong> No almacenamos datos de tu tarjeta ni de tus cuentas bancarias. El cobro lo realiza directamente la pasarela autorizada.
                  </div>
                </div>

                {/* Aceptación de términos y política de reembolso */}
                <label className="flex items-start gap-2.5 text-xs text-charcoal-700 font-sans cursor-pointer select-none">
                  <input
                    type="checkbox"
                    checked={acceptedTerms}
                    onChange={(e) => {
                      setAcceptedTerms(e.target.checked);
                      setPaymentErrors((prev) => ({ ...prev, terms: '' }));
                    }}
                    className="mt-0.5 h-4 w-4 accent-black shrink-0"
                  />
                  <span>
                    He leído y acepto los{' '}
                    <button type="button" onClick={() => setPolicyView('terms')} className="underline font-semibold text-charcoal-900 hover:text-black">
                      Términos y Condiciones
                    </button>{' '}
                    y la{' '}
                    <button type="button" onClick={() => setPolicyView('refund')} className="underline font-semibold text-charcoal-900 hover:text-black">
                      Política de Reembolso
                    </button>.
                  </span>
                </label>
                {paymentErrors.terms && <p className="text-[11px] text-charcoal-900 font-semibold -mt-3">{paymentErrors.terms}</p>}

                {/* Back / Pay Actions */}
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
                    onClick={handleProcessPayment}
                    disabled={processing}
                    className="group px-8 py-3.5 bg-charcoal-900 hover:bg-gold-coulisse hover:text-charcoal-950 text-white rounded-full text-xs uppercase tracking-widest font-semibold flex items-center justify-center space-x-2 transition-all shadow-md min-w-[180px] disabled:opacity-70"
                  >
                    {processing ? (
                      <>
                        <Loader2 className="w-4.5 h-4.5 animate-spin" />
                        <span>Procesando…</span>
                      </>
                    ) : (
                      <span>Pagar {formatCOP(total)}</span>
                    )}
                  </button>
                </div>
              </motion.div>
            )}

            {/* Step 4: Order confirmation */}
            {step === 4 && (
              <motion.div
                key="step4"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="space-y-6 pt-2 text-center"
              >
                <div className="space-y-2">
                  <span className="bg-gold-500/10 border border-gold-400/30 text-gold-600 text-[10px] font-bold tracking-widest uppercase px-3.5 py-1.5 rounded-full inline-block font-sans">
                    ★ PEDIDO REGISTRADO
                  </span>
                  <h3 className="font-serif text-2xl font-extrabold text-charcoal-950">¡Gracias por tu compra!</h3>
                  <p className="text-xs text-neutral-500 max-w-sm mx-auto">
                    {paymentLinkConfigured
                      ? 'Abrimos la pasarela de pago en una nueva pestaña. Apenas confirmemos tu pago, despachamos tu pedido.'
                      : 'Te enviamos el resumen por WhatsApp. Coordina ahí tu pago y despachamos tu pedido de inmediato.'}
                  </p>
                </div>

                {/* Order summary sheet */}
                <div className="border border-neutral-250 rounded-2xl bg-[#fafafa] p-5 text-left text-xs font-sans space-y-4 shadow-sm">
                  <div className="border-b border-neutral-200 pb-3 space-y-1">
                    <p className="text-neutral-400 font-semibold uppercase text-[9px] tracking-wider">N.º de pedido</p>
                    <p className="font-bold text-charcoal-800 text-[11px]">{generatedOrderId}</p>
                    <div className="flex justify-between text-[10px] text-neutral-500 pt-1">
                      <span>Prime Drop Elite · Colombia</span>
                      <span>{new Date().toLocaleDateString('es-CO')}</span>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <p className="font-bold text-charcoal-800 text-[10px] uppercase tracking-wider">Datos de entrega</p>
                    <div className="text-neutral-500 text-[11px] space-y-0.5 font-light">
                      <p><strong className="font-medium text-charcoal-800">Destinatario:</strong> {customerInfo.fullName}</p>
                      <p><strong className="font-medium text-charcoal-800">Dirección:</strong> {customerInfo.address}</p>
                      <p><strong className="font-medium text-charcoal-800">Ciudad:</strong> {customerInfo.city}, {customerInfo.department}</p>
                      <p><strong className="font-medium text-charcoal-800">Celular:</strong> {customerInfo.phone}</p>
                      <p><strong className="font-medium text-charcoal-800">Envío:</strong> {selectedShipping.name} ({selectedShipping.estimatedDays})</p>
                      <p><strong className="font-medium text-charcoal-800">Pago:</strong> {paymentMethod}{paymentMethod === 'PSE' && pseBank ? ` · ${pseBank}` : ''}</p>
                    </div>
                  </div>

                  <div className="border-t border-neutral-200 pt-3 flex justify-between items-center text-charcoal-900 font-serif">
                    <span className="font-medium uppercase text-[10px] tracking-wider">Total a pagar:</span>
                    <strong className="font-black text-sm text-gold-700">{formatCOP(total)}</strong>
                  </div>
                </div>

                {/* Action buttons */}
                <div className="flex flex-col gap-3 pt-2">
                  <button
                    id="whatsapp-confirm-btn"
                    onClick={openWhatsapp}
                    className="w-full py-3 px-4 rounded-xl bg-[#25D366] hover:bg-[#1ebe5b] text-white font-semibold text-xs uppercase tracking-wider flex items-center justify-center space-x-2 shadow-md transition"
                  >
                    <MessageCircle className="w-4 h-4" />
                    <span>Enviar comprobante por WhatsApp</span>
                  </button>

                  <div className="flex flex-col sm:flex-row gap-3">
                    <button
                      id="on-print-recipe"
                      onClick={() => window.print()}
                      className="flex-1 py-3 px-4 rounded-xl border border-neutral-200 font-semibold text-xs uppercase tracking-wider text-charcoal-700 hover:bg-neutral-50 flex items-center justify-center space-x-1.5"
                    >
                      <Printer className="w-4 h-4" />
                      <span>Imprimir pedido</span>
                    </button>

                    <button
                      id="finish-checkout-btn"
                      onClick={handleFinishAndExit}
                      className="flex-1 py-3 px-4 rounded-xl bg-charcoal-900 hover:bg-gold-coulisse hover:text-charcoal-950 text-white font-semibold text-xs uppercase tracking-wider flex items-center justify-center space-x-1.5 shadow-md"
                    >
                      <span>Volver a la tienda</span>
                    </button>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>

      {/* Modal de política (Términos / Reembolso) dentro del checkout */}
      {policyView && (
        <div className="fixed inset-0 z-[60] flex items-center justify-center p-4">
          <div className="absolute inset-0 bg-black/60" onClick={() => setPolicyView(null)} />
          <div className="relative bg-white text-charcoal-900 w-full max-w-lg rounded-2xl shadow-2xl border border-neutral-200 z-10 flex flex-col max-h-[85vh]">
            <div className="flex items-center justify-between p-5 border-b border-neutral-150">
              <h4 className="font-serif text-lg font-black">
                {policyView === 'terms' ? 'Términos y Condiciones' : 'Política de Reembolso'}
              </h4>
              <button onClick={() => setPolicyView(null)} className="p-1.5 rounded-full hover:bg-neutral-100">
                <X className="w-5 h-5" />
              </button>
            </div>
            <div className="p-5 overflow-y-auto text-sm font-light text-charcoal-600 leading-relaxed whitespace-pre-line">
              {policyView === 'terms' ? TERMS_CONTENT : REFUND_CONTENT}
            </div>
            <div className="p-4 border-t border-neutral-150 text-right">
              <button
                onClick={() => setPolicyView(null)}
                className="px-6 py-2.5 bg-charcoal-900 text-white rounded-full text-xs font-bold uppercase tracking-widest hover:bg-charcoal-700"
              >
                Entendido
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

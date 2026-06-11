/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { X, ShieldCheck, LogOut, AlertCircle, Sparkles, Eye, EyeOff } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';
import { BACKEND_ENABLED, apiLogin, apiRegister } from '../lib/api';

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
  onLoginSuccess: (name: string, email: string) => void;
  onLogout: () => void;
  isPrimeMember: boolean;
  currentUserEmail: string;
  currentUsername: string;
}

export default function AuthModal({
  isOpen,
  onClose,
  onLoginSuccess,
  onLogout,
  isPrimeMember,
  currentUserEmail,
  currentUsername
}: AuthModalProps) {
  const [authTab, setAuthTab] = useState<'login' | 'register'>('login');
  
  // Login inputs
  const [loginEmail, setLoginEmail] = useState('');
  const [loginPassword, setLoginPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  
  // Register inputs
  const [regName, setRegName] = useState('');
  const [regEmail, setRegEmail] = useState('');
  const [regPassword, setRegPassword] = useState('');

  // Feedback
  const [errorMsg, setErrorMsg] = useState('');
  const [successMsg, setSuccessMsg] = useState('');

  const finishSuccess = (msg: string) => {
    setSuccessMsg(msg);
    setTimeout(() => {
      onClose();
      setSuccessMsg('');
    }, 1500);
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg('');
    setSuccessMsg('');

    if (!loginEmail || !loginPassword) {
      setErrorMsg('Por favor complete todos los campos.');
      return;
    }

    if (BACKEND_ENABLED) {
      try {
        const { user } = await apiLogin(loginEmail.trim(), loginPassword);
        localStorage.setItem('prime_user_name', user.name);
        localStorage.setItem('prime_user_email', user.email);
        onLoginSuccess(user.name, user.email);
        finishSuccess(`¡Bienvenido de vuelta, ${user.name}!`);
      } catch (err: any) {
        setErrorMsg(err.message || 'No se pudo iniciar sesión.');
      }
      return;
    }

    // Fallback sin backend: cuentas guardadas en el navegador
    const accounts = JSON.parse(localStorage.getItem('premium_prime_accounts') || '[]');
    const matched = accounts.find(
      (acc: any) => acc.email.toLowerCase() === loginEmail.toLowerCase() && acc.password === loginPassword
    );

    if (matched) {
      localStorage.setItem('prime_user_name', matched.name);
      localStorage.setItem('prime_user_email', matched.email);
      onLoginSuccess(matched.name, matched.email);
      finishSuccess(`¡Bienvenido de vuelta, ${matched.name}!`);
    } else {
      setErrorMsg('Correo o contraseña incorrectos.');
    }
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg('');
    setSuccessMsg('');

    if (!regName.trim() || !regEmail.trim() || !regPassword) {
      setErrorMsg('Completa nombre, correo y contraseña.');
      return;
    }
    if (regPassword.length < 6) {
      setErrorMsg('La contraseña debe tener al menos 6 caracteres.');
      return;
    }

    if (BACKEND_ENABLED) {
      try {
        const { user } = await apiRegister(regName.trim(), regEmail.trim(), regPassword);
        localStorage.setItem('prime_user_name', user.name);
        localStorage.setItem('prime_user_email', user.email);
        onLoginSuccess(user.name, user.email);
        setRegName(''); setRegEmail(''); setRegPassword('');
        finishSuccess('¡Cuenta creada con éxito!');
      } catch (err: any) {
        setErrorMsg(err.message || 'No se pudo crear la cuenta.');
      }
      return;
    }

    // Fallback sin backend: cuentas guardadas en el navegador
    const accounts = JSON.parse(localStorage.getItem('premium_prime_accounts') || '[]');
    const emailExists = accounts.some((acc: any) => acc.email.toLowerCase() === regEmail.toLowerCase());
    if (emailExists) {
      setErrorMsg('Esta dirección de correo ya tiene una cuenta registrada.');
      return;
    }

    accounts.push({ name: regName.trim(), email: regEmail.trim(), password: regPassword });
    localStorage.setItem('premium_prime_accounts', JSON.stringify(accounts));
    localStorage.setItem('prime_user_name', regName.trim());
    localStorage.setItem('prime_user_email', regEmail.trim());

    onLoginSuccess(regName.trim(), regEmail.trim());
    setRegName(''); setRegEmail(''); setRegPassword('');
    finishSuccess('¡Cuenta creada con éxito!');
  };


  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="absolute inset-0 bg-charcoal-950/40 backdrop-blur-[2px]"
          />

          {/* Modal Container */}
          <motion.div
            initial={{ opacity: 0, scale: 0.97, y: 10 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.97, y: 10 }}
            transition={{ type: 'spring', duration: 0.4 }}
            className="bg-white text-charcoal-900 rounded-[24px] overflow-hidden shadow-2xl border border-neutral-100 max-w-[450px] w-full relative z-10"
          >
            {/* Close Toggle */}
            <button
              id="auth-close-btn"
              onClick={onClose}
              className="absolute top-4 right-4 z-20 p-1.5 rounded-full bg-neutral-50 text-neutral-400 hover:text-charcoal-900 transition-colors"
              aria-label="Cerrar modal"
            >
              <X className="w-4 h-4" />
            </button>

            {/* Profile view (if already authenticated) */}
            {isPrimeMember ? (
              <div className="p-8 text-center space-y-6">
                <div className="w-16 h-16 bg-gold-50 text-gold-700 rounded-full flex items-center justify-center mx-auto border border-gold-200">
                  <ShieldCheck className="w-8 h-8" />
                </div>
                <div className="space-y-1">
                  <span className="text-[10px] uppercase tracking-[0.25em] font-extrabold text-gold-600">Socio VIP Activo</span>
                  <h3 className="font-serif text-2xl font-black text-charcoal-950">{currentUsername}</h3>
                  <p className="text-xs text-charcoal-500 font-mono">{currentUserEmail}</p>
                </div>

                <div className="bg-neutral-50 rounded-2xl p-4 border border-neutral-100 text-left space-y-2">
                  <div className="flex items-center space-x-2 text-xs font-semibold text-charcoal-800">
                    <Sparkles className="w-4 h-4 text-gold-500" />
                    <span>Beneficios Activos en PRIME DROP:</span>
                  </div>
                  <ul className="text-[11px] text-charcoal-550 space-y-1.5 ml-6 list-disc font-medium">
                    <li>Acceso anticipado a los nuevos drops.</li>
                    <li>Ofertas y novedades exclusivas por correo.</li>
                    <li>Atención prioritaria por WhatsApp.</li>
                  </ul>
                </div>

                <button
                  id="auth-logout-btn"
                  onClick={() => {
                    onLogout();
                    onClose();
                  }}
                  className="w-full py-3 bg-neutral-100 hover:bg-neutral-200 border border-neutral-300 text-charcoal-900 rounded-full text-xs font-bold uppercase tracking-widest flex items-center justify-center space-x-2 transition duration-200"
                >
                  <LogOut className="w-4 h-4" />
                  <span>Cerrar Sesión</span>
                </button>
              </div>
            ) : (
              /* Auth Form View with Split Header (Login / Register Tabs) */
              <div className="flex flex-col">
                {/* Tabs Switcher - Split 50/50 exactly like the provided screenshot */}
                <div className="flex border-b border-neutral-200 text-center">
                  <button
                    id="modal-tab-login"
                    type="button"
                    onClick={() => {
                      setAuthTab('login');
                      setErrorMsg('');
                    }}
                    className={`flex-1 py-4.5 text-[11px] uppercase tracking-[0.18em] font-bold transition-all relative ${
                      authTab === 'login'
                        ? 'text-charcoal-950 bg-white font-black'
                        : 'text-neutral-450 hover:text-charcoal-800 bg-neutral-50/50'
                    }`}
                  >
                    ACCEDER
                    {authTab === 'login' && (
                      <div className="absolute bottom-0 left-0 right-0 h-[2px] bg-charcoal-950" />
                    )}
                  </button>
                  <button
                    id="modal-tab-register"
                    type="button"
                    onClick={() => {
                      setAuthTab('register');
                      setErrorMsg('');
                    }}
                    className={`flex-1 py-4.5 text-[11px] uppercase tracking-[0.18em] font-bold transition-all relative border-l border-neutral-200 ${
                      authTab === 'register'
                        ? 'text-charcoal-950 bg-white font-black'
                        : 'text-neutral-450 hover:text-charcoal-800 bg-neutral-50/50'
                    }`}
                  >
                    REGISTRARSE
                    {authTab === 'register' && (
                      <div className="absolute bottom-0 left-0 right-0 h-[2px] bg-charcoal-950" />
                    )}
                  </button>
                </div>

                {/* Form Body - Extremely clean padding and space */}
                <div className="p-7 sm:p-9 space-y-6">
                  {/* Notifications info */}
                  {errorMsg && (
                    <div className="p-3 bg-neutral-100 border border-neutral-200 rounded-xl text-charcoal-900 text-xs flex items-start space-x-2.5">
                      <AlertCircle className="w-4 h-4 shrink-0 text-charcoal-800 mt-0.5" />
                      <span className="font-medium">{errorMsg}</span>
                    </div>
                  )}
                  {successMsg && (
                    <div className="p-3 bg-neutral-100 border border-neutral-200 rounded-xl text-charcoal-900 text-xs flex items-start space-x-2.5">
                      <ShieldCheck className="w-4 h-4 shrink-0 text-charcoal-900 mt-0.5" />
                      <span className="font-semibold">{successMsg}</span>
                    </div>
                  )}

                  {/* Form fields */}
                  {authTab === 'login' ? (
                    <form onSubmit={handleLogin} className="space-y-5">
                      <div className="space-y-1.5 text-left">
                        <label className="text-xs font-semibold text-charcoal-800 font-sans">
                          Correo electrónico
                        </label>
                        <input
                          id="modal-login-email-input"
                          type="email"
                          required
                          placeholder=""
                          value={loginEmail}
                          onChange={(e) => setLoginEmail(e.target.value)}
                          className="w-full bg-[#fff] border border-neutral-300 rounded-full py-3 px-5 text-sm font-medium focus:outline-none focus:border-charcoal-900 transition-all font-sans"
                        />
                      </div>

                      <div className="space-y-1.5 text-left relative">
                        <label className="text-xs font-semibold text-charcoal-800 font-sans">
                          Contraseña
                        </label>
                        <div className="relative">
                          <input
                            id="modal-login-pass-input"
                            type={showPassword ? 'text' : 'password'}
                            required
                            placeholder=""
                            value={loginPassword}
                            onChange={(e) => setLoginPassword(e.target.value)}
                            className="w-full bg-[#fff] border border-neutral-300 rounded-full py-3 pl-5 pr-12 text-sm font-medium focus:outline-none focus:border-charcoal-900 transition-all font-sans"
                          />
                          <button
                            type="button"
                            onClick={() => setShowPassword(!showPassword)}
                            className="absolute right-4 top-1/2 -translate-y-1/2 p-1 text-neutral-400 hover:text-charcoal-900 transition-colors"
                          >
                            {showPassword ? <EyeOff className="w-4.5 h-4.5" /> : <Eye className="w-4.5 h-4.5" />}
                          </button>
                        </div>
                      </div>

                      {/* Remember me + Forgot password layout */}
                      <div className="flex items-center justify-between text-xs text-charcoal-700 font-sans font-medium pt-1">
                        <label className="flex items-center space-x-2 cursor-pointer select-none">
                          <input
                            type="checkbox"
                            checked={rememberMe}
                            onChange={() => setRememberMe(!rememberMe)}
                            className="w-4 h-4 rounded-full border-neutral-300 text-charcoal-950 focus:ring-charcoal-950 cursor-pointer"
                          />
                          <span>Recordarme</span>
                        </label>
                        <button
                          type="button"
                          onClick={() => alert('Se ha enviado una solicitud de recuperación a su correo electrónico.')}
                          className="hover:underline text-charcoal-600 focus:outline-none"
                        >
                          ¿Olvidaste tu contraseña?
                        </button>
                      </div>

                      <button
                        id="modal-login-submit"
                        type="submit"
                        className="w-full py-3.5 bg-black text-white rounded-full text-xs font-bold uppercase tracking-[0.15em] hover:bg-neutral-850 active:scale-98 transition duration-200 mt-2 shadow-md leading-none"
                      >
                        Acceder
                      </button>
                    </form>
                  ) : (
                    /* Elegant register design as depicted in the 2nd screenshot */
                    <form onSubmit={handleRegister} className="space-y-5">
                      <div className="space-y-1.5 text-left">
                        <label className="text-xs font-semibold text-charcoal-800 font-sans">
                          Nombre completo
                        </label>
                        <input
                          id="modal-reg-name"
                          type="text"
                          required
                          value={regName}
                          onChange={(e) => setRegName(e.target.value)}
                          className="w-full bg-[#fff] border border-neutral-300 rounded-full py-3 px-5 text-sm font-medium focus:outline-none focus:border-charcoal-900 transition-all font-sans"
                        />
                      </div>

                      <div className="space-y-1.5 text-left">
                        <label className="text-xs font-semibold text-charcoal-800 font-sans">
                          Correo electrónico
                        </label>
                        <input
                          id="modal-reg-email"
                          type="email"
                          required
                          value={regEmail}
                          onChange={(e) => setRegEmail(e.target.value)}
                          className="w-full bg-[#fff] border border-neutral-300 rounded-full py-3 px-5 text-sm font-medium focus:outline-none focus:border-charcoal-900 transition-all font-sans"
                        />
                      </div>

                      <div className="space-y-1.5 text-left">
                        <label className="text-xs font-semibold text-charcoal-800 font-sans">
                          Contraseña
                        </label>
                        <input
                          id="modal-reg-password"
                          type="password"
                          required
                          value={regPassword}
                          onChange={(e) => setRegPassword(e.target.value)}
                          placeholder="Mínimo 6 caracteres"
                          className="w-full bg-[#fff] border border-neutral-300 rounded-full py-3 px-5 text-sm font-medium focus:outline-none focus:border-charcoal-900 transition-all font-sans"
                        />
                      </div>

                      <button
                        id="modal-register-submit"
                        type="submit"
                        className="w-full py-3.5 bg-black text-white rounded-full text-xs font-bold uppercase tracking-[0.15em] hover:bg-neutral-850 active:scale-98 transition duration-200 mt-2 shadow-md leading-none"
                      >
                        Registrarse
                      </button>

                      <p className="text-xs leading-relaxed text-left text-neutral-500 font-sans pt-1 border-t border-neutral-100">
                        Tus datos personales se usarán para gestionar tu cuenta y otros propósitos descritos en nuestra <a href="#privacy" className="underline hover:text-charcoal-950 font-medium">política de privacidad</a>.
                      </p>
                    </form>
                  )}
                </div>
              </div>
            )}
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}

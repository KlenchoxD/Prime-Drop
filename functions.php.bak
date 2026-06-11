<?php
/**
 * Blocksy functions and definitions
 *
 * @link https://developer.wordpress.org/themes/basics/theme-functions/
 *
 * @package Blocksy
 */

if (version_compare(PHP_VERSION, '5.7.0', '<')) {
	require get_template_directory() . '/inc/php-fallback.php';
	return;
}

require get_template_directory() . '/inc/init.php';

/* ============================================================
   PRIME DROP ELITE — MASTER BLOCK v2.0
   Dispositivos: Mobile ≤767px | Tablet 768-999px | Desktop ≥1000px
   ============================================================ */

/* ---------- 1. FOOTER VIDEO ---------- */
if (!function_exists('primedrop_footer_video_optimized_markup')) {
    function primedrop_footer_video_optimized_markup() {
        return '<video class="footer-video-bg" autoplay muted loop playsinline preload="auto" style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);min-width:100%;min-height:100%;width:auto;height:auto;object-fit:cover;z-index:0;"><source src="https://videos.pexels.com/video-files/3571264/3571264-uhd_2560_1440_30fps.mp4" type="video/mp4"></video>';
    }
}
if (!function_exists('primedrop_footer_video_optimize_output')) {
    function primedrop_footer_video_optimize_output($html) {
        $pattern = '#<video\s+class="footer-video-bg"[^>]*>\s*<source\s+src="https://videos\.pexels\.com/video-files/3571264/[^"]*"[^>]*>\s*</video>#i';
        return preg_replace($pattern, primedrop_footer_video_optimized_markup(), $html);
    }
}
add_action('template_redirect', function() {
    ob_start('primedrop_footer_video_optimize_output');
}, 0);

/* ---------- 2. CART DRAWER ---------- */
if (!function_exists('pd_cart_drawer_template_path')) {
    function pd_cart_drawer_template_path() {
        return trailingslashit(get_stylesheet_directory()) . 'cart-drawer.php';
    }
}
if (!function_exists('pd_cart_fragments')) {
    function pd_cart_fragments($fragments) {
        if (!function_exists('WC') || !WC()->cart) return $fragments;
        ob_start();
        echo '<div class="pd-cart-count">' . esc_html(WC()->cart->get_cart_contents_count()) . '</div>';
        $fragments['.pd-cart-count'] = ob_get_clean();
        ob_start();
        $t = pd_cart_drawer_template_path();
        if (file_exists($t)) include $t;
        $fragments['.pd-cart-drawer'] = ob_get_clean();
        return $fragments;
    }
    add_filter('woocommerce_add_to_cart_fragments', 'pd_cart_fragments');
}
if (!function_exists('pd_cart_drawer_scripts')) {
    function pd_cart_drawer_scripts() {
        if (!function_exists('is_woocommerce')) return;
        wp_enqueue_script('wc-cart-fragments');
        wp_enqueue_script('pd-cart-drawer', trailingslashit(get_stylesheet_directory_uri()) . 'js/cart-drawer.js', array('jquery','wc-cart-fragments'), '1.0.8', true);
        wp_localize_script('pd-cart-drawer', 'pdCartDrawerParams', array(
            'ajax_url' => admin_url('admin-ajax.php'),
            'nonce'    => wp_create_nonce('pd_cart_drawer_nonce'),
        ));
    }
    add_action('wp_enqueue_scripts', 'pd_cart_drawer_scripts');
}
if (!function_exists('pd_render_cart_drawer')) {
    function pd_render_cart_drawer() {
        if (!function_exists('WC') || !WC()->cart) return;
        $t = pd_cart_drawer_template_path();
        if (file_exists($t)) include $t;
        echo '<div id="cart-drawer-overlay" class="pd-cart-overlay cart-drawer-overlay"></div>';
    }
    add_action('wp_footer', 'pd_render_cart_drawer');
}
if (!function_exists('pd_update_cart_quantity')) {
    function pd_update_cart_quantity() {
        check_ajax_referer('pd_cart_drawer_nonce', 'nonce');
        if (!function_exists('WC') || !WC()->cart) wp_send_json_error(array('message' => 'Cart unavailable'));
        $key = isset($_POST['cart_item_key']) ? sanitize_text_field(wp_unslash($_POST['cart_item_key'])) : '';
        $qty = isset($_POST['quantity']) ? max(0, absint($_POST['quantity'])) : 0;
        if (!$key || !isset(WC()->cart->cart_contents[$key])) wp_send_json_error(array('message' => 'Invalid item'));
        WC()->cart->set_quantity($key, $qty, true);
        WC()->cart->calculate_totals();
        wp_send_json_success(array(
            'count'    => WC()->cart->get_cart_contents_count(),
            'subtotal' => WC()->cart->get_cart_subtotal(),
        ));
    }
    add_action('wp_ajax_pd_update_cart_quantity', 'pd_update_cart_quantity');
    add_action('wp_ajax_nopriv_pd_update_cart_quantity', 'pd_update_cart_quantity');
}

/* ---------- 3. BUSCADOR EN TIENDA ---------- */
add_action('woocommerce_before_shop_loop', function() {
    echo '<div class="pd-shop-search"><form role="search" method="get" action="' . esc_url(home_url('/')) . '"><input type="search" placeholder="Buscar bolsos..." value="' . get_search_query() . '" name="s"/><input type="hidden" name="post_type" value="product"/><button type="submit"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg></button></form></div>';
}, 25);

/* ---------- 4. REDIRECCIÓN CATEGORÍAS VIEJAS ---------- */
add_filter('wp_nav_menu_objects', function($items) {
    return array_values(array_filter($items, function($item) {
        $title = strtolower(trim(wp_strip_all_tags($item->title)));
        $url   = strtolower($item->url);
        return !(
            in_array($title, array('mujer','hombre'), true)
            || strpos($url, '/categoria-producto/mujer/') !== false
            || strpos($url, '/categoria-producto/hombre/') !== false
        );
    }));
}, 20);

add_action('template_redirect', function() {
    $path   = isset($_SERVER['REQUEST_URI']) ? trim(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH), '/') : '';
    $legacy = array('categoria-producto/mujer','categoria-producto/hombre','categoria-producto/ropa','categoria-producto/accesorios','product-category/mujer','product-category/hombre','product-category/ropa','product-category/accesorios','mujer','hombre');
    if (in_array($path, $legacy, true) || (function_exists('is_product_category') && is_product_category(array('mujer','hombre','ropa','accesorios')))) {
        wp_safe_redirect(home_url('/bolsos/'), 301);
        exit;
    }
});

/* ---------- 5. ÍCONO CUENTA MOBILE ---------- */
add_action('template_redirect', function() {
    if (is_admin() || wp_doing_ajax()) return;
    ob_start(function($html) {
        if (strpos($html, 'pd-mobile-account-server') !== false) return $html;
        $account_html = '<a href="#account-modal" class="ct-account-item pd-mobile-account-server" aria-label="ACCEDER" data-label="left"><svg class="ct-icon" aria-hidden="true" width="26" height="26" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="7.5" r="3.7" stroke="currentColor" stroke-width="1.7"></circle><path d="M4.8 20.2c0.8-4.3 3.7-6.6 7.2-6.6s6.4 2.3 7.2 6.6" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"></path></svg></a>';
        $mobile_pos = strpos($html, '<div data-device="mobile">');
        if ($mobile_pos === false) return $html;
        $cart_pos = strpos($html, 'class="ct-header-cart"', $mobile_pos);
        if ($cart_pos === false) return $html;
        $cart_div_start = strrpos(substr($html, 0, $cart_pos), '<div');
        if ($cart_div_start === false || $cart_div_start < $mobile_pos) return $html;
        return substr($html, 0, $cart_div_start) . $account_html . substr($html, $cart_div_start);
    });
}, 1);

add_action('wp_footer', function() {
    echo '<script>document.addEventListener("click",function(e){var t=e.target.closest&&e.target.closest(".pd-mobile-account-server");if(!t)return;var n=document.querySelector("[data-device=\'desktop\'] .ct-account-item[href=\'#account-modal\']");if(n&&n!==t){e.preventDefault();n.dispatchEvent(new MouseEvent("click",{bubbles:true,cancelable:true,view:window}))}});</script>';
}, 30);

/* ---------- 6. MUNDO PRIME CONTENIDO ---------- */
add_filter('the_content', function($content) {
    if (is_admin() || !is_page('mundo-prime') || !in_the_loop() || !is_main_query()) return $content;
    return '<main class="pd-mundo-prime-page">
      <section class="pd-mundo-hero"><h1>MUNDO PRIME</h1><p>La historia detrás de Prime Drop Elite</p></section>
      <section class="pd-mundo-story"><h2>Moda auténtica, elegida para Colombia</h2><p>Prime Drop Elite nace con una visión clara: Acercar las mejores marcas del mundo a quienes realmente saben de estilo. Nos especializamos en traer productos 100% originales de Michael Kors, Steve Madden y Tommy Hilfiger. Sin intermediarios, sin sobreprecios. Solo moda auténtica, exclusiva y al mejor precio para Colombia.</p></section>
      <section class="pd-mundo-values"><article class="pd-mundo-value"><svg viewBox="0 0 24 24" fill="none"><path d="M20 6 9 17l-5-5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg><h3>ORIGINALES</h3><p>Productos seleccionados con autenticidad y marcas reconocidas.</p></article><article class="pd-mundo-value"><svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="8" stroke="currentColor" stroke-width="1.8"/><path d="M4 12h16M12 4v16" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg><h3>SIN INTERMEDIARIOS</h3><p>Compras más directas para mantener precios justos.</p></article><article class="pd-mundo-value"><svg viewBox="0 0 24 24" fill="none"><path d="M12 21s7-5.1 7-11a7 7 0 0 0-14 0c0 5.9 7 11 7 11Z" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="10" r="2.4" stroke="currentColor" stroke-width="1.8"/></svg><h3>PARA COLOMBIA</h3><p>Una experiencia pensada para clientes que compran desde Colombia.</p></article></section>
      <div class="pd-mundo-cta"><a href="/bolsos/">VER COLECCIÓN</a></div>
    </main>';
}, 20);

/* ---------- 7. HERO /bolsos/ ---------- */
add_action('template_redirect', function() {
    if (is_admin()) return;
    ob_start(function($html) {
        if (!is_page('bolsos')) return $html;
        if (strpos($html, 'pd-shop-collection-hero') !== false) return $html;
        $hero = '<section class="pd-shop-collection-hero"><div class="pd-shop-collection-inner"><span>COLECCIÓN PRIME DROP</span><h1>BOLSOS</h1><p>Bolsos originales seleccionados para elevar tu estilo diario con marcas internacionales.</p></div></section>';
        return preg_replace('/(<section[^>]*elementor-element-0a7c205[^>]*>)/i', $hero . '$1', $html, 1);
    });
}, 1);

/* ---------- 8. SECCIÓN COLECCIÓN HOMEPAGE ---------- */
if (!function_exists('prime_drop_collection_showcase_markup')) {
    function prime_drop_collection_showcase_markup() {
        return '<section class="pd-collection-showcase" data-pd-collection-ready="1">
          <div class="pd-collection-heading"><h2>NUESTRA COLECCIÓN</h2><p>Bolsos originales Michael Kors, Steve Madden y Tommy Hilfiger</p></div>
          <div class="pd-collection-layout">
            <div class="pd-collection-media"><img src="/wp-content/uploads/2026/05/bolsos-categoria-scaled.jpg" alt="Bolsos Prime Drop"></div>
            <div class="pd-collection-content">
              <a class="pd-brand-row" href="/bolsos/"><span><strong>MICHAEL KORS</strong><span>15 estilos disponibles</span></span><em class="pd-brand-arrow">→</em></a>
              <a class="pd-brand-row" href="/bolsos/"><span><strong>STEVE MADDEN</strong><span>10 estilos disponibles</span></span><em class="pd-brand-arrow">→</em></a>
              <a class="pd-brand-row" href="/bolsos/"><span><strong>TOMMY HILFIGER</strong><span>3 estilos disponibles</span></span><em class="pd-brand-arrow">→</em></a>
              <a class="pd-collection-btn" href="/bolsos/">VER TODA LA COLECCIÓN</a>
            </div>
          </div>
        </section>';
    }
}
add_action('template_redirect', function() {
    if (is_admin()) return;
    $is_home = is_front_page() || is_home();
    ob_start(function($html) use ($is_home) {
        if ($is_home) {
            $html = preg_replace('/<section\b(?=[^>]*\bpd-categories\b)[^>]*>[\s\S]*?<\/section>/i', prime_drop_collection_showcase_markup(), $html, 1);
        }
        return $html;
    });
}, 0);

/* ---------- 9. CSS MAESTRO POR DISPOSITIVO ---------- */
add_action('wp_head', function() { ?>
<style id="pd-master-css">

/* =============================================
   GLOBAL — aplica a todos los dispositivos
   ============================================= */

/* Footer falso oculto */
footer.ct-footer:not(.pd-footer),
.ct-footer:not(.pd-footer) {
  display: none !important;
  visibility: hidden !important;
  height: 0 !important;
  overflow: hidden !important;
}
.pd-footer { display: block !important; visibility: visible !important; }

/* Íconos header — base */
.ct-account-item,
.ct-account-item .ct-icon {
  background: none !important;
  border: none !important;
  box-shadow: none !important;
  border-radius: 0 !important;
  padding: 0 !important;
  width: auto !important;
  height: auto !important;
}
.ct-account-item,
.ct-cart-item {
  display: flex !important;
  align-items: center !important;
  visibility: visible !important;
  opacity: 1 !important;
}
.ct-account-item svg,
.ct-account-item .ct-icon svg,
.ct-cart-item svg {
  width: 22px !important;
  height: 22px !important;
  fill: none !important;
  stroke: #000 !important;
  display: block !important;
}

/* Cart drawer — base */
html body #cart-drawer.pd-cart-drawer {
  position: fixed !important;
  top: 0 !important; right: 0 !important; bottom: 0 !important; left: auto !important;
  height: 100dvh !important;
  background: #fff !important;
  z-index: 99999 !important;
  display: flex !important;
  flex-direction: column !important;
  overflow: hidden !important;
  box-shadow: -4px 0 20px rgba(0,0,0,.12) !important;
  transform: translate3d(100%, 0, 0) !important;
  transition: transform .34s cubic-bezier(.4,0,.2,1) !important;
}
html body #cart-drawer.pd-cart-drawer.active,
html body #cart-drawer.pd-cart-drawer.open {
  transform: translate3d(0, 0, 0) !important;
}
html body #cart-drawer-overlay.pd-cart-overlay {
  position: fixed !important;
  inset: 0 !important;
  background: rgba(29,30,32,.2) !important;
  z-index: 99998 !important;
  opacity: 0 !important;
  pointer-events: none !important;
  transition: opacity .3s ease !important;
}
html body #cart-drawer-overlay.pd-cart-overlay.active {
  opacity: 1 !important;
  pointer-events: all !important;
}
.pd-cart-drawer-header {
  flex-shrink: 0 !important;
  height: 72px !important;
  padding: 0 20px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  border-bottom: 1px solid #eee !important;
}
.pd-cart-drawer-items {
  flex: 1 1 auto !important;
  overflow-y: auto !important;
  padding: 18px 20px 0 !important;
  -webkit-overflow-scrolling: touch !important;
}
.pd-cart-subtotal {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  font-size: 15px !important;
  font-weight: 700 !important;
  margin: 0 0 6px !important;
}
.pd-cart-checkout {
  display: block !important;
  width: 100% !important;
  padding: 13px 18px !important;
  background: #18181b !important;
  color: #fff !important;
  border-radius: 6px !important;
  text-align: center !important;
  font-size: 14px !important;
  font-weight: 600 !important;
  text-decoration: none !important;
}
.pd-cart-drawer-footer {
  flex-shrink: 0 !important;
  padding: 14px 20px 12px !important;
  border-top: 1px solid #dedede !important;
}

/* Menú hamburguesa negro — base */
#offcanvas,
#offcanvas .ct-panel-inner,
#offcanvas .ct-panel-content,
#offcanvas .ct-panel-content-inner {
  background: #000 !important;
  color: #fff !important;
}
#offcanvas nav[data-id="mobile-menu"] a.ct-menu-link,
#offcanvas .ct-menu a {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  color: #fff !important;
  font-weight: 700 !important;
  letter-spacing: 2.4px !important;
  text-transform: uppercase !important;
  text-decoration: none !important;
  padding: 18px 0 !important;
  border-bottom: 1px solid rgba(255,255,255,.14) !important;
  transition: color .22s ease, padding-left .22s ease !important;
}
#offcanvas nav[data-id="mobile-menu"] a.ct-menu-link::after,
#offcanvas .ct-menu a::after { content: "→" !important; opacity: .72 !important; }
.pd-mobile-trust {
  margin-top: auto !important;
  padding-top: 26px !important;
  display: grid !important;
  gap: 12px !important;
}
.pd-mobile-trust-item {
  display: flex !important;
  align-items: center !important;
  gap: 10px !important;
  color: rgba(255,255,255,.86) !important;
  font-size: 12px !important;
  letter-spacing: 1.2px !important;
  text-transform: uppercase !important;
}
.pd-mobile-trust-item svg { width: 18px !important; height: 18px !important; stroke: #fff !important; }

/* Buscador tienda — base */
.pd-shop-search form {
  display: flex !important;
  border: 1.5px solid #000 !important;
  border-radius: 999px !important;
  overflow: hidden !important;
  height: 44px !important;
}
.pd-shop-search input[type="search"] {
  flex: 1 !important;
  border: none !important;
  padding: 0 18px !important;
  font-size: 14px !important;
  outline: none !important;
}
.pd-shop-search button {
  width: 52px !important;
  background: #000 !important;
  color: #fff !important;
  border: none !important;
  cursor: pointer !important;
}

/* Hero /bolsos/ — base */
.pd-shop-collection-hero {
  width: 100vw !important;
  max-width: none !important;
  margin-left: calc(50% - 50vw) !important;
  background: #000 !important;
  color: #fff !important;
  text-align: center !important;
}
.pd-shop-collection-inner h1 {
  font-family: "Playfair Display", serif !important;
  color: #fff !important;
  margin: 0 0 18px !important;
  line-height: .98 !important;
}
.pd-shop-collection-inner span {
  display: block !important;
  font-size: 11px !important;
  letter-spacing: 2.8px !important;
  color: rgba(255,255,255,.74) !important;
  text-transform: uppercase !important;
  margin-bottom: 14px !important;
}
.pd-shop-collection-inner p {
  color: rgba(255,255,255,.82) !important;
  line-height: 1.8 !important;
  margin: 0 auto !important;
}

/* Colección homepage — base */
.pd-collection-showcase {
  width: 100vw !important;
  max-width: none !important;
  margin-left: calc(50% - 50vw) !important;
  background: #fff !important;
  box-sizing: border-box !important;
}
.pd-collection-heading { text-align: center !important; }
.pd-collection-heading h2 {
  font-family: "Playfair Display", serif !important;
  color: #000 !important;
  line-height: 1 !important;
  margin: 0 0 12px !important;
}
.pd-collection-heading p { color: #444 !important; font-size: 14px !important; margin: 0 !important; }
.pd-collection-layout { box-sizing: border-box !important; overflow: hidden !important; }
.pd-collection-media img {
  width: 100% !important;
  height: 100% !important;
  object-fit: cover !important;
  display: block !important;
}
.pd-brand-row {
  display: flex !important;
  justify-content: space-between !important;
  align-items: center !important;
  padding: 20px 0 !important;
  border-bottom: 1px solid #ddd7cf !important;
  color: #000 !important;
  text-decoration: none !important;
}
.pd-brand-row strong { display: block !important; font-family: "Playfair Display", serif !important; color: #000 !important; }
.pd-brand-row span span { display: block !important; color: #555 !important; margin-top: 5px !important; font-size: 13px !important; }
.pd-collection-btn {
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  background: #000 !important;
  color: #fff !important;
  border-radius: 999px !important;
  text-decoration: none !important;
  font-size: 12px !important;
  font-weight: 700 !important;
  letter-spacing: 1.8px !important;
}

/* Productos — estado base para animación */
.woocommerce ul.products li.product {
  display: flex !important;
  flex-direction: column !important;
  opacity: 0;
  transform: translate3d(0, 22px, 0);
  transition: opacity .55s ease, transform .55s ease !important;
}
.woocommerce ul.products li.product.pd-product-visible {
  opacity: 1;
  transform: translate3d(0,0,0);
}
.woocommerce ul.products li.product a img {
  width: 100% !important;
  object-fit: contain !important;
  background: #f4f4f4 !important;
  box-sizing: border-box !important;
  transition: transform .28s ease !important;
}
.woocommerce ul.products li.product .woocommerce-loop-product__title {
  font-family: "Playfair Display", serif !important;
  color: #000 !important;
  text-align: center !important;
}
.woocommerce ul.products li.product .price { color: #000 !important; text-align: center !important; }
.woocommerce ul.products li.product .button {
  background: #000 !important;
  color: #fff !important;
  border-radius: 999px !important;
  text-align: center !important;
  text-transform: uppercase !important;
  border: none !important;
  align-self: center !important;
  letter-spacing: 1.5px !important;
}

/* Mundo Prime — base */
.pd-mundo-prime-page { background: #fff !important; color: #000 !important; }
.pd-mundo-hero { background: #000 !important; color: #fff !important; text-align: center !important; }
.pd-mundo-hero h1 { font-family: "Playfair Display", serif !important; color: #fff !important; margin: 0 0 12px !important; line-height: 1 !important; }
.pd-mundo-hero p { margin: 0 !important; color: rgba(255,255,255,.78) !important; }
.pd-mundo-story { margin: 0 auto !important; text-align: center !important; }
.pd-mundo-story h2 { font-family: "Playfair Display", serif !important; color: #000 !important; }
.pd-mundo-story p { line-height: 1.8 !important; color: #333 !important; }
.pd-mundo-values { margin: 0 auto !important; display: grid !important; }
.pd-mundo-value { border: 1px solid #e5e0da !important; text-align: center !important; background: #fff !important; }
.pd-mundo-value svg { width: 28px !important; height: 28px !important; stroke: #000 !important; margin-bottom: 12px !important; }
.pd-mundo-value h3 { font-size: 13px !important; letter-spacing: 1.8px !important; margin: 0 0 8px !important; }
.pd-mundo-value p { font-size: 14px !important; color: #555 !important; margin: 0 !important; line-height: 1.6 !important; }
.pd-mundo-cta { text-align: center !important; }
.pd-mundo-cta a { display: inline-flex !important; background: #000 !important; color: #fff !important; border-radius: 999px !important; text-decoration: none !important; font-weight: 700 !important; letter-spacing: 1.8px !important; }


/* =============================================
   MOBILE / ANDROID — hasta 767px
   Touch, sin hover, botones grandes
   ============================================= */
@media (max-width: 767px) {

  /* Header mobile: mantener cuenta visible antes del carrito */
  .ct-header-account[data-id="account"] {
    display: flex !important;
    align-items: center !important;
    opacity: 1 !important;
    visibility: visible !important;
    pointer-events: auto !important;
  }
  .pd-mobile-account-server {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 28px !important;
    height: 28px !important;
    color: #000 !important;
    text-decoration: none !important;
  }
  .pd-mobile-account-server svg { width: 26px !important; height: 26px !important; stroke: #000 !important; fill: none !important; }

  /* Cart drawer ancho móvil */
  html body #cart-drawer.pd-cart-drawer { width: 80vw !important; max-width: 320px !important; }

  /* Menú hamburguesa móvil */
  #offcanvas { --side-panel-width: min(86vw, 340px) !important; }
  #offcanvas nav[data-id="mobile-menu"] a.ct-menu-link,
  #offcanvas .ct-menu a { font-size: 16px !important; letter-spacing: 2px !important; min-height: 52px !important; }

  /* Hero /bolsos/ móvil */
  .pd-shop-collection-hero { padding: 48px 20px 52px !important; }
  .pd-shop-collection-inner h1 { font-size: 46px !important; }
  .pd-shop-collection-inner p { font-size: 14px !important; max-width: 100% !important; }

  /* Colección homepage móvil — apilado vertical */
  .pd-collection-showcase { padding: 48px 16px 56px !important; }
  .pd-collection-heading { margin: 0 auto 24px !important; }
  .pd-collection-heading h2 { font-size: 30px !important; }
  .pd-collection-layout {
    grid-template-columns: 1fr !important;
    border: 1px solid #e3ded6 !important;
    background: #f8f5f1 !important;
  }
  .pd-collection-media,
  .pd-collection-media img { min-height: 280px !important; max-height: 280px !important; }
  .pd-collection-content { padding: 24px 20px 28px !important; }
  .pd-brand-row strong { font-size: 18px !important; }
  .pd-brand-arrow { font-size: 22px !important; }
  .pd-collection-btn { width: 100% !important; padding: 14px 20px !important; margin-top: 24px !important; }

  /* Productos móvil — 2 columnas */
  .woocommerce ul.products {
    display: grid !important;
    grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
    gap: 20px 12px !important;
    padding: 0 14px 80px !important;
    margin: 0 !important;
  }
  .woocommerce ul.products li.product { width: 100% !important; max-width: 100% !important; float: none !important; margin: 0 !important; }
  .woocommerce ul.products li.product a img { height: 170px !important; min-height: 170px !important; max-height: 170px !important; padding: 8px !important; }
  .woocommerce ul.products li.product .woocommerce-loop-product__title { font-size: 11px !important; min-height: 34px !important; line-height: 1.35 !important; }
  .woocommerce ul.products li.product .price { font-size: 12px !important; }
  .woocommerce ul.products li.product .button { font-size: 9px !important; padding: 9px 10px !important; max-width: 130px !important; margin: 8px auto 0 !important; letter-spacing: 1px !important; min-height: 38px !important; }
  /* Ocultar marcas en cards — ensucian en pantalla pequeña */
  .woocommerce ul.products li.product .entry-meta,
  .woocommerce ul.products li.product .meta-categories { display: none !important; }

  /* Buscador móvil — ancho completo */
  .pd-shop-search { width: 100% !important; margin: 0 0 14px !important; }
  .pd-shop-search form { max-width: 100% !important; }
  .woocommerce .woocommerce-result-count,
  .woocommerce .woocommerce-ordering { display: block !important; width: 100% !important; margin: 0 0 12px !important; float: none !important; }
  .woocommerce .woocommerce-ordering select { width: 100% !important; }

  /* Mundo Prime móvil */
  .pd-mundo-hero { padding: 64px 20px 70px !important; }
  .pd-mundo-hero h1 { font-size: 48px !important; }
  .pd-mundo-hero p { font-size: 14px !important; }
  .pd-mundo-story { width: calc(100vw - 36px) !important; padding: 48px 0 36px !important; }
  .pd-mundo-story h2 { font-size: 26px !important; margin: 0 0 18px !important; }
  .pd-mundo-story p { font-size: 15px !important; }
  .pd-mundo-values { width: calc(100vw - 36px) !important; grid-template-columns: 1fr !important; gap: 12px !important; padding: 0 0 32px !important; }
  .pd-mundo-value { padding: 22px 18px !important; }
  .pd-mundo-cta { padding: 0 20px 60px !important; }
  .pd-mundo-cta a { padding: 14px 28px !important; font-size: 11px !important; }
}


/* =============================================
   TABLET — 768px a 999px
   Puede ser touch, layout intermedio, 2-3 col
   ============================================= */
@media (min-width: 768px) and (max-width: 999px) {

  /* Header — ícono cuenta visible pero no fijo */
  .ct-header-account[data-id="account"] {
    position: fixed !important;
    top: 18px !important;
    right: 80px !important;
    z-index: 10000 !important;
    display: flex !important;
    opacity: 1 !important;
    visibility: visible !important;
  }
  .pd-mobile-account-server { display: inline-flex !important; width: 28px !important; height: 28px !important; }

  /* Cart drawer tablet */
  html body #cart-drawer.pd-cart-drawer { width: 60vw !important; max-width: 380px !important; }

  /* Menú hamburguesa tablet */
  #offcanvas { --side-panel-width: 420px !important; }
  #offcanvas nav[data-id="mobile-menu"] a.ct-menu-link,
  #offcanvas .ct-menu a { font-size: 17px !important; letter-spacing: 2.2px !important; }

  /* Hero /bolsos/ tablet */
  .pd-shop-collection-hero { padding: 58px 28px 62px !important; }
  .pd-shop-collection-inner h1 { font-size: 58px !important; }
  .pd-shop-collection-inner p { font-size: 15px !important; max-width: 560px !important; }

  /* Colección homepage tablet — apilado vertical */
  .pd-collection-showcase { padding: 58px 22px 66px !important; }
  .pd-collection-heading { margin: 0 auto 30px !important; }
  .pd-collection-heading h2 { font-size: 36px !important; }
  .pd-collection-layout { grid-template-columns: 1fr !important; border: 1px solid #e3ded6 !important; background: #f8f5f1 !important; }
  .pd-collection-media,
  .pd-collection-media img { min-height: 360px !important; max-height: 360px !important; }
  .pd-collection-content { padding: 32px 28px 36px !important; }
  .pd-brand-row strong { font-size: 21px !important; }
  .pd-collection-btn { width: 100% !important; padding: 14px 24px !important; margin-top: 28px !important; }

  /* Productos tablet — 3 columnas */
  .woocommerce ul.products {
    display: grid !important;
    grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
    gap: 28px 18px !important;
    padding: 0 22px 60px !important;
  }
  .woocommerce ul.products li.product { width: 100% !important; float: none !important; margin: 0 !important; }
  .woocommerce ul.products li.product a img { height: 220px !important; min-height: 220px !important; max-height: 220px !important; padding: 10px !important; }
  .woocommerce ul.products li.product .woocommerce-loop-product__title { font-size: 13px !important; }
  .woocommerce ul.products li.product .button { font-size: 10px !important; padding: 10px 14px !important; max-width: 160px !important; margin: 8px auto 0 !important; }
  .woocommerce ul.products li.product .entry-meta,
  .woocommerce ul.products li.product .meta-categories { display: none !important; }

  /* Buscador tablet */
  .pd-shop-search { width: 100% !important; margin: 0 0 14px !important; }
  .woocommerce .woocommerce-result-count,
  .woocommerce .pd-shop-search,
  .woocommerce .woocommerce-ordering { display: block !important; width: 100% !important; float: none !important; margin: 0 0 12px !important; }
  .woocommerce .pd-shop-search form { max-width: 100% !important; }
  .woocommerce .woocommerce-ordering select { width: 100% !important; }

  /* Mundo Prime tablet */
  .pd-mundo-hero { padding: 76px 28px 82px !important; }
  .pd-mundo-hero h1 { font-size: 62px !important; }
  .pd-mundo-story { width: calc(100vw - 56px) !important; padding: 58px 0 44px !important; }
  .pd-mundo-story h2 { font-size: 32px !important; }
  .pd-mundo-values { width: calc(100vw - 56px) !important; grid-template-columns: 1fr !important; padding: 0 0 38px !important; }
  .pd-mundo-cta { padding: 0 28px 70px !important; }
}


/* =============================================
   DESKTOP / PC — ≥1000px
   Mouse, hover activo, layouts de 2 col, amplio
   ============================================= */
@media (min-width: 1000px) {

  /* Header — cuenta en posición normal del header */
  .pd-mobile-account-server { display: none !important; }
  .ct-account-item:hover svg,
  .ct-cart-item:hover svg { opacity: .7 !important; }

  /* Cart drawer desktop */
  html body #cart-drawer.pd-cart-drawer { width: 360px !important; max-width: 360px !important; }

  /* Menú hamburguesa desktop */
  #offcanvas { --side-panel-width: 420px !important; }
  #offcanvas nav[data-id="mobile-menu"] a.ct-menu-link,
  #offcanvas .ct-menu a { font-size: 18px !important; }

  /* Hero /bolsos/ desktop */
  .pd-shop-collection-hero { padding: 72px 24px 76px !important; }
  .pd-shop-collection-inner h1 { font-size: clamp(52px, 7vw, 82px) !important; }
  .pd-shop-collection-inner p { font-size: 16px !important; max-width: 620px !important; }

  /* Colección homepage desktop — 2 columnas lado a lado */
  .pd-collection-showcase { padding: 82px max(24px, calc((100vw - 1120px) / 2)) 92px !important; }
  .pd-collection-heading { margin: 0 auto 42px !important; }
  .pd-collection-heading h2 { font-size: 46px !important; }
  .pd-collection-layout {
    width: min(1080px, 100%) !important;
    margin: 0 auto !important;
    display: grid !important;
    grid-template-columns: minmax(0, 1.05fr) minmax(340px, .95fr) !important;
    border: 1px solid #e3ded6 !important;
    background: #f8f5f1 !important;
    box-shadow: 0 24px 60px rgba(0,0,0,.08) !important;
  }
  .pd-collection-media { min-height: 500px !important; }
  .pd-collection-media img { min-height: 500px !important; }
  .pd-collection-content { padding: 58px !important; }
  .pd-brand-row strong { font-size: 25px !important; }
  .pd-brand-arrow { font-size: 28px !important; }
  .pd-collection-btn { margin-top: 34px !important; padding: 15px 32px !important; }

  /* Productos desktop — hover activo */
  .woocommerce ul.products li.product a img { height: 320px !important; padding: 14px !important; }
  .woocommerce ul.products li.product:hover img { transform: scale(1.025) !important; }
  .woocommerce ul.products li.product .woocommerce-loop-product__title { font-size: 15px !important; }
  .woocommerce ul.products li.product .price { font-size: 14px !important; }
  .woocommerce ul.products li.product .button { font-size: 11px !important; padding: 10px 20px !important; }
  .woocommerce ul.products li.product .button:hover { background: #333 !important; transform: translateY(-1px) !important; }

  /* Buscador desktop — inline */
  .woocommerce .woocommerce-result-count {
    display: inline-flex !important;
    align-items: center !important;
    height: 44px !important;
    margin: 0 18px 24px 0 !important;
    float: none !important;
    vertical-align: middle !important;
  }
  .woocommerce .pd-shop-search {
    display: inline-flex !important;
    align-items: center !important;
    vertical-align: middle !important;
    margin: 0 24px 24px 0 !important;
  }
  .woocommerce .pd-shop-search form { height: 44px !important; max-width: 360px !important; }
  .woocommerce .woocommerce-ordering {
    float: right !important;
    display: inline-flex !important;
    align-items: center !important;
    margin: 0 0 24px 18px !important;
    height: 44px !important;
  }
  .woocommerce .woocommerce-ordering select { height: 44px !important; min-width: 220px !important; }

  /* Mundo Prime desktop */
  .pd-mundo-hero { padding: 94px 24px 100px !important; }
  .pd-mundo-hero h1 { font-size: clamp(52px, 7vw, 84px) !important; }
  .pd-mundo-hero p { font-size: 16px !important; }
  .pd-mundo-story { width: min(920px, calc(100vw - 44px)) !important; padding: 76px 0 56px !important; }
  .pd-mundo-story h2 { font-size: 38px !important; margin: 0 0 24px !important; }
  .pd-mundo-story p { font-size: 17px !important; }
  .pd-mundo-values { width: min(1040px, calc(100vw - 44px)) !important; grid-template-columns: repeat(3, 1fr) !important; gap: 18px !important; padding: 0 0 46px !important; }
  .pd-mundo-value { padding: 30px 24px !important; }
  .pd-mundo-cta { padding: 0 24px 82px !important; }
  .pd-mundo-cta a { padding: 15px 34px !important; font-size: 12px !important; }
}
</style>
<?php }, 999);

/* ---------- 10. JS MAESTRO ---------- */
add_action('wp_footer', function() { ?>
<script id="pd-master-js">
(function(){
  /* Detectar tipo de dispositivo */
  var isMobile = function(){ return window.innerWidth <= 767; };
  var isTablet = function(){ return window.innerWidth >= 768 && window.innerWidth <= 999; };
  var isDesktop = function(){ return window.innerWidth >= 1000; };

  /* Productos fadeIn con IntersectionObserver */
  function animateProducts(){
    var items = document.querySelectorAll('.woocommerce ul.products li.product');
    if (!items.length) return;
    /* Delay escalonado según dispositivo */
    var delayStep = isMobile() ? 40 : isTablet() ? 50 : 60;
    items.forEach(function(el, i){ el.style.transitionDelay = Math.min(i * delayStep, 400) + 'ms'; });
    if (!('IntersectionObserver' in window)){
      items.forEach(function(el){ el.classList.add('pd-product-visible'); });
      return;
    }
    var obs = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if (e.isIntersecting){ e.target.classList.add('pd-product-visible'); obs.unobserve(e.target); }
      });
    }, { threshold: isMobile() ? 0.05 : 0.12 });
    items.forEach(function(el){ obs.observe(el); });
  }

  /* Menú hamburguesa enriquecido */
  function enhanceMobileMenu(){
    var panel = document.querySelector('#offcanvas .ct-panel-content-inner');
    if (!panel || panel.dataset.pdMenu === '1') return;
    panel.dataset.pdMenu = '1';
    /* Cabecera */
    var head = document.createElement('div');
    head.className = 'pd-mobile-menu-head';
    head.innerHTML = '<strong>PRIME DROP</strong><button class="pd-mobile-menu-close" type="button">Cerrar ×</button>';
    panel.insertBefore(head, panel.firstChild);
    head.querySelector('.pd-mobile-menu-close').addEventListener('click', function(){
      var c = document.querySelector('#offcanvas .ct-toggle-close');
      if (c) c.click();
    });
    /* Agregar políticas al menú */
    var nav = panel.querySelector('nav[data-id="mobile-menu"] ul, .mobile-menu ul, .ct-menu');
    if (nav && !nav.querySelector('.pd-policy-link')){
      [['POLÍTICA DE PRIVACIDAD', '/politica-de-privacidad/'], ['POLÍTICA DE REEMBOLSO', '/politica-de-reembolso/']].forEach(function(item){
        var li = document.createElement('li');
        li.className = 'menu-item pd-policy-link';
        li.innerHTML = '<a class="ct-menu-link" href="' + item[1] + '">' + item[0] + '</a>';
        nav.appendChild(li);
      });
    }
    /* Trust badges */
    var trust = document.createElement('div');
    trust.className = 'pd-mobile-trust';
    trust.innerHTML =
      '<div class="pd-mobile-trust-item"><svg viewBox="0 0 24 24" fill="none"><path d="M20 6 9 17l-5-5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg><span>Productos originales</span></div>' +
      '<div class="pd-mobile-trust-item"><svg viewBox="0 0 24 24" fill="none"><path d="M3 7h11v10H3zM14 11h3l3 3v3h-6z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><circle cx="7" cy="18" r="1.7" stroke="currentColor" stroke-width="1.7"/><circle cx="17" cy="18" r="1.7" stroke="currentColor" stroke-width="1.7"/></svg><span>Envíos a Colombia</span></div>' +
      '<div class="pd-mobile-trust-item"><svg viewBox="0 0 24 24" fill="none"><path d="M12 3 5 6v5c0 4.4 2.9 7.4 7 9 4.1-1.6 7-4.6 7-9V6z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/></svg><span>Pago seguro</span></div>';
    panel.appendChild(trust);
  }

  /* Reconstruir colección homepage si Elementor la sobreescribe */
  function rebuildCollection(){
    var s = document.querySelector('.pd-categories, .pd-collection-showcase');
    if (!s || s.dataset.pdCollectionReady === '1') return;
    s.dataset.pdCollectionReady = '1';
    s.className = 'pd-collection-showcase';
    s.innerHTML =
      '<div class="pd-collection-heading"><h2>NUESTRA COLECCIÓN</h2><p>Bolsos originales Michael Kors, Steve Madden y Tommy Hilfiger</p></div>' +
      '<div class="pd-collection-layout">' +
        '<div class="pd-collection-media"><img src="/wp-content/uploads/2026/05/bolsos-categoria-scaled.jpg" alt="Bolsos Prime Drop"></div>' +
        '<div class="pd-collection-content">' +
          '<a class="pd-brand-row" href="/bolsos/"><span><strong>MICHAEL KORS</strong><span>15 estilos disponibles</span></span><em class="pd-brand-arrow">→</em></a>' +
          '<a class="pd-brand-row" href="/bolsos/"><span><strong>STEVE MADDEN</strong><span>10 estilos disponibles</span></span><em class="pd-brand-arrow">→</em></a>' +
          '<a class="pd-brand-row" href="/bolsos/"><span><strong>TOMMY HILFIGER</strong><span>3 estilos disponibles</span></span><em class="pd-brand-arrow">→</em></a>' +
          '<a class="pd-collection-btn" href="/bolsos/">VER TODA LA COLECCIÓN</a>' +
        '</div>' +
      '</div>';
  }

  /* Scroll lock carrito — solo mobile y tablet touch */
  function initCartScrollLock(){
    var drawer = document.querySelector('#cart-drawer, .cart-drawer');
    if (!drawer) return;
    var locked = false, savedY = 0;
    function shouldLock(){ return isMobile() || isTablet(); }
    function lock(){
      if (locked || !shouldLock()) return;
      savedY = window.pageYOffset || 0;
      document.body.style.cssText += ';position:fixed;top:-' + savedY + 'px;left:0;right:0;width:100%;overflow:hidden';
      document.documentElement.style.overflow = 'hidden';
      locked = true;
    }
    function unlock(){
      if (!locked) return;
      var y = Math.abs(parseInt(document.body.style.top || '0')) || savedY || 0;
      ['position','top','left','right','width','overflow'].forEach(function(p){ document.body.style[p] = ''; });
      document.documentElement.style.overflow = '';
      locked = false;
      requestAnimationFrame(function(){ window.scrollTo(0, y); });
    }
    function sync(){
      if (!shouldLock()){ unlock(); return; }
      (drawer.classList.contains('active') || drawer.classList.contains('open')) ? lock() : unlock();
    }
    new MutationObserver(sync).observe(drawer, { attributes: true, attributeFilter: ['class'] });
    document.addEventListener('click', function(){ setTimeout(sync, 0); }, true);
    window.addEventListener('resize', sync);
  }

  function init(){
    animateProducts();
    enhanceMobileMenu();
    rebuildCollection();
    initCartScrollLock();
  }

  document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', init) : init();
  window.addEventListener('load', init);
  setTimeout(init, 700);
})();
</script>
<?php }, 999);

/* ============================================================
   FIN PRIME DROP ELITE — MASTER BLOCK v2.0
   ============================================================ */

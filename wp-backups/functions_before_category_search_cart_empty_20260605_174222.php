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

add_action('init', function() {
    $flag = 'pd_lscwp_purge_home_carousel_20260603_v3';
    if (get_option($flag) === 'done') return;

    if (class_exists('LiteSpeed_Cache_API') && method_exists('LiteSpeed_Cache_API', 'purge_all')) {
        LiteSpeed_Cache_API::purge_all();
    }

    do_action('litespeed_purge_all');
    update_option($flag, 'done', false);
}, 1);

/* ---------- 1. FOOTER VIDEO ---------- */
if (!function_exists('primedrop_footer_video_optimized_markup')) {
    function primedrop_footer_video_optimized_markup() {
        return '';
    }
}
if (!function_exists('primedrop_footer_video_optimize_output')) {
    function primedrop_footer_video_optimize_output($html) {
        $pattern = '#<video\s+class="footer-video-bg"[^>]*>\s*<source\s+src="https://videos\.pexels\.com/video-files/3571264/[^"]*"[^>]*>\s*</video>#i';
        return preg_replace($pattern, '', $html);
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

add_filter('woocommerce_product_add_to_cart_text', function() { return 'AÑADIR A LA BOLSA'; });
add_filter('woocommerce_product_single_add_to_cart_text', function() { return 'AÑADIR A LA BOLSA'; });
add_filter('gettext', function($translated, $text, $domain) {
    $map = array(
        'Añadir al carrito' => 'AÑADIR A LA BOLSA',
        'Add to cart' => 'AÑADIR A LA BOLSA',
        'Add to Cart' => 'AÑADIR A LA BOLSA',
    );
    return isset($map[$translated]) ? $map[$translated] : (isset($map[$text]) ? $map[$text] : $translated);
}, 20, 3);

/* /bolsos/: mostrar todos los bolsos en una sola pagina */
function pd_is_bolsos_context() {
    if (is_admin()) return false;
    if (function_exists('is_page') && is_page('bolsos')) return true;
    if (function_exists('is_product_category') && is_product_category('bolsos')) return true;
    $path = isset($_SERVER['REQUEST_URI']) ? trim(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH), '/') : '';
    return $path === 'bolsos';
}

add_filter('loop_shop_per_page', function($per_page) {
    return pd_is_bolsos_context() ? 999 : $per_page;
}, 999);

add_filter('woocommerce_shortcode_products_query', function($query_args, $atts, $type) {
    if (pd_is_bolsos_context()) {
        $query_args['posts_per_page'] = 999;
        $query_args['limit'] = 999;
        $query_args['paginate'] = false;
        $query_args['paged'] = 1;
    }
    return $query_args;
}, 999, 3);

add_action('woocommerce_product_query', function($query) {
    if (pd_is_bolsos_context()) {
        $query->set('posts_per_page', 999);
        $query->set('paged', 1);
    }
}, 999);

add_action('pre_get_posts', function($query) {
    if (!is_admin() && $query->is_main_query() && pd_is_bolsos_context()) {
        $query->set('posts_per_page', 999);
        $query->set('paged', 1);
    }
}, 999);

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
        if (strpos($html, 'class="ct-account-item pd-mobile-account-server"') !== false) return $html;
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
        $html = preg_replace('/<section class="pd-page-hero">[\s\S]*?<\/section>\s*/i', '', $html, 1);
        $html = preg_replace('/<section class="pd-shop-collection-hero">[\s\S]*?<\/section>\s*/i', '', $html, 1);
        if (strpos($html, '<section class="pd-luxium-collection-head"') !== false) return $html;
        $head = '<section class="pd-luxium-collection-head"><div class="pd-luxium-collection-inner"><span>COLECCIÓN PRIME DROP</span><h1>BOLSOS</h1><p>Bolsos originales Michael Kors, Steve Madden y Tommy Hilfiger seleccionados para Colombia.</p><div class="pd-luxium-trust-row"><span>Productos originales</span><span>Compras seguras</span><span>Envíos a Colombia</span></div></div></section>';
        return preg_replace('/(<section[^>]*elementor-element-0a7c205[^>]*>)/i', $head . '$1', $html, 1);
    });
}, 1);

/* ---------- 8. SECCIÓN COLECCIÓN HOMEPAGE ---------- */
if (!function_exists('prime_drop_collection_showcase_markup')) {
    function prime_drop_collection_showcase_markup() {
        return '';
    }
}
add_action('template_redirect', function() {
    if (is_admin()) return;
    $is_home = is_front_page() || is_home();
    ob_start(function($html) use ($is_home) {
        if ($is_home) {
            $html = preg_replace('/<section\b(?=[^>]*\bpd-categories\b)[^>]*>[\s\S]*?<\/section>/i', prime_drop_collection_showcase_markup(), $html, 1);
            $html = preg_replace('/<section\b(?=[^>]*\bpd-collection-showcase\b)[^>]*>[\s\S]*?<\/section>/i', '', $html, 1);
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

/* Cart drawer — estilo builder anterior */
html body #cart-drawer.pd-cart-drawer {
  position: fixed !important;
  top: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
  left: auto !important;
  height: 100dvh !important;
  max-height: 100dvh !important;
  background: #fff !important;
  z-index: 99999 !important;
  display: flex !important;
  flex-direction: column !important;
  overflow: hidden !important;
  box-shadow: -4px 0 20px rgba(0,0,0,.12) !important;
  transform: translate3d(100%, 0, 0) !important;
  transition: transform .36s cubic-bezier(.4,0,.2,1) !important;
}
html body #cart-drawer.pd-cart-drawer.active,
html body #cart-drawer.pd-cart-drawer.open {
  transform: translate3d(0, 0, 0) !important;
}
html body #cart-drawer-overlay.pd-cart-overlay {
  position: fixed !important;
  inset: 0 !important;
  background: rgba(0,0,0,.45) !important;
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
  background: #fff !important;
}
.pd-cart-drawer-header h3 {
  margin: 0 !important;
  color: #111 !important;
  font-family: 'Playfair Display', serif !important;
  font-size: 16px !important;
  font-weight: 700 !important;
  letter-spacing: 3px !important;
  text-transform: uppercase !important;
}
.pd-cart-drawer-close {
  width: 32px !important;
  height: 32px !important;
  min-width: 32px !important;
  padding: 0 !important;
  border: 0 !important;
  background: transparent !important;
  color: #111 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  font-size: 21px !important;
  line-height: 1 !important;
  cursor: pointer !important;
}
.pd-cart-drawer-items {
  flex: 1 1 auto !important;
  min-height: 0 !important;
  overflow-y: auto !important;
  overflow-x: hidden !important;
  padding: 18px 20px 0 !important;
  -webkit-overflow-scrolling: touch !important;
  scrollbar-width: none !important;
  -ms-overflow-style: none !important;
}
.pd-cart-drawer-items::-webkit-scrollbar {
  width: 0 !important;
  height: 0 !important;
  display: none !important;
}
.pd-cart-empty {
  margin: 0 !important;
  padding: 2px 0 !important;
  color: #111 !important;
  font-size: 18px !important;
  line-height: 1.45 !important;
}
.pd-cart-item {
  display: grid !important;
  grid-template-columns: 76px minmax(0, 1fr) 22px !important;
  gap: 12px !important;
  align-items: start !important;
  padding: 15px 0 !important;
  border-bottom: 1px solid #eee !important;
}
.pd-cart-item-thumb,
.pd-cart-item-thumb img {
  display: block !important;
}
.pd-cart-item-thumb img {
  width: 76px !important;
  height: 76px !important;
  min-width: 76px !important;
  object-fit: contain !important;
  object-position: center !important;
  background: #fafafa !important;
  border: 1px solid #e5e5e5 !important;
  border-radius: 5px !important;
}
.pd-cart-item-info {
  min-width: 0 !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 6px !important;
}
.pd-cart-item-name {
  color: #111 !important;
  font-family: 'Playfair Display', serif !important;
  font-size: 14px !important;
  font-weight: 700 !important;
  line-height: 1.25 !important;
  text-decoration: none !important;
}
.pd-cart-item-meta {
  margin: -2px 0 0 !important;
  color: #777 !important;
  font-size: 12px !important;
  line-height: 1.35 !important;
}
.pd-cart-item-bottom {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  gap: 10px !important;
  margin-top: 2px !important;
}
.pd-cart-qty {
  display: inline-flex !important;
  align-items: center !important;
  gap: 7px !important;
  color: #111 !important;
  font-size: 13px !important;
  line-height: 1 !important;
}
.pd-cart-qty span {
  min-width: 10px !important;
  text-align: center !important;
}
.pd-cart-drawer .pd-cart-qty-btn,
.pd-cart-drawer button.pd-cart-qty-btn {
  width: 18px !important;
  height: 18px !important;
  min-width: 18px !important;
  min-height: 18px !important;
  padding: 0 !important;
  border: 1px solid #d8d8d8 !important;
  border-radius: 50% !important;
  background: #fff !important;
  color: #111 !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  font-size: 12px !important;
  font-weight: 500 !important;
  line-height: 1 !important;
  letter-spacing: 0 !important;
  text-transform: none !important;
  cursor: pointer !important;
}
.pd-cart-drawer .pd-cart-qty-btn:hover {
  background: #111 !important;
  border-color: #111 !important;
  color: #fff !important;
}
.pd-cart-item-price {
  color: #111 !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  white-space: nowrap !important;
}
.pd-cart-item-remove {
  width: 22px !important;
  height: 22px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  color: #999 !important;
  text-decoration: none !important;
}
.pd-cart-item-remove:hover {
  color: #111 !important;
}
.pd-cart-drawer-footer {
  flex-shrink: 0 !important;
  padding: 16px 20px calc(15px + env(safe-area-inset-bottom)) !important;
  border-top: 1px solid #dedede !important;
  background: #fff !important;
}
.pd-cart-subtotal {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  gap: 16px !important;
  margin: 0 0 8px !important;
  color: #111 !important;
  font-size: 15px !important;
  font-weight: 800 !important;
  letter-spacing: 1px !important;
  text-transform: uppercase !important;
}
.pd-cart-subtotal span:last-child {
  text-align: right !important;
  white-space: nowrap !important;
}
.pd-cart-shipping-note {
  margin: 0 0 17px !important;
  color: #222 !important;
  font-size: 14px !important;
  line-height: 1.45 !important;
}
.pd-cart-checkout {
  width: 100% !important;
  min-height: 54px !important;
  padding: 14px 18px !important;
  background: #000 !important;
  color: #fff !important;
  border: 0 !important;
  border-radius: 999px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  text-align: center !important;
  font-size: 13px !important;
  font-weight: 800 !important;
  letter-spacing: 1.8px !important;
  line-height: 1.2 !important;
  text-transform: uppercase !important;
  text-decoration: none !important;
  box-sizing: border-box !important;
}
.pd-cart-checkout:hover {
  background: #222 !important;
  color: #fff !important;
}
.pd-cart-secure {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 6px !important;
  margin-top: 8px !important;
  color: #333 !important;
  font-size: 13px !important;
  line-height: 1.2 !important;
}
.pd-cart-secure svg {
  flex: 0 0 auto !important;
  width: 13px !important;
  height: 13px !important;
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
  opacity: 1 !important;
  transform: translate3d(0, 0, 0) !important;
  transition: transform .28s ease, opacity .28s ease !important;
}
.woocommerce ul.products li.product.pd-product-visible {
  animation: pdFadeInUp .55s ease both;
}
@keyframes pdFadeInUp {
  from {
    opacity: 0;
    transform: translate3d(0, 18px, 0);
  }
  to {
    opacity: 1;
    transform: translate3d(0, 0, 0);
  }
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
    width: 26px !important;
    height: 26px !important;
    min-width: 26px !important;
    margin: 0 4px 0 0 !important;
    color: #000 !important;
    text-decoration: none !important;
    opacity: 1 !important;
    visibility: visible !important;
    pointer-events: auto !important;
  }
  .pd-mobile-account-server svg { width: 24px !important; height: 24px !important; stroke: #000 !important; fill: none !important; display: block !important; }
  [data-device="mobile"] .ct-header-cart,
  [data-device="mobile"] .ct-cart-item,
  .pd-mobile-account-server + .ct-header-cart,
  .pd-mobile-account-server + [data-id="cart"] {
    margin-left: 0 !important;
  }

  /* Cart drawer móvil: pantalla completa como el builder anterior */
  html body #cart-drawer.pd-cart-drawer { width: 100vw !important; max-width: 100vw !important; }

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
  .pd-mobile-account-server {
    position: fixed !important;
    top: 35px !important;
    right: 96px !important;
    z-index: 10000 !important;
    display: inline-flex !important;
    width: 28px !important;
    height: 28px !important;
    margin: 0 !important;
  }
  [data-device="mobile"] .ct-header-cart,
  [data-device="mobile"] .ct-cart-item {
    margin-left: 0 !important;
  }

  /* Cart drawer tablet */
  html body #cart-drawer.pd-cart-drawer { width: 420px !important; max-width: 88vw !important; }

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
  html body #cart-drawer.pd-cart-drawer { width: 380px !important; max-width: 380px !important; }

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

/* =============================================
   /BOLSOS/ — estilo colección Luxium
   ============================================= */
@media (max-width: 767px) {
  body.page-id-547 .elementor-element-bc942e4,
  body.page-id-547 .pd-page-hero,
  body.page-id-547 .pd-shop-collection-hero,
  body.page-id-547 .elementor-element-2fc690d {
    display: none !important;
  }

  body.page-id-547 .pd-luxium-collection-head {
    width: 100% !important;
    padding: 30px 18px 18px !important;
    text-align: center !important;
    background: #ffffff !important;
    box-sizing: border-box !important;
  }

  body.page-id-547 .pd-luxium-collection-inner span {
    display: block !important;
    font-family: Inter, sans-serif !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    color: #777777 !important;
    text-transform: uppercase !important;
    margin-bottom: 8px !important;
  }

  body.page-id-547 .pd-luxium-collection-inner h1 {
    font-family: "Playfair Display", serif !important;
    font-size: 34px !important;
    line-height: 1 !important;
    color: #000000 !important;
    margin: 0 0 10px !important;
    text-transform: uppercase !important;
  }

  body.page-id-547 .pd-luxium-collection-inner p {
    width: min(420px, 100%) !important;
    margin: 0 auto 14px !important;
    color: #444444 !important;
    font-family: Inter, sans-serif !important;
    font-size: 13px !important;
    line-height: 1.6 !important;
  }

  body.page-id-547 .pd-luxium-trust-row {
    display: flex !important;
    flex-wrap: wrap !important;
    justify-content: center !important;
    gap: 8px 14px !important;
    font-family: Inter, sans-serif !important;
    font-size: 9px !important;
    font-weight: 700 !important;
    letter-spacing: 1.3px !important;
    text-transform: uppercase !important;
    color: #777777 !important;
  }

  body.page-id-547 .pd-luxium-trust-row span {
    margin: 0 !important;
    color: #777777 !important;
  }

  body.page-id-547 .elementor-element-0a7c205 {
    padding: 0 0 64px !important;
  }

  body.page-id-547 .elementor-element-0a7c205 > .elementor-container,
  body.page-id-547 .elementor-element-9884376,
  body.page-id-547 .elementor-element-9884376 > .elementor-widget-wrap {
    width: 100% !important;
    max-width: none !important;
    display: block !important;
  }

  body.page-id-547 .woo-listing-top {
    display: grid !important;
    grid-template-columns: 1fr !important;
    gap: 12px !important;
    padding: 14px 16px 18px !important;
    margin: 0 !important;
    border-top: 1px solid #eeeeee !important;
    border-bottom: 1px solid #eeeeee !important;
  }

  body.page-id-547 .woo-listing-top .woocommerce-result-count {
    display: none !important;
  }

  body.page-id-547 .pd-shop-search,
  body.page-id-547 .woocommerce-ordering {
    width: 100% !important;
    margin: 0 !important;
    float: none !important;
  }

  body.page-id-547 .pd-shop-search form,
  body.page-id-547 .woocommerce-ordering select {
    width: 100% !important;
    max-width: none !important;
    height: 42px !important;
  }

  body.page-id-547 .woocommerce ul.products {
    display: grid !important;
    grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
    gap: 26px 14px !important;
    padding: 22px 14px 80px !important;
    margin: 0 !important;
  }

  body.page-id-547 .woocommerce ul.products li.product {
    width: auto !important;
    max-width: none !important;
    min-height: 0 !important;
    height: auto !important;
    overflow: visible !important;
    float: none !important;
    margin: 0 !important;
    text-align: center !important;
  }

  body.page-id-547 .woocommerce ul.products li.product figure {
    margin: 0 0 12px !important;
    background: #f5f5f5 !important;
    overflow: hidden !important;
  }

  body.page-id-547 .woocommerce ul.products li.product a img {
    height: 168px !important;
    min-height: 168px !important;
    max-height: 168px !important;
    padding: 10px !important;
    object-fit: contain !important;
  }

  body.page-id-547 .woocommerce ul.products li.product .woocommerce-loop-product__title {
    min-height: 34px !important;
    margin: 0 0 8px !important;
    font-family: Inter, sans-serif !important;
    font-size: 10.5px !important;
    font-weight: 700 !important;
    letter-spacing: .6px !important;
    line-height: 1.35 !important;
    text-transform: uppercase !important;
  }

  body.page-id-547 .woocommerce ul.products li.product .price {
    margin: 0 0 10px !important;
    font-family: Inter, sans-serif !important;
    font-size: 12px !important;
    font-weight: 500 !important;
  }

  body.page-id-547 .woocommerce ul.products li.product .entry-meta,
  body.page-id-547 .woocommerce ul.products li.product .meta-categories {
    display: none !important;
  }

  body.page-id-547 .woocommerce ul.products li.product .button {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    min-height: 36px !important;
    width: auto !important;
    max-width: 132px !important;
    padding: 9px 12px !important;
    margin: 0 auto !important;
    border-radius: 999px !important;
    font-size: 9px !important;
    letter-spacing: 1px !important;
    line-height: 1.25 !important;
  }
}

@media (min-width: 768px) and (max-width: 999px) {
  body.page-id-547 .elementor-element-bc942e4,
  body.page-id-547 .pd-page-hero,
  body.page-id-547 .pd-shop-collection-hero,
  body.page-id-547 .elementor-element-2fc690d {
    display: none !important;
  }

  body.page-id-547 .pd-luxium-collection-head {
    padding: 38px 28px 22px !important;
    text-align: center !important;
    background: #ffffff !important;
  }

  body.page-id-547 .pd-luxium-collection-inner h1 {
    font-family: "Playfair Display", serif !important;
    font-size: 42px !important;
    color: #000000 !important;
    margin: 0 0 10px !important;
    text-transform: uppercase !important;
  }

  body.page-id-547 .pd-luxium-collection-inner > span,
  body.page-id-547 .pd-luxium-trust-row {
    font-family: Inter, sans-serif !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    color: #777777 !important;
    text-transform: uppercase !important;
  }

  body.page-id-547 .pd-luxium-collection-inner p {
    width: min(620px, 100%) !important;
    margin: 8px auto 16px !important;
    color: #444444 !important;
    font-size: 14px !important;
    line-height: 1.7 !important;
  }

  body.page-id-547 .pd-luxium-trust-row {
    display: flex !important;
    justify-content: center !important;
    gap: 22px !important;
  }

  body.page-id-547 .elementor-element-0a7c205 {
    padding: 0 22px 72px !important;
  }

  body.page-id-547 .elementor-element-0a7c205 > .elementor-container,
  body.page-id-547 .elementor-element-9884376,
  body.page-id-547 .elementor-element-9884376 > .elementor-widget-wrap {
    width: 100% !important;
    max-width: none !important;
    display: block !important;
  }

  body.page-id-547 .woo-listing-top {
    display: grid !important;
    grid-template-columns: 1fr 1fr !important;
    gap: 14px !important;
    align-items: center !important;
    padding: 16px 0 20px !important;
    margin: 0 0 8px !important;
    border-top: 1px solid #eeeeee !important;
    border-bottom: 1px solid #eeeeee !important;
  }

  body.page-id-547 .woo-listing-top .woocommerce-result-count {
    grid-column: 1 / -1 !important;
    text-align: center !important;
    margin: 0 !important;
    font-family: Inter, sans-serif !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 1.2px !important;
    text-transform: uppercase !important;
  }

  body.page-id-547 .pd-shop-search,
  body.page-id-547 .woocommerce-ordering {
    width: 100% !important;
    margin: 0 !important;
    float: none !important;
  }

  body.page-id-547 .pd-shop-search form,
  body.page-id-547 .woocommerce-ordering select {
    width: 100% !important;
    max-width: none !important;
    height: 44px !important;
  }

  body.page-id-547 .woocommerce ul.products {
    display: grid !important;
    grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
    gap: 34px 20px !important;
    padding: 26px 0 80px !important;
    margin: 0 !important;
  }

  body.page-id-547 .woocommerce ul.products li.product {
    width: auto !important;
    max-width: none !important;
    height: auto !important;
    min-height: 0 !important;
    overflow: visible !important;
    float: none !important;
    margin: 0 !important;
    text-align: center !important;
  }

  body.page-id-547 .woocommerce ul.products li.product a img {
    height: 220px !important;
    min-height: 220px !important;
    max-height: 220px !important;
    padding: 14px !important;
    object-fit: contain !important;
  }

  body.page-id-547 .woocommerce ul.products li.product .entry-meta,
  body.page-id-547 .woocommerce ul.products li.product .meta-categories {
    display: none !important;
  }
}

@media (min-width: 1000px) {
  body.page-id-547 .elementor-element-bc942e4,
  body.page-id-547 .pd-page-hero,
  body.page-id-547 .pd-shop-collection-hero,
  body.page-id-547 .elementor-element-2fc690d {
    display: none !important;
  }

  body.page-id-547 .pd-luxium-collection-head {
    width: min(1240px, calc(100vw - 70px)) !important;
    margin: 0 auto !important;
    padding: 36px 0 24px !important;
    text-align: center !important;
    background: #ffffff !important;
  }

  body.page-id-547 .pd-luxium-collection-inner > span {
    display: block !important;
    margin-bottom: 10px !important;
    font-family: Inter, sans-serif !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 2.4px !important;
    color: #777777 !important;
    text-transform: uppercase !important;
  }

  body.page-id-547 .pd-luxium-collection-inner h1 {
    margin: 0 0 10px !important;
    font-family: "Playfair Display", serif !important;
    font-size: 48px !important;
    line-height: 1 !important;
    color: #000000 !important;
    text-transform: uppercase !important;
  }

  body.page-id-547 .pd-luxium-collection-inner p {
    width: min(640px, 100%) !important;
    margin: 0 auto 16px !important;
    font-family: Inter, sans-serif !important;
    font-size: 14px !important;
    line-height: 1.7 !important;
    color: #444444 !important;
  }

  body.page-id-547 .pd-luxium-trust-row {
    display: flex !important;
    justify-content: center !important;
    gap: 30px !important;
    font-family: Inter, sans-serif !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 1.8px !important;
    color: #777777 !important;
    text-transform: uppercase !important;
  }

  body.page-id-547 .elementor-element-0a7c205 {
    padding: 0 max(35px, calc((100vw - 1240px) / 2)) 86px !important;
  }

  body.page-id-547 .elementor-element-0a7c205 > .elementor-container,
  body.page-id-547 .elementor-element-9884376,
  body.page-id-547 .elementor-element-9884376 > .elementor-widget-wrap {
    width: 100% !important;
    max-width: none !important;
    display: block !important;
  }

  body.page-id-547 .woo-listing-top {
    display: grid !important;
    grid-template-columns: minmax(180px, 1fr) minmax(260px, 360px) minmax(210px, 240px) !important;
    gap: 24px !important;
    align-items: center !important;
    padding: 16px 0 !important;
    margin: 0 0 32px !important;
    border-top: 1px solid #eeeeee !important;
    border-bottom: 1px solid #eeeeee !important;
  }

  body.page-id-547 .woo-listing-top .woocommerce-result-count {
    margin: 0 !important;
    font-family: Inter, sans-serif !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 1.4px !important;
    text-transform: uppercase !important;
    color: #000000 !important;
    white-space: nowrap !important;
  }

  body.page-id-547 .pd-shop-search,
  body.page-id-547 .woocommerce-ordering {
    width: 100% !important;
    margin: 0 !important;
    float: none !important;
  }

  body.page-id-547 .pd-shop-search form {
    width: 100% !important;
    max-width: 360px !important;
    height: 42px !important;
    margin: 0 auto !important;
    border-radius: 0 !important;
  }

  body.page-id-547 .woocommerce-ordering {
    justify-self: end !important;
  }

  body.page-id-547 .woocommerce-ordering select {
    width: 240px !important;
    height: 42px !important;
    border: 1px solid #dddddd !important;
    border-radius: 0 !important;
    font-family: Inter, sans-serif !important;
    font-size: 12px !important;
  }

  body.page-id-547 .woocommerce ul.products {
    display: grid !important;
    grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
    gap: 42px 28px !important;
    padding: 0 0 90px !important;
    margin: 0 !important;
    justify-content: stretch !important;
    align-items: start !important;
  }

  body.page-id-547 .woocommerce ul.products li.product {
    width: auto !important;
    max-width: none !important;
    flex: none !important;
    height: auto !important;
    min-height: 0 !important;
    overflow: visible !important;
    float: none !important;
    margin: 0 !important;
    text-align: center !important;
  }

  body.page-id-547 .woocommerce ul.products li.product figure {
    margin: 0 0 16px !important;
    background: #f5f5f5 !important;
    overflow: hidden !important;
  }

  body.page-id-547 .woocommerce ul.products li.product a img {
    width: 100% !important;
    height: 270px !important;
    min-height: 270px !important;
    max-height: 270px !important;
    padding: 18px !important;
    object-fit: contain !important;
    background: #f5f5f5 !important;
  }

  body.page-id-547 .woocommerce ul.products li.product .woocommerce-loop-product__title {
    min-height: 38px !important;
    margin: 0 0 10px !important;
    font-family: Inter, sans-serif !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    letter-spacing: .6px !important;
    line-height: 1.35 !important;
    text-transform: uppercase !important;
  }

  body.page-id-547 .woocommerce ul.products li.product .price {
    height: auto !important;
    min-height: 0 !important;
    margin: 0 0 12px !important;
    font-family: Inter, sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    color: #000000 !important;
  }

  body.page-id-547 .woocommerce ul.products li.product .entry-meta,
  body.page-id-547 .woocommerce ul.products li.product .meta-categories,
  body.page-id-547 .woocommerce ul.products li.product [class*="brand"] {
    display: none !important;
  }

  body.page-id-547 .woocommerce ul.products li.product .button {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: auto !important;
    min-width: 138px !important;
    max-width: none !important;
    min-height: 36px !important;
    padding: 10px 18px !important;
    margin: 0 auto !important;
    border-radius: 999px !important;
    font-size: 10px !important;
    letter-spacing: 1.3px !important;
    line-height: 1 !important;
    opacity: 0 !important;
    transform: translateY(6px) !important;
    transition: opacity .22s ease, transform .22s ease, background .22s ease !important;
  }

  body.page-id-547 .woocommerce ul.products li.product:hover .button {
    opacity: 1 !important;
    transform: translateY(0) !important;
  }
}

/* /bolsos/ — controles separados por dispositivo */
@media (max-width: 999px) {
  body.page-id-547 .woo-listing-top {
    grid-template-columns: 1fr !important;
    justify-items: center !important;
  }

  body.page-id-547 .woocommerce-ordering {
    display: none !important;
  }

  body.page-id-547 .pd-shop-search {
    width: min(420px, 100%) !important;
    margin: 0 auto !important;
  }

  body.page-id-547 .pd-shop-search form {
    width: 100% !important;
    max-width: none !important;
  }
}

@media (min-width: 768px) and (max-width: 999px) {
  body.page-id-547 .woocommerce ul.products li.product .button {
    min-width: 172px !important;
    max-width: 190px !important;
    min-height: 42px !important;
    padding: 10px 14px !important;
    font-size: 9.5px !important;
    letter-spacing: 1px !important;
    line-height: 1 !important;
    white-space: nowrap !important;
  }
}

/* HOME — Productos destacados estilo Luxium / mas vendidos */
body.page-id-14 .pd-best-section {
  width: 100% !important;
  background: #ffffff !important;
  padding: 18px 0 72px !important;
  overflow: hidden !important;
}

body.page-id-14 .pd-best-title {
  margin: 0 0 34px !important;
  text-align: center !important;
  font-family: Inter, sans-serif !important;
  font-size: 24px !important;
  line-height: 1.2 !important;
  font-weight: 800 !important;
  letter-spacing: .2px !important;
  color: #000000 !important;
  text-transform: uppercase !important;
}

body.page-id-14 .pd-best-carousel-wrap {
  position: relative !important;
  width: min(100%, 1200px) !important;
  margin: 0 auto !important;
  padding: 0 42px !important;
  box-sizing: border-box !important;
}

body.page-id-14 .pd-best-carousel-wrap ul.products {
  display: flex !important;
  flex-wrap: nowrap !important;
  align-items: stretch !important;
  justify-content: flex-start !important;
  gap: 30px !important;
  width: 100% !important;
  margin: 0 !important;
  padding: 0 !important;
  overflow-x: auto !important;
  overflow-y: hidden !important;
  scroll-snap-type: x mandatory !important;
  scroll-behavior: smooth !important;
  scrollbar-width: none !important;
  -ms-overflow-style: none !important;
}

body.page-id-14 .pd-best-carousel-wrap ul.products::-webkit-scrollbar {
  width: 0 !important;
  height: 0 !important;
  display: none !important;
}

body.page-id-14 .pd-best-carousel-wrap ul.products li.product {
  position: relative !important;
  flex: 0 0 270px !important;
  width: 270px !important;
  max-width: 270px !important;
  min-height: 0 !important;
  height: auto !important;
  margin: 0 !important;
  float: none !important;
  overflow: visible !important;
  text-align: center !important;
  scroll-snap-align: start !important;
  background: #ffffff !important;
}

body.page-id-14 .pd-best-carousel-wrap ul.products li.product a.woocommerce-loop-product__link {
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  text-decoration: none !important;
}

body.page-id-14 .pd-best-carousel-wrap ul.products li.product a img,
body.page-id-14 .pd-best-carousel-wrap ul.products li.product img {
  width: 268px !important;
  height: 268px !important;
  min-height: 268px !important;
  max-height: 268px !important;
  padding: 10px !important;
  object-fit: contain !important;
  object-position: center !important;
  background: #ffffff !important;
  display: block !important;
  transition: transform .26s ease !important;
}

body.page-id-14 .pd-best-carousel-wrap ul.products li.product:hover img {
  transform: scale(1.03) !important;
}

body.page-id-14 .pd-best-carousel-wrap ul.products li.product .woocommerce-loop-product__title {
  min-height: 38px !important;
  margin: 16px auto 8px !important;
  max-width: 230px !important;
  font-family: Inter, sans-serif !important;
  font-size: 13px !important;
  font-weight: 800 !important;
  line-height: 1.38 !important;
  letter-spacing: 0 !important;
  color: #252525 !important;
  text-align: center !important;
  text-transform: uppercase !important;
}

body.page-id-14 .pd-best-carousel-wrap ul.products li.product .price {
  min-height: 22px !important;
  margin: 0 !important;
  color: #222222 !important;
  font-family: Inter, sans-serif !important;
  font-size: 15px !important;
  font-weight: 500 !important;
  text-align: center !important;
}

body.page-id-14 .pd-best-carousel-wrap ul.products li.product .entry-meta,
body.page-id-14 .pd-best-carousel-wrap ul.products li.product .meta-categories,
body.page-id-14 .pd-best-carousel-wrap ul.products li.product [class*="brand"] {
  display: none !important;
}

body.page-id-14 .pd-best-carousel-wrap ul.products li.product .button {
  opacity: 0 !important;
  transform: translateY(8px) !important;
  pointer-events: none !important;
  margin: 12px auto 0 !important;
  min-width: 150px !important;
  min-height: 38px !important;
  padding: 10px 16px !important;
  border-radius: 999px !important;
  background: #000000 !important;
  color: #ffffff !important;
  font-size: 10px !important;
  letter-spacing: 1.4px !important;
  transition: opacity .2s ease, transform .2s ease !important;
}

body.page-id-14 .pd-best-carousel-wrap ul.products li.product:hover .button {
  opacity: 1 !important;
  transform: translateY(0) !important;
  pointer-events: auto !important;
}

body.page-id-14 .pd-best-arrow {
  position: absolute !important;
  top: 146px !important;
  z-index: 3 !important;
  width: 35px !important;
  height: 35px !important;
  border: 0 !important;
  border-radius: 0 !important;
  background: rgba(0,0,0,.78) !important;
  color: #ffffff !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 0 !important;
  font-size: 0 !important;
  line-height: 1 !important;
  cursor: pointer !important;
  display: none !important;
}

body.page-id-14 .pd-best-arrow::before {
  font-size: 26px !important;
  line-height: 1 !important;
  font-family: Arial, sans-serif !important;
}

body.page-id-14 .pd-best-prev { left: 0 !important; }
body.page-id-14 .pd-best-next { right: 0 !important; }
body.page-id-14 .pd-best-prev::before { content: "<" !important; }
body.page-id-14 .pd-best-next::before { content: ">" !important; }

body.page-id-14 .pd-best-offer {
  position: absolute !important;
  top: 0 !important;
  left: 50% !important;
  transform: translateX(-50%) !important;
  z-index: 2 !important;
  background: #14a514 !important;
  color: #ffffff !important;
  font-size: 11px !important;
  font-weight: 800 !important;
  line-height: 1 !important;
  padding: 4px 7px !important;
  text-transform: uppercase !important;
}

@media (max-width: 767px) {
  body.page-id-14 .pd-best-section {
    padding: 10px 0 52px !important;
  }

  body.page-id-14 .pd-best-title {
    font-size: 18px !important;
    margin-bottom: 30px !important;
  }

  body.page-id-14 .pd-best-carousel-wrap {
    width: 100% !important;
    padding: 0 15px !important;
  }

  body.page-id-14 .pd-best-carousel-wrap ul.products {
    gap: 10px !important;
  }

  body.page-id-14 .pd-best-carousel-wrap ul.products li.product {
    flex: 0 0 calc(50vw - 20px) !important;
    width: calc(50vw - 20px) !important;
    max-width: 175px !important;
  }

  body.page-id-14 .pd-best-carousel-wrap ul.products li.product a img,
  body.page-id-14 .pd-best-carousel-wrap ul.products li.product img {
    width: 100% !important;
    height: 173px !important;
    min-height: 173px !important;
    max-height: 173px !important;
    padding: 6px !important;
  }

  body.page-id-14 .pd-best-carousel-wrap ul.products li.product .woocommerce-loop-product__title {
    max-width: 160px !important;
    min-height: 40px !important;
    margin-top: 14px !important;
    font-size: 12px !important;
    line-height: 1.35 !important;
  }

  body.page-id-14 .pd-best-carousel-wrap ul.products li.product .price {
    font-size: 14px !important;
  }

  body.page-id-14 .pd-best-carousel-wrap ul.products li.product .button {
    display: none !important;
  }

  body.page-id-14 .pd-best-arrow {
    top: 148px !important;
    width: 30px !important;
    height: 30px !important;
    background: rgba(0,0,0,.58) !important;
  }

  body.page-id-14 .pd-best-prev { left: 10px !important; }
  body.page-id-14 .pd-best-next { right: 10px !important; }
}

/* Producto y checkout — quitar hero vacío de Blocksy */
.single-product .hero-section,
.woocommerce-checkout .hero-section,
body.page-id-752 .hero-section {
  min-height: 0 !important;
  height: auto !important;
  margin-bottom: 0 !important;
  padding: 14px 0 0 !important;
}

.single-product .hero-section .entry-header,
.woocommerce-checkout .hero-section .entry-header,
body.page-id-752 .hero-section .entry-header {
  min-height: 0 !important;
  height: auto !important;
  margin: 0 !important;
  padding: 0 !important;
}

.single-product .ct-container-full,
.woocommerce-checkout .ct-container-full,
body.page-id-752 .ct-container-full {
  padding-top: 18px !important;
}

@media (max-width: 767px) {
  .single-product .hero-section,
  .woocommerce-checkout .hero-section,
  body.page-id-752 .hero-section {
    padding-top: 8px !important;
  }

  .single-product .ct-breadcrumbs {
    font-size: 10px !important;
    letter-spacing: .8px !important;
    padding: 0 20px !important;
  }

  .single-product .ct-container-full,
  .woocommerce-checkout .ct-container-full,
  body.page-id-752 .ct-container-full {
    padding-top: 16px !important;
    padding-bottom: 36px !important;
  }

  .single-product .product-entry-wrapper {
    margin-top: 0 !important;
  }
}

/* ============================================================
   PRIME DROP — AJUSTES COACH / HOME CLEANUP
   ============================================================ */

:root {
  --pd-heading-font: "Playfair Display", Georgia, serif;
  --pd-body-font: Inter, Lato, Arial, sans-serif;
}

body,
button,
input,
select,
textarea {
  font-family: var(--pd-body-font) !important;
}

h1, h2, h3, h4,
.elementor-heading-title,
.woocommerce-loop-product__title {
  font-family: var(--pd-heading-font) !important;
}

/* Hero home: estilo builder anterior, sin Comprar ya */
body.page-id-14 .pd-promo-strip {
  background: #000000 !important;
  color: #ffffff !important;
  text-align: center !important;
  font-family: var(--pd-body-font) !important;
  font-size: 14px !important;
  font-weight: 700 !important;
  line-height: 1 !important;
  padding: 9px 16px !important;
}

body.page-id-14 .pd-hero {
  display: flex !important;
  align-items: center !important;
}

body.page-id-14 .pd-hero .pd-kicker {
  display: block !important;
  margin: 0 0 18px !important;
  color: #ffffff !important;
  font-family: var(--pd-heading-font) !important;
  font-size: clamp(15px, 1.3vw, 18px) !important;
  font-weight: 800 !important;
  letter-spacing: 0 !important;
  text-transform: uppercase !important;
}

body.page-id-14 .pd-hero .pd-hero-inner {
  width: min(44vw, 620px) !important;
  max-width: 620px !important;
  margin: 0 auto 0 clamp(86px, 9vw, 126px) !important;
  text-align: left !important;
  align-items: flex-start !important;
  transform: translateY(42px) !important;
}

body.page-id-14 .pd-hero h1 {
  max-width: 100% !important;
  margin-left: 0 !important;
  text-align: left !important;
  white-space: nowrap !important;
  font-size: clamp(62px, 6.2vw, 86px) !important;
  line-height: .96 !important;
}

body.page-id-14 .pd-hero p:not(.pd-kicker) {
  max-width: 100% !important;
  text-align: left !important;
  font-family: var(--pd-heading-font) !important;
  font-size: clamp(17px, 1.45vw, 20px) !important;
  font-weight: 700 !important;
  line-height: 1.35 !important;
}

body.page-id-14 .pd-hero .pd-btn,
body.page-id-14 .pd-hero .pd-btn-outline {
  border-radius: 25px !important;
  min-width: 174px !important;
  min-height: 50px !important;
}

/* Historia de marca después del video */
body.page-id-14 .pd-home-story-builder {
  width: min(1120px, calc(100vw - 48px)) !important;
  margin: 0 auto !important;
  padding: 78px 0 84px !important;
  display: grid !important;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr) !important;
  gap: clamp(56px, 9vw, 116px) !important;
  align-items: center !important;
  background: #ffffff !important;
}

body.page-id-14 .pd-story-left,
body.page-id-14 .pd-story-right {
  min-width: 0 !important;
}

body.page-id-14 .pd-story-left > p,
body.page-id-14 .pd-story-right p {
  margin: 0 !important;
  color: #252525 !important;
  font-family: var(--pd-heading-font) !important;
  font-size: 20px !important;
  line-height: 1.18 !important;
  letter-spacing: 0 !important;
}

body.page-id-14 .pd-story-logo {
  width: 230px !important;
  height: auto !important;
  margin: 34px 0 0 !important;
  display: block !important;
  object-fit: contain !important;
}

body.page-id-14 .pd-story-image {
  width: 100% !important;
  aspect-ratio: 1.55 / 1 !important;
  height: auto !important;
  display: block !important;
  object-fit: cover !important;
  border-radius: 20px !important;
}

body.page-id-14 .pd-story-copy {
  display: grid !important;
  gap: 28px !important;
  margin-top: 30px !important;
}

/* Quitar Quiénes Somos y banner antiguo del home */
body.page-id-14 .elementor-element-6f27344,
body.page-id-14 .elementor-element-9855adf,
body.page-id-14 .pd-about,
body.page-id-14 .about-section,
body.page-id-14 .quienes-somos-section {
  display: none !important;
}

body.page-id-14 .pd-home-benefits {
  width: min(1180px, calc(100vw - 36px)) !important;
  margin: 0 auto !important;
  padding: 64px 0 36px !important;
  display: grid !important;
  grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
  gap: 18px !important;
  background: #fff !important;
}

body.page-id-14 .pd-benefit-item {
  text-align: center !important;
  padding: 22px 12px !important;
  border: 1px solid #eeeeee !important;
  border-radius: 12px !important;
  background: #ffffff !important;
}

body.page-id-14 .pd-benefit-item svg {
  width: 28px !important;
  height: 28px !important;
  display: block !important;
  margin: 0 auto 12px !important;
  stroke: #000 !important;
}

body.page-id-14 .pd-benefit-item span {
  display: block !important;
  font-size: 12px !important;
  font-weight: 700 !important;
  letter-spacing: 1.4px !important;
  text-transform: uppercase !important;
  color: #000 !important;
}

body.page-id-14 .pd-home-bag-feature {
  display: none !important;
}

body.page-id-14 .pd-home-bag-feature img {
  display: none !important;
}

/* Categorías home */
.pd-collection-showcase {
  display: none !important;
}

body.page-id-14 .pd-categories,
body.page-id-14 .pd-collection-showcase,
body.page-id-14 .pd-category-grid,
body.page-id-14 .pd-collection-heading {
  display: none !important;
}

.pd-category-grid {
  width: min(1180px, calc(100vw - 36px)) !important;
  margin: 34px auto 0 !important;
  display: grid !important;
  grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
  gap: 18px !important;
}

.pd-category-card {
  display: block !important;
  color: #000 !important;
  text-decoration: none !important;
  border-radius: 12px !important;
  overflow: hidden !important;
  background: #f6f6f6 !important;
  transition: transform .25s ease, opacity .25s ease !important;
}

.pd-category-card:hover {
  transform: translateY(-3px) !important;
}

.pd-category-card img {
  width: 100% !important;
  aspect-ratio: 1 / 1 !important;
  height: auto !important;
  object-fit: cover !important;
  display: block !important;
}

.pd-category-card span {
  display: block !important;
  padding: 16px 10px 18px !important;
  background: #fff !important;
  text-align: center !important;
  font-size: 12px !important;
  font-weight: 800 !important;
  letter-spacing: 1.5px !important;
}

/* Destacadas: limpio, 4 productos, botones visibles */
body.page-id-14 .pd-home-featured-rebuilt,
body.page-id-14 .pd-best-section {
  width: min(1240px, calc(100vw - 32px)) !important;
  margin: 0 auto !important;
  padding: 24px 0 78px !important;
  overflow: hidden !important;
}

body.page-id-14 .pd-best-title,
body.page-id-14 .pd-products-title {
  margin: 0 0 32px !important;
  text-align: center !important;
  font-family: var(--pd-heading-font) !important;
  font-size: clamp(30px, 3.8vw, 48px) !important;
  line-height: 1.05 !important;
  letter-spacing: 0 !important;
  color: #000 !important;
  text-transform: uppercase !important;
}

body.page-id-14 .pd-best-arrow,
body.page-id-14 .pd-best-offer {
  display: none !important;
}

body.page-id-14 .pd-best-carousel-wrap ul.products,
body.page-id-14 .pd-home-featured-rebuilt ul.products {
  display: grid !important;
  grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
  gap: 28px !important;
  overflow: visible !important;
}

body.page-id-14 .pd-best-carousel-wrap ul.products li.product,
body.page-id-14 .pd-home-featured-rebuilt ul.products li.product {
  width: auto !important;
  max-width: none !important;
  flex: none !important;
  min-width: 0 !important;
}

body.page-id-14 .pd-best-carousel-wrap ul.products li.product a img,
body.page-id-14 .pd-home-featured-rebuilt ul.products li.product a img,
.woocommerce ul.products li.product a img,
.woocommerce ul.products li.product img {
  aspect-ratio: 1 / 1 !important;
  height: auto !important;
  min-height: 0 !important;
  max-height: none !important;
  object-fit: cover !important;
  border-radius: 12px !important;
}

body.page-id-14 .pd-best-carousel-wrap ul.products li.product .button,
body.page-id-14 .pd-home-featured-rebuilt ul.products li.product .button,
.woocommerce ul.products li.product .button {
  display: inline-flex !important;
  opacity: 1 !important;
  transform: none !important;
  pointer-events: auto !important;
  border-radius: 25px !important;
}

/* Bolsa/header: trazo más fino */
.ct-cart-item svg,
.ct-header-cart svg,
.ct-cart-content svg {
  stroke-width: 1.45 !important;
}

/* Producto individual: sin espacio inicial */
.single-product .entry-header,
.single-product .pd-page-hero,
.single-product .woocommerce-breadcrumb,
.single-product .ct-breadcrumbs {
  display: none !important;
}

.single-product .site-main {
  padding-top: 0 !important;
  margin-top: 0 !important;
}

.single-product .product-entry-wrapper,
.single-product div.product {
  margin-top: 0 !important;
  padding-top: 0 !important;
}

/* /bolsos/: sin título gigante, filtros visibles, buscador limpio */
body.page-id-547 .pd-luxium-collection-inner h1 {
  display: none !important;
}

body.page-id-547 .pd-luxium-collection-head {
  padding-top: 28px !important;
  padding-bottom: 18px !important;
}

body.page-id-547 .pd-brand-filter {
  width: min(760px, calc(100vw - 36px)) !important;
  margin: 18px auto 0 !important;
  display: flex !important;
  flex-wrap: wrap !important;
  justify-content: center !important;
  gap: 10px !important;
}

body.page-id-547 .pd-brand-filter a {
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  min-height: 36px !important;
  padding: 8px 18px !important;
  border: 1px solid #d8d8d8 !important;
  border-radius: 25px !important;
  color: #000 !important;
  background: #fff !important;
  text-decoration: none !important;
  font-size: 11px !important;
  font-weight: 700 !important;
  letter-spacing: 1.2px !important;
  text-transform: uppercase !important;
}

body.page-id-547 .pd-brand-filter a:hover {
  border-color: #000 !important;
}

body.page-id-547 .pd-shop-search form,
.pd-shop-search form {
  border-radius: 25px !important;
}

body.page-id-547 .woocommerce-pagination ul {
  border: none !important;
  display: flex !important;
  justify-content: center !important;
  gap: 8px !important;
}

body.page-id-547 .woocommerce-pagination a,
body.page-id-547 .woocommerce-pagination span {
  border-radius: 25px !important;
  border: 1px solid #ddd !important;
}

/* /bolsos/: quitar buscador y mantener botones siempre visibles */
body.page-id-547 .pd-shop-search {
  display: none !important;
}

body.page-id-547 .woo-listing-top {
  grid-template-columns: 1fr auto !important;
  align-items: center !important;
}

body.page-id-547 .woocommerce ul.products li.product .button,
body.page-id-547 .woocommerce ul.products li.product:hover .button {
  display: inline-flex !important;
  visibility: visible !important;
  opacity: 1 !important;
  transform: none !important;
  pointer-events: auto !important;
}

body.page-id-547 .woocommerce-pagination,
body.page-id-547 nav.woocommerce-pagination,
body.page-id-547 .ct-pagination,
body.page-id-547 .page-numbers {
  display: none !important;
}

body.page-id-547 .woocommerce-ordering {
  margin: 0 !important;
  width: auto !important;
}

body.page-id-547 .woocommerce-ordering select,
body.page-id-547 select.orderby {
  appearance: none !important;
  -webkit-appearance: none !important;
  min-width: 220px !important;
  height: 44px !important;
  padding: 0 46px 0 22px !important;
  border: 0 !important;
  border-radius: 25px !important;
  background-color: #000000 !important;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='%23ffffff' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E") !important;
  background-repeat: no-repeat !important;
  background-position: right 18px center !important;
  color: #ffffff !important;
  font-family: var(--pd-body-font) !important;
  font-size: 11px !important;
  font-weight: 800 !important;
  letter-spacing: 1.2px !important;
  text-transform: uppercase !important;
  box-shadow: none !important;
  cursor: pointer !important;
}

body.page-id-547 .woocommerce-ordering select:focus,
body.page-id-547 select.orderby:focus {
  outline: none !important;
  box-shadow: 0 0 0 2px rgba(0,0,0,.16) !important;
}

/* Ocultar solo la vista previa hover del carrito de Blocksy */
.ct-header-cart > .ct-cart-content {
  display: none !important;
}

/* Menú BOLSOS con submenu Hombre / Mujer */
.pd-bolsos-menu-parent {
  position: relative !important;
}

.pd-bolsos-menu-parent > .pd-bolsos-submenu {
  position: absolute !important;
  top: calc(100% + 14px) !important;
  left: 50% !important;
  z-index: 9999 !important;
  min-width: 190px !important;
  margin: 0 !important;
  padding: 10px 0 !important;
  list-style: none !important;
  background: #ffffff !important;
  border: 1px solid #eeeeee !important;
  border-radius: 8px !important;
  box-shadow: 0 14px 34px rgba(0,0,0,.12) !important;
  opacity: 0 !important;
  visibility: hidden !important;
  transform: translate(-50%, 8px) !important;
  transition: opacity .2s ease, transform .2s ease, visibility .2s ease !important;
}

.pd-bolsos-menu-parent:hover > .pd-bolsos-submenu,
.pd-bolsos-menu-parent:focus-within > .pd-bolsos-submenu,
.pd-bolsos-menu-parent.pd-submenu-open > .pd-bolsos-submenu {
  opacity: 1 !important;
  visibility: visible !important;
  transform: translate(-50%, 0) !important;
}

.pd-bolsos-submenu li {
  margin: 0 !important;
  padding: 0 !important;
  list-style: none !important;
}

.pd-bolsos-submenu a {
  display: block !important;
  padding: 11px 20px !important;
  color: #000000 !important;
  background: #ffffff !important;
  font-family: var(--pd-body-font) !important;
  font-size: 12px !important;
  font-weight: 700 !important;
  letter-spacing: 1.4px !important;
  text-decoration: none !important;
  text-transform: uppercase !important;
  white-space: nowrap !important;
}

.pd-bolsos-submenu a:hover {
  background: #f6f6f6 !important;
}

.pd-submenu-toggle {
  display: none !important;
}

/* /bolsos/: imagenes cuadradas con prioridad final */
body.page-id-547 .woocommerce ul.products li.product a.woocommerce-loop-product__link {
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
}

body.page-id-547 .woocommerce ul.products li.product a img,
body.page-id-547 .woocommerce ul.products li.product img,
body.page-id-547 .woocommerce-page ul.products li.product a img,
body.page-id-547 .woocommerce-page ul.products li.product img {
  width: 100% !important;
  aspect-ratio: 1 / 1 !important;
  object-fit: cover !important;
  object-position: center !important;
  border-radius: 12px !important;
  background: #f7f7f7 !important;
  padding: 0 !important;
  display: block !important;
  flex-shrink: 0 !important;
}

@media (min-width: 1000px) {
  body.page-id-547 .woocommerce ul.products li.product a img,
  body.page-id-547 .woocommerce ul.products li.product img,
  body.page-id-547 .woocommerce-page ul.products li.product a img,
  body.page-id-547 .woocommerce-page ul.products li.product img {
    height: 280px !important;
    min-height: 280px !important;
    max-height: 280px !important;
  }
}

@media (min-width: 768px) and (max-width: 999px) {
  body.page-id-547 .woocommerce ul.products li.product a img,
  body.page-id-547 .woocommerce ul.products li.product img,
  body.page-id-547 .woocommerce-page ul.products li.product a img,
  body.page-id-547 .woocommerce-page ul.products li.product img {
    height: 221px !important;
    min-height: 221px !important;
    max-height: 221px !important;
  }
}

@media (max-width: 767px) {
  body.page-id-547 .woocommerce ul.products li.product a img,
  body.page-id-547 .woocommerce ul.products li.product img,
  body.page-id-547 .woocommerce-page ul.products li.product a img,
  body.page-id-547 .woocommerce-page ul.products li.product img {
    height: calc(50vw - 31px) !important;
    min-height: calc(50vw - 31px) !important;
    max-height: calc(50vw - 31px) !important;
  }
}

/* DESTACADAS: siempre visible, sin flechas, cuatro productos cuando hay espacio */
body.page-id-14 .pd-best-carousel-wrap ul.products li.product .button {
  display: inline-flex !important;
  opacity: 1 !important;
  transform: none !important;
  pointer-events: auto !important;
  justify-content: center !important;
  align-items: center !important;
}

body.page-id-14 .pd-best-arrow {
  display: none !important;
}

body.page-id-14 .pd-best-carousel-wrap ul.products li.product a img,
body.page-id-14 .pd-best-carousel-wrap ul.products li.product img {
  object-fit: cover !important;
  border-radius: 12px !important;
}

@media (min-width: 1100px) {
  body.page-id-14 .pd-best-carousel-wrap ul.products li.product {
    flex-basis: 250px !important;
    width: 250px !important;
    max-width: 250px !important;
  }

  body.page-id-14 .pd-best-carousel-wrap ul.products li.product a img,
  body.page-id-14 .pd-best-carousel-wrap ul.products li.product img {
    width: 250px !important;
    height: 250px !important;
    min-height: 250px !important;
    max-height: 250px !important;
  }
}

/* Redondeo global */
.woocommerce ul.products li.product,
.product,
.elementor-widget-container,
input,
select,
textarea,
.wp-block-button__link,
.elementor-button,
button,
a.button,
input[type="submit"] {
  border-radius: 12px !important;
}

.wp-block-button__link,
.elementor-button,
.woocommerce a.button,
.woocommerce button.button,
.woocommerce input.button,
button,
a.button,
input[type="submit"] {
  border-radius: 25px !important;
}

input,
select,
textarea {
  border-radius: 25px !important;
}

/* Footer negro sólido, sin video y sin texto de redes */
.footer-video-bg,
.pd-footer video {
  display: none !important;
}

.pd-footer {
  background: #000 !important;
  color: #fff !important;
  overflow: hidden !important;
}

.pd-footer-main {
  width: min(1180px, calc(100vw - 48px)) !important;
  margin: 0 auto !important;
  display: grid !important;
  grid-template-columns: 1.2fr 1fr 1fr !important;
  gap: clamp(36px, 7vw, 92px) !important;
  align-items: start !important;
}

.pd-footer-column h3,
.pd-footer-column h4 {
  margin: 0 0 20px !important;
  color: #ffffff !important;
  font-family: var(--pd-heading-font) !important;
  letter-spacing: 1px !important;
}

.pd-footer-column p {
  margin: 0 0 12px !important;
  color: #ffffff !important;
  line-height: 1.65 !important;
}

.pd-footer::before {
  display: none !important;
}

.pd-footer a,
.pd-footer p,
.pd-footer li,
.pd-footer h3,
.pd-footer h4 {
  color: #fff !important;
}

.pd-footer-social-text {
  display: none !important;
}

.pd-social-icons {
  display: flex !important;
  gap: 12px !important;
}

.pd-footer-social-column .pd-social-icons {
  margin-top: 14px !important;
  justify-content: flex-start !important;
}

.pd-footer-links-removed,
.pd-footer .pd-footer-links {
  display: none !important;
}

.pd-social-icons a {
  width: 34px !important;
  height: 34px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  border: 1px solid rgba(255,255,255,.35) !important;
  border-radius: 50% !important;
}

.pd-social-icons svg {
  width: 17px !important;
  height: 17px !important;
  fill: #fff !important;
}

.pd-footer-newsletter {
  grid-column: 1 / -1 !important;
  width: min(520px, 100%) !important;
  margin: 28px auto 0 !important;
  text-align: center !important;
}

.pd-footer-newsletter h4 {
  margin: 0 0 14px !important;
  font-size: 13px !important;
  letter-spacing: 2px !important;
  text-transform: uppercase !important;
}

.pd-footer-newsletter p {
  margin: -4px 0 16px !important;
  color: rgba(255,255,255,.72) !important;
  text-align: center !important;
  font-size: 14px !important;
}

.pd-footer-newsletter form {
  display: flex !important;
  gap: 8px !important;
}

.pd-footer-newsletter input {
  flex: 1 !important;
  min-height: 44px !important;
  border: 1px solid rgba(255,255,255,.35) !important;
  background: transparent !important;
  color: #fff !important;
  padding: 0 18px !important;
}

.pd-footer-newsletter button {
  min-height: 44px !important;
  padding: 0 22px !important;
  background: #fff !important;
  color: #000 !important;
  border: none !important;
}

.pd-footer-bottom {
  width: min(1180px, calc(100vw - 48px)) !important;
  margin: 40px auto 0 !important;
  padding-top: 24px !important;
  border-top: 1px solid rgba(255,255,255,.18) !important;
  text-align: center !important;
  justify-content: center !important;
}

/* Instagram feed */
.pd-instagram-feed {
  width: min(1180px, calc(100vw - 36px)) !important;
  margin: 0 auto 76px !important;
  padding-top: 18px !important;
  text-align: center !important;
}

.pd-instagram-feed h2 {
  margin: 0 0 28px !important;
  font-family: var(--pd-heading-font) !important;
  font-size: clamp(28px, 3vw, 42px) !important;
}

.pd-instagram-grid {
  display: grid !important;
  grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
  gap: 14px !important;
}

.pd-instagram-grid a {
  display: block !important;
  border-radius: 12px !important;
  overflow: hidden !important;
}

.pd-instagram-grid img,
.pd-instagram-grid video {
  width: 100% !important;
  aspect-ratio: 1 / 1 !important;
  height: 100% !important;
  object-fit: cover !important;
  object-position: center !important;
  display: block !important;
}

@media (max-width: 767px) {
  body.page-id-14 .pd-promo-strip {
    font-size: 12px !important;
    padding: 8px 12px !important;
  }

  body.page-id-14 .pd-hero .pd-hero-inner {
    width: min(86vw, 360px) !important;
    max-width: 86vw !important;
    margin-left: 28px !important;
    text-align: left !important;
    transform: translateY(18px) !important;
  }

  body.page-id-14 .pd-hero h1 {
    white-space: normal !important;
    font-size: clamp(42px, 12vw, 52px) !important;
  }

  body.page-id-14 .pd-hero .pd-kicker {
    font-size: 13px !important;
    margin-bottom: 14px !important;
  }

  body.page-id-14 .pd-hero p:not(.pd-kicker) {
    font-size: 16px !important;
  }

  body.page-id-14 .pd-home-story-builder {
    width: min(100%, calc(100vw - 36px)) !important;
    padding: 50px 0 56px !important;
    grid-template-columns: 1fr !important;
    gap: 38px !important;
  }

  body.page-id-14 .pd-story-left > p,
  body.page-id-14 .pd-story-right p {
    font-size: 18px !important;
    line-height: 1.22 !important;
  }

  body.page-id-14 .pd-story-logo {
    width: 180px !important;
    margin-top: 26px !important;
  }

  body.page-id-14 .pd-story-image {
    border-radius: 14px !important;
  }

  body.page-id-14 .pd-story-copy {
    gap: 22px !important;
    margin-top: 24px !important;
  }

  body.page-id-14 .pd-home-benefits {
    grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
    padding: 42px 0 22px !important;
  }

  body.page-id-14 .pd-home-bag-feature {
    margin-bottom: 48px !important;
  }

  .pd-category-grid,
  body.page-id-14 .pd-best-carousel-wrap ul.products,
  body.page-id-14 .pd-home-featured-rebuilt ul.products {
    grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
  }

  .pd-instagram-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
  }

  .pd-footer-newsletter form {
    flex-direction: column !important;
  }

  .pd-footer-main {
    grid-template-columns: 1fr !important;
    gap: 34px !important;
    width: min(100%, calc(100vw - 44px)) !important;
  }

  #offcanvas .pd-bolsos-menu-parent {
    position: relative !important;
  }

  #offcanvas .pd-bolsos-menu-parent > a {
    padding-right: 44px !important;
  }

  #offcanvas .pd-bolsos-menu-parent > a::after {
    display: none !important;
  }

  #offcanvas .pd-submenu-toggle {
    position: absolute !important;
    top: 14px !important;
    right: 0 !important;
    z-index: 2 !important;
    width: 28px !important;
    min-width: 0 !important;
    height: 28px !important;
    min-height: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    border: 0 !important;
    border-radius: 50% !important;
    background: transparent !important;
    box-shadow: none !important;
    color: #ffffff !important;
    padding: 0 !important;
    outline: none !important;
    font-size: 14px !important;
    line-height: 1 !important;
    transition: transform .2s ease !important;
  }

  #offcanvas .pd-submenu-toggle:focus,
  #offcanvas .pd-submenu-toggle:hover {
    background: transparent !important;
    border: 0 !important;
    box-shadow: none !important;
    outline: none !important;
    color: #ffffff !important;
  }

  #offcanvas .pd-bolsos-menu-parent.pd-submenu-open > .pd-submenu-toggle {
    transform: rotate(180deg) !important;
  }

  #offcanvas .pd-bolsos-menu-parent > .pd-bolsos-submenu {
    position: static !important;
    min-width: 0 !important;
    margin: 0 !important;
    padding: 0 0 6px 16px !important;
    border: 0 !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    background: transparent !important;
    opacity: 1 !important;
    visibility: visible !important;
    transform: none !important;
    display: none !important;
  }

  #offcanvas .pd-bolsos-menu-parent.pd-submenu-open > .pd-bolsos-submenu {
    display: block !important;
  }

  #offcanvas .pd-bolsos-submenu a {
    padding: 10px 0 !important;
    color: rgba(255,255,255,.76) !important;
    background: transparent !important;
    border-bottom: 1px solid rgba(255,255,255,.08) !important;
    font-size: 12px !important;
  }
}

@media (min-width: 768px) and (max-width: 999px) {
  body.page-id-14 .pd-hero .pd-hero-inner {
    width: min(42vw, 420px) !important;
    max-width: 42vw !important;
    margin-left: 42px !important;
  }

  .pd-category-grid,
  body.page-id-14 .pd-best-carousel-wrap ul.products,
  body.page-id-14 .pd-home-featured-rebuilt ul.products {
    grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
    gap: 14px !important;
  }

  .pd-instagram-grid {
    grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
    gap: 14px !important;
  }

  #offcanvas .pd-bolsos-menu-parent {
    position: relative !important;
  }

  #offcanvas .pd-bolsos-menu-parent > a {
    padding-right: 44px !important;
  }

  #offcanvas .pd-bolsos-menu-parent > a::after {
    display: none !important;
  }

  #offcanvas .pd-submenu-toggle {
    position: absolute !important;
    top: 14px !important;
    right: 0 !important;
    z-index: 2 !important;
    width: 28px !important;
    min-width: 0 !important;
    height: 28px !important;
    min-height: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    border: 0 !important;
    border-radius: 50% !important;
    background: transparent !important;
    box-shadow: none !important;
    color: #ffffff !important;
    padding: 0 !important;
    outline: none !important;
    font-size: 14px !important;
    line-height: 1 !important;
  }

  #offcanvas .pd-submenu-toggle:focus,
  #offcanvas .pd-submenu-toggle:hover {
    background: transparent !important;
    border: 0 !important;
    box-shadow: none !important;
    outline: none !important;
    color: #ffffff !important;
  }

  #offcanvas .pd-bolsos-menu-parent > .pd-bolsos-submenu {
    position: static !important;
    min-width: 0 !important;
    margin: 0 !important;
    padding: 0 0 6px 16px !important;
    border: 0 !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    background: transparent !important;
    opacity: 1 !important;
    visibility: visible !important;
    transform: none !important;
    display: none !important;
  }

  #offcanvas .pd-bolsos-menu-parent.pd-submenu-open > .pd-bolsos-submenu {
    display: block !important;
  }

  #offcanvas .pd-bolsos-submenu a {
    padding: 10px 0 !important;
    color: rgba(255,255,255,.76) !important;
    background: transparent !important;
    border-bottom: 1px solid rgba(255,255,255,.08) !important;
    font-size: 12px !important;
  }
}

/* Submenu móvil/tablet BOLSOS: control limpio, sin heredar estilos de botones */
#offcanvas .pd-bolsos-menu-parent > a::after,
.ct-panel .pd-bolsos-menu-parent > a::after,
.ct-drawer-canvas .pd-bolsos-menu-parent > a::after {
  display: none !important;
  content: none !important;
}

#offcanvas .pd-submenu-toggle,
.ct-panel .pd-submenu-toggle,
.ct-drawer-canvas .pd-submenu-toggle {
  appearance: none !important;
  -webkit-appearance: none !important;
  position: absolute !important;
  top: 14px !important;
  right: 0 !important;
  z-index: 2 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  width: 24px !important;
  min-width: 24px !important;
  max-width: 24px !important;
  height: 24px !important;
  min-height: 24px !important;
  max-height: 24px !important;
  padding: 0 !important;
  margin: 0 !important;
  border: 0 !important;
  outline: 0 !important;
  box-shadow: none !important;
  background: transparent !important;
  background-image: none !important;
  border-radius: 0 !important;
  color: #ffffff !important;
  font-size: 14px !important;
  line-height: 1 !important;
  letter-spacing: 0 !important;
  text-indent: 0 !important;
  cursor: pointer !important;
}

#offcanvas .pd-submenu-toggle:hover,
#offcanvas .pd-submenu-toggle:focus,
.ct-panel .pd-submenu-toggle:hover,
.ct-panel .pd-submenu-toggle:focus,
.ct-drawer-canvas .pd-submenu-toggle:hover,
.ct-drawer-canvas .pd-submenu-toggle:focus {
  border: 0 !important;
  outline: 0 !important;
  box-shadow: none !important;
  background: transparent !important;
  color: #ffffff !important;
}

#offcanvas .pd-bolsos-menu-parent.pd-submenu-open > .pd-submenu-toggle,
.ct-panel .pd-bolsos-menu-parent.pd-submenu-open > .pd-submenu-toggle,
.ct-drawer-canvas .pd-bolsos-menu-parent.pd-submenu-open > .pd-submenu-toggle {
  transform: rotate(180deg) !important;
}

/* DESTACADAS: carrusel horizontal automatico estilo Luxium */
body.page-id-14 .pd-best-section,
body.page-id-14 .pd-home-featured-rebuilt {
  width: min(1240px, calc(100vw - 32px)) !important;
  overflow: hidden !important;
}

body.page-id-14 .pd-best-carousel-wrap {
  width: 100% !important;
  max-width: 1240px !important;
  margin: 0 auto !important;
  padding: 0 !important;
  overflow: hidden !important;
}

body.page-id-14 .pd-best-carousel-wrap ul.products,
body.page-id-14 .pd-home-featured-rebuilt ul.products {
  display: flex !important;
  flex-wrap: nowrap !important;
  align-items: stretch !important;
  justify-content: flex-start !important;
  grid-template-columns: none !important;
  gap: 28px !important;
  width: 100% !important;
  margin: 0 !important;
  padding: 0 !important;
  overflow-x: auto !important;
  overflow-y: hidden !important;
  scroll-snap-type: x mandatory !important;
  scroll-behavior: smooth !important;
  scrollbar-width: none !important;
  -ms-overflow-style: none !important;
}

body.page-id-14 .pd-best-carousel-wrap ul.products::-webkit-scrollbar,
body.page-id-14 .pd-home-featured-rebuilt ul.products::-webkit-scrollbar {
  width: 0 !important;
  height: 0 !important;
  display: none !important;
}

body.page-id-14 .pd-best-carousel-wrap ul.products li.product,
body.page-id-14 .pd-home-featured-rebuilt ul.products li.product {
  flex: 0 0 calc((100% - 84px) / 4) !important;
  width: calc((100% - 84px) / 4) !important;
  max-width: calc((100% - 84px) / 4) !important;
  min-width: 0 !important;
  margin: 0 !important;
  float: none !important;
  scroll-snap-align: start !important;
}

body.page-id-14 .pd-best-carousel-wrap ul.products li.product a img,
body.page-id-14 .pd-best-carousel-wrap ul.products li.product img,
body.page-id-14 .pd-home-featured-rebuilt ul.products li.product a img,
body.page-id-14 .pd-home-featured-rebuilt ul.products li.product img {
  width: 100% !important;
  height: auto !important;
  min-height: 0 !important;
  max-height: none !important;
  aspect-ratio: 1 / 1 !important;
  object-fit: cover !important;
}

body.page-id-14 .pd-best-arrow {
  display: none !important;
}

@media (max-width: 767px) {
  body.page-id-14 .pd-best-carousel-wrap ul.products,
  body.page-id-14 .pd-home-featured-rebuilt ul.products {
    gap: 12px !important;
  }

  body.page-id-14 .pd-best-carousel-wrap ul.products li.product,
  body.page-id-14 .pd-home-featured-rebuilt ul.products li.product {
    flex-basis: calc((100% - 12px) / 2) !important;
    width: calc((100% - 12px) / 2) !important;
    max-width: calc((100% - 12px) / 2) !important;
  }
}

@media (min-width: 768px) and (max-width: 999px) {
  body.page-id-14 .pd-best-carousel-wrap ul.products,
  body.page-id-14 .pd-home-featured-rebuilt ul.products {
    gap: 18px !important;
  }

  body.page-id-14 .pd-best-carousel-wrap ul.products li.product,
  body.page-id-14 .pd-home-featured-rebuilt ul.products li.product {
    flex-basis: calc((100% - 36px) / 3) !important;
    width: calc((100% - 36px) / 3) !important;
    max-width: calc((100% - 36px) / 3) !important;
  }
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

  var pdBagSvg = '<svg class="ct-icon pd-bag-icon" aria-hidden="true" width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M7.4 8.2V7a4.6 4.6 0 0 1 9.2 0v1.2" stroke="currentColor" stroke-width="1.45" stroke-linecap="round"/><path d="M5.7 8.2h12.6l1.1 13H4.6l1.1-13Z" stroke="currentColor" stroke-width="1.45" stroke-linejoin="round"/></svg>';

  function pdIcon(name){
    var icons = {
      truck: '<svg viewBox="0 0 24 24" fill="none"><path d="M3 7h11v10H3V7Zm14 4h2.4l1.6 2.4V17h-4v-6Z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><circle cx="7" cy="18" r="1.7" stroke="currentColor" stroke-width="1.7"/><circle cx="18" cy="18" r="1.7" stroke="currentColor" stroke-width="1.7"/></svg>',
      check: '<svg viewBox="0 0 24 24" fill="none"><path d="M20 6 9 17l-5-5" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg>',
      lock: '<svg viewBox="0 0 24 24" fill="none"><path d="M7 10V7a5 5 0 0 1 10 0v3M6 10h12v10H6V10Z" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>',
      refresh: '<svg viewBox="0 0 24 24" fill="none"><path d="M20 12a8 8 0 0 1-13.5 5.8M4 12A8 8 0 0 1 17.5 6.2M17.5 2.8v3.4h-3.4M6.5 20.2v-3.4h3.4" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    };
    return icons[name] || icons.check;
  }

  function closestSection(el){
    return el && (el.closest('.elementor-section, section') || el);
  }

  function hideOldHomeSections(){
    if (!document.body.classList.contains('page-id-14')) return;
    document.querySelectorAll('.elementor-element-6f27344, .elementor-element-9855adf, .pd-about, .about-section, .quienes-somos-section').forEach(function(el){
      closestSection(el).style.display = 'none';
    });

    document.querySelectorAll('.pd-home-bag-feature, .pd-categories, .pd-collection-showcase').forEach(function(el){
      el.remove();
    });

    Array.prototype.slice.call(document.querySelectorAll('section,.elementor-section,.elementor-element')).forEach(function(el){
      var t = (el.textContent || '').replace(/\s+/g, ' ').trim();
      if (/NO SOMOS SOLO UNA TIENDA/i.test(t) && !el.closest('.pd-hero')) {
        closestSection(el).style.display = 'none';
      }
    });
  }

  function polishHeroLikeBuilder(){
    if (!document.body.classList.contains('page-id-14')) return;
    var hero = document.querySelector('.pd-hero');
    if (!hero) return;

    if (!document.querySelector('.pd-promo-strip')) {
      var strip = document.createElement('div');
      strip.className = 'pd-promo-strip';
      strip.textContent = 'Descuentos exclusivos hasta 20%';
      var heroSection = closestSection(hero);
      if (heroSection && heroSection.parentNode) heroSection.parentNode.insertBefore(strip, heroSection);
    }

    Array.prototype.slice.call(hero.querySelectorAll('a, button')).forEach(function(el){
      var t = (el.textContent || '').replace(/\s+/g, ' ').trim();
      if (/comprar\s+ya/i.test(t)) el.remove();
      if (/ver\s+m[aá]s/i.test(t)) el.textContent = 'Ver más';
    });
  }

  function buildHomeStory(){
    if (!document.body.classList.contains('page-id-14') || document.querySelector('.pd-home-story-builder')) return;
    var heroWrap = document.querySelector('.elementor-element-de06f38') || closestSection(document.querySelector('.pd-hero'));
    if (!heroWrap || !heroWrap.parentNode) return;

    var story = document.createElement('section');
    story.className = 'pd-home-story-builder';
    story.innerHTML =
      '<div class="pd-story-left">' +
        '<p>Prime Drop Elite nace con una visión clara: Acercar las mejores marcas del mundo a quienes realmente saben de estilo. Nos especializamos en traer prendas 100% originales. Sin intermediarios, sin sobreprecios. Solo moda auténtica, exclusiva y al mejor precio.</p>' +
        '<img class="pd-story-logo" src="/wp-content/uploads/2026/05/LOGO-NEGRO.png" alt="Prime Drop">' +
      '</div>' +
      '<div class="pd-story-right">' +
        '<img class="pd-story-image" src="/wp-content/uploads/2026/05/bolsos-categoria-scaled.jpg" alt="Bolso Prime Drop Elite">' +
        '<div class="pd-story-copy">' +
          '<p>No somos solo una tienda de ropa, somos el puente entre el lujo internacional y tu clóset.</p>' +
          '<p>En Prime Drop Elite creemos que vestir bien no debe ser un privilegio, sino una posibilidad real para quienes quieren destacar.</p>' +
        '</div>' +
      '</div>';

    var benefits = document.querySelector('.pd-home-benefits');
    if (benefits && benefits.parentNode === heroWrap.parentNode) {
      heroWrap.parentNode.insertBefore(story, benefits);
    } else {
      heroWrap.parentNode.insertBefore(story, heroWrap.nextSibling);
    }
  }

  function buildHomeBenefits(){
    if (!document.body.classList.contains('page-id-14') || document.querySelector('.pd-home-benefits')) return;
    var heroWrap = document.querySelector('.elementor-element-de06f38') || closestSection(document.querySelector('.pd-hero'));
    if (!heroWrap || !heroWrap.parentNode) return;
    var benefits = document.createElement('section');
    benefits.className = 'pd-home-benefits';
    benefits.innerHTML =
      '<div class="pd-benefit-item">' + pdIcon('truck') + '<span>Envíos a Colombia</span></div>' +
      '<div class="pd-benefit-item">' + pdIcon('check') + '<span>Productos originales</span></div>' +
      '<div class="pd-benefit-item">' + pdIcon('lock') + '<span>Pago seguro</span></div>' +
      '<div class="pd-benefit-item">' + pdIcon('refresh') + '<span>Cambios fáciles</span></div>';
    heroWrap.parentNode.insertBefore(benefits, heroWrap.nextSibling);
  }

  function categoryMarkup(){
    return '';
  }

  function ensureHomeCategories(){
    if (!document.body.classList.contains('page-id-14')) return;
    document.querySelectorAll('.pd-categories, .pd-collection-showcase').forEach(function(el){ el.remove(); });
  }

  function addInstagramFeed(){
    if (!document.body.classList.contains('page-id-14')) return;
    var footer = document.querySelector('.pd-footer, footer');
    var feed = document.querySelector('.pd-instagram-feed') || document.createElement('section');
    feed.className = 'pd-instagram-feed';
    feed.dataset.pdInstagramUpdated = '1';
    feed.innerHTML = '<h2>SÍGUENOS EN INSTAGRAM</h2><div class="pd-instagram-grid">' +
      '<a href="https://www.instagram.com/primedrop_elite/" target="_blank" rel="noopener"><video autoplay muted loop playsinline preload="metadata" aria-label="Instagram Prime Drop"><source src="https://primedropelite.com/wp-content/uploads/2026/06/SaveClip.App_AQOcZ1fo0tYjSVT_mLVHL_hA6sg34N5TYV6vS4O66b_7c32WV189ZykhAEOkYSK1luyRv7jH2tXgUlSEoSvs02G6GxXLkIdcB6piB7I.mp4" type="video/mp4"></video></a>' +
      '<a href="https://www.instagram.com/primedrop_elite/" target="_blank" rel="noopener"><img src="https://primedropelite.com/wp-content/uploads/2026/06/SaveClip.App_587104948_17864405985517476_4398825993832880462_n.jpg" alt="Instagram Prime Drop"></a>' +
      '<a href="https://www.instagram.com/primedrop_elite/" target="_blank" rel="noopener"><img src="https://primedropelite.com/wp-content/uploads/2026/06/SaveClip.App_572398440_17861483832517476_3552697528818690790_n.jpg" alt="Instagram Prime Drop"></a>' +
      '<a href="https://www.instagram.com/primedrop_elite/" target="_blank" rel="noopener"><img src="https://primedropelite.com/wp-content/uploads/2026/06/SaveClip.App_573856704_17862540060517476_5724372966851338903_n.jpg" alt="Instagram Prime Drop"></a>' +
      '</div>';
    var benefits = document.querySelector('.pd-home-benefits');
    if (benefits && benefits.parentNode) {
      benefits.parentNode.insertBefore(feed, benefits.nextSibling);
      return;
    }

    if (footer && footer.parentNode && !feed.parentNode) footer.parentNode.insertBefore(feed, footer);
  }

  function cleanupFooter(){
    document.querySelectorAll('.footer-video-bg, .pd-footer video, footer.ct-footer, .ct-footer').forEach(function(el){
      if (!el.classList.contains('pd-footer')) el.remove();
    });
    var footer = document.querySelector('.pd-footer');
    if (!footer) return;
    if (footer.dataset.pdFooterClean === '1') return;
    footer.dataset.pdFooterClean = '1';
    footer.innerHTML =
      '<div class="pd-footer-main">' +
        '<div class="pd-footer-column pd-footer-brand">' +
          '<h3>PRIME DROP</h3>' +
          '<p>Descubre nuestra tienda de bolsos, donde traemos lo mejor de las últimas tendencias importadas desde Estados Unidos.</p>' +
        '</div>' +
        '<div class="pd-footer-column pd-footer-contact">' +
          '<h4>CONTACTO</h4>' +
          '<p>primedropelite@gmail.com</p>' +
          '<p>57-316-068-5555</p>' +
        '</div>' +
        '<div class="pd-footer-column pd-footer-social-column">' +
          '<h4>REDES SOCIALES</h4>' +
          '<div class="pd-social-icons">' +
            '<a href="https://www.instagram.com/primedrop_elite/" target="_blank" rel="noopener" aria-label="Instagram"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7.8 2h8.4A5.8 5.8 0 0 1 22 7.8v8.4a5.8 5.8 0 0 1-5.8 5.8H7.8A5.8 5.8 0 0 1 2 16.2V7.8A5.8 5.8 0 0 1 7.8 2Zm0 2A3.8 3.8 0 0 0 4 7.8v8.4A3.8 3.8 0 0 0 7.8 20h8.4a3.8 3.8 0 0 0 3.8-3.8V7.8A3.8 3.8 0 0 0 16.2 4H7.8Zm4.2 3.4A4.6 4.6 0 1 1 12 16.6 4.6 4.6 0 0 1 12 7.4Zm0 2A2.6 2.6 0 1 0 14.6 12 2.6 2.6 0 0 0 12 9.4ZM17 6.8a1.1 1.1 0 1 1-1.1 1.1A1.1 1.1 0 0 1 17 6.8Z"/></svg></a>' +
            '<a href="https://www.tiktok.com/@primedrop_elite" target="_blank" rel="noopener" aria-label="TikTok"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15.6 2c.4 3 2.1 4.8 5 5.1v3.3a8 8 0 0 1-4.8-1.6v6.8A6.4 6.4 0 1 1 9.4 9.2c.5 0 .9.1 1.4.2v3.5a3 3 0 1 0 1.7 2.7V2h3.1Z"/></svg></a>' +
            '<a href="https://wa.me/573160685555" target="_blank" rel="noopener" aria-label="WhatsApp"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a9.8 9.8 0 0 0-8.4 14.9L2.3 22l5.3-1.4A9.8 9.8 0 1 0 12 2Zm0 2a7.8 7.8 0 0 1 0 15.6 7.6 7.6 0 0 1-3.9-1.1l-.4-.2-2.5.7.7-2.4-.3-.4A7.8 7.8 0 0 1 12 4Zm-3.1 4.2c-.2 0-.5.1-.7.4-.3.3-.9.9-.9 2.1s.9 2.4 1 2.6c.1.2 1.8 2.9 4.4 4 .6.2 1 .4 1.4.4.6.2 1.1.1 1.5.1.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.1-1.2-.1-.1-.2-.2-.5-.4l-1.7-.8c-.2-.1-.4-.1-.6.2l-.8 1c-.1.2-.3.2-.5.1-1.4-.6-2.4-1.5-3.1-2.8-.1-.2 0-.4.1-.5l.4-.5c.1-.2.2-.3.3-.5.1-.2.1-.4 0-.6l-.8-1.9c-.2-.4-.4-.4-.6-.4h-.7Z"/></svg></a>' +
          '</div>' +
        '</div>' +
      '</div>' +
      '<div class="pd-footer-newsletter"><h4>ÚNETE A PRIME DROP</h4><p>Recibe ofertas exclusivas y novedades.</p><form><input type="email" placeholder="Introducir dirección de correo electrónico" aria-label="Correo electrónico"><button type="submit">REGISTRARSE</button></form></div>' +
      '<div class="pd-footer-bottom">© 2026 Prime Drop Elite. Todos los derechos reservados.</div>';
  }

  function replaceCartIcon(){
    document.querySelectorAll('.ct-cart-item svg, .ct-header-cart svg, .ct-cart-content svg').forEach(function(svg){
      if (svg.closest('#cart-drawer, .pd-cart-drawer')) return;
      if (svg.classList.contains('pd-bag-icon')) return;
      svg.outerHTML = pdBagSvg;
    });
  }

  function replaceAddToBagText(){
    var targets = document.querySelectorAll('.add_to_cart_button, .single_add_to_cart_button, .woocommerce a.button, .woocommerce button.button');
    targets.forEach(function(el){
      var t = (el.textContent || '').trim();
      if (/añadir\s+al\s+carrito|add\s+to\s+cart/i.test(t)) el.textContent = 'AÑADIR A LA BOLSA';
    });
  }

  function addBolsosBrandFilter(){
    if (!document.body.classList.contains('page-id-547') || document.querySelector('.pd-brand-filter')) return;
    var head = document.querySelector('.pd-luxium-collection-inner') || document.querySelector('.pd-luxium-collection-head');
    if (!head) return;
    var filter = document.createElement('nav');
    filter.className = 'pd-brand-filter';
    filter.setAttribute('aria-label', 'Filtrar por marca');
    filter.innerHTML = '<a href="/bolsos/">Todos</a><a href="/categoria-producto/michael-kors/">Michael Kors</a><a href="/categoria-producto/steve-madden/">Steve Madden</a><a href="/categoria-producto/tommy-hilfiger/">Tommy Hilfiger</a>';
    head.appendChild(filter);
  }

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

  function enhanceBolsosSubmenus(){
    var navs = document.querySelectorAll('nav[data-id="menu"], nav[data-id="mobile-menu"]');
    navs.forEach(function(nav){
      Array.prototype.slice.call(nav.querySelectorAll('li')).forEach(function(li){
        var directLink = Array.prototype.slice.call(li.children).find(function(child){
          return child.tagName === 'A';
        });
        if (!directLink || !/^BOLSOS$/i.test((directLink.textContent || '').trim()) || li.classList.contains('pd-bolsos-menu-parent')) return;

        li.classList.add('pd-bolsos-menu-parent');
        var submenu = document.createElement('ul');
        submenu.className = 'pd-bolsos-submenu';
        submenu.innerHTML =
          '<li><a href="/categoria-producto/hombre/">HOMBRE</a></li>' +
          '<li><a href="/categoria-producto/mujer/">MUJER</a></li>';
        li.appendChild(submenu);

        if (nav.getAttribute('data-id') === 'mobile-menu') {
          var toggle = document.createElement('span');
          toggle.setAttribute('role', 'button');
          toggle.setAttribute('tabindex', '0');
          toggle.className = 'pd-submenu-toggle';
          toggle.setAttribute('aria-label', 'Abrir submenu Bolsos');
          toggle.setAttribute('aria-expanded', 'false');
          toggle.textContent = '⌄';
          toggle.addEventListener('keydown', function(e){
            if (e.key !== 'Enter' && e.key !== ' ') return;
            e.preventDefault();
            toggle.click();
          });
          toggle.addEventListener('click', function(e){
            e.preventDefault();
            e.stopPropagation();
            var open = li.classList.toggle('pd-submenu-open');
            toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
          });
          li.insertBefore(toggle, submenu);
        } else {
          li.addEventListener('mouseenter', function(){
            li.classList.add('pd-submenu-open');
          });
          li.addEventListener('mouseleave', function(){
            li.classList.remove('pd-submenu-open');
          });
          li.addEventListener('focusin', function(){
            li.classList.add('pd-submenu-open');
          });
          li.addEventListener('focusout', function(e){
            if (!li.contains(e.relatedTarget)) li.classList.remove('pd-submenu-open');
          });
        }
      });
    });
  }

  /* Reconstruir colección homepage si Elementor la sobreescribe */
  function rebuildCollection(){
    if (!document.body.classList.contains('page-id-14')) return;
    document.querySelectorAll('.pd-categories, .pd-collection-showcase').forEach(function(el){ el.remove(); });
  }

  /* Icono cuenta visible en mobile/tablet con el mismo modal de desktop */
  function ensureMobileAccountIcon(){
    if (!(isMobile() || isTablet())) return;
    function isVisibleNode(el){
      if (!el) return false;
      var r = el.getBoundingClientRect();
      var cs = window.getComputedStyle(el);
      return r.width > 4 && r.height > 4 && cs.display !== 'none' && cs.visibility !== 'hidden' && cs.opacity !== '0';
    }
    var alreadyVisible = Array.prototype.slice.call(document.querySelectorAll('.pd-mobile-account-server')).some(isVisibleNode);
    if (alreadyVisible) return;
    var cart = Array.prototype.slice.call(document.querySelectorAll('[data-device="mobile"] .ct-cart-item, [data-device="mobile"] .ct-header-cart, [data-device="mobile"] [data-id="cart"], a.ct-cart-item, .ct-header-cart')).find(isVisibleNode);
    var menu = Array.prototype.slice.call(document.querySelectorAll('[data-device="mobile"] [aria-label="Menú"], [data-device="mobile"] .ct-header-trigger, [aria-label="Menú"], .ct-header-trigger')).find(isVisibleNode);
    if (!cart && !menu) return;
    var cartNode = cart ? (cart.closest('[data-id="cart"], .ct-header-cart') || cart) : null;
    var targetNode = cart ? cartNode : menu;
    var parent = targetNode.parentNode;
    if (!parent) return;
    var parentHasVisibleAccount = Array.prototype.slice.call(parent.querySelectorAll('.pd-mobile-account-server')).some(isVisibleNode);
    if (parentHasVisibleAccount) return;

    var icon = document.createElement('a');
    icon.href = '#account-modal';
    icon.className = 'ct-account-item pd-mobile-account-server';
    icon.setAttribute('aria-label', 'ACCEDER');
    icon.setAttribute('data-label', 'left');
    icon.innerHTML = '<svg class="ct-icon pd-account-icon-shein" aria-hidden="true" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="7.5" r="3.7" stroke="currentColor" stroke-width="1.7"></circle><path d="M4.8 20.2c0.8-4.3 3.7-6.6 7.2-6.6s6.4 2.3 7.2 6.6" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"></path></svg>';
    icon.addEventListener('click', function(e){
      e.preventDefault();
      var nativeAccount = document.querySelector('.ct-header-account .ct-account-item:not(.pd-mobile-account-server), [data-id="account"] .ct-account-item:not(.pd-mobile-account-server)');
      if (nativeAccount) {
        nativeAccount.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: window }));
        return;
      }
      window.location.hash = 'account-modal';
    });
    parent.insertBefore(icon, targetNode);
  }

  function hydrateFeaturedProducts(ul) {
    if (!ul || ul.dataset.pdFeaturedHydrated === '1' || !window.fetch) return;
    ul.dataset.pdFeaturedHydrated = '1';

    fetch('/wp-json/wc/store/v1/products?per_page=8&orderby=popularity&order=desc', {
      credentials: 'same-origin'
    })
      .then(function(res){ return res.ok ? res.json() : null; })
      .then(function(products){
        if (!Array.isArray(products) || products.length < 4) return;
        ul.innerHTML = '';

        products.slice(0, 8).forEach(function(product){
          var li = document.createElement('li');
          li.className = 'product type-product status-publish';

          var link = document.createElement('a');
          link.className = 'woocommerce-loop-product__link';
          link.href = product.permalink || '#';

          var image = document.createElement('img');
          var imageData = product.images && product.images[0] ? product.images[0] : {};
          image.src = imageData.thumbnail || imageData.src || '';
          image.alt = imageData.alt || product.name || '';
          image.loading = 'lazy';
          link.appendChild(image);

          var title = document.createElement('h2');
          title.className = 'woocommerce-loop-product__title';
          title.textContent = product.name || '';
          link.appendChild(title);

          var price = document.createElement('span');
          price.className = 'price';
          price.innerHTML = product.price_html || '';
          link.appendChild(price);

          var button = document.createElement('a');
          button.href = '/?add-to-cart=' + product.id;
          button.className = 'button product_type_simple add_to_cart_button ajax_add_to_cart';
          button.setAttribute('data-product_id', product.id);
          button.setAttribute('data-quantity', '1');
          button.setAttribute('rel', 'nofollow');
          button.textContent = 'AÑADIR A LA BOLSA';

          li.appendChild(link);
          li.appendChild(button);
          ul.appendChild(li);
        });

        replaceAddToBagText();
        animateProducts();
      })
      .catch(function(){
        ul.dataset.pdFeaturedHydrated = '0';
      });
  }

  /* Home: convertir Productos Destacados en carrusel estilo Luxium */
  function enhanceBestSellers(){
    if (!document.body.classList.contains('page-id-14')) return;
    var headings = Array.prototype.slice.call(document.querySelectorAll('h1,h2,h3,.elementor-heading-title'));
    var heading = headings.find(function(el){ return /PRODUCTOS\s+DESTACADOS|LOS\s+MAS\s+VENDIDOS|LOS\s+MÁS\s+VENDIDOS/i.test((el.textContent || '').trim()); });
    if (heading) {
      heading.textContent = 'DESTACADAS';
      heading.classList.add('pd-best-title');
      var headingSection = heading.closest('.elementor-section, .elementor-element');
      if (headingSection) headingSection.classList.add('pd-best-heading-section');
    }

    var ul = document.querySelector('.elementor-element-741b26a ul.products, body.page-id-14 .woocommerce ul.products');
    if (!ul) return;
    hydrateFeaturedProducts(ul);
    var widget = ul.closest('.elementor-widget-shortcode, .elementor-element') || ul.parentNode;
    if (widget) widget.classList.add('pd-best-section');
    if (ul.closest('.pd-best-carousel-wrap')) return;

    var wrap = document.createElement('div');
    wrap.className = 'pd-best-carousel-wrap';
    ul.parentNode.insertBefore(wrap, ul);
    wrap.appendChild(ul);

    wrap.querySelectorAll('.pd-best-arrow').forEach(function(arrow){ arrow.remove(); });
    ul.querySelectorAll('.pd-best-offer').forEach(function(badge){ badge.remove(); });

    if (!ul.dataset.pdAutoScroll) {
      ul.dataset.pdAutoScroll = '1';
      var paused = false;
      ['mouseenter', 'touchstart', 'focusin'].forEach(function(evt){
        ul.addEventListener(evt, function(){ paused = true; }, { passive: true });
      });
      ['mouseleave', 'touchend', 'focusout'].forEach(function(evt){
        ul.addEventListener(evt, function(){ paused = false; }, { passive: true });
      });
      setInterval(function(){
        if (paused || !document.body.classList.contains('page-id-14')) return;
        var max = ul.scrollWidth - ul.clientWidth;
        if (max <= 12) return;
        var firstCard = ul.querySelector('li.product');
        var gap = parseFloat(window.getComputedStyle(ul).gap || '0') || 0;
        var step = firstCard ? firstCard.getBoundingClientRect().width + gap : Math.round(ul.clientWidth * 0.25);
        if (ul.scrollLeft + step >= max - 4) {
          ul.scrollTo({ left: 0, behavior: 'smooth' });
        } else {
          ul.scrollBy({ left: step, behavior: 'smooth' });
        }
      }, 3000);
    }
  }

  /* Scroll lock carrito — solo mobile y tablet touch */
  function initCartScrollLock(){
    var drawer = document.querySelector('#cart-drawer, .cart-drawer');
    if (!drawer) return;
    if (drawer.dataset.pdScrollLockReady === '1') return;
    drawer.dataset.pdScrollLockReady = '1';
    var locked = false, savedY = 0, lastCartClickY = 0;
    function shouldLock(){ return isMobile() || isTablet(); }
    function isCartTrigger(target){
      if (!target || !target.closest) return false;
      return !!target.closest('a.ct-cart-item, .ct-cart-item, .ct-header-cart, [data-id="cart"], a[href*="cart"]');
    }
    function lock(){
      if (locked || !shouldLock()) return;
      var currentY = window.pageYOffset || 0;
      savedY = currentY > 0 ? currentY : (lastCartClickY || 0);
      document.body.style.cssText += ';position:fixed;top:-' + savedY + 'px;left:0;right:0;width:100%;overflow:hidden';
      document.documentElement.style.overflow = 'hidden';
      locked = true;
    }
    function unlock(){
      if (!locked) return;
      var y = savedY || Math.abs(parseInt(document.body.style.top || '0')) || lastCartClickY || 0;
      ['position','top','left','right','width','overflow'].forEach(function(p){ document.body.style[p] = ''; });
      document.documentElement.style.overflow = '';
      locked = false;
      requestAnimationFrame(function(){
        window.scrollTo(0, y);
        setTimeout(function(){ window.scrollTo(0, y); }, 60);
      });
    }
    function sync(){
      if (!shouldLock()){ unlock(); return; }
      (drawer.classList.contains('active') || drawer.classList.contains('open')) ? lock() : unlock();
    }
    new MutationObserver(sync).observe(drawer, { attributes: true, attributeFilter: ['class'] });
    document.addEventListener('click', function(e){
      if (isCartTrigger(e.target) && shouldLock()) {
        lastCartClickY = window.pageYOffset || lastCartClickY || 0;
        e.preventDefault();
      }
      setTimeout(sync, 0);
    }, true);
    window.addEventListener('resize', sync);
  }

  function init(){
    hideOldHomeSections();
    polishHeroLikeBuilder();
    buildHomeBenefits();
    buildHomeStory();
    ensureMobileAccountIcon();
    animateProducts();
    enhanceMobileMenu();
    enhanceBolsosSubmenus();
    rebuildCollection();
    ensureHomeCategories();
    enhanceBestSellers();
    addInstagramFeed();
    cleanupFooter();
    replaceCartIcon();
    replaceAddToBagText();
    addBolsosBrandFilter();
    initCartScrollLock();
  }

  document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', init) : init();
  window.addEventListener('load', init);
  setTimeout(init, 700);
  [150, 450, 1000, 1800, 3000, 5000].forEach(function(delay){
    setTimeout(function(){
      hideOldHomeSections();
      polishHeroLikeBuilder();
      buildHomeBenefits();
      buildHomeStory();
      ensureMobileAccountIcon();
      enhanceBolsosSubmenus();
      rebuildCollection();
      ensureHomeCategories();
      enhanceBestSellers();
      addInstagramFeed();
      cleanupFooter();
      replaceCartIcon();
      replaceAddToBagText();
      addBolsosBrandFilter();
    }, delay);
  });
})();
</script>
<?php }, 999);

/* ---------- 11. PRODUCTO INDIVIDUAL — ESTILO COACH ---------- */
add_action('wp_head', function() {
    if (!function_exists('is_product') || !is_product()) return;
?>
<style id="pd-coach-product-css">
/* Prime Drop producto individual: galería contenida + detalles tipo Coach */
.single-product .product-entry-wrapper,
.single-product div.product {
  max-width: 1240px !important;
  margin-left: auto !important;
  margin-right: auto !important;
}

.single-product div.product {
  padding: 24px clamp(16px, 4vw, 56px) 56px !important;
}

@media (min-width: 1000px) {
  .single-product div.product {
    display: grid !important;
    grid-template-columns: minmax(0, 1.22fr) minmax(360px, .78fr) !important;
    gap: clamp(34px, 4vw, 54px) !important;
    align-items: start !important;
  }

  .single-product .woocommerce-product-gallery {
    width: 100% !important;
    max-width: none !important;
    grid-column: 1 !important;
  }

  .single-product .entry-summary {
    width: 100% !important;
    max-width: none !important;
    grid-column: 2 !important;
    position: sticky !important;
    top: 96px !important;
    align-self: start !important;
  }

  .single-product .related.products,
  .single-product .up-sells,
  .single-product .cross-sells {
    grid-column: 1 / -1 !important;
  }
}

.single-product .woocommerce-product-gallery,
.single-product .woocommerce-product-gallery .ct-product-gallery-container {
  overflow: visible !important;
}

.single-product .woocommerce-product-gallery .flexy-container {
  width: 100% !important;
}

@media (min-width: 1000px) {
  .single-product .woocommerce-product-gallery .flexy-container {
    display: grid !important;
    grid-template-columns: 86px minmax(0, 1fr) !important;
    gap: 18px !important;
    align-items: start !important;
  }

  .single-product .woocommerce-product-gallery .flexy {
    grid-column: 2 !important;
    grid-row: 1 !important;
  }

  .single-product .woocommerce-product-gallery .flexy-pills {
    grid-column: 1 !important;
    grid-row: 1 !important;
    width: 86px !important;
    height: auto !important;
    margin: 0 !important;
    position: sticky !important;
    top: 96px !important;
  }

  .single-product .woocommerce-product-gallery .flexy-pills ol {
    display: flex !important;
    flex-direction: column !important;
    gap: 12px !important;
    width: 86px !important;
    height: auto !important;
    margin: 0 !important;
    padding: 0 !important;
    transform: none !important;
  }

  .single-product .woocommerce-product-gallery .flexy-pills li {
    width: 86px !important;
    height: 108px !important;
    flex: 0 0 108px !important;
    padding: 0 !important;
    border: 1px solid transparent !important;
    background: #f6f6f4 !important;
    overflow: hidden !important;
  }

  .single-product .woocommerce-product-gallery .flexy-pills li.active {
    border-color: #000000 !important;
  }
}

.single-product .woocommerce-product-gallery .flexy-view,
.single-product .woocommerce-product-gallery .flexy-items,
.single-product .woocommerce-product-gallery .flexy-item,
.single-product .woocommerce-product-gallery .ct-media-container {
  height: auto !important;
  min-height: 0 !important;
  max-height: none !important;
}

.single-product .woocommerce-product-gallery .flexy-view,
.single-product .woocommerce-product-gallery .flexy-item,
.single-product .woocommerce-product-gallery .ct-media-container {
  aspect-ratio: 1 / 1 !important;
}

.single-product .woocommerce-product-gallery .ct-media-container {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  background: #f6f6f4 !important;
  overflow: hidden !important;
}

.single-product .woocommerce-product-gallery .ct-media-container img {
  width: 100% !important;
  height: 100% !important;
  max-width: 100% !important;
  max-height: 100% !important;
  object-fit: contain !important;
  object-position: center center !important;
  padding: clamp(18px, 3vw, 34px) !important;
  background: transparent !important;
}

.single-product .woocommerce-product-gallery .flexy-pills .ct-media-container,
.single-product .woocommerce-product-gallery .flexy-pills .ct-media-container img {
  aspect-ratio: auto !important;
}

.single-product .woocommerce-product-gallery .flexy-pills .ct-media-container {
  width: 100% !important;
  height: 100% !important;
  min-height: 0 !important;
  max-height: 100% !important;
}

.single-product .woocommerce-product-gallery .flexy-pills .ct-media-container img {
  width: 100% !important;
  height: 100% !important;
  min-height: 0 !important;
  max-height: 100% !important;
  padding: 8px !important;
  box-sizing: border-box !important;
}

.single-product .woocommerce-product-gallery__trigger {
  top: 18px !important;
  right: 18px !important;
  background: #ffffff !important;
  border: 1px solid #e3e3e3 !important;
  color: #000000 !important;
  box-shadow: none !important;
}

.single-product .entry-summary .product_title,
.single-product .entry-summary h1 {
  font-family: var(--pd-heading-font) !important;
  font-size: clamp(30px, 3vw, 42px) !important;
  font-weight: 700 !important;
  line-height: 1.08 !important;
  letter-spacing: 0 !important;
  margin: 0 0 12px !important;
  color: #000000 !important;
}

.single-product .entry-summary .price {
  color: #000000 !important;
  font-family: var(--pd-body-font) !important;
  font-size: 22px !important;
  font-weight: 700 !important;
  margin: 0 0 28px !important;
}

.single-product .entry-summary form.cart {
  display: grid !important;
  grid-template-columns: 130px minmax(0, 1fr) !important;
  gap: 12px !important;
  align-items: stretch !important;
  padding-top: 24px !important;
  border-top: 1px solid #eeeeee !important;
}

.single-product .entry-summary .quantity {
  width: 130px !important;
  min-width: 130px !important;
  height: 56px !important;
  border: 1px solid #000000 !important;
  border-radius: 0 !important;
  overflow: hidden !important;
}

.single-product .entry-summary .quantity input,
.single-product .entry-summary .quantity button {
  height: 56px !important;
  border: none !important;
  background: #ffffff !important;
  color: #000000 !important;
}

.single-product .entry-summary .single_add_to_cart_button,
.single-product .entry-summary button.single_add_to_cart_button {
  min-height: 56px !important;
  border-radius: 0 !important;
  background: #000000 !important;
  color: #ffffff !important;
  font-family: var(--pd-body-font) !important;
  font-size: 12px !important;
  font-weight: 800 !important;
  letter-spacing: 1.35px !important;
  text-transform: uppercase !important;
  white-space: nowrap !important;
  padding-left: 18px !important;
  padding-right: 18px !important;
}

.single-product .entry-summary .single_add_to_cart_button:hover {
  background: #222222 !important;
  color: #ffffff !important;
}

.single-product .entry-summary .product_meta {
  margin-top: 28px !important;
  padding-top: 24px !important;
  border-top: 1px solid #eeeeee !important;
  color: #222222 !important;
  font-family: var(--pd-body-font) !important;
  font-size: 12px !important;
  letter-spacing: 1.2px !important;
  text-transform: uppercase !important;
}

.single-product .entry-summary .product_meta a {
  color: #333333 !important;
  text-decoration: none !important;
}

.single-product .entry-summary .yith-wcwl-add-to-wishlist,
.single-product .entry-summary .ct-wishlist-button-archive {
  margin-top: 22px !important;
}

.single-product .entry-summary .pd-coach-details {
  margin-top: 30px !important;
  border-top: 1px solid #dcdcdc !important;
}

.single-product .entry-summary .pd-coach-details .tabs,
.single-product .entry-summary .pd-coach-details > h2,
.single-product .entry-summary .pd-coach-details .wc-tab > h2:first-child {
  display: none !important;
}

.single-product .pd-coach-detail {
  border-bottom: 1px solid #dcdcdc !important;
}

.single-product .pd-coach-detail summary {
  list-style: none !important;
  cursor: pointer !important;
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  gap: 18px !important;
  padding: 18px 0 !important;
  color: #000000 !important;
  font-family: var(--pd-body-font) !important;
  font-size: 13px !important;
  font-weight: 700 !important;
  letter-spacing: 1.1px !important;
  text-transform: uppercase !important;
}

.single-product .pd-coach-detail summary::-webkit-details-marker {
  display: none !important;
}

.single-product .pd-coach-plus {
  flex: 0 0 auto !important;
  font-size: 20px !important;
  line-height: 1 !important;
  font-weight: 300 !important;
  transition: transform .2s ease !important;
}

.single-product .pd-coach-detail[open] .pd-coach-plus {
  transform: rotate(45deg) !important;
}

.single-product .pd-coach-detail .wc-tab {
  display: block !important;
  padding: 0 0 22px !important;
  color: #222222 !important;
  font-family: var(--pd-body-font) !important;
  font-size: 14px !important;
  line-height: 1.75 !important;
}

.single-product .pd-coach-detail .wc-tab p {
  margin: 0 0 12px !important;
}

.single-product .pd-coach-detail .wc-tab ul,
.single-product .pd-product-bullets {
  list-style: none !important;
  margin: 0 !important;
  padding: 0 !important;
  display: grid !important;
  gap: 10px !important;
}

.single-product .pd-coach-detail .wc-tab li,
.single-product .pd-product-bullets li {
  position: relative !important;
  padding-left: 18px !important;
  color: #222222 !important;
}

.single-product .pd-coach-detail .wc-tab li:before,
.single-product .pd-product-bullets li:before {
  content: "" !important;
  position: absolute !important;
  left: 0 !important;
  top: .85em !important;
  width: 5px !important;
  height: 5px !important;
  border-radius: 50% !important;
  background: #000000 !important;
}

.single-product .pd-coach-detail table.shop_attributes {
  width: 100% !important;
  border: none !important;
  margin: 0 !important;
}

.single-product .pd-coach-detail table.shop_attributes th,
.single-product .pd-coach-detail table.shop_attributes td {
  border: none !important;
  border-bottom: 1px solid #eeeeee !important;
  padding: 10px 0 !important;
  font-family: var(--pd-body-font) !important;
  font-size: 13px !important;
  text-align: left !important;
}

@media (max-width: 999px) {
  .single-product div.product {
    display: block !important;
    padding: 12px 16px 44px !important;
  }

  .single-product .entry-summary {
    position: static !important;
    margin-top: 24px !important;
  }

  .single-product .woocommerce-product-gallery .flexy-view,
  .single-product .woocommerce-product-gallery .flexy-item,
  .single-product .woocommerce-product-gallery .ct-media-container {
    aspect-ratio: 1 / 1 !important;
  }

  .single-product .woocommerce-product-gallery .ct-media-container img {
    padding: 18px !important;
  }

  .single-product .woocommerce-product-gallery .flexy-pills {
    width: 100% !important;
    height: auto !important;
    margin-top: 14px !important;
    overflow-x: auto !important;
    overflow-y: hidden !important;
    scrollbar-width: none !important;
  }

  .single-product .woocommerce-product-gallery .flexy-pills::-webkit-scrollbar {
    display: none !important;
  }

  .single-product .woocommerce-product-gallery .flexy-pills ol {
    display: flex !important;
    flex-direction: row !important;
    gap: 10px !important;
    width: auto !important;
    height: auto !important;
    margin: 0 !important;
    padding: 0 !important;
    transform: none !important;
  }

  .single-product .woocommerce-product-gallery .flexy-pills li {
    width: 88px !important;
    height: 88px !important;
    flex: 0 0 88px !important;
    padding: 0 !important;
    border: 1px solid transparent !important;
    background: #f6f6f4 !important;
    overflow: hidden !important;
  }

  .single-product .woocommerce-product-gallery .flexy-pills li.active {
    border-color: #000000 !important;
  }

  .single-product .woocommerce-product-gallery .flexy-pills .ct-media-container {
    width: 100% !important;
    height: 100% !important;
    min-height: 0 !important;
    max-height: 100% !important;
  }

  .single-product .woocommerce-product-gallery .flexy-pills .ct-media-container img {
    width: 100% !important;
    height: 100% !important;
    min-height: 0 !important;
    max-height: 100% !important;
    padding: 8px !important;
    object-fit: contain !important;
  }

  .single-product .entry-summary form.cart {
    grid-template-columns: 106px minmax(0, 1fr) !important;
  }

  .single-product .entry-summary .quantity {
    width: 106px !important;
    min-width: 106px !important;
  }
}

@media (min-width: 1000px) {
  .single-product div.product {
    display: block !important;
  }

  .single-product .product-entry-wrapper {
    display: grid !important;
    grid-template-columns: minmax(0, 1.22fr) minmax(380px, .78fr) !important;
    gap: clamp(34px, 4vw, 54px) !important;
    align-items: start !important;
    width: 100% !important;
    max-width: 1240px !important;
    margin: 0 auto !important;
  }

  .single-product .product-entry-wrapper .woocommerce-product-gallery {
    grid-column: 1 !important;
    width: 100% !important;
  }

  .single-product .product-entry-wrapper .entry-summary {
    grid-column: 2 !important;
    width: 100% !important;
  }

  .single-product .entry-summary form.cart {
    grid-template-columns: 104px minmax(0, 1fr) !important;
  }

  .single-product .entry-summary .quantity {
    width: 104px !important;
    min-width: 104px !important;
  }
}
</style>
<?php
}, 1001);

add_action('wp_footer', function() {
    if (!function_exists('is_product') || !is_product()) return;
?>
<script id="pd-coach-product-js">
(function(){
  function labelForPanel(panel){
    var id = (panel.id || '').toLowerCase();
    if (id.indexOf('description') !== -1) return 'Detalles del producto';
    if (id.indexOf('additional') !== -1) return 'Información adicional';
    var h = panel.querySelector('h2, h3');
    return h ? h.textContent.trim() : 'Detalles';
  }

  function normalizeBullets(panel){
    if (!panel || panel.querySelector('ul, ol, table')) return;
    var text = (panel.textContent || '').replace(/\u00a0/g, ' ').trim();
    var parts = text.split(/(?:\n+|•)/).map(function(item){
      return item.replace(/\s+/g, ' ').trim();
    }).filter(function(item){
      return item.length > 2 && !/^descripci[oó]n$/i.test(item);
    });
    if (parts.length < 3) return;
    var ul = document.createElement('ul');
    ul.className = 'pd-product-bullets';
    parts.forEach(function(part){
      var li = document.createElement('li');
      li.textContent = part;
      ul.appendChild(li);
    });
    panel.innerHTML = '';
    panel.appendChild(ul);
  }

  function buildCoachDetails(){
    if (!document.body.classList.contains('single-product')) return;
    var summary = document.querySelector('.entry-summary');
    var tabs = document.querySelector('.woocommerce-tabs.wc-tabs-wrapper');
    if (!summary || !tabs || tabs.classList.contains('pd-coach-details-ready')) return;

    tabs.classList.add('pd-coach-details', 'pd-coach-details-ready');
    var tabList = tabs.querySelector('.tabs, ul.wc-tabs');
    if (tabList) tabList.remove();

    Array.prototype.slice.call(tabs.querySelectorAll('.wc-tab')).forEach(function(panel, index){
      normalizeBullets(panel);
      var details = document.createElement('details');
      details.className = 'pd-coach-detail';
      if (index === 0) details.open = true;

      var head = document.createElement('summary');
      head.innerHTML = '<span>' + labelForPanel(panel) + '</span><span class="pd-coach-plus" aria-hidden="true">+</span>';
      details.appendChild(head);

      panel.style.display = 'block';
      details.appendChild(panel);
      tabs.appendChild(details);
    });

    summary.appendChild(tabs);
  }

  document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', buildCoachDetails) : buildCoachDetails();
  window.addEventListener('load', buildCoachDetails);
  setTimeout(buildCoachDetails, 600);
})();
</script>
<?php
}, 1001);

/* ============================================================
   FIN PRIME DROP ELITE — MASTER BLOCK v2.0
   ============================================================ */

/* PRIME_DROP_MOBILE_BOLSOS_DROPDOWN_FIX_START */
add_action('wp_head', function () {
    ?>
    <style id="pd-discount-mobile-bolsos-css">
/* PD remove discount and mobile Bolsos submenu - START */
/* Quitar franja 'Descuentos exclusivos hasta 20%' en inicio */
.pd-promo-strip {
  display: none !important;
}

/* BOLSOS: dropdown funcional en tablet y Android */
@media (max-width: 999px) {
  #header [data-device="desktop"] .pd-bolsos-menu-parent {
    position: relative !important;
  }

  #header [data-device="desktop"] .pd-bolsos-menu-parent > a {
    position: relative !important;
    padding-right: 16px !important;
  }

  #header [data-device="desktop"] .pd-bolsos-menu-parent > a::after {
    content: "⌄" !important;
    display: inline-block !important;
    margin-left: 6px !important;
    font-size: 11px !important;
    line-height: 1 !important;
    transform: translateY(-1px) !important;
  }

  #header [data-device="desktop"] .pd-bolsos-menu-parent > .pd-bolsos-submenu {
    display: block !important;
    position: absolute !important;
    top: calc(100% + 10px) !important;
    left: 50% !important;
    min-width: 152px !important;
    margin: 0 !important;
    padding: 8px 0 !important;
    list-style: none !important;
    background: #ffffff !important;
    border: 1px solid rgba(0,0,0,.12) !important;
    border-radius: 10px !important;
    box-shadow: 0 12px 28px rgba(0,0,0,.12) !important;
    opacity: 0 !important;
    visibility: hidden !important;
    pointer-events: none !important;
    transform: translate(-50%, 6px) !important;
    transition: opacity .2s ease, transform .2s ease, visibility .2s ease !important;
    z-index: 99999 !important;
  }

  #header [data-device="desktop"] .pd-bolsos-menu-parent:hover > .pd-bolsos-submenu,
  #header [data-device="desktop"] .pd-bolsos-menu-parent:focus-within > .pd-bolsos-submenu,
  #header [data-device="desktop"] .pd-bolsos-menu-parent.pd-submenu-open > .pd-bolsos-submenu {
    opacity: 1 !important;
    visibility: visible !important;
    pointer-events: auto !important;
    transform: translate(-50%, 0) !important;
  }

  #header [data-device="desktop"] .pd-bolsos-submenu li {
    margin: 0 !important;
    padding: 0 !important;
    list-style: none !important;
  }

  #header [data-device="desktop"] .pd-bolsos-submenu a {
    display: block !important;
    padding: 11px 18px !important;
    color: #000000 !important;
    background: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 1.4px !important;
    text-transform: uppercase !important;
    text-decoration: none !important;
    white-space: nowrap !important;
  }

  #header [data-device="desktop"] .pd-bolsos-submenu a:hover {
    background: #f5f5f5 !important;
  }
}

@media (max-width: 480px) {
  #header [data-device="desktop"] .pd-bolsos-menu-parent > .pd-bolsos-submenu {
    top: calc(100% + 8px) !important;
    min-width: 140px !important;
  }

  #header [data-device="desktop"] .pd-bolsos-submenu a {
    padding: 10px 15px !important;
    font-size: 10px !important;
  }
}
/* PD remove discount and mobile Bolsos submenu - END */
    </style>
    <?php
}, 999);

add_action('wp_footer', function () {
    ?>
    <script id="pd-mobile-bolsos-dropdown-fix">
    (function() {
      if (window.PDMobileBolsosDropdownFix) return;
      window.PDMobileBolsosDropdownFix = true;

      function isMobileHeaderMode() {
        return window.matchMedia && window.matchMedia('(max-width: 999px)').matches;
      }

      function closeOthers(current) {
        document.querySelectorAll('#header [data-device="desktop"] .pd-bolsos-menu-parent.pd-submenu-open').forEach(function(item) {
          if (item === current) return;
          item.classList.remove('pd-submenu-open');
          var link = item.querySelector(':scope > a');
          if (link) link.setAttribute('aria-expanded', 'false');
        });
      }

      function syncBolsosLinkMode() {
        document.querySelectorAll('#header [data-device="desktop"] .pd-bolsos-menu-parent > a').forEach(function(link) {
          if (!link.dataset.pdOriginalHref) {
            link.dataset.pdOriginalHref = link.getAttribute('href') || '/bolsos/';
          }

          if (isMobileHeaderMode()) {
            link.setAttribute('href', 'javascript:void(0)');
          } else {
            link.setAttribute('href', link.dataset.pdOriginalHref);
          }
        });
      }

      function setupBolsosDropdown() {
        syncBolsosLinkMode();

        document.querySelectorAll('#header [data-device="desktop"] .pd-bolsos-menu-parent').forEach(function(item) {
          if (item.dataset.pdMobileBolsosBound === '1') return;

          var link = item.querySelector(':scope > a');
          var submenu = item.querySelector(':scope > .pd-bolsos-submenu');
          if (!link || !submenu) return;

          item.dataset.pdMobileBolsosBound = '1';
          link.setAttribute('aria-haspopup', 'true');
          link.setAttribute('aria-expanded', 'false');

          link.addEventListener('click', function(event) {
            if (!isMobileHeaderMode()) return;

            if (!item.classList.contains('pd-submenu-open')) {
              event.preventDefault();
              event.stopPropagation();
              closeOthers(item);
              item.classList.add('pd-submenu-open');
              link.setAttribute('aria-expanded', 'true');
            }
          });
        });
      }

      function handleBolsosOpenEvent(event) {
        if (!isMobileHeaderMode()) return;

        var target = event.target && event.target.nodeType === 1 ? event.target : event.target.parentElement;
        if (!target || !target.closest) return;

        var item = target.closest('#header [data-device="desktop"] .pd-bolsos-menu-parent');
        if (!item) return;
        var link = item.querySelector(':scope > a');
        if (!link) return;

        if (event.clientX && event.clientY) {
          var rect = link.getBoundingClientRect();
          var insideLinkArea = event.clientX >= rect.left - 10 &&
            event.clientX <= rect.right + 10 &&
            event.clientY >= rect.top - 12 &&
            event.clientY <= rect.bottom + 12;
          if (!insideLinkArea) return;
        }

        if (!item.classList.contains('pd-submenu-open')) {
          event.preventDefault();
          event.stopPropagation();
          if (event.stopImmediatePropagation) event.stopImmediatePropagation();
          closeOthers(item);
          item.classList.add('pd-submenu-open');
          link.setAttribute('aria-expanded', 'true');
        }
      }

      ['pointerdown', 'touchstart', 'mousedown', 'click'].forEach(function(eventName) {
        document.addEventListener(eventName, handleBolsosOpenEvent, true);
      });

      document.addEventListener('click', function(event) {
        if (!isMobileHeaderMode()) return;
        if (event.target.closest('#header [data-device="desktop"] .pd-bolsos-menu-parent')) return;
        closeOthers(null);
      }, true);

      document.addEventListener('DOMContentLoaded', setupBolsosDropdown);
      window.addEventListener('resize', function() {
        syncBolsosLinkMode();
        setupBolsosDropdown();
      });
      setTimeout(setupBolsosDropdown, 250);
      setTimeout(setupBolsosDropdown, 1000);
      setTimeout(setupBolsosDropdown, 2000);
    })();
    </script>
    <?php
}, 999);
/* PRIME_DROP_MOBILE_BOLSOS_DROPDOWN_FIX_END */

/* PRIME_DROP_PRODUCT_DETAILS_COMPACT_FIX_START */
add_action('wp_head', function () {
    ?>
    <style id="pd-product-details-compact-css">
    /* Producto: detalles estilo limpio tipo Coach, cerrado por defecto */
    .single-product .pd-coach-details {
      margin-top: 24px !important;
      border-top: 1px solid #e5e5e5 !important;
    }

    .single-product .pd-coach-detail {
      border-bottom: 1px solid #e5e5e5 !important;
      margin: 0 !important;
    }

    .single-product .pd-coach-detail summary {
      min-height: 54px !important;
      padding: 17px 0 !important;
      display: flex !important;
      align-items: center !important;
      justify-content: space-between !important;
      gap: 18px !important;
      cursor: pointer !important;
      font-family: 'Inter', sans-serif !important;
      font-size: 12px !important;
      font-weight: 700 !important;
      letter-spacing: 1.4px !important;
      line-height: 1.3 !important;
      text-transform: uppercase !important;
      color: #000000 !important;
      list-style: none !important;
    }

    .single-product .pd-coach-detail summary::-webkit-details-marker {
      display: none !important;
    }

    .single-product .pd-coach-plus {
      width: 18px !important;
      height: 18px !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      flex: 0 0 18px !important;
      font-size: 18px !important;
      font-weight: 400 !important;
      line-height: 1 !important;
      transition: transform .2s ease !important;
    }

    .single-product .pd-coach-detail[open] .pd-coach-plus {
      transform: rotate(45deg) !important;
    }

    .single-product .pd-coach-detail > .woocommerce-Tabs-panel {
      display: none !important;
      padding: 0 0 18px !important;
      margin: 0 !important;
      font-family: 'Inter', sans-serif !important;
      font-size: 13px !important;
      line-height: 1.55 !important;
      color: #333333 !important;
    }

    .single-product .pd-coach-detail[open] > .woocommerce-Tabs-panel {
      display: block !important;
    }

    .single-product .pd-coach-detail h2,
    .single-product .pd-coach-detail h3 {
      display: none !important;
    }

    .single-product .pd-coach-detail p {
      margin: 0 0 10px !important;
      font-size: 13px !important;
      line-height: 1.55 !important;
      color: #333333 !important;
    }

    .single-product .pd-coach-detail ul,
    .single-product .pd-coach-detail ol {
      margin: 10px 0 0 !important;
      padding: 0 !important;
      list-style: none !important;
    }

    .single-product .pd-coach-detail li {
      position: relative !important;
      margin: 0 0 7px !important;
      padding: 0 0 0 14px !important;
      font-size: 13px !important;
      line-height: 1.45 !important;
      color: #333333 !important;
    }

    .single-product .pd-coach-detail li::before {
      content: "" !important;
      position: absolute !important;
      left: 0 !important;
      top: .65em !important;
      width: 4px !important;
      height: 4px !important;
      border-radius: 50% !important;
      background: #000000 !important;
    }

    .single-product .pd-coach-detail li p {
      margin: 0 !important;
    }

    @media (max-width: 768px) {
      .single-product .pd-coach-details {
        margin-top: 18px !important;
      }

      .single-product .pd-coach-detail summary {
        min-height: 50px !important;
        padding: 15px 0 !important;
        font-size: 11px !important;
      }
    }
    </style>
    <?php
}, 1001);

add_action('wp_footer', function () {
    ?>
    <script id="pd-product-details-compact-js">
    (function() {
      function compactPrimeDropDetails() {
        if (!document.body.classList.contains('single-product')) return;

        document.querySelectorAll('.pd-coach-detail').forEach(function(detail) {
          if (detail.dataset.pdCompactReady === '1') return;
          detail.dataset.pdCompactReady = '1';
          detail.removeAttribute('open');

          var panel = detail.querySelector(':scope > .woocommerce-Tabs-panel');
          if (panel) {
            panel.style.removeProperty('display');
          }
        });
      }

      document.addEventListener('DOMContentLoaded', compactPrimeDropDetails);
      setTimeout(compactPrimeDropDetails, 250);
      setTimeout(compactPrimeDropDetails, 900);
      setTimeout(compactPrimeDropDetails, 1800);
    })();
    </script>
    <?php
}, 1001);
/* PRIME_DROP_PRODUCT_DETAILS_COMPACT_FIX_END */

/* PRIME_DROP_FOOTER_CONTACT_POLICIES_START */
add_action('wp_head', function () {
    ?>
    <style id="pd-footer-contact-policies-css">
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Serif:wght@400;500;600;700&display=swap');

    .pd-footer,
    .pd-footer * {
      font-family: 'Roboto Serif', serif !important;
    }

    .pd-footer-contact .pd-footer-policies {
      display: flex !important;
      flex-direction: column !important;
      gap: 8px !important;
      margin-top: 8px !important;
    }

    .pd-footer-contact .pd-footer-policies a {
      color: #ffffff !important;
      text-decoration: none !important;
      font-size: 12px !important;
      line-height: 1.45 !important;
    }

    .pd-footer-contact .pd-footer-policies a:hover {
      opacity: .75 !important;
      text-decoration: underline !important;
    }

    .pd-footer-social-column .pd-social-icons {
      display: flex !important;
      align-items: center !important;
      gap: 12px !important;
      flex-wrap: wrap !important;
    }

    .pd-footer-social-column .pd-social-icons a {
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
    }

    .pd-footer-social-column .pd-social-icons svg {
      width: 18px !important;
      height: 18px !important;
    }

    .pd-footer-social-column .pd-social-email svg {
      width: 22px !important;
      height: 22px !important;
      display: block !important;
    }

    .pd-policy-page {
      max-width: 900px !important;
      margin: 90px auto !important;
      padding: 0 24px !important;
      color: #111111 !important;
    }

    .pd-policy-page h1,
    .pd-policy-page h2 {
      font-family: 'Roboto Serif', serif !important;
      color: #000000 !important;
    }

    .pd-policy-page h1 {
      font-size: clamp(34px, 5vw, 58px) !important;
      margin-bottom: 28px !important;
    }

    .pd-policy-page h2 {
      font-size: 22px !important;
      margin-top: 32px !important;
      margin-bottom: 10px !important;
    }

    .pd-policy-page p {
      font-family: 'Roboto Serif', serif !important;
      font-size: 16px !important;
      line-height: 1.75 !important;
      margin-bottom: 14px !important;
    }

    @media (max-width: 768px) {
      .pd-footer-contact .pd-footer-policies {
        align-items: center !important;
      }

      .pd-footer-social-column .pd-social-icons {
        justify-content: center !important;
      }
    }
    </style>
    <?php
}, 1002);

add_action('wp_footer', function () {
    ?>
    <script id="pd-footer-contact-policies-js">
    (function() {
      function updatePrimeDropFooterPoliciesAndSocialEmail() {
        document.querySelectorAll('.pd-footer-contact').forEach(function(column) {
          column.innerHTML =
            '<h4>POLÍTICAS</h4>' +
            '<div class="pd-footer-policies" aria-label="Políticas">' +
              '<a href="/terminos-y-condiciones/">Términos y condiciones</a>' +
              '<a href="/politica-de-privacidad/">Política de Privacidad</a>' +
              '<a href="/politica-de-reembolso/">Política de Reembolso</a>' +
            '</div>';
        });

        document.querySelectorAll('.pd-footer-social-column .pd-social-icons').forEach(function(icons) {
          var existing = icons.querySelector('.pd-social-email');
          if (existing) existing.remove();

          var email = document.createElement('a');
          email.className = 'pd-social-email';
          email.href = 'mailto:primedropelite@gmail.com';
          email.setAttribute('aria-label', 'Gmail');
          email.innerHTML =
            '<svg viewBox="0 0 48 48" aria-hidden="true">' +
              '<path fill="#4CAF50" d="M45 16.2V37c0 1.7-1.3 3-3 3h-7V23.7l10-7.5z"></path>' +
              '<path fill="#1E88E5" d="M3 16.2V37c0 1.7 1.3 3 3 3h7V23.7L3 16.2z"></path>' +
              '<path fill="#E53935" d="M35 11.2 24 19.5 13 11.2l-1 6 1 6.5 11 8.3 11-8.3 1-6.5-1-6z"></path>' +
              '<path fill="#C62828" d="M3 12.3v3.9l10 7.5V11.2L9.9 8.9C7.9 7.4 5.1 7.8 3.7 9.7 3.2 10.3 3 11 3 11.8v.5z"></path>' +
              '<path fill="#FBC02D" d="M45 12.3v3.9l-10 7.5V11.2l3.1-2.3c2-1.5 4.8-1.1 6.2.8.5.6.7 1.3.7 2.1v.5z"></path>' +
            '</svg>';
          icons.appendChild(email);
        });
      }

      document.addEventListener('DOMContentLoaded', updatePrimeDropFooterPoliciesAndSocialEmail);
      setTimeout(updatePrimeDropFooterPoliciesAndSocialEmail, 250);
      setTimeout(updatePrimeDropFooterPoliciesAndSocialEmail, 1000);
      setTimeout(updatePrimeDropFooterPoliciesAndSocialEmail, 2000);
    })();
    </script>
    <?php
}, 1002);
/* PRIME_DROP_FOOTER_CONTACT_POLICIES_END */

/* PRIME_DROP_SELECTION_VISUAL_START */
add_action('wp_head', function() {
    ?>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto+Serif:opsz,wght@8..144,400;8..144,500;8..144,600;8..144,700&display=swap" rel="stylesheet">
    <style id="prime-drop-selection-visual">
    /* Prime Drop - tipografia global */
    html body,
    html body *:not(svg):not(path):not(i):not(.dashicons):not([class*="icon"]):not([class*="Icon"]) {
      font-family: "Roboto Serif", Georgia, serif !important;
    }

    input,
    select,
    textarea,
    button {
      font-family: "Roboto Serif", Georgia, serif !important;
    }

    /* Botones redondeados en todo WooCommerce */
    .woocommerce a.button,
    .woocommerce button.button,
    .woocommerce input.button,
    .woocommerce #respond input#submit,
    .woocommerce a.button.alt,
    .woocommerce button.button.alt,
    .woocommerce input.button.alt,
    .woocommerce #payment #place_order,
    .single_add_to_cart_button,
    .wp-block-button__link,
    .elementor-button,
    .elementor-button-wrapper .elementor-button,
    a.button,
    button[type="submit"],
    input[type="submit"],
    .pd-cart-checkout,
    .wc-block-components-button {
      border-radius: 25px !important;
      overflow: hidden !important;
    }

    /* Producto: cantidad + boton alineados y redondeados */
    .single-product form.cart {
      display: flex !important;
      align-items: center !important;
      gap: 10px !important;
      flex-wrap: wrap !important;
    }

    .single-product form.cart .quantity,
    .single-product .quantity {
      border-radius: 25px !important;
      overflow: hidden !important;
      height: 44px !important;
      min-height: 44px !important;
      display: inline-flex !important;
      align-items: center !important;
      border: 1px solid #000000 !important;
      background: #ffffff !important;
    }

    .single-product form.cart .quantity input,
    .single-product form.cart .quantity button,
    .single-product .quantity input,
    .single-product .quantity button {
      height: 44px !important;
      border: 0 !important;
      background: #ffffff !important;
      color: #000000 !important;
      box-shadow: none !important;
    }

    .single-product form.cart .single_add_to_cart_button {
      height: 44px !important;
      min-height: 44px !important;
      padding: 0 28px !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      border-radius: 25px !important;
      background: #000000 !important;
      color: #ffffff !important;
      border: 0 !important;
    }

    /* Checkout centrado y consistente */
    body.woocommerce-checkout .site-main,
    body.woocommerce-checkout main.site-main,
    body.woocommerce-checkout .ct-main {
      padding-top: 0 !important;
    }

    body.woocommerce-checkout .entry-header {
      max-width: 1180px !important;
      margin: 0 auto !important;
      padding: 42px 24px 22px !important;
      text-align: center !important;
    }

    body.woocommerce-checkout .entry-header .page-title,
    body.woocommerce-checkout .entry-title {
      margin: 0 !important;
      text-align: center !important;
      font-size: clamp(32px, 3vw, 46px) !important;
      line-height: 1.08 !important;
      color: #000000 !important;
    }

    body.woocommerce-checkout .woocommerce {
      max-width: 1180px !important;
      margin-left: auto !important;
      margin-right: auto !important;
      padding-left: 24px !important;
      padding-right: 24px !important;
      box-sizing: border-box !important;
    }

    body.woocommerce-checkout .woocommerce-form-login-toggle,
    body.woocommerce-checkout .woocommerce-form-coupon-toggle {
      max-width: 1180px !important;
      margin: 0 auto 24px !important;
      padding: 0 !important;
    }

    body.woocommerce-checkout form.checkout,
    body.woocommerce-checkout form.checkout.ct-woocommerce-checkout {
      width: 100% !important;
      max-width: 1180px !important;
      margin: 0 auto 80px !important;
      padding: 0 !important;
      display: grid !important;
      grid-template-columns: minmax(0, 1fr) minmax(390px, 0.82fr) !important;
      column-gap: 56px !important;
      row-gap: 28px !important;
      align-items: start !important;
      box-sizing: border-box !important;
    }

    body.woocommerce-checkout #customer_details,
    body.woocommerce-checkout .col2-set {
      grid-column: 1 !important;
      width: 100% !important;
      max-width: none !important;
      float: none !important;
      margin: 0 !important;
      padding: 0 !important;
    }

    body.woocommerce-checkout #order_review_heading,
    body.woocommerce-checkout #order_review {
      grid-column: 2 !important;
      width: 100% !important;
      max-width: none !important;
      float: none !important;
      margin-left: 0 !important;
      margin-right: 0 !important;
      padding-left: 0 !important;
      padding-right: 0 !important;
      box-sizing: border-box !important;
    }

    body.woocommerce-checkout #order_review_heading {
      margin-top: 0 !important;
      margin-bottom: 18px !important;
    }

    body.woocommerce-checkout .form-row {
      margin-bottom: 20px !important;
    }

    body.woocommerce-checkout input.input-text,
    body.woocommerce-checkout textarea,
    body.woocommerce-checkout select,
    body.woocommerce-checkout .select2-container--default .select2-selection--single {
      min-height: 46px !important;
      border-radius: 25px !important;
      border: 1px solid #d9d9d9 !important;
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      background: #ffffff !important;
      box-shadow: none !important;
      padding-left: 16px !important;
      padding-right: 16px !important;
      box-sizing: border-box !important;
    }

    body.woocommerce-checkout .select2-container--default .select2-selection--single .select2-selection__rendered {
      line-height: 46px !important;
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      padding-left: 0 !important;
    }

    body.woocommerce-checkout .select2-container--default .select2-selection--single .select2-selection__arrow {
      height: 46px !important;
      right: 12px !important;
    }

    /* Metodo de pago: radio visible, negro con punto blanco */
    body.woocommerce-checkout #payment ul.payment_methods,
    body.woocommerce-checkout #payment ul.payment_methods li,
    body.woocommerce-checkout .wc_payment_method,
    body.woocommerce-checkout #payment ul.payment_methods li:hover,
    body.woocommerce-checkout .wc_payment_method:hover {
      background: transparent !important;
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      opacity: 1 !important;
    }

    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method {
      position: relative !important;
    }

    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method > input.input-radio,
    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method > input[name="payment_method"] {
      position: absolute !important;
      left: 18px !important;
      top: 24px !important;
      width: 1px !important;
      height: 1px !important;
      min-width: 1px !important;
      opacity: 0 !important;
      pointer-events: none !important;
      appearance: none !important;
      -webkit-appearance: none !important;
    }

    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method > label {
      position: relative !important;
      display: flex !important;
      align-items: center !important;
      min-height: 28px !important;
      padding-left: 34px !important;
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      opacity: 1 !important;
      background: transparent !important;
      cursor: pointer !important;
    }

    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method > label::before {
      content: "" !important;
      position: absolute !important;
      left: 0 !important;
      top: 50% !important;
      transform: translateY(-50%) !important;
      width: 18px !important;
      height: 18px !important;
      border: 1.5px solid #d7d7d7 !important;
      border-radius: 50% !important;
      background: #ffffff !important;
      box-sizing: border-box !important;
    }

    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method > input.input-radio:checked + label::before,
    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method > input[name="payment_method"]:checked + label::before {
      border-color: #000000 !important;
      background: radial-gradient(circle at center, #ffffff 0 3px, #000000 3.4px 100%) !important;
    }

    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method > input.input-radio:checked + label,
    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method > input[name="payment_method"]:checked + label {
      font-weight: 700 !important;
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
    }

    body.woocommerce-checkout #payment ul.payment_methods li label:hover,
    body.woocommerce-checkout .wc_payment_method label:hover {
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      opacity: 1 !important;
    }

    /* Header tablet/iPad: cuenta, bolsa y menu alineados */
    @media (min-width: 768px) and (max-width: 1024px) {
      .ct-header [data-column="end"],
      .ct-header .ct-header-account,
      .ct-header .ct-header-cart,
      .ct-header-trigger {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        position: static !important;
        transform: none !important;
      }

      .ct-header [data-column="end"] {
        gap: 14px !important;
        justify-content: flex-end !important;
      }

      .ct-header .ct-header-account,
      .ct-header .ct-header-cart,
      .ct-header-trigger {
        margin: 0 !important;
        padding: 0 !important;
      }
    }

    @media (max-width: 1024px) {
      body.woocommerce-checkout .woocommerce {
        max-width: 760px !important;
        padding-left: 22px !important;
        padding-right: 22px !important;
      }

      body.woocommerce-checkout form.checkout,
      body.woocommerce-checkout form.checkout.ct-woocommerce-checkout {
        grid-template-columns: 1fr !important;
        gap: 28px !important;
      }

      body.woocommerce-checkout #customer_details,
      body.woocommerce-checkout #order_review_heading,
      body.woocommerce-checkout #order_review {
        grid-column: 1 !important;
      }
    }

    @media (max-width: 600px) {
      body.woocommerce-checkout .entry-header {
        padding: 30px 18px 18px !important;
      }

      body.woocommerce-checkout .woocommerce {
        padding-left: 16px !important;
        padding-right: 16px !important;
      }
    }
    </style>
    <script id="prime-drop-checkout-drawer-fix">
    (function() {
      function closePrimeDropCartDrawer() {
        var onCheckout = document.body.classList.contains('woocommerce-checkout') || /\/checkout\/?/.test(window.location.pathname);
        if (!onCheckout) return;

        document.querySelectorAll('#cart-drawer, .cart-drawer, .pd-cart-drawer').forEach(function(el) {
          el.classList.remove('active', 'open', 'show', 'is-open');
          el.setAttribute('aria-hidden', 'true');
        });

        document.querySelectorAll('#cart-drawer-overlay, .cart-drawer-overlay, .pd-cart-overlay, .pd-cart-drawer-overlay').forEach(function(el) {
          el.classList.remove('active', 'open', 'show', 'is-open');
        });

        document.body.style.overflow = '';
        document.body.style.position = '';
        document.body.style.width = '';
      }

      document.addEventListener('click', function(event) {
        var link = event.target.closest('a[href*="checkout"], a[href*="/checkout/"]');
        if (!link) return;
        closePrimeDropCartDrawer();
        window.sessionStorage.setItem('pd_close_cart_on_checkout', '1');
      }, true);

      document.addEventListener('DOMContentLoaded', closePrimeDropCartDrawer);
      window.addEventListener('pageshow', closePrimeDropCartDrawer);
      window.addEventListener('load', closePrimeDropCartDrawer);
      setTimeout(closePrimeDropCartDrawer, 250);
      setTimeout(closePrimeDropCartDrawer, 900);
    })();
    </script>
    <?php
}, 999);
/* PRIME_DROP_SELECTION_VISUAL_END */

/* PRIME_DROP_ROUND_BUTTONS_FINAL_START */
add_action('wp_footer', function() {
    ?>
    <style id="prime-drop-round-buttons-final">
    body.woocommerce button,
    body.woocommerce a.button,
    body.woocommerce button.button,
    body.woocommerce input.button,
    body.woocommerce a.button.alt,
    body.woocommerce button.button.alt,
    body.woocommerce input.button.alt,
    body.woocommerce #payment #place_order,
    body.single-product form.cart button.single_add_to_cart_button,
    body.single-product form.cart .single_add_to_cart_button,
    body .single_add_to_cart_button,
    body .add_to_cart_button,
    body .product_type_simple,
    body .wp-block-button__link,
    body .elementor-button,
    body .pd-cart-checkout,
    body .wc-block-components-button,
    body button[type="submit"],
    body input[type="submit"] {
      border-radius: 25px !important;
      -webkit-border-radius: 25px !important;
    }

    body.single-product form.cart .quantity,
    body.single-product .quantity,
    body.woocommerce .quantity {
      border-radius: 25px !important;
      -webkit-border-radius: 25px !important;
      overflow: hidden !important;
    }
    </style>
    <script id="prime-drop-round-buttons-final-js">
    (function() {
      function roundPrimeDropButtons() {
        document.querySelectorAll('button, a.button, .single_add_to_cart_button, .add_to_cart_button, .elementor-button, .pd-cart-checkout, .wc-block-components-button, input[type="submit"]').forEach(function(el) {
          el.style.setProperty('border-radius', '25px', 'important');
          el.style.setProperty('-webkit-border-radius', '25px', 'important');
        });
        document.querySelectorAll('.single-product form.cart .quantity, .woocommerce .quantity').forEach(function(el) {
          el.style.setProperty('border-radius', '25px', 'important');
          el.style.setProperty('overflow', 'hidden', 'important');
        });
      }
      document.addEventListener('DOMContentLoaded', roundPrimeDropButtons);
      window.addEventListener('load', roundPrimeDropButtons);
      setTimeout(roundPrimeDropButtons, 500);
      setTimeout(roundPrimeDropButtons, 1500);
    })();
    </script>
    <?php
}, 9999);
/* PRIME_DROP_ROUND_BUTTONS_FINAL_END */

/* PRIME_DROP_PRODUCT_RELATED_RESPONSIVE_START */
add_action('wp_footer', function() {
    if (!is_product()) {
        return;
    }
    ?>
    <style id="prime-drop-product-related-responsive">
    /* Producto: quitar aire superior en tablet/movil sin tocar desktop general */
    @media (max-width: 1024px) {
      body.single-product .site-main,
      body.single-product main.site-main,
      body.single-product .ct-main {
        padding-top: 0 !important;
        margin-top: 0 !important;
      }

      body.single-product div.product,
      body.single-product .product {
        margin-top: 0 !important;
        padding-top: 18px !important;
      }
    }

    /* Producto: cantidad + anadir centrado en todos los dispositivos */
    body.single-product form.cart {
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      gap: 10px !important;
      flex-wrap: wrap !important;
      width: 100% !important;
      text-align: center !important;
    }

    body.single-product form.cart .quantity,
    body.single-product .quantity {
      margin: 0 !important;
      border-radius: 25px !important;
      overflow: hidden !important;
    }

    body.single-product form.cart .single_add_to_cart_button,
    body.single-product .single_add_to_cart_button {
      margin: 0 !important;
      border-radius: 25px !important;
      -webkit-border-radius: 25px !important;
      align-self: center !important;
    }

    /* Productos relacionados visibles y ordenados tambien en tablet/movil */
    body.single-product .related.products,
    body.single-product section.related.products,
    body.single-product section.related {
      display: block !important;
      visibility: visible !important;
      opacity: 1 !important;
      max-width: 1280px !important;
      margin: 72px auto 0 !important;
      padding: 0 24px !important;
      box-sizing: border-box !important;
    }

    body.single-product .related.products > h2,
    body.single-product section.related > h2 {
      margin: 0 0 28px !important;
      text-align: left !important;
    }

    body.single-product .related.products ul.products,
    body.single-product section.related ul.products {
      display: grid !important;
      grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
      gap: 30px !important;
      align-items: stretch !important;
      justify-content: center !important;
      margin: 0 !important;
      padding: 0 !important;
    }

    body.single-product .related.products ul.products li.product,
    body.single-product section.related ul.products li.product {
      width: auto !important;
      max-width: none !important;
      min-width: 0 !important;
      height: auto !important;
      min-height: 0 !important;
      flex: initial !important;
      display: flex !important;
      flex-direction: column !important;
      align-items: center !important;
      text-align: center !important;
      margin: 0 !important;
    }

    body.single-product .related.products ul.products li.product a.woocommerce-loop-product__link,
    body.single-product section.related ul.products li.product a.woocommerce-loop-product__link {
      width: 100% !important;
      display: flex !important;
      flex-direction: column !important;
      align-items: center !important;
      text-align: center !important;
    }

    body.single-product .related.products ul.products li.product .button,
    body.single-product .related.products ul.products li.product .add_to_cart_button,
    body.single-product section.related ul.products li.product .button,
    body.single-product section.related ul.products li.product .add_to_cart_button {
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      align-self: center !important;
      width: auto !important;
      min-width: 182px !important;
      max-width: 100% !important;
      margin: 18px auto 0 !important;
      text-align: center !important;
      border-radius: 25px !important;
      -webkit-border-radius: 25px !important;
    }

    @media (max-width: 1024px) {
      body.single-product .related.products,
      body.single-product section.related.products,
      body.single-product section.related {
        margin-top: 52px !important;
        padding-left: 22px !important;
        padding-right: 22px !important;
      }

      body.single-product .related.products ul.products,
      body.single-product section.related ul.products {
        grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
        gap: 26px 18px !important;
      }
    }

    @media (max-width: 520px) {
      body.single-product form.cart {
        justify-content: center !important;
      }

      body.single-product .related.products,
      body.single-product section.related.products,
      body.single-product section.related {
        padding-left: 16px !important;
        padding-right: 16px !important;
      }

      body.single-product .related.products ul.products,
      body.single-product section.related ul.products {
        grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
        gap: 24px 14px !important;
      }

      body.single-product .related.products ul.products li.product .button,
      body.single-product .related.products ul.products li.product .add_to_cart_button,
      body.single-product section.related ul.products li.product .button,
      body.single-product section.related ul.products li.product .add_to_cart_button {
        min-width: 0 !important;
        width: 100% !important;
        padding-left: 12px !important;
        padding-right: 12px !important;
      }
    }
    </style>
    <?php
}, 10000);
/* PRIME_DROP_PRODUCT_RELATED_RESPONSIVE_END */

/* PRIME_DROP_PRODUCT_QTY_WISHLIST_START */
add_action('wp_footer', function() {
    if (!is_product()) {
        return;
    }
    ?>
    <style id="prime-drop-product-qty-wishlist">
    /* Producto tablet/iPad: compactar espacio superior solo en ficha de producto */
    @media (max-width: 1024px) {
      body.single-product #header [data-device="desktop"] [data-row="middle"] {
        min-height: 108px !important;
        height: 108px !important;
      }

      body.single-product #header [data-device="desktop"] [data-row="middle"] > .ct-container {
        min-height: 96px !important;
        height: 96px !important;
        grid-template-rows: 54px 42px !important;
        row-gap: 0 !important;
        padding-top: 6px !important;
        padding-bottom: 6px !important;
        align-items: center !important;
      }

      body.single-product #header [data-device="desktop"] [data-row="middle"] [data-column="start"],
      body.single-product #header [data-device="desktop"] [data-row="middle"] [data-column="end"] {
        min-height: 54px !important;
        height: 54px !important;
      }

      body.single-product #header [data-device="desktop"] [data-row="middle"] [data-column="middle"] {
        min-height: 42px !important;
        height: 42px !important;
      }

      body.single-product div.product {
        padding-top: 6px !important;
      }
    }

    /* Cantidad: dejar espacio real para el numero entre - y + */
    body.single-product form.cart .quantity,
    body.single-product .quantity[data-type="type-2"] {
      width: 112px !important;
      min-width: 112px !important;
      height: 44px !important;
      min-height: 44px !important;
      position: relative !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      border: 1px solid #000000 !important;
      border-radius: 25px !important;
      background: #ffffff !important;
      overflow: hidden !important;
      margin: 0 !important;
    }

    body.single-product form.cart .quantity .qty,
    body.single-product .quantity[data-type="type-2"] .qty {
      width: 100% !important;
      min-width: 100% !important;
      height: 44px !important;
      line-height: 44px !important;
      padding: 0 38px !important;
      text-align: center !important;
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      opacity: 1 !important;
      font-size: 15px !important;
      font-weight: 600 !important;
      background: transparent !important;
      border: 0 !important;
      box-shadow: none !important;
      appearance: textfield !important;
      -moz-appearance: textfield !important;
      z-index: 1 !important;
    }

    body.single-product form.cart .quantity .qty::-webkit-inner-spin-button,
    body.single-product form.cart .quantity .qty::-webkit-outer-spin-button {
      -webkit-appearance: none !important;
      margin: 0 !important;
    }

    body.single-product form.cart .quantity .ct-decrease,
    body.single-product form.cart .quantity .ct-increase,
    body.single-product .quantity[data-type="type-2"] .ct-decrease,
    body.single-product .quantity[data-type="type-2"] .ct-increase {
      position: absolute !important;
      top: 0 !important;
      width: 36px !important;
      height: 44px !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      color: #000000 !important;
      z-index: 2 !important;
      cursor: pointer !important;
      background: transparent !important;
    }

    body.single-product form.cart .quantity .ct-decrease,
    body.single-product .quantity[data-type="type-2"] .ct-decrease {
      left: 0 !important;
    }

    body.single-product form.cart .quantity .ct-increase,
    body.single-product .quantity[data-type="type-2"] .ct-increase {
      right: 0 !important;
    }

    body.single-product form.cart {
      justify-content: center !important;
      gap: 12px !important;
    }

    /* Wishlist: boton visible, elegante y centrado */
    body.single-product .yith-add-to-wishlist-button-block,
    body.single-product .yith-wcwl-add-to-wishlist {
      width: 100% !important;
      display: flex !important;
      justify-content: center !important;
      align-items: center !important;
      margin: 20px auto 0 !important;
      padding: 0 !important;
      border: 0 !important;
    }

    body.single-product .yith-wcwl-add-to-wishlist-button,
    body.single-product .yith-wcwl-add-button a,
    body.single-product a[href*="wishlist"] {
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      gap: 10px !important;
      min-height: 44px !important;
      padding: 11px 22px !important;
      border: 1px solid #d9d9d9 !important;
      border-radius: 25px !important;
      background: #ffffff !important;
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      text-decoration: none !important;
      font-size: 12px !important;
      font-weight: 700 !important;
      letter-spacing: 1.2px !important;
      text-transform: uppercase !important;
      transition: background-color 0.2s ease, color 0.2s ease, border-color 0.2s ease !important;
    }

    body.single-product .yith-wcwl-add-to-wishlist-button:hover,
    body.single-product .yith-wcwl-add-button a:hover,
    body.single-product a[href*="wishlist"]:hover {
      background: #000000 !important;
      color: #ffffff !important;
      -webkit-text-fill-color: #ffffff !important;
      border-color: #000000 !important;
    }

    body.single-product .yith-wcwl-add-to-wishlist-button svg,
    body.single-product .yith-wcwl-add-button a svg {
      width: 17px !important;
      height: 17px !important;
      flex: 0 0 auto !important;
      stroke: currentColor !important;
    }
    </style>
    <?php
}, 10001);
/* PRIME_DROP_PRODUCT_QTY_WISHLIST_END */

/* PRIME_DROP_WISHLIST_PAGE_START */
add_action('wp_footer', function() {
    if (!is_page('wishlist') && !is_page(591)) {
        return;
    }
    ?>
    <style id="prime-drop-wishlist-page">
    body.woocommerce-wishlist .entry-header {
      max-width: 1180px !important;
      margin: 0 auto !important;
      padding: 44px 24px 28px !important;
      text-align: center !important;
      background: #ffffff !important;
    }

    body.woocommerce-wishlist .entry-title,
    body.woocommerce-wishlist .page-title {
      margin: 0 !important;
      color: #000000 !important;
      font-size: clamp(34px, 4vw, 54px) !important;
      line-height: 1.05 !important;
      letter-spacing: 0 !important;
    }

    body.woocommerce-wishlist .entry-content {
      max-width: 1180px !important;
      margin: 0 auto 90px !important;
      padding: 0 24px !important;
      box-sizing: border-box !important;
    }

    body.woocommerce-wishlist .yith-wcwl-form {
      width: 100% !important;
      max-width: 100% !important;
      margin: 0 auto !important;
      padding: 0 !important;
    }

    body.woocommerce-wishlist .wishlist-title-container,
    body.woocommerce-wishlist .wishlist-title {
      text-align: center !important;
      margin: 0 0 28px !important;
    }

    body.woocommerce-wishlist .wishlist-title h2,
    body.woocommerce-wishlist .yith-wcwl-form h2 {
      margin: 0 !important;
      font-size: clamp(28px, 3vw, 42px) !important;
      line-height: 1.1 !important;
      color: #000000 !important;
      text-align: center !important;
    }

    body.woocommerce-wishlist .wishlist_table {
      width: 100% !important;
      border: 1px solid #eeeeee !important;
      border-radius: 14px !important;
      overflow: hidden !important;
      background: #ffffff !important;
      box-shadow: 0 18px 50px rgba(0, 0, 0, 0.05) !important;
      border-collapse: separate !important;
      border-spacing: 0 !important;
      margin: 0 !important;
    }

    body.woocommerce-wishlist .wishlist_table th {
      padding: 18px 16px !important;
      background: #f7f7f7 !important;
      color: #000000 !important;
      font-size: 11px !important;
      font-weight: 700 !important;
      letter-spacing: 1.4px !important;
      text-transform: uppercase !important;
      text-align: center !important;
      border: 0 !important;
    }

    body.woocommerce-wishlist .wishlist_table td {
      padding: 18px 16px !important;
      vertical-align: middle !important;
      text-align: center !important;
      border-top: 1px solid #f0f0f0 !important;
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
    }

    body.woocommerce-wishlist .wishlist_table .product-thumbnail img {
      width: 92px !important;
      height: 92px !important;
      object-fit: contain !important;
      background: #f7f7f7 !important;
      border-radius: 10px !important;
      padding: 8px !important;
    }

    body.woocommerce-wishlist .wishlist_table .product-name a {
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      font-size: 15px !important;
      font-weight: 700 !important;
      line-height: 1.35 !important;
      text-decoration: none !important;
    }

    body.woocommerce-wishlist .wishlist_table .product-price,
    body.woocommerce-wishlist .wishlist_table .product-price * {
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      font-weight: 600 !important;
    }

    body.woocommerce-wishlist .wishlist_table .product-stock-status span {
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      min-height: 30px !important;
      padding: 6px 13px !important;
      border-radius: 20px !important;
      background: #f3f3f3 !important;
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      font-size: 11px !important;
      font-weight: 700 !important;
      letter-spacing: 1px !important;
      text-transform: uppercase !important;
    }

    body.woocommerce-wishlist .wishlist_table .product-add-to-cart a,
    body.woocommerce-wishlist .wishlist_table .product-add-to-cart .button {
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      min-height: 42px !important;
      padding: 11px 24px !important;
      border-radius: 25px !important;
      background: #000000 !important;
      color: #ffffff !important;
      -webkit-text-fill-color: #ffffff !important;
      border: 0 !important;
      font-size: 11px !important;
      font-weight: 700 !important;
      letter-spacing: 1.5px !important;
      text-transform: uppercase !important;
      text-decoration: none !important;
      white-space: nowrap !important;
    }

    body.woocommerce-wishlist .wishlist_table .product-remove a {
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      width: 34px !important;
      height: 34px !important;
      border-radius: 50% !important;
      border: 1px solid #eeeeee !important;
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      background: #ffffff !important;
      text-decoration: none !important;
    }

    body.woocommerce-wishlist.pd-wishlist-empty .wishlist_table thead {
      display: none !important;
    }

    body.woocommerce-wishlist .wishlist-empty {
      padding: 58px 24px !important;
      text-align: center !important;
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      font-size: 0 !important;
      border: 0 !important;
    }

    body.woocommerce-wishlist .wishlist-empty::before {
      content: "♡" !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      width: 58px !important;
      height: 58px !important;
      margin: 0 auto 18px !important;
      border-radius: 50% !important;
      border: 1px solid #e4e4e4 !important;
      color: #000000 !important;
      font-size: 30px !important;
      line-height: 1 !important;
    }

    body.woocommerce-wishlist .wishlist-empty::after {
      content: "Tu lista de deseos está vacía" !important;
      display: block !important;
      max-width: 360px !important;
      margin: 0 auto !important;
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      font-size: 22px !important;
      font-weight: 700 !important;
      line-height: 1.25 !important;
      text-align: center !important;
    }

    body.woocommerce-wishlist .pd-wishlist-empty-copy {
      max-width: 430px !important;
      margin: 12px auto 0 !important;
      color: #555555 !important;
      -webkit-text-fill-color: #555555 !important;
      font-size: 14px !important;
      line-height: 1.55 !important;
      text-align: center !important;
    }

    body.woocommerce-wishlist .pd-wishlist-empty-cta {
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      min-height: 44px !important;
      margin: 22px auto 0 !important;
      padding: 12px 28px !important;
      border-radius: 25px !important;
      background: #000000 !important;
      color: #ffffff !important;
      -webkit-text-fill-color: #ffffff !important;
      font-size: 12px !important;
      font-weight: 700 !important;
      letter-spacing: 1.8px !important;
      text-transform: uppercase !important;
      text-decoration: none !important;
    }

    @media (max-width: 768px) {
      body.woocommerce-wishlist .entry-header {
        padding: 34px 18px 18px !important;
      }

      body.woocommerce-wishlist .entry-content {
        padding-left: 16px !important;
        padding-right: 16px !important;
        margin-bottom: 64px !important;
      }

      body.woocommerce-wishlist .wishlist_table,
      body.woocommerce-wishlist .wishlist_table thead,
      body.woocommerce-wishlist .wishlist_table tbody,
      body.woocommerce-wishlist .wishlist_table tr,
      body.woocommerce-wishlist .wishlist_table td {
        display: block !important;
        width: 100% !important;
        box-sizing: border-box !important;
      }

      body.woocommerce-wishlist .wishlist_table thead {
        display: none !important;
      }

      body.woocommerce-wishlist .wishlist_table tr {
        padding: 18px !important;
        border-top: 1px solid #f0f0f0 !important;
      }

      body.woocommerce-wishlist .wishlist_table td {
        padding: 8px 0 !important;
        border: 0 !important;
      }

      body.woocommerce-wishlist .wishlist_table .product-thumbnail img {
        width: 140px !important;
        height: 140px !important;
      }

      body.woocommerce-wishlist .wishlist-empty {
        padding: 48px 20px !important;
      }
    }
    </style>
    <script id="prime-drop-wishlist-page-js">
    (function() {
      function polishWishlist() {
        var emptyCell = document.querySelector('body.woocommerce-wishlist .wishlist-empty');
        if (!emptyCell) return;
        document.body.classList.add('pd-wishlist-empty');

        if (!emptyCell.querySelector('.pd-wishlist-empty-copy')) {
          var copy = document.createElement('p');
          copy.className = 'pd-wishlist-empty-copy';
          copy.textContent = 'Guarda aquí tus bolsos favoritos para encontrarlos rápido cuando quieras comprarlos.';
          emptyCell.appendChild(copy);
        }

        if (!emptyCell.querySelector('.pd-wishlist-empty-cta')) {
          var cta = document.createElement('a');
          cta.className = 'pd-wishlist-empty-cta';
          cta.href = '/bolsos/';
          cta.textContent = 'VER BOLSOS';
          emptyCell.appendChild(cta);
        }
      }

      document.addEventListener('DOMContentLoaded', polishWishlist);
      window.addEventListener('load', polishWishlist);
      setTimeout(polishWishlist, 600);
    })();
    </script>
    <?php
}, 10002);
/* PRIME_DROP_WISHLIST_PAGE_END */

/* PRIME_DROP_CHECKOUT_MOBILE_PAYMENT_DRAWER_START */
add_action('wp_footer', function() {
    if (!is_checkout()) {
        return;
    }
    ?>
    <style id="prime-drop-checkout-stable">
    body.woocommerce-checkout .entry-header,
    body.woocommerce-checkout header.entry-header {
      width: 100% !important;
      max-width: 1180px !important;
      margin: 0 auto !important;
      padding: 34px 24px 20px !important;
      text-align: center !important;
      box-sizing: border-box !important;
    }

    body.woocommerce-checkout .entry-title,
    body.woocommerce-checkout .page-title,
    body.woocommerce-checkout h1 {
      width: 100% !important;
      max-width: 100% !important;
      margin: 0 auto !important;
      text-align: center !important;
    }

    body.woocommerce-checkout .woocommerce-form-login-toggle .woocommerce-info {
      display: flex !important;
      align-items: center !important;
      justify-content: space-between !important;
      gap: 18px !important;
      border: 1px solid #eeeeee !important;
      border-radius: 14px !important;
      background: #fafafa !important;
      padding: 16px 22px !important;
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      line-height: 1.35 !important;
    }

    body.woocommerce-checkout .woocommerce-form-login-toggle .woocommerce-info::before,
    body.woocommerce-checkout .woocommerce-info::before {
      display: none !important;
      content: none !important;
    }

    body.woocommerce-checkout .woocommerce-form-login-toggle .woocommerce-info a {
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      text-decoration: underline !important;
      text-underline-offset: 3px !important;
      white-space: nowrap !important;
    }

    body.woocommerce-checkout #payment,
    body.woocommerce-checkout #payment ul.payment_methods {
      width: 100% !important;
      max-width: 100% !important;
      box-sizing: border-box !important;
      overflow-x: hidden !important;
    }

    body.woocommerce-checkout #payment .pd-payment-title {
      display: block !important;
      margin: 0 0 14px !important;
      padding: 0 !important;
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      font-size: 16px !important;
      font-weight: 800 !important;
      line-height: 1.3 !important;
      text-align: left !important;
    }

    body.woocommerce-checkout #payment ul.payment_methods {
      border: 1px solid #eeeeee !important;
      border-radius: 14px !important;
      background: #ffffff !important;
      padding: 0 !important;
      margin: 0 0 22px !important;
    }

    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method {
      width: 100% !important;
      max-width: 100% !important;
      margin: 0 !important;
      padding: 0 !important;
      overflow: visible !important;
      background: #ffffff !important;
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      border-bottom: 1px solid #f0f0f0 !important;
      box-sizing: border-box !important;
      position: relative !important;
    }

    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method > input.input-radio,
    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method > input[name="payment_method"] {
      position: absolute !important;
      width: 0 !important;
      height: 0 !important;
      opacity: 0 !important;
      pointer-events: none !important;
      clip: rect(0 0 0 0) !important;
      clip-path: inset(50%) !important;
      margin: 0 !important;
    }

    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method > label {
      display: flex !important;
      align-items: center !important;
      width: 100% !important;
      min-height: 58px !important;
      margin: 0 !important;
      padding: 15px 16px 15px 58px !important;
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      background: #ffffff !important;
      line-height: 1.35 !important;
      box-sizing: border-box !important;
      position: relative !important;
      cursor: pointer !important;
    }

    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method > label::before {
      content: "" !important;
      position: absolute !important;
      left: 22px !important;
      top: 50% !important;
      transform: translateY(-50%) !important;
      width: 18px !important;
      height: 18px !important;
      border: 1.5px solid #d1d1d1 !important;
      border-radius: 50% !important;
      background: #ffffff !important;
      box-sizing: border-box !important;
    }

    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method > input:checked + label::before {
      border-color: #000000 !important;
      background: radial-gradient(circle at center, #ffffff 0 2.5px, #000000 3px 100%) !important;
    }

    body.woocommerce-checkout #payment .payment_box {
      margin: 0 !important;
      padding: 18px !important;
      border-top: 1px solid #f2f2f2 !important;
      background: #ffffff !important;
      overflow-x: hidden !important;
      box-sizing: border-box !important;
    }
    </style>
    <script id="prime-drop-checkout-stable-js">
    (function() {
      function ensurePaymentTitle() {
        var payment = document.querySelector('#payment');
        if (!payment) return;
        var methods = payment.querySelector('ul.payment_methods');
        if (!methods || payment.querySelector('.pd-payment-title')) return;
        var title = document.createElement('h3');
        title.className = 'pd-payment-title';
        title.textContent = 'Metodos de pago:';
        payment.insertBefore(title, methods);
      }

      function closeCheckoutDrawerOnce() {
        if (!document.body.classList.contains('woocommerce-checkout')) return;
        document.querySelectorAll('#cart-drawer, .cart-drawer, .pd-cart-drawer').forEach(function(el) {
          el.classList.remove('active', 'open', 'show', 'is-open', 'ct-open');
          el.setAttribute('aria-hidden', 'true');
        });
        document.querySelectorAll('#cart-drawer-overlay, .cart-drawer-overlay, .pd-cart-overlay, .pd-cart-drawer-overlay').forEach(function(el) {
          el.classList.remove('active', 'open', 'show', 'is-open', 'ct-open');
        });
        document.documentElement.style.overflow = '';
        document.body.style.overflow = '';
        document.body.style.position = '';
        document.body.style.top = '';
        document.body.style.left = '';
        document.body.style.right = '';
        document.body.style.width = '';
      }

      document.addEventListener('DOMContentLoaded', function() {
        ensurePaymentTitle();
        closeCheckoutDrawerOnce();
      });
      window.addEventListener('pageshow', function() {
        ensurePaymentTitle();
        closeCheckoutDrawerOnce();
      });
      document.body && document.body.addEventListener('updated_checkout', ensurePaymentTitle);
      [150, 700, 1600].forEach(function(delay) {
        setTimeout(function() {
          ensurePaymentTitle();
          closeCheckoutDrawerOnce();
        }, delay);
      });
    })();
    </script>
    <?php
}, 10003);
/* PRIME_DROP_CHECKOUT_MOBILE_PAYMENT_DRAWER_END */

/* PRIME_DROP_CHECKOUT_WISHLIST_CART_NAV_START */
add_filter('default_checkout_billing_country', function() {
    return 'CO';
});

add_filter('default_checkout_shipping_country', function() {
    return 'CO';
});

add_filter('woocommerce_checkout_fields', function($fields) {
    foreach (['billing', 'shipping'] as $section) {
        if (isset($fields[$section][$section . '_country'])) {
            $fields[$section][$section . '_country']['default'] = 'CO';
            $fields[$section][$section . '_country']['priority'] = 40;
            $fields[$section][$section . '_country']['class'] = ['form-row-wide', 'pd-country-hidden'];
        }

        if (isset($fields[$section][$section . '_state'])) {
            $fields[$section][$section . '_state']['label'] = 'Departamento';
            $fields[$section][$section . '_state']['priority'] = 55;
            $fields[$section][$section . '_state']['class'] = ['form-row-wide'];
        }

        if (isset($fields[$section][$section . '_city'])) {
            $fields[$section][$section . '_city']['label'] = 'Localidad / Ciudad';
            $fields[$section][$section . '_city']['priority'] = 60;
            $fields[$section][$section . '_city']['class'] = ['form-row-wide'];
        }

        if (isset($fields[$section][$section . '_address_1'])) {
            $fields[$section][$section . '_address_1']['priority'] = 65;
        }

        if (isset($fields[$section][$section . '_address_2'])) {
            $fields[$section][$section . '_address_2']['priority'] = 70;
        }
    }

    return $fields;
}, 30);

add_filter('woocommerce_default_address_fields', function($fields) {
    if (isset($fields['state'])) {
        $fields['state']['label'] = 'Departamento';
        $fields['state']['priority'] = 55;
    }

    if (isset($fields['city'])) {
        $fields['city']['label'] = 'Localidad / Ciudad';
        $fields['city']['priority'] = 60;
    }

    return $fields;
}, 40);

add_filter('woocommerce_get_country_locale', function($locale) {
    if (!isset($locale['CO'])) {
        $locale['CO'] = [];
    }

    $locale['CO']['state']['label'] = 'Departamento';
    $locale['CO']['state']['priority'] = 55;
    $locale['CO']['city']['label'] = 'Localidad / Ciudad';
    $locale['CO']['city']['priority'] = 60;

    return $locale;
}, 40);

add_filter('woocommerce_product_get_name', function($name) {
    return html_entity_decode($name, ENT_QUOTES | ENT_HTML5, 'UTF-8');
}, 20);

add_filter('the_title', function($title, $post_id = null) {
    if ($post_id && get_post_type($post_id) === 'product') {
        return html_entity_decode($title, ENT_QUOTES | ENT_HTML5, 'UTF-8');
    }

    return $title;
}, 20, 2);

function prime_drop_checkout_policy_text() {
    return 'Tus datos personales se utilizarán para procesar tu pedido, gestionar tu experiencia en esta tienda y otros fines descritos en nuestra <a href="' . esc_url(home_url('/politica-de-privacidad/')) . '">Política de Privacidad</a> y <a href="' . esc_url(home_url('/politica-de-reembolso/')) . '">Política de Reembolso</a>.';
}

add_filter('woocommerce_get_privacy_policy_text', function($text, $type = '') {
    if ($type === 'checkout') {
        return prime_drop_checkout_policy_text();
    }

    return $text;
}, 20, 2);

add_filter('woocommerce_checkout_privacy_policy_text', function() {
    return prime_drop_checkout_policy_text();
}, 20);

add_filter('woocommerce_ship_to_different_address_checked', '__return_false');

add_action('wp_head', function() {
    ?>
    <style id="prime-drop-head-bag-guard">
    header [data-id="cart"] svg:not(.pd-bag-icon),
    .ct-header-cart svg:not(.pd-bag-icon),
    header a[href*="cart"] svg:not(.pd-bag-icon),
    .ct-cart-item svg:not(.pd-bag-icon) {
      opacity: 0 !important;
      transition: none !important;
    }

    header [data-id="cart"] svg.pd-bag-icon,
    .ct-header-cart svg.pd-bag-icon,
    header a[href*="cart"] svg.pd-bag-icon,
    .ct-cart-item svg.pd-bag-icon {
      opacity: 1 !important;
    }
    </style>
    <script id="prime-drop-head-bag-guard-js">
    (function() {
      var bagSvg = '<svg class="ct-icon pd-bag-icon" aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.45" stroke-linecap="round" stroke-linejoin="round"><path d="M7 9V7a5 5 0 0 1 10 0v2"/><path d="M5.4 8.5h13.2l.9 11.2a2 2 0 0 1-2 2.1H6.5a2 2 0 0 1-2-2.1l.9-11.2Z"/></svg>';

      function replaceBagIconEarly() {
        document.querySelectorAll('header [data-id="cart"] svg, .ct-header-cart svg, header a[href*="cart"] svg, .ct-cart-item svg').forEach(function(svg) {
          if (svg.classList.contains('pd-bag-icon')) return;
          var holder = document.createElement('span');
          holder.innerHTML = bagSvg;
          svg.replaceWith(holder.firstChild);
        });
      }

      replaceBagIconEarly();
      document.addEventListener('DOMContentLoaded', replaceBagIconEarly);
      window.addEventListener('pageshow', replaceBagIconEarly);
      [25, 75, 150, 300, 600, 1200].forEach(function(delay) {
        setTimeout(replaceBagIconEarly, delay);
      });

      if (window.MutationObserver) {
        var header = document.querySelector('header');
        if (header) {
          new MutationObserver(replaceBagIconEarly).observe(header, { childList: true, subtree: true });
        }
      }
    })();
    </script>
    <?php
}, 1);

add_action('woocommerce_thankyou', function($order_id) {
    if (!$order_id) {
        return;
    }

    $order = wc_get_order($order_id);
    if (!$order) {
        return;
    }

    $paid = $order->is_paid();
    ?>
    <div class="pd-thankyou-finish">
      <h2><?php echo esc_html($paid ? 'Pago realizado' : 'Pedido recibido'); ?></h2>
      <p><?php echo esc_html($paid ? 'Te enviamos el comprobante y los detalles de tu pedido al correo registrado.' : 'Cuando el pago sea confirmado, recibirás el comprobante en tu correo.'); ?></p>
      <a href="<?php echo esc_url(home_url('/bolsos/')); ?>">Finalizar</a>
    </div>
    <?php
}, 25);

add_action('wp_footer', function() {
    ?>
    <style id="prime-drop-checkout-wishlist-cart-nav">
    /* Checkout: campos, selectores y selects */
    body.woocommerce-checkout .pd-country-hidden {
      display: none !important;
    }

    body.woocommerce-checkout .select2-search,
    body.woocommerce-checkout .select2-search--dropdown {
      display: none !important;
    }

    body.woocommerce-checkout .select2-container,
    body.woocommerce-checkout .select2-selection,
    body.woocommerce-checkout select,
    body.woocommerce-checkout input,
    body.woocommerce-checkout textarea {
      border-radius: 25px !important;
      box-sizing: border-box !important;
    }

    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method {
      overflow: visible !important;
    }

    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method > label {
      padding-left: 62px !important;
    }

    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method > label::before {
      left: 24px !important;
      width: 18px !important;
      height: 18px !important;
      border-color: #cfcfcf !important;
      background: #ffffff !important;
    }

    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method > input.input-radio:checked + label::before,
    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method > input[name="payment_method"]:checked + label::before {
      border-color: #000000 !important;
      background: radial-gradient(circle at center, #ffffff 0 2.4px, #000000 2.8px 100%) !important;
    }

    body.woocommerce-checkout input[type="checkbox"].input-checkbox:checked,
    body.woocommerce-checkout input[type="checkbox"].woocommerce-form__input-checkbox:checked {
      background-color: #000000 !important;
      background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 6 9 17l-5-5'/%3E%3C/svg%3E") !important;
      background-repeat: no-repeat !important;
      background-position: center !important;
      background-size: 12px 12px !important;
      border-color: #000000 !important;
    }

    body.woocommerce-checkout .woocommerce-form-login-toggle .woocommerce-info {
      align-items: center !important;
      border: 1px solid #eeeeee !important;
      border-radius: 14px !important;
      background: #fafafa !important;
      padding: 18px 22px !important;
      gap: 12px !important;
    }

    body.woocommerce-checkout .woocommerce-privacy-policy-text {
      margin-top: 22px !important;
      color: #111111 !important;
      -webkit-text-fill-color: #111111 !important;
      font-size: 14px !important;
      line-height: 1.55 !important;
    }

    body.woocommerce-checkout .woocommerce-privacy-policy-text a {
      color: #000000 !important;
      font-weight: 800 !important;
      text-decoration: underline !important;
      text-underline-offset: 3px !important;
    }

    body.woocommerce-checkout label[for="createaccount"],
    body.woocommerce-checkout label[for="ship-to-different-address-checkbox"] {
      line-height: 1.4 !important;
      color: #111111 !important;
      -webkit-text-fill-color: #111111 !important;
    }

    @media (max-width: 1024px) {
      body.woocommerce-checkout .select2-container {
        display: none !important;
      }

      body.woocommerce-checkout select.select2-hidden-accessible {
        position: static !important;
        width: 100% !important;
        height: auto !important;
        opacity: 1 !important;
        clip: auto !important;
        clip-path: none !important;
        pointer-events: auto !important;
        display: block !important;
      }
    }

    /* Wishlist limpio */
    body.pd-wishlist-page .entry-header,
    body.pd-wishlist-page .page-title,
    body.pd-wishlist-page h1.entry-title,
    body.pd-wishlist-page .ct-breadcrumbs {
      display: none !important;
    }

    body.pd-wishlist-page .site-main,
    body.pd-wishlist-page main {
      padding-top: 48px !important;
    }

    .pd-wishlist-empty-clean {
      max-width: 880px !important;
      margin: 30px auto 90px !important;
      padding: 56px 28px !important;
      border: 1px solid #eeeeee !important;
      border-radius: 18px !important;
      background: #ffffff !important;
      box-shadow: 0 18px 55px rgba(0,0,0,0.06) !important;
      text-align: center !important;
      display: flex !important;
      flex-direction: column !important;
      align-items: center !important;
      gap: 18px !important;
    }

    .pd-wishlist-empty-clean .pd-wishlist-icon {
      width: 56px !important;
      height: 56px !important;
      border: 1px solid #e5e5e5 !important;
      border-radius: 50% !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      font-size: 24px !important;
      line-height: 1 !important;
    }

    .pd-wishlist-empty-clean h2 {
      margin: 0 !important;
      font-family: 'Roboto Serif', Georgia, serif !important;
      font-size: clamp(28px, 4vw, 44px) !important;
      line-height: 1.1 !important;
      color: #000000 !important;
    }

    .pd-wishlist-empty-clean p {
      max-width: 520px !important;
      margin: 0 !important;
      font-size: 16px !important;
      line-height: 1.6 !important;
      color: #333333 !important;
    }

    .pd-wishlist-empty-clean a {
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      min-width: 150px !important;
      min-height: 44px !important;
      padding: 12px 28px !important;
      border-radius: 25px !important;
      background: #000000 !important;
      color: #ffffff !important;
      text-decoration: none !important;
      font-size: 12px !important;
      font-weight: 800 !important;
      letter-spacing: 1.5px !important;
      text-transform: uppercase !important;
    }

    /* Pagina carrito */
    body.woocommerce-cart .entry-header,
    body.woocommerce-cart .page-title,
    body.woocommerce-cart h1.entry-title {
      text-align: center !important;
    }

    body.woocommerce-cart .woocommerce {
      max-width: 1180px !important;
      margin: 0 auto !important;
      padding: 36px 24px 80px !important;
      box-sizing: border-box !important;
    }

    body.woocommerce-cart table.shop_table {
      border: 1px solid #eeeeee !important;
      border-radius: 16px !important;
      overflow: hidden !important;
      background: #ffffff !important;
      box-shadow: 0 16px 45px rgba(0,0,0,0.05) !important;
    }

    body.woocommerce-cart table.shop_table th,
    body.woocommerce-cart table.shop_table td {
      padding: 18px !important;
      border-color: #eeeeee !important;
      vertical-align: middle !important;
    }

    body.woocommerce-cart table.shop_table img {
      width: 92px !important;
      height: 92px !important;
      object-fit: contain !important;
      background: #ffffff !important;
      border-radius: 12px !important;
    }

    body.woocommerce-cart .cart_totals {
      border: 1px solid #eeeeee !important;
      border-radius: 16px !important;
      padding: 24px !important;
      background: #ffffff !important;
      box-shadow: 0 16px 45px rgba(0,0,0,0.05) !important;
    }

    body.woocommerce-cart .cart_totals h2 {
      margin-top: 0 !important;
      font-size: 24px !important;
    }

    body.woocommerce-cart .wc-proceed-to-checkout a.checkout-button,
    body.woocommerce-cart .return-to-shop a.button,
    body.woocommerce-cart button.button,
    body.woocommerce-cart a.button {
      border-radius: 25px !important;
      background: #000000 !important;
      color: #ffffff !important;
      border: none !important;
      text-transform: uppercase !important;
      letter-spacing: 1.4px !important;
    }

    body.woocommerce-cart .cart-empty {
      max-width: 720px !important;
      margin: 40px auto 18px !important;
      padding: 44px 24px !important;
      border: 1px solid #eeeeee !important;
      border-radius: 18px !important;
      text-align: center !important;
      box-shadow: 0 16px 45px rgba(0,0,0,0.05) !important;
      background: #ffffff !important;
    }

    .pd-thankyou-finish {
      max-width: 760px !important;
      margin: 32px auto !important;
      padding: 34px 28px !important;
      border: 1px solid #eeeeee !important;
      border-radius: 18px !important;
      text-align: center !important;
      background: #ffffff !important;
      box-shadow: 0 16px 45px rgba(0,0,0,0.05) !important;
    }

    .pd-thankyou-finish h2 {
      margin: 0 0 10px !important;
      font-size: 34px !important;
    }

    .pd-thankyou-finish a {
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      margin-top: 18px !important;
      padding: 13px 34px !important;
      border-radius: 25px !important;
      background: #000000 !important;
      color: #ffffff !important;
      text-decoration: none !important;
      text-transform: uppercase !important;
      letter-spacing: 1.5px !important;
      font-size: 12px !important;
      font-weight: 800 !important;
    }
    </style>

    <script id="prime-drop-checkout-wishlist-cart-nav-js">
    (function() {
      var bagSvg = '<svg class="ct-icon pd-bag-icon" aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.45" stroke-linecap="round" stroke-linejoin="round"><path d="M7 9V7a5 5 0 0 1 10 0v2"/><path d="M5.4 8.5h13.2l.9 11.2a2 2 0 0 1-2 2.1H6.5a2 2 0 0 1-2-2.1l.9-11.2Z"/></svg>';

      function replaceBagIcon() {
        document.querySelectorAll('header [data-id="cart"] svg, .ct-header-cart svg, header a[href*="cart"] svg, .ct-cart-item svg').forEach(function(svg) {
          if (svg.classList.contains('pd-bag-icon')) return;
          var holder = document.createElement('span');
          holder.innerHTML = bagSvg;
          svg.replaceWith(holder.firstChild);
        });
      }

      function fixBolsosClick() {
        document.querySelectorAll('header a, .ct-header a, .site-header a').forEach(function(a) {
          if ((a.textContent || '').trim().toUpperCase() !== 'BOLSOS') return;
          if (a.dataset.pdBolsosFixed === '1') return;
          a.dataset.pdBolsosFixed = '1';
          a.setAttribute('href', '/bolsos/');
          a.addEventListener('click', function(event) {
            event.preventDefault();
            event.stopImmediatePropagation();
            window.location.href = '/bolsos/';
          }, true);
        });
      }

      function fixCheckoutLabels() {
        function setLabel(label, input, text) {
          if (!label) return;
          var inputInside = input && label.contains(input) ? input : null;
          label.textContent = '';
          if (inputInside) {
            label.appendChild(inputInside);
            label.appendChild(document.createTextNode(' '));
          }
          label.appendChild(document.createTextNode(text + ' '));
          var optional = document.createElement('span');
          optional.className = 'pd-optional';
          optional.textContent = '(opcional)';
          label.appendChild(optional);
        }

        var accountInput = document.querySelector('#createaccount, input[name="createaccount"]');
        var account = document.querySelector('label[for="createaccount"]') || accountInput?.closest('label') || accountInput?.parentElement?.querySelector('label');
        setLabel(account, accountInput, 'Crear cuenta para guardar tus pedidos');

        var shipInput = document.querySelector('#ship-to-different-address-checkbox, input[name="ship_to_different_address"]');
        var ship = document.querySelector('label[for="ship-to-different-address-checkbox"]') || shipInput?.closest('label') || shipInput?.parentElement?.querySelector('label');
        setLabel(ship, shipInput, 'Enviar a otra direccion');

        [['billing_state_field', 'billing_city_field'], ['shipping_state_field', 'shipping_city_field']].forEach(function(pair) {
          var state = document.getElementById(pair[0]);
          var city = document.getElementById(pair[1]);
          if (state && city && state.compareDocumentPosition(city) & Node.DOCUMENT_POSITION_PRECEDING) {
            city.parentNode.insertBefore(state, city);
          }
        });

        if (window.innerWidth <= 1024 && window.jQuery) {
          jQuery('#billing_state, #shipping_state, #billing_country, #shipping_country').each(function() {
            var $el = jQuery(this);
            try {
              if ($el.data('select2')) $el.select2('destroy');
              if ($el.data('selectWoo')) $el.selectWoo('destroy');
            } catch (e) {}
            $el.removeClass('select2-hidden-accessible').show();
            $el.next('.select2-container').remove();
          });
        }
      }
      function runAll() {
        replaceBagIcon();
        fixBolsosClick();
        fixCheckoutLabels();
      }

      document.addEventListener('DOMContentLoaded', runAll);
      window.addEventListener('pageshow', runAll);
      window.addEventListener('load', runAll);
      [100, 300, 700, 1400, 2600].forEach(function(delay) {
        setTimeout(runAll, delay);
      });

      if (document.body && window.MutationObserver) {
        var header = document.querySelector('header');
        if (header) {
          new MutationObserver(function() {
            replaceBagIcon();
            fixBolsosClick();
          }).observe(header, { childList: true, subtree: true });
        }
      }
    })();
    </script>
    <?php
}, 10006);
/* PRIME_DROP_CHECKOUT_WISHLIST_CART_NAV_END */

/* PRIME_DROP_FINAL_CHECKOUT_WISHLIST_SELECT_FIX_START */
add_action('wp_footer', function() {
    ?>
    <style id="prime-drop-final-checkout-wishlist-select-fix">
    /* Checkout: no permitir que el drawer/parpadeo aparezca dentro del checkout */
    body.woocommerce-checkout #cart-drawer,
    body.woocommerce-checkout .cart-drawer,
    body.woocommerce-checkout .pd-cart-drawer,
    body.woocommerce-checkout [id*="cart-drawer"],
    body.woocommerce-checkout [class*="cart-drawer"],
    body.woocommerce-checkout #cart-drawer-overlay,
    body.woocommerce-checkout .cart-drawer-overlay,
    body.woocommerce-checkout .pd-cart-overlay,
    body.woocommerce-checkout .pd-cart-drawer-overlay {
      display: none !important;
      visibility: hidden !important;
      opacity: 0 !important;
      pointer-events: none !important;
    }

    /* Checkout: "Ya eres cliente" limpio, sin icono peleando con texto */
    body.woocommerce-checkout .woocommerce-form-login-toggle .woocommerce-info {
      display: flex !important;
      align-items: center !important;
      justify-content: space-between !important;
      gap: 18px !important;
      min-height: 48px !important;
      padding: 14px 22px !important;
      border: 1px solid #eeeeee !important;
      border-radius: 14px !important;
      background: #fafafa !important;
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      line-height: 1.35 !important;
      overflow: hidden !important;
    }

    body.woocommerce-checkout .woocommerce-form-login-toggle .woocommerce-info::before,
    body.woocommerce-checkout .woocommerce-form-login-toggle .woocommerce-info svg,
    body.woocommerce-checkout .woocommerce-form-login-toggle .woocommerce-info .ct-icon,
    body.woocommerce-checkout .woocommerce-form-login-toggle .woocommerce-info i,
    body.woocommerce-checkout .woocommerce-form-login-toggle .woocommerce-info [class*="icon"] {
      display: none !important;
      content: none !important;
      width: 0 !important;
      height: 0 !important;
      margin: 0 !important;
      padding: 0 !important;
      opacity: 0 !important;
    }

    body.woocommerce-checkout .woocommerce-form-login-toggle .woocommerce-info a {
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      text-decoration: underline !important;
      text-underline-offset: 3px !important;
      white-space: nowrap !important;
    }

    @media (max-width: 600px) {
      body.woocommerce-checkout .woocommerce-form-login-toggle .woocommerce-info {
        align-items: flex-start !important;
        flex-direction: column !important;
        gap: 8px !important;
      }
    }

    /* Checkout: select/dropdown sin hover transparente */
    body.woocommerce-checkout select,
    body.woocommerce-checkout select option,
    body.woocommerce-checkout .select2-container,
    body.woocommerce-checkout .select2-selection,
    body.woocommerce-checkout .select2-dropdown,
    body.woocommerce-checkout .select2-results__option {
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      background: #ffffff !important;
    }

    body.woocommerce-checkout select:focus,
    body.woocommerce-checkout select:hover,
    body.woocommerce-checkout select option:hover,
    body.woocommerce-checkout select option:focus,
    body.woocommerce-checkout select option:checked,
    body.woocommerce-checkout .select2-results__option--highlighted,
    body.woocommerce-checkout .select2-results__option--highlighted[aria-selected],
    body.woocommerce-checkout .select2-results__option--highlighted[data-selected],
    body.woocommerce-checkout .select2-results__option[aria-selected="true"],
    body.woocommerce-checkout .select2-results__option[data-selected="true"] {
      color: #ffffff !important;
      -webkit-text-fill-color: #ffffff !important;
      background: #000000 !important;
    }

    body.woocommerce-checkout .select2-dropdown {
      border: 1px solid #000000 !important;
      border-radius: 12px !important;
      overflow: hidden !important;
      box-shadow: 0 12px 28px rgba(0,0,0,0.12) !important;
    }

    body.woocommerce-checkout .select2-results__option {
      padding: 11px 16px !important;
      font-size: 14px !important;
      line-height: 1.35 !important;
    }

    /* Wishlist: no reemplazar contenido real, solo maquillar estados del plugin */
    body.woocommerce-wishlist .pd-wishlist-empty-clean {
      display: none !important;
    }

    body.woocommerce-wishlist .entry-header,
    body.woocommerce-wishlist .entry-title,
    body.woocommerce-wishlist h1.entry-title {
      display: none !important;
    }

    body.woocommerce-wishlist .entry-content {
      padding-top: 54px !important;
    }

    body.woocommerce-wishlist .wishlist-title h2,
    body.woocommerce-wishlist .yith-wcwl-form h2 {
      font-size: clamp(34px, 4vw, 52px) !important;
      line-height: 1.08 !important;
      text-align: center !important;
      margin-bottom: 34px !important;
    }

    body.woocommerce-wishlist .wishlist_table,
    body.woocommerce-wishlist .yith-wcwl-form,
    body.woocommerce-wishlist .entry-content,
    body.woocommerce-wishlist .woocommerce {
      visibility: visible !important;
      opacity: 1 !important;
    }

    body.woocommerce-wishlist .wishlist_table {
      max-width: 980px !important;
      margin-left: auto !important;
      margin-right: auto !important;
      border-radius: 18px !important;
      box-shadow: 0 18px 60px rgba(0,0,0,0.06) !important;
    }

    body.woocommerce-wishlist .wishlist-empty {
      padding-top: 64px !important;
      padding-bottom: 64px !important;
    }

    body.woocommerce-wishlist .wishlist-empty::after {
      display: none !important;
      content: none !important;
    }

    body.woocommerce-wishlist .pd-wishlist-empty-title {
      display: block !important;
      margin: 18px auto 10px !important;
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      font-family: 'Roboto Serif', Georgia, serif !important;
      font-size: clamp(24px, 3vw, 34px) !important;
      line-height: 1.15 !important;
      font-weight: 800 !important;
      text-align: center !important;
    }
    </style>
    <script id="prime-drop-final-checkout-wishlist-select-fix-js">
    (function() {
      function decodeProductTitles() {
        document.querySelectorAll('.woocommerce-loop-product__title, h1.product_title, .product-title, .product-name a').forEach(function(el) {
          if (!el || !el.textContent) return;
          el.textContent = el.textContent
            .replace(/&amp;#8211;|&#8211;|&amp;ndash;|&ndash;/g, '–')
            .replace(/\s+–\s+/g, ' – ');
        });
      }

      function stabilizeCheckout() {
        if (!document.body.classList.contains('woocommerce-checkout')) return;
        document.querySelectorAll('#cart-drawer, .cart-drawer, .pd-cart-drawer, [id*="cart-drawer"], [class*="cart-drawer"], #cart-drawer-overlay, .cart-drawer-overlay, .pd-cart-overlay, .pd-cart-drawer-overlay').forEach(function(el) {
          el.classList.remove('active', 'open', 'show', 'is-open', 'ct-open');
          el.setAttribute('aria-hidden', 'true');
        });
        document.documentElement.style.overflow = '';
        document.body.style.overflow = '';
        document.body.style.position = '';
        document.body.style.top = '';
        document.body.style.left = '';
        document.body.style.right = '';
        document.body.style.width = '';
      }

      function recoverWishlist() {
        if (!/\/wishlist\/?/.test(window.location.pathname)) return;
        document.body.classList.remove('pd-wishlist-empty');
        document.querySelectorAll('.pd-wishlist-empty-clean').forEach(function(el) {
          el.remove();
        });

        var emptyCell = document.querySelector('.wishlist-empty');
        if (!emptyCell) return;

        var hasProductRows = Array.from(document.querySelectorAll('.wishlist_table tbody tr')).some(function(row) {
          return !row.querySelector('.wishlist-empty') && (row.querySelector('.product-name a') || row.querySelector('.product-thumbnail img'));
        });

        if (hasProductRows) return;

        if (!emptyCell.querySelector('.pd-wishlist-empty-title')) {
          var title = document.createElement('h2');
          title.className = 'pd-wishlist-empty-title';
          title.textContent = 'Tu lista de deseos esta vacia';
          var copy = emptyCell.querySelector('.pd-wishlist-empty-copy');
          emptyCell.insertBefore(title, copy || emptyCell.firstChild);
        }
      }

      function run() {
        decodeProductTitles();
        stabilizeCheckout();
        recoverWishlist();
      }

      document.addEventListener('DOMContentLoaded', run);
      window.addEventListener('pageshow', run);
      window.addEventListener('load', run);
      document.body && document.body.addEventListener('updated_checkout', run);
      [100, 500, 1200, 2400].forEach(function(delay) {
        setTimeout(run, delay);
      });
    })();
    </script>
    <?php
}, 10009);
/* PRIME_DROP_FINAL_CHECKOUT_WISHLIST_SELECT_FIX_END */

/* PRIME_DROP_FINAL_PRODUCT_CHECKOUT_BUTTON_FIX_START */
add_action('wp_footer', function() {
    ?>
    <style id="prime-drop-final-product-checkout-button-fix">
    /* Producto: quitar enlace Ver carrito despues de anadir */
    .single-product a.added_to_cart,
    .single-product a.added_to_cart.wc-forward,
    .woocommerce a.added_to_cart,
    .woocommerce a.added_to_cart.wc-forward {
      display: none !important;
      visibility: hidden !important;
      opacity: 0 !important;
      width: 0 !important;
      height: 0 !important;
      margin: 0 !important;
      padding: 0 !important;
      overflow: hidden !important;
    }

    /* Producto: cantidad + boton alineados sin desbordarse */
    .single-product form.cart,
    .single-product .summary form.cart {
      display: flex !important;
      align-items: center !important;
      gap: 12px !important;
      flex-wrap: nowrap !important;
      width: 100% !important;
      max-width: 100% !important;
      box-sizing: border-box !important;
      overflow: visible !important;
    }

    .single-product form.cart .quantity {
      flex: 0 0 112px !important;
      width: 112px !important;
      min-width: 112px !important;
      margin: 0 !important;
    }

    .single-product form.cart .single_add_to_cart_button,
    .single-product form.cart button.single_add_to_cart_button {
      flex: 0 1 auto !important;
      width: auto !important;
      min-width: 205px !important;
      max-width: calc(100% - 124px) !important;
      margin: 0 !important;
      padding: 14px 28px !important;
      border-radius: 25px !important;
      box-sizing: border-box !important;
      white-space: nowrap !important;
      overflow: visible !important;
      text-overflow: clip !important;
      line-height: 1.2 !important;
      text-align: center !important;
    }

    @media (max-width: 520px) {
      .single-product form.cart,
      .single-product .summary form.cart {
        gap: 8px !important;
      }

      .single-product form.cart .quantity {
        flex-basis: 104px !important;
        width: 104px !important;
        min-width: 104px !important;
      }

      .single-product form.cart .single_add_to_cart_button,
      .single-product form.cart button.single_add_to_cart_button {
        flex: 1 1 auto !important;
        min-width: 0 !important;
        max-width: none !important;
        padding: 13px 16px !important;
        font-size: 11px !important;
        letter-spacing: 1.1px !important;
      }
    }

    /* Checkout: titulo centrado contra la pantalla */
    body.woocommerce-checkout .entry-header,
    body.woocommerce-checkout header.entry-header,
    body.woocommerce-checkout .page-title-wrapper {
      width: 100% !important;
      max-width: none !important;
      margin: 0 !important;
      padding: 34px 0 20px !important;
      box-sizing: border-box !important;
      text-align: center !important;
      display: block !important;
    }

    body.woocommerce-checkout .entry-title,
    body.woocommerce-checkout .page-title,
    body.woocommerce-checkout h1 {
      position: relative !important;
      left: 50vw !important;
      transform: translateX(-50%) !important;
      width: 100vw !important;
      max-width: 100vw !important;
      margin: 0 !important;
      padding: 0 18px !important;
      box-sizing: border-box !important;
      text-align: center !important;
      display: block !important;
    }
    </style>
    <?php
}, 10020);
/* PRIME_DROP_FINAL_PRODUCT_CHECKOUT_BUTTON_FIX_END */

/* PRIME_DROP_MOBILE_BOLSOS_AND_BAG_TITLE_START */
add_action('wp_footer', function() {
    ?>
    <style id="prime-drop-mobile-bolsos-and-bag-title-css">
    @media (max-width: 1024px) {
      .pd-bolsos-menu-parent.pd-submenu-open > .pd-bolsos-submenu {
        opacity: 1 !important;
        visibility: visible !important;
        pointer-events: auto !important;
      }

      .pd-bolsos-submenu a[data-pd-all-bags="1"] {
        font-weight: 900 !important;
      }
    }
    </style>

    <script id="prime-drop-mobile-bolsos-and-bag-title-js">
    (function() {
      function isTouchMenuMode() {
        return window.matchMedia('(max-width: 1024px)').matches || window.matchMedia('(hover: none)').matches;
      }

      function getDirectBolsosLink(li) {
        if (!li) return null;
        return Array.prototype.slice.call(li.children).find(function(child) {
          return child.tagName === 'A' && /^BOLSOS$/i.test((child.textContent || '').trim());
        });
      }

      function ensureAllBagsItem(li) {
        var submenu = li && li.querySelector(':scope > .pd-bolsos-submenu');
        if (!submenu || submenu.querySelector('a[data-pd-all-bags="1"]')) return;
        var item = document.createElement('li');
        item.innerHTML = '<a data-pd-all-bags="1" href="/bolsos/">TODOS LOS BOLSOS</a>';
        submenu.insertBefore(item, submenu.firstChild);
      }

      function fixMobileBolsosMenu() {
        var selectors = [
          'nav[data-id="mobile-menu"] li.pd-bolsos-menu-parent',
          '#offcanvas li.pd-bolsos-menu-parent',
          '.ct-panel li.pd-bolsos-menu-parent',
          '.ct-drawer-canvas li.pd-bolsos-menu-parent',
          'header li.pd-bolsos-menu-parent'
        ].join(',');

        document.querySelectorAll(selectors).forEach(function(li) {
          var link = getDirectBolsosLink(li);
          if (!link) return;

          ensureAllBagsItem(li);

          if (link.dataset.pdTouchBolsosReady === '1') return;

          var cleanLink = link.cloneNode(true);
          cleanLink.dataset.pdBolsosFixed = '1';
          cleanLink.dataset.pdTouchBolsosReady = '1';
          cleanLink.setAttribute('href', '/bolsos/');
          link.replaceWith(cleanLink);

          cleanLink.addEventListener('click', function(event) {
            if (!isTouchMenuMode()) return;
            event.preventDefault();
            event.stopPropagation();
            event.stopImmediatePropagation();
            var open = li.classList.toggle('pd-submenu-open');
            cleanLink.setAttribute('aria-expanded', open ? 'true' : 'false');

            var toggle = li.querySelector(':scope > .pd-submenu-toggle');
            if (toggle) toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
          }, true);
        });
      }

      function renameCartDrawerTitle() {
        var selectors = [
          '.pd-cart-drawer-header h3',
          '.cart-drawer-header h3',
          '#cart-drawer h3',
          '.pd-cart-drawer h3',
          '.cart-drawer h3'
        ].join(',');

        document.querySelectorAll(selectors).forEach(function(title) {
          var text = (title.textContent || '').trim();
          if (/carrito\s+de\s+compra/i.test(text) || /carrito\s+de\s+compras/i.test(text)) {
            title.textContent = 'Bolsa de compra';
          }
        });
      }

      function runPrimeDropMobileBagFixes() {
        fixMobileBolsosMenu();
        renameCartDrawerTitle();
      }

      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', runPrimeDropMobileBagFixes);
      } else {
        runPrimeDropMobileBagFixes();
      }

      window.addEventListener('load', runPrimeDropMobileBagFixes);
      window.addEventListener('resize', runPrimeDropMobileBagFixes);
      document.addEventListener('click', function() {
        setTimeout(runPrimeDropMobileBagFixes, 80);
      }, true);

      var attempts = 0;
      var timer = setInterval(function() {
        runPrimeDropMobileBagFixes();
        attempts += 1;
        if (attempts >= 20) clearInterval(timer);
      }, 250);

      new MutationObserver(runPrimeDropMobileBagFixes).observe(document.documentElement, {
        childList: true,
        subtree: true
      });
    })();
    </script>
    <?php
}, 10040);
/* PRIME_DROP_MOBILE_BOLSOS_AND_BAG_TITLE_END */

/* PRIME_DROP_BOLSOS_IMAGES_COMPLETE_START */
add_action('wp_footer', function() {
    ?>
    <style id="prime-drop-bolsos-images-complete-css">
    /* /bolsos/: mostrar bolsos completos, sin recorte */
    body.page-id-547 .woocommerce ul.products li.product {
      overflow: visible !important;
      text-align: center !important;
    }

    body.page-id-547 .woocommerce ul.products li.product a.woocommerce-loop-product__link {
      display: flex !important;
      flex-direction: column !important;
      align-items: center !important;
      width: 100% !important;
      background: #ffffff !important;
      text-decoration: none !important;
    }

    body.page-id-547 .woocommerce ul.products li.product a img,
    body.page-id-547 .woocommerce ul.products li.product img,
    body.page-id-547 .woocommerce-page ul.products li.product a img,
    body.page-id-547 .woocommerce-page ul.products li.product img {
      width: 100% !important;
      height: 320px !important;
      min-height: 320px !important;
      max-height: 320px !important;
      aspect-ratio: auto !important;
      object-fit: contain !important;
      object-position: center center !important;
      background: #ffffff !important;
      border-radius: 8px !important;
      padding: 16px !important;
      box-sizing: border-box !important;
      display: block !important;
      transform: none !important;
      filter: none !important;
    }

    body.page-id-547 .woocommerce ul.products li.product figure {
      background: #ffffff !important;
      border-radius: 8px !important;
      overflow: visible !important;
    }

    @media (min-width: 768px) and (max-width: 1024px) {
      body.page-id-547 .woocommerce ul.products li.product a img,
      body.page-id-547 .woocommerce ul.products li.product img,
      body.page-id-547 .woocommerce-page ul.products li.product a img,
      body.page-id-547 .woocommerce-page ul.products li.product img {
        height: 285px !important;
        min-height: 285px !important;
        max-height: 285px !important;
        padding: 14px !important;
      }
    }

    @media (max-width: 767px) {
      body.page-id-547 .woocommerce ul.products li.product a img,
      body.page-id-547 .woocommerce ul.products li.product img,
      body.page-id-547 .woocommerce-page ul.products li.product a img,
      body.page-id-547 .woocommerce-page ul.products li.product img {
        height: 235px !important;
        min-height: 235px !important;
        max-height: 235px !important;
        padding: 12px !important;
      }
    }
    </style>
    <?php
}, 10060);
/* PRIME_DROP_BOLSOS_IMAGES_COMPLETE_END */

/* PRIME_DROP_BOLSOS_OLD_CARD_STYLE_START */
add_action('wp_footer', function() {
    ?>
    <style id="prime-drop-bolsos-old-card-style-css">
    /* /bolsos/: tarjetas estilo pagina anterior */
    body.page-id-547 .woocommerce ul.products {
      align-items: stretch !important;
      gap: 28px 22px !important;
    }

    body.page-id-547 .woocommerce ul.products li.product {
      display: flex !important;
      flex-direction: column !important;
      align-items: stretch !important;
      justify-content: flex-start !important;
      background: #ffffff !important;
      border: 1px solid #d8d8d8 !important;
      border-radius: 0 !important;
      padding: 0 6px 8px !important;
      overflow: hidden !important;
      text-align: left !important;
      box-sizing: border-box !important;
      box-shadow: none !important;
    }

    body.page-id-547 .woocommerce ul.products li.product a.woocommerce-loop-product__link {
      display: flex !important;
      flex-direction: column !important;
      align-items: stretch !important;
      justify-content: flex-start !important;
      width: 100% !important;
      background: #ffffff !important;
      text-align: left !important;
      color: #000000 !important;
      text-decoration: none !important;
    }

    body.page-id-547 .woocommerce ul.products li.product a img,
    body.page-id-547 .woocommerce ul.products li.product img,
    body.page-id-547 .woocommerce-page ul.products li.product a img,
    body.page-id-547 .woocommerce-page ul.products li.product img {
      width: calc(100% + 12px) !important;
      margin: 0 0 12px -6px !important;
      height: 300px !important;
      min-height: 300px !important;
      max-height: 300px !important;
      object-fit: contain !important;
      object-position: center center !important;
      background: #f4f4f4 !important;
      border-radius: 0 !important;
      padding: 14px !important;
      box-sizing: border-box !important;
      display: block !important;
      flex-shrink: 0 !important;
    }

    body.page-id-547 .woocommerce ul.products li.product figure {
      margin: 0 !important;
      background: #f4f4f4 !important;
      border-radius: 0 !important;
      overflow: hidden !important;
    }

    body.page-id-547 .woocommerce ul.products li.product .woocommerce-loop-product__title {
      min-height: 0 !important;
      height: auto !important;
      margin: 0 0 6px !important;
      padding: 0 !important;
      overflow: visible !important;
      display: block !important;
      -webkit-line-clamp: unset !important;
      -webkit-box-orient: initial !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      font-size: 18px !important;
      font-weight: 800 !important;
      line-height: 1.12 !important;
      letter-spacing: 0 !important;
      text-transform: none !important;
      text-align: left !important;
      color: #000000 !important;
    }

    body.page-id-547 .woocommerce ul.products li.product .price {
      display: block !important;
      height: auto !important;
      min-height: 0 !important;
      margin: 0 0 10px !important;
      padding: 0 !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      font-size: 12px !important;
      font-weight: 400 !important;
      line-height: 1.3 !important;
      text-align: left !important;
      color: #000000 !important;
    }

    body.page-id-547 .woocommerce ul.products li.product .button,
    body.page-id-547 .woocommerce ul.products li.product:hover .button {
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      width: 100% !important;
      min-width: 0 !important;
      max-width: none !important;
      min-height: 36px !important;
      margin: auto 0 0 !important;
      padding: 9px 14px !important;
      background: #ffffff !important;
      color: #000000 !important;
      border: 1.5px solid #000000 !important;
      border-radius: 999px !important;
      box-shadow: none !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      font-size: 12px !important;
      font-weight: 500 !important;
      letter-spacing: 0 !important;
      line-height: 1.15 !important;
      text-align: center !important;
      text-transform: none !important;
      white-space: normal !important;
      opacity: 1 !important;
      transform: none !important;
      pointer-events: auto !important;
    }

    body.page-id-547 .woocommerce ul.products li.product .button:hover {
      background: #000000 !important;
      color: #ffffff !important;
    }

    @media (min-width: 1000px) {
      body.page-id-547 .woocommerce ul.products li.product a img,
      body.page-id-547 .woocommerce ul.products li.product img,
      body.page-id-547 .woocommerce-page ul.products li.product a img,
      body.page-id-547 .woocommerce-page ul.products li.product img {
        height: 330px !important;
        min-height: 330px !important;
        max-height: 330px !important;
      }
    }

    @media (min-width: 768px) and (max-width: 999px) {
      body.page-id-547 .woocommerce ul.products {
        gap: 24px 18px !important;
      }

      body.page-id-547 .woocommerce ul.products li.product a img,
      body.page-id-547 .woocommerce ul.products li.product img,
      body.page-id-547 .woocommerce-page ul.products li.product a img,
      body.page-id-547 .woocommerce-page ul.products li.product img {
        height: 285px !important;
        min-height: 285px !important;
        max-height: 285px !important;
      }
    }

    @media (max-width: 767px) {
      body.page-id-547 .woocommerce ul.products {
        grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
        gap: 18px 12px !important;
        padding-left: 10px !important;
        padding-right: 10px !important;
      }

      body.page-id-547 .woocommerce ul.products li.product {
        padding: 0 5px 7px !important;
      }

      body.page-id-547 .woocommerce ul.products li.product a img,
      body.page-id-547 .woocommerce ul.products li.product img,
      body.page-id-547 .woocommerce-page ul.products li.product a img,
      body.page-id-547 .woocommerce-page ul.products li.product img {
        width: calc(100% + 10px) !important;
        margin-left: -5px !important;
        height: 235px !important;
        min-height: 235px !important;
        max-height: 235px !important;
        padding: 10px !important;
      }

      body.page-id-547 .woocommerce ul.products li.product .woocommerce-loop-product__title {
        font-size: 15px !important;
        line-height: 1.12 !important;
      }

      body.page-id-547 .woocommerce ul.products li.product .button,
      body.page-id-547 .woocommerce ul.products li.product:hover .button {
        min-height: 35px !important;
        font-size: 11px !important;
        padding: 8px 10px !important;
      }
    }
    </style>
    <?php
}, 10080);
/* PRIME_DROP_BOLSOS_OLD_CARD_STYLE_END */

/* PRIME_DROP_MATCH_BUILDER_PRODUCTS_START */
add_action('wp_footer', function() {
    ?>
    <style id="prime-drop-match-builder-products-css">
    /* Solo cards: /bolsos, hombre, mujer y destacadas */
    body.page-id-547 .woocommerce ul.products li.product,
    body.tax-product_cat .woocommerce ul.products li.product,
    body.post-type-archive-product .woocommerce ul.products li.product,
    body.page-id-14 .woocommerce ul.products li.product {
      display: flex !important;
      flex-direction: column !important;
      align-items: center !important;
      justify-content: flex-start !important;
      background: transparent !important;
      border: none !important;
      box-shadow: none !important;
      overflow: visible !important;
      text-align: center !important;
      height: auto !important;
      min-height: 0 !important;
      padding: 0 !important;
    }

    body.page-id-547 .woocommerce ul.products li.product a.woocommerce-loop-product__link,
    body.tax-product_cat .woocommerce ul.products li.product a.woocommerce-loop-product__link,
    body.post-type-archive-product .woocommerce ul.products li.product a.woocommerce-loop-product__link,
    body.page-id-14 .woocommerce ul.products li.product a.woocommerce-loop-product__link {
      display: flex !important;
      flex-direction: column !important;
      align-items: center !important;
      width: 100% !important;
      flex: 1 1 auto !important;
      background: transparent !important;
      text-align: center !important;
      color: #000000 !important;
      text-decoration: none !important;
    }

    body.page-id-547 .woocommerce ul.products li.product a img,
    body.page-id-547 .woocommerce ul.products li.product img,
    body.tax-product_cat .woocommerce ul.products li.product a img,
    body.tax-product_cat .woocommerce ul.products li.product img,
    body.post-type-archive-product .woocommerce ul.products li.product a img,
    body.post-type-archive-product .woocommerce ul.products li.product img,
    body.page-id-14 .woocommerce ul.products li.product a img,
    body.page-id-14 .woocommerce ul.products li.product img {
      width: 100% !important;
      aspect-ratio: 4 / 5 !important;
      height: auto !important;
      min-height: 0 !important;
      max-height: none !important;
      object-fit: contain !important;
      object-position: center center !important;
      margin: 0 0 14px !important;
      padding: 24px 18px 18px !important;
      background: #f5f5f5 !important;
      border: none !important;
      border-radius: 0 !important;
      box-sizing: border-box !important;
      display: block !important;
      transform: none !important;
      filter: none !important;
    }

    body.page-id-547 .woocommerce ul.products li.product .woocommerce-loop-product__title,
    body.tax-product_cat .woocommerce ul.products li.product .woocommerce-loop-product__title,
    body.post-type-archive-product .woocommerce ul.products li.product .woocommerce-loop-product__title,
    body.page-id-14 .woocommerce ul.products li.product .woocommerce-loop-product__title {
      width: 100% !important;
      min-height: 44px !important;
      height: auto !important;
      margin: 0 0 8px !important;
      padding: 0 8px !important;
      display: flex !important;
      align-items: flex-start !important;
      justify-content: center !important;
      overflow: visible !important;
      -webkit-line-clamp: unset !important;
      -webkit-box-orient: initial !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      font-size: 18px !important;
      font-weight: 800 !important;
      line-height: 1.08 !important;
      letter-spacing: 0 !important;
      text-align: center !important;
      text-transform: none !important;
      color: #000000 !important;
    }

    @media (min-width: 768px) {
      body.page-id-547 .woocommerce ul.products li.product .woocommerce-loop-product__title,
      body.tax-product_cat .woocommerce ul.products li.product .woocommerce-loop-product__title,
      body.post-type-archive-product .woocommerce ul.products li.product .woocommerce-loop-product__title,
      body.page-id-14 .woocommerce ul.products li.product .woocommerce-loop-product__title {
        min-height: 66px !important;
      }
    }

    body.page-id-547 .woocommerce ul.products li.product .price,
    body.tax-product_cat .woocommerce ul.products li.product .price,
    body.post-type-archive-product .woocommerce ul.products li.product .price,
    body.page-id-14 .woocommerce ul.products li.product .price {
      width: 100% !important;
      min-height: 18px !important;
      height: auto !important;
      margin: 0 0 16px !important;
      padding: 0 !important;
      display: block !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      font-size: 12px !important;
      font-weight: 400 !important;
      line-height: 1.2 !important;
      text-align: center !important;
      color: #000000 !important;
    }

    body.page-id-547 .woocommerce ul.products li.product .button,
    body.tax-product_cat .woocommerce ul.products li.product .button,
    body.post-type-archive-product .woocommerce ul.products li.product .button,
    body.page-id-14 .woocommerce ul.products li.product .button {
      margin-top: auto !important;
      align-self: center !important;
    }

    @media (max-width: 520px) {
      body.page-id-547 .woocommerce ul.products li.product a img,
      body.tax-product_cat .woocommerce ul.products li.product a img,
      body.post-type-archive-product .woocommerce ul.products li.product a img,
      body.page-id-14 .woocommerce ul.products li.product a img {
        padding: 18px 10px 12px !important;
      }

      body.page-id-547 .woocommerce ul.products li.product .woocommerce-loop-product__title,
      body.tax-product_cat .woocommerce ul.products li.product .woocommerce-loop-product__title,
      body.post-type-archive-product .woocommerce ul.products li.product .woocommerce-loop-product__title,
      body.page-id-14 .woocommerce ul.products li.product .woocommerce-loop-product__title {
        min-height: 50px !important;
        font-size: 15px !important;
      }
    }
    </style>
    <?php
}, 10100);
/* PRIME_DROP_MATCH_BUILDER_PRODUCTS_END */

/* PRIME_DROP_TODAY_FINAL_FIXES_START */
add_action('wp_footer', function() {
    ?>
    <style id="prime-drop-today-final-fixes-css">
    /* Orden por defecto: opciones legibles al hover/seleccion */
    body.page-id-547 select.orderby,
    body.page-id-547 .woocommerce-ordering select,
    body.woocommerce-shop select.orderby,
    body.tax-product_cat select.orderby {
      color: #ffffff !important;
    }

    body.page-id-547 select.orderby option,
    body.page-id-547 .woocommerce-ordering select option,
    body.woocommerce-shop select.orderby option,
    body.tax-product_cat select.orderby option {
      background: #ffffff !important;
      color: #000000 !important;
    }

    body.page-id-547 select.orderby option:hover,
    body.page-id-547 select.orderby option:focus,
    body.page-id-547 select.orderby option:checked,
    body.woocommerce-shop select.orderby option:hover,
    body.woocommerce-shop select.orderby option:checked,
    body.tax-product_cat select.orderby option:hover,
    body.tax-product_cat select.orderby option:checked {
      background: #000000 !important;
      color: #ffffff !important;
    }

    body.page-id-547 .select2-container--default .select2-results__option--highlighted[aria-selected],
    body.woocommerce-shop .select2-container--default .select2-results__option--highlighted[aria-selected],
    body.tax-product_cat .select2-container--default .select2-results__option--highlighted[aria-selected] {
      background: #000000 !important;
      color: #ffffff !important;
    }

    /* Reseñas antes de productos relacionados */
    .pd-product-reviews-preview {
      margin: 42px auto 26px !important;
      padding: 28px 30px !important;
      border-top: 1px solid #eeeeee !important;
      border-bottom: 1px solid #eeeeee !important;
      max-width: 1180px !important;
      display: grid !important;
      grid-template-columns: minmax(0, 1fr) auto !important;
      align-items: center !important;
      gap: 20px !important;
      background: #ffffff !important;
    }

    .pd-product-reviews-preview h2 {
      margin: 0 0 8px !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      font-size: 28px !important;
      line-height: 1.1 !important;
      color: #000000 !important;
    }

    .pd-product-reviews-preview p {
      margin: 0 !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      font-size: 14px !important;
      line-height: 1.55 !important;
      color: #333333 !important;
      max-width: 620px !important;
    }

    .pd-product-review-stars {
      display: flex !important;
      align-items: center !important;
      gap: 4px !important;
      font-size: 18px !important;
      line-height: 1 !important;
      letter-spacing: 2px !important;
      color: #000000 !important;
      margin-bottom: 10px !important;
    }

    .pd-product-review-note {
      text-align: right !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      font-size: 12px !important;
      font-weight: 800 !important;
      letter-spacing: 1.5px !important;
      text-transform: uppercase !important;
      color: #000000 !important;
      white-space: nowrap !important;
    }

    @media (max-width: 768px) {
      .pd-product-reviews-preview {
        grid-template-columns: 1fr !important;
        margin: 34px 18px 24px !important;
        padding: 24px 0 !important;
      }

      .pd-product-review-note {
        text-align: left !important;
        white-space: normal !important;
      }
    }

    /* Terminos y condiciones: lectura limpia */
    body.page-id-751 .entry-content,
    body.page-id-751 .ct-container-full .entry-content {
      max-width: 920px !important;
      margin-left: auto !important;
      margin-right: auto !important;
      padding: 42px 20px 70px !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      color: #111111 !important;
    }

    body.page-id-751 .entry-content p {
      font-size: 15px !important;
      line-height: 1.75 !important;
      margin: 0 0 16px !important;
    }
    </style>

    <script id="prime-drop-today-final-fixes-js">
    (function() {
      var brandItems = [
        ['TODOS LOS BOLSOS', '/bolsos/'],
        ['KARL LAGERFELD', '/product-category/karl-lagerfeld/'],
        ['MICHAEL KORS', '/product-category/michael-kors/'],
        ['STEVE MADDEN', '/product-category/steve-madden/'],
        ['TOMMY HILFIGER', '/product-category/tommy-hilfiger/']
      ];

      function brandListHtml() {
        return brandItems.map(function(item) {
          return '<li><a href="' + item[1] + '"' + (item[0] === 'TODOS LOS BOLSOS' ? ' data-pd-all-bags="1"' : '') + '>' + item[0] + '</a></li>';
        }).join('');
      }

      function fixBolsosSubmenus() {
        document.querySelectorAll('.pd-bolsos-menu-parent').forEach(function(li) {
          var submenu = li.querySelector(':scope > .pd-bolsos-submenu');
          if (!submenu) return;
          if (submenu.dataset.pdBrandsOnly === '1') return;
          submenu.innerHTML = brandListHtml();
          submenu.dataset.pdBrandsOnly = '1';
        });
      }

      function fixBrandFilter() {
        if (!document.body.classList.contains('page-id-547')) return;
        var filter = document.querySelector('.pd-brand-filter');
        if (!filter || filter.dataset.pdBrandsOnly === '1') return;
        filter.innerHTML = brandItems.map(function(item) {
          return '<a href="' + item[1] + '">' + item[0] + '</a>';
        }).join('');
        filter.dataset.pdBrandsOnly = '1';
      }

      function run() {
        fixBolsosSubmenus();
        fixBrandFilter();
      }

      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', run);
      } else {
        run();
      }
      window.addEventListener('load', run);
      document.addEventListener('click', function(){ setTimeout(run, 120); }, true);
      new MutationObserver(run).observe(document.documentElement, { childList: true, subtree: true });
    })();
    </script>
    <?php
}, 10120);

add_action('woocommerce_after_single_product_summary', function() {
    if (!function_exists('is_product') || !is_product()) {
        return;
    }
    echo '<section class="pd-product-reviews-preview" aria-label="Reseñas de clientes">';
    echo '<div>';
    echo '<div class="pd-product-review-stars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</div>';
    echo '<h2>Reseñas de clientes</h2>';
    echo '<p>Aún no hay reseñas publicadas para este bolso. Cuando completes tu compra, podrás compartir tu experiencia y ayudar a otras clientas a elegir mejor.</p>';
    echo '</div>';
    echo '<div class="pd-product-review-note">Opiniones verificadas</div>';
    echo '</section>';
}, 19);
/* PRIME_DROP_TODAY_FINAL_FIXES_END */

/* PRIME_DROP_BRAND_ARCHIVE_PRICE_STYLE_START */
add_action('wp_footer', function() {
    ?>
    <style id="prime-drop-brand-archive-price-style-css">
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Serif:wght@400;500;600;700;800&display=swap');

    /* Marcas: misma base visual de productos que /bolsos/ */
    body.tax-product_cat .woocommerce-products-header,
    body.tax-product_cat .woocommerce-notices-wrapper,
    body.tax-product_cat .woocommerce-result-count,
    body.tax-product_cat .woocommerce-ordering,
    body.tax-product_cat .woocommerce ul.products,
    body.tax-product_cat .woocommerce ul.products li.product,
    body.tax-product_cat .woocommerce ul.products li.product a,
    body.tax-product_cat .woocommerce ul.products li.product .woocommerce-loop-product__title,
    body.tax-product_cat .woocommerce ul.products li.product .price,
    body.tax-product_cat .woocommerce ul.products li.product .button {
      font-family: "Roboto Serif", Georgia, serif !important;
    }

    body.tax-product_cat .woocommerce-products-header {
      max-width: 1200px !important;
      margin: 0 auto 22px !important;
      padding: 26px 20px 0 !important;
      text-align: center !important;
    }

    body.tax-product_cat .woocommerce-products-header .page-title {
      margin: 0 !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      font-size: 30px !important;
      font-weight: 800 !important;
      line-height: 1.15 !important;
      color: #000000 !important;
      text-align: center !important;
    }

    body.tax-product_cat .woocommerce-result-count,
    body.tax-product_cat .woocommerce-ordering {
      font-size: 12px !important;
      font-weight: 700 !important;
      letter-spacing: 1.2px !important;
      text-transform: uppercase !important;
      color: #000000 !important;
    }

    /* Precio estilo Parchita: visible, centrado y con COP solo en listados */
    body.page-id-547 .woocommerce ul.products li.product .price,
    body.tax-product_cat .woocommerce ul.products li.product .price,
    body.post-type-archive-product .woocommerce ul.products li.product .price,
    body.page-id-14 .woocommerce ul.products li.product .price,
    body.single-product .related.products ul.products li.product .price {
      display: block !important;
      width: 100% !important;
      min-height: 22px !important;
      margin: 0 0 16px !important;
      padding: 0 !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      font-size: 14px !important;
      font-weight: 700 !important;
      line-height: 1.25 !important;
      letter-spacing: 0 !important;
      text-align: center !important;
      color: #000000 !important;
      opacity: 1 !important;
      visibility: visible !important;
    }

    body.page-id-547 .woocommerce ul.products li.product .price .woocommerce-Price-amount,
    body.tax-product_cat .woocommerce ul.products li.product .price .woocommerce-Price-amount,
    body.post-type-archive-product .woocommerce ul.products li.product .price .woocommerce-Price-amount,
    body.page-id-14 .woocommerce ul.products li.product .price .woocommerce-Price-amount,
    body.single-product .related.products ul.products li.product .price .woocommerce-Price-amount {
      color: #000000 !important;
      font: inherit !important;
      white-space: nowrap !important;
    }

    body.page-id-547 .woocommerce ul.products li.product .price .woocommerce-Price-amount::after,
    body.tax-product_cat .woocommerce ul.products li.product .price .woocommerce-Price-amount::after,
    body.post-type-archive-product .woocommerce ul.products li.product .price .woocommerce-Price-amount::after,
    body.page-id-14 .woocommerce ul.products li.product .price .woocommerce-Price-amount::after,
    body.single-product .related.products ul.products li.product .price .woocommerce-Price-amount::after {
      content: " COP";
      font: inherit;
    }

    body.page-id-547 .woocommerce ul.products li.product .woocommerce-loop-product__title,
    body.tax-product_cat .woocommerce ul.products li.product .woocommerce-loop-product__title,
    body.post-type-archive-product .woocommerce ul.products li.product .woocommerce-loop-product__title,
    body.page-id-14 .woocommerce ul.products li.product .woocommerce-loop-product__title,
    body.single-product .related.products ul.products li.product .woocommerce-loop-product__title {
      font-family: "Roboto Serif", Georgia, serif !important;
    }

    body.tax-product_cat select.orderby,
    body.page-id-547 select.orderby,
    body.woocommerce-shop select.orderby {
      color: #ffffff !important;
      background-color: #000000 !important;
      border-color: #000000 !important;
      font-family: "Roboto Serif", Georgia, serif !important;
    }

    body.tax-product_cat select.orderby option,
    body.page-id-547 select.orderby option,
    body.woocommerce-shop select.orderby option {
      color: #000000 !important;
      background-color: #ffffff !important;
    }

    @media (max-width: 768px) {
      body.tax-product_cat .woocommerce-products-header {
        padding-top: 18px !important;
        margin-bottom: 18px !important;
      }

      body.tax-product_cat .woocommerce-products-header .page-title {
        font-size: 24px !important;
      }

      body.page-id-547 .woocommerce ul.products li.product .price,
      body.tax-product_cat .woocommerce ul.products li.product .price,
      body.post-type-archive-product .woocommerce ul.products li.product .price,
      body.page-id-14 .woocommerce ul.products li.product .price,
      body.single-product .related.products ul.products li.product .price {
        font-size: 13px !important;
      }
    }
    </style>
    <?php
}, 10220);
/* PRIME_DROP_BRAND_ARCHIVE_PRICE_STYLE_END */

/* PRIME_DROP_TAX_CATEGORIES_MATCH_BOLSOS_START */
add_action('wp_footer', function() {
    ?>
    <style id="prime-drop-tax-categories-match-bolsos-css">
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Serif:wght@400;500;600;700;800&display=swap');

    /* Categorias/marcas: misma estructura visual que /bolsos/ */
    body.tax-product_cat .woocommerce-products-header,
    body.tax-product_cat .pd-shop-search {
      display: none !important;
    }

    body.tax-product_cat .site-main .woocommerce {
      max-width: 900px !important;
      margin: 0 auto !important;
      padding: 0 0 78px !important;
      border-top: 1px solid #eeeeee !important;
      font-family: "Roboto Serif", Georgia, serif !important;
    }

    body.tax-product_cat .woocommerce-result-count {
      float: left !important;
      display: flex !important;
      align-items: center !important;
      min-height: 58px !important;
      margin: 0 !important;
      padding: 0 !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      font-size: 12px !important;
      font-weight: 800 !important;
      letter-spacing: 1.3px !important;
      text-transform: uppercase !important;
      color: #000000 !important;
    }

    body.tax-product_cat .woocommerce-ordering {
      float: right !important;
      display: flex !important;
      align-items: center !important;
      min-height: 58px !important;
      margin: 0 !important;
      padding: 0 !important;
      font-family: "Roboto Serif", Georgia, serif !important;
    }

    body.tax-product_cat select.orderby {
      min-width: 180px !important;
      height: 34px !important;
      border-radius: 999px !important;
      border: 1px solid #000000 !important;
      background-color: #000000 !important;
      color: #ffffff !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      font-size: 11px !important;
      font-weight: 800 !important;
      letter-spacing: 1px !important;
      text-transform: uppercase !important;
      padding: 0 34px 0 18px !important;
      box-shadow: none !important;
    }

    body.tax-product_cat select.orderby option {
      background: #ffffff !important;
      color: #000000 !important;
      font-family: "Roboto Serif", Georgia, serif !important;
    }

    body.tax-product_cat .woocommerce ul.products {
      clear: both !important;
      display: grid !important;
      grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
      gap: 46px 28px !important;
      align-items: stretch !important;
      width: 100% !important;
      max-width: 900px !important;
      margin: 0 auto !important;
      padding: 24px 0 0 !important;
      border-top: 1px solid #eeeeee !important;
      list-style: none !important;
    }

    body.tax-product_cat .woocommerce ul.products::before,
    body.tax-product_cat .woocommerce ul.products::after {
      display: none !important;
      content: none !important;
    }

    body.tax-product_cat .woocommerce ul.products li.product {
      float: none !important;
      width: auto !important;
      max-width: none !important;
      min-width: 0 !important;
      margin: 0 !important;
      padding: 0 !important;
      display: flex !important;
      flex-direction: column !important;
      align-items: center !important;
      justify-content: flex-start !important;
      text-align: center !important;
      background: transparent !important;
      border: none !important;
      box-shadow: none !important;
      overflow: visible !important;
      box-sizing: border-box !important;
    }

    body.tax-product_cat .woocommerce ul.products li.product figure {
      width: 100% !important;
      margin: 0 0 0 !important;
      padding: 0 !important;
      background: #f5f5f5 !important;
      overflow: hidden !important;
      border: none !important;
      border-radius: 0 !important;
      box-sizing: border-box !important;
    }

    body.tax-product_cat .woocommerce ul.products li.product figure a.ct-media-container,
    body.tax-product_cat .woocommerce ul.products li.product a.woocommerce-loop-product__link {
      width: 100% !important;
      display: flex !important;
      flex-direction: column !important;
      align-items: center !important;
      justify-content: flex-start !important;
      text-align: center !important;
      color: #000000 !important;
      text-decoration: none !important;
      background: transparent !important;
    }

    body.tax-product_cat .woocommerce ul.products li.product figure a.ct-media-container {
      height: 278px !important;
      min-height: 278px !important;
      max-height: 278px !important;
      justify-content: center !important;
      background: #f5f5f5 !important;
    }

    body.tax-product_cat .woocommerce ul.products li.product a img,
    body.tax-product_cat .woocommerce ul.products li.product img {
      width: 100% !important;
      height: 100% !important;
      min-height: 0 !important;
      max-height: none !important;
      aspect-ratio: auto !important;
      object-fit: contain !important;
      object-position: center center !important;
      margin: 0 !important;
      padding: 18px !important;
      background: #f5f5f5 !important;
      border: none !important;
      border-radius: 0 !important;
      box-shadow: none !important;
      display: block !important;
      box-sizing: border-box !important;
      transform: none !important;
      filter: none !important;
    }

    body.tax-product_cat .woocommerce ul.products li.product .woocommerce-loop-product__title {
      width: 100% !important;
      min-height: 42px !important;
      margin: 0 0 10px !important;
      padding: 0 8px !important;
      display: flex !important;
      align-items: flex-start !important;
      justify-content: center !important;
      overflow: visible !important;
      -webkit-line-clamp: unset !important;
      -webkit-box-orient: initial !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      font-size: 16px !important;
      font-weight: 800 !important;
      line-height: 1.12 !important;
      letter-spacing: 0 !important;
      text-align: center !important;
      text-transform: none !important;
      color: #000000 !important;
    }

    body.tax-product_cat .woocommerce ul.products li.product .woocommerce-loop-product__title a {
      color: #000000 !important;
      text-decoration: none !important;
      font: inherit !important;
      text-align: center !important;
    }

    body.tax-product_cat .woocommerce ul.products li.product .price {
      width: 100% !important;
      min-height: 22px !important;
      margin: 0 0 16px !important;
      padding: 0 !important;
      display: block !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      font-size: 14px !important;
      font-weight: 700 !important;
      line-height: 1.25 !important;
      letter-spacing: 0 !important;
      text-align: center !important;
      color: #000000 !important;
    }

    body.tax-product_cat .woocommerce ul.products li.product .entry-meta,
    body.tax-product_cat .woocommerce ul.products li.product .meta-categories {
      display: none !important;
    }

    body.tax-product_cat .woocommerce ul.products li.product .button,
    body.tax-product_cat .woocommerce ul.products li.product:hover .button {
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      width: auto !important;
      min-width: 120px !important;
      max-width: 100% !important;
      min-height: 30px !important;
      margin: auto auto 0 !important;
      padding: 7px 14px !important;
      background: #ffffff !important;
      color: #000000 !important;
      border: 1.4px solid #000000 !important;
      border-radius: 999px !important;
      box-shadow: none !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      font-size: 10.5px !important;
      font-weight: 700 !important;
      letter-spacing: 0 !important;
      line-height: 1.15 !important;
      text-align: center !important;
      text-transform: uppercase !important;
      white-space: nowrap !important;
      opacity: 1 !important;
      transform: none !important;
      pointer-events: auto !important;
      box-sizing: border-box !important;
    }

    body.tax-product_cat .woocommerce ul.products li.product .button:hover {
      background: #000000 !important;
      color: #ffffff !important;
    }

    @media (max-width: 999px) {
      body.tax-product_cat .site-main .woocommerce {
        max-width: calc(100% - 36px) !important;
      }

      body.tax-product_cat .woocommerce ul.products {
        grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
        gap: 34px 18px !important;
      }

      body.tax-product_cat .woocommerce ul.products li.product figure a.ct-media-container {
        height: 245px !important;
        min-height: 245px !important;
        max-height: 245px !important;
      }
    }

    @media (max-width: 767px) {
      body.tax-product_cat .site-main .woocommerce {
        max-width: 100% !important;
        padding-left: 10px !important;
        padding-right: 10px !important;
      }

      body.tax-product_cat .woocommerce-result-count,
      body.tax-product_cat .woocommerce-ordering {
        float: none !important;
        width: 100% !important;
        min-height: 0 !important;
        justify-content: center !important;
        margin: 0 0 12px !important;
      }

      body.tax-product_cat .woocommerce-result-count {
        padding-top: 14px !important;
      }

      body.tax-product_cat .woocommerce ul.products {
        grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
        gap: 24px 12px !important;
        padding-top: 18px !important;
      }

      body.tax-product_cat .woocommerce ul.products li.product figure a.ct-media-container {
        height: 235px !important;
        min-height: 235px !important;
        max-height: 235px !important;
      }

      body.tax-product_cat .woocommerce ul.products li.product a img,
      body.tax-product_cat .woocommerce ul.products li.product img {
        padding: 10px !important;
      }

      body.tax-product_cat .woocommerce ul.products li.product .woocommerce-loop-product__title {
        min-height: 48px !important;
        font-size: 15px !important;
      }
    }
    </style>
    <?php
}, 10240);
/* PRIME_DROP_TAX_CATEGORIES_MATCH_BOLSOS_END */

/* PRIME_DROP_TAX_CATEGORIES_FORCE_BOLSOS_GRID_START */
add_action('wp_footer', function() {
    ?>
    <style id="prime-drop-tax-categories-force-bolsos-grid-css">
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Serif:wght@400;500;600;700;800&display=swap');

    /* Categorias de marca: misma grilla/cards que Todos los bolsos */
    body.tax-product_cat .hero-section,
    body.tax-product_cat .pd-shop-search,
    body.tax-product_cat .woocommerce-products-header {
      display: none !important;
    }

    body.tax-product_cat .woo-listing-top {
      width: 100% !important;
      min-height: 78px !important;
      margin: 0 !important;
      padding: 0 !important;
      display: flex !important;
      align-items: center !important;
      justify-content: space-between !important;
      gap: 20px !important;
      border-top: 1px solid #eeeeee !important;
      border-bottom: 1px solid #eeeeee !important;
      box-sizing: border-box !important;
    }

    body.tax-product_cat.woocommerce ul.products.products,
    body.tax-product_cat.woocommerce-page ul.products.products {
      clear: both !important;
      display: grid !important;
      grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
      gap: 46px 28px !important;
      align-items: stretch !important;
      width: 100% !important;
      margin: 0 auto !important;
      padding: 24px 0 0 !important;
      border-top: 1px solid #eeeeee !important;
      list-style: none !important;
      font-family: "Roboto Serif", Georgia, serif !important;
    }

    body.tax-product_cat .woocommerce-result-count {
      float: none !important;
      flex: 1 1 auto !important;
      width: auto !important;
      min-height: 0 !important;
      margin: 0 !important;
      padding: 0 !important;
      display: flex !important;
      align-items: center !important;
      justify-content: flex-start !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      font-size: 12px !important;
      font-weight: 800 !important;
      letter-spacing: 1.3px !important;
      text-transform: uppercase !important;
      color: #000000 !important;
    }

    body.tax-product_cat .woocommerce-ordering {
      float: none !important;
      flex: 0 0 auto !important;
      width: 240px !important;
      min-height: 0 !important;
      margin: 0 !important;
      padding: 0 !important;
      display: flex !important;
      align-items: center !important;
      justify-content: flex-end !important;
    }

    body.tax-product_cat .woocommerce-ordering select.orderby {
      width: 240px !important;
      min-width: 240px !important;
      max-width: 240px !important;
      height: 44px !important;
      min-height: 44px !important;
    }

    body.tax-product_cat.woocommerce ul.products.products::before,
    body.tax-product_cat.woocommerce ul.products.products::after,
    body.tax-product_cat.woocommerce-page ul.products.products::before,
    body.tax-product_cat.woocommerce-page ul.products.products::after {
      display: none !important;
      content: none !important;
    }

    body.tax-product_cat.woocommerce ul.products.products li.product,
    body.tax-product_cat.woocommerce-page ul.products.products li.product {
      float: none !important;
      width: auto !important;
      max-width: none !important;
      min-width: 0 !important;
      margin: 0 !important;
      padding: 0 !important;
      display: flex !important;
      flex-direction: column !important;
      align-items: center !important;
      justify-content: flex-start !important;
      text-align: center !important;
      background: transparent !important;
      border: none !important;
      box-shadow: none !important;
      overflow: visible !important;
      box-sizing: border-box !important;
    }

    body.tax-product_cat.woocommerce ul.products.products li.product figure,
    body.tax-product_cat.woocommerce-page ul.products.products li.product figure {
      width: 100% !important;
      margin: 0 0 14px !important;
      padding: 0 !important;
      background: #f5f5f5 !important;
      border: none !important;
      border-radius: 0 !important;
      overflow: hidden !important;
      box-sizing: border-box !important;
    }

    body.tax-product_cat.woocommerce ul.products.products li.product figure a.ct-media-container,
    body.tax-product_cat.woocommerce-page ul.products.products li.product figure a.ct-media-container {
      width: 100% !important;
      aspect-ratio: 4 / 5 !important;
      height: auto !important;
      min-height: 0 !important;
      max-height: none !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      background: #f5f5f5 !important;
    }

    body.tax-product_cat.woocommerce ul.products.products li.product figure img,
    body.tax-product_cat.woocommerce ul.products.products li.product a img,
    body.tax-product_cat.woocommerce ul.products.products li.product img,
    body.tax-product_cat.woocommerce-page ul.products.products li.product figure img,
    body.tax-product_cat.woocommerce-page ul.products.products li.product a img,
    body.tax-product_cat.woocommerce-page ul.products.products li.product img {
      width: 100% !important;
      height: 100% !important;
      min-height: 0 !important;
      max-height: none !important;
      aspect-ratio: auto !important;
      object-fit: contain !important;
      object-position: center center !important;
      margin: 0 !important;
      padding: 24px 18px 18px !important;
      background: #f5f5f5 !important;
      border: none !important;
      border-radius: 0 !important;
      box-shadow: none !important;
      display: block !important;
      box-sizing: border-box !important;
      transform: none !important;
      filter: none !important;
    }

    body.tax-product_cat.woocommerce ul.products.products li.product .woocommerce-loop-product__title,
    body.tax-product_cat.woocommerce-page ul.products.products li.product .woocommerce-loop-product__title {
      width: 100% !important;
      min-height: 66px !important;
      height: auto !important;
      margin: 0 0 8px !important;
      padding: 0 8px !important;
      display: flex !important;
      align-items: flex-start !important;
      justify-content: center !important;
      overflow: visible !important;
      -webkit-line-clamp: unset !important;
      -webkit-box-orient: initial !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      font-size: 18px !important;
      font-weight: 800 !important;
      line-height: 1.08 !important;
      letter-spacing: 0 !important;
      text-align: center !important;
      text-transform: none !important;
      color: #000000 !important;
    }

    body.tax-product_cat.woocommerce ul.products.products li.product .woocommerce-loop-product__title a,
    body.tax-product_cat.woocommerce-page ul.products.products li.product .woocommerce-loop-product__title a {
      color: #000000 !important;
      text-decoration: none !important;
      font: inherit !important;
      text-align: center !important;
    }

    body.tax-product_cat.woocommerce ul.products.products li.product .price,
    body.tax-product_cat.woocommerce-page ul.products.products li.product .price {
      width: 100% !important;
      min-height: 22px !important;
      margin: 0 0 16px !important;
      padding: 0 !important;
      display: block !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      font-size: 14px !important;
      font-weight: 700 !important;
      line-height: 1.25 !important;
      text-align: center !important;
      color: #000000 !important;
    }

    body.tax-product_cat.woocommerce ul.products.products li.product .entry-meta,
    body.tax-product_cat.woocommerce ul.products.products li.product .meta-categories,
    body.tax-product_cat.woocommerce-page ul.products.products li.product .entry-meta,
    body.tax-product_cat.woocommerce-page ul.products.products li.product .meta-categories {
      display: none !important;
    }

    body.tax-product_cat.woocommerce ul.products.products li.product .button,
    body.tax-product_cat.woocommerce ul.products.products li.product:hover .button,
    body.tax-product_cat.woocommerce-page ul.products.products li.product .button,
    body.tax-product_cat.woocommerce-page ul.products.products li.product:hover .button {
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      width: auto !important;
      min-width: 120px !important;
      max-width: 100% !important;
      min-height: 30px !important;
      margin: auto auto 0 !important;
      padding: 7px 14px !important;
      background: #ffffff !important;
      color: #000000 !important;
      border: 1.4px solid #000000 !important;
      border-radius: 999px !important;
      box-shadow: none !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      font-size: 10.5px !important;
      font-weight: 700 !important;
      letter-spacing: 0 !important;
      line-height: 1.15 !important;
      text-align: center !important;
      text-transform: uppercase !important;
      white-space: nowrap !important;
      opacity: 1 !important;
      transform: none !important;
      pointer-events: auto !important;
      box-sizing: border-box !important;
    }

    body.tax-product_cat.woocommerce ul.products.products li.product .button:hover,
    body.tax-product_cat.woocommerce-page ul.products.products li.product .button:hover {
      background: #000000 !important;
      color: #ffffff !important;
    }

    @media (max-width: 999px) {
      body.tax-product_cat.woocommerce ul.products.products,
      body.tax-product_cat.woocommerce-page ul.products.products {
        grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
        gap: 34px 18px !important;
      }
    }

    @media (max-width: 767px) {
      body.tax-product_cat.woocommerce ul.products.products,
      body.tax-product_cat.woocommerce-page ul.products.products {
        grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
        gap: 24px 12px !important;
        padding-top: 18px !important;
      }

      body.tax-product_cat.woocommerce ul.products.products li.product figure img,
      body.tax-product_cat.woocommerce ul.products.products li.product a img,
      body.tax-product_cat.woocommerce ul.products.products li.product img,
      body.tax-product_cat.woocommerce-page ul.products.products li.product figure img,
      body.tax-product_cat.woocommerce-page ul.products.products li.product a img,
      body.tax-product_cat.woocommerce-page ul.products.products li.product img {
        padding: 18px 10px 12px !important;
      }

      body.tax-product_cat.woocommerce ul.products.products li.product .woocommerce-loop-product__title,
      body.tax-product_cat.woocommerce-page ul.products.products li.product .woocommerce-loop-product__title {
        min-height: 50px !important;
        font-size: 15px !important;
      }
    }
    </style>
    <?php
}, 10280);
/* PRIME_DROP_TAX_CATEGORIES_FORCE_BOLSOS_GRID_END */

/* PRIME_DROP_CENTER_ORDERBY_OPTIONS_START */
add_filter('woocommerce_catalog_orderby', function($options) {
    $labels = array(
        'menu_order' => 'ORDEN POR DEFECTO',
        'popularity' => 'POPULARIDAD',
        'rating' => 'CALIFICACIÓN',
        'date' => 'ÚLTIMAS',
        'price' => 'MENOR PRECIO',
        'price-desc' => 'MAYOR PRECIO',
    );

    foreach ($labels as $key => $label) {
        if (isset($options[$key])) {
            $options[$key] = $label;
        }
    }

    return $options;
}, 99);

add_filter('woocommerce_default_catalog_orderby_options', function($options) {
    $labels = array(
        'menu_order' => 'ORDEN POR DEFECTO',
        'popularity' => 'POPULARIDAD',
        'rating' => 'CALIFICACIÓN',
        'date' => 'ÚLTIMAS',
        'price' => 'MENOR PRECIO',
        'price-desc' => 'MAYOR PRECIO',
    );

    foreach ($labels as $key => $label) {
        if (isset($options[$key])) {
            $options[$key] = $label;
        }
    }

    return $options;
}, 99);

add_action('wp_footer', function() {
    ?>
    <style id="prime-drop-center-orderby-options-css">
    body.page-id-547 select.orderby,
    body.tax-product_cat select.orderby,
    body.woocommerce-shop select.orderby,
    body.post-type-archive-product select.orderby {
      appearance: none !important;
      -webkit-appearance: none !important;
      -moz-appearance: none !important;
      text-align: center !important;
      text-align-last: center !important;
      -moz-text-align-last: center !important;
      text-indent: 0 !important;
      padding-left: 44px !important;
      padding-right: 44px !important;
      background-image: none !important;
    }

    body.page-id-547 select.orderby::-ms-expand,
    body.tax-product_cat select.orderby::-ms-expand,
    body.woocommerce-shop select.orderby::-ms-expand,
    body.post-type-archive-product select.orderby::-ms-expand {
      display: none !important;
    }

    body.page-id-547 .woocommerce-ordering,
    body.tax-product_cat .woocommerce-ordering,
    body.woocommerce-shop .woocommerce-ordering,
    body.post-type-archive-product .woocommerce-ordering {
      position: relative !important;
    }

    body.page-id-547 .woocommerce-ordering::after,
    body.tax-product_cat .woocommerce-ordering::after,
    body.woocommerce-shop .woocommerce-ordering::after,
    body.post-type-archive-product .woocommerce-ordering::after {
      content: "" !important;
      position: absolute !important;
      top: 50% !important;
      right: 22px !important;
      width: 6px !important;
      height: 6px !important;
      border-right: 1.5px solid #ffffff !important;
      border-bottom: 1.5px solid #ffffff !important;
      transform: translateY(-65%) rotate(45deg) !important;
      pointer-events: none !important;
      z-index: 2 !important;
    }

    body.page-id-547 select.orderby option,
    body.tax-product_cat select.orderby option,
    body.woocommerce-shop select.orderby option,
    body.post-type-archive-product select.orderby option {
      text-align: center !important;
      text-align-last: center !important;
      -moz-text-align-last: center !important;
      padding-left: 0 !important;
      padding-right: 0 !important;
      text-indent: 0 !important;
      direction: ltr !important;
    }

    body.page-id-547 .woof_products_top_panel,
    body.page-id-547 .woof_products_top_panel_content,
    body.tax-product_cat .woof_products_top_panel,
    body.tax-product_cat .woof_products_top_panel_content,
    body.woocommerce-shop .woof_products_top_panel,
    body.woocommerce-shop .woof_products_top_panel_content,
    body.post-type-archive-product .woof_products_top_panel,
    body.post-type-archive-product .woof_products_top_panel_content {
      display: none !important;
      height: 0 !important;
      min-height: 0 !important;
      margin: 0 !important;
      padding: 0 !important;
      overflow: hidden !important;
    }
    </style>
    <script id="prime-drop-center-orderby-options-js">
    (function() {
      function centerOrderOptions() {
        document.querySelectorAll('select.orderby option').forEach(function(option) {
          option.style.textAlign = 'center';
          option.style.textAlignLast = 'center';
          option.style.paddingLeft = '0';
          option.style.paddingRight = '0';
          option.style.textIndent = '0';
          option.style.direction = 'ltr';
        });
      }

      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', centerOrderOptions);
      } else {
        centerOrderOptions();
      }

      window.addEventListener('pageshow', centerOrderOptions);
      window.addEventListener('load', centerOrderOptions);
    })();
    </script>
    <?php
}, 10300);
/* PRIME_DROP_CENTER_ORDERBY_OPTIONS_END */

/* PRIME_DROP_HOME_HERO_LOCAL_VIDEO_START */
add_filter('the_content', function($content) {
    if (!is_front_page() && !is_page(14)) {
        return $content;
    }

    $old_source = '<source src="https://videos.pexels.com/video-files/6649983/6649983-uhd_2732_1440_25fps.mp4" type="video/mp4">';
    $new_source = '<source src="' . esc_url('https://primedropelite.com/wp-content/uploads/2026/06/IMG_14355.mp4') . '" type="video/mp4">';
    $content = str_replace($old_source, $new_source, $content);
    $content = str_replace('https://videos.pexels.com/video-files/6649983/6649983-uhd_2732_1440_25fps.mp4', esc_url('https://primedropelite.com/wp-content/uploads/2026/06/IMG_14355.mp4'), $content);
    return $content;
}, 999);

add_action('wp_footer', function() {
    if (!is_front_page() && !is_page(14)) {
        return;
    }
    ?>
    <style id="prime-drop-home-hero-local-video-css">
    .pd-hero,
    .pd-hero-video.hero-section,
    .hero-video-section {
      position: relative !important;
      overflow: hidden !important;
    }

    .pd-hero .pd-hero-video-bg,
    .pd-hero video,
    .hero-video-section video {
      position: absolute !important;
      top: 50% !important;
      left: 50% !important;
      transform: translate(-50%, -50%) !important;
      min-width: 100% !important;
      min-height: 100% !important;
      width: auto !important;
      height: auto !important;
      object-fit: cover !important;
      object-position: center center !important;
      z-index: 0 !important;
    }
    </style>
    <?php
}, 10320);
/* PRIME_DROP_HOME_HERO_LOCAL_VIDEO_END */

/* PRIME_DROP_CATEGORY_SEARCH_CART_EMPTY_FIXES_START */
add_filter('woocommerce_return_to_shop_redirect', function() {
    return home_url('/');
}, 99);

add_filter('woocommerce_return_to_shop_text', function() {
    return 'Volver al inicio';
}, 99);

add_filter('wc_empty_cart_message', function() {
    return 'Tu bolsa de compra está vacía.';
}, 99);

add_action('wp_footer', function() {
    ?>
    <style id="prime-drop-category-search-cart-empty-fixes-css">
    /* Productos: eliminar cuadros/fondos que se ven como parches blancos */
    body.page-id-547 ul.products li.product,
    body.tax-product_cat ul.products li.product {
      background: transparent !important;
      box-shadow: none !important;
      border: 0 !important;
    }

    body.page-id-547 ul.products li.product figure,
    body.tax-product_cat ul.products li.product figure,
    body.page-id-547 ul.products li.product .ct-media-container,
    body.tax-product_cat ul.products li.product .ct-media-container,
    body.page-id-547 ul.products li.product a.woocommerce-loop-product__link,
    body.tax-product_cat ul.products li.product a.woocommerce-loop-product__link {
      background: #ffffff !important;
      border: 0 !important;
      box-shadow: none !important;
      outline: 0 !important;
      border-radius: 0 !important;
    }

    body.page-id-547 ul.products li.product img,
    body.tax-product_cat ul.products li.product img {
      background: #ffffff !important;
      box-shadow: none !important;
      border: 0 !important;
      object-fit: contain !important;
      object-position: center center !important;
      mix-blend-mode: multiply;
    }

    /* Buscador centrado para todos los listados y categorias */
    body.page-id-547 .woo-listing-top,
    body.tax-product_cat .woo-listing-top,
    body.woocommerce-shop .woo-listing-top,
    body.post-type-archive-product .woo-listing-top {
      display: grid !important;
      grid-template-columns: minmax(160px, 1fr) minmax(260px, 430px) minmax(160px, 1fr) !important;
      grid-template-areas:
        ". search ."
        "count . order" !important;
      gap: 18px 24px !important;
      align-items: center !important;
      width: 100% !important;
    }

    body.page-id-547 .woo-listing-top .woocommerce-result-count,
    body.tax-product_cat .woo-listing-top .woocommerce-result-count,
    body.woocommerce-shop .woo-listing-top .woocommerce-result-count,
    body.post-type-archive-product .woo-listing-top .woocommerce-result-count {
      grid-area: count !important;
      margin: 0 !important;
      justify-self: start !important;
    }

    body.page-id-547 .pd-shop-search,
    body.tax-product_cat .pd-shop-search,
    body.woocommerce-shop .pd-shop-search,
    body.post-type-archive-product .pd-shop-search {
      grid-area: search !important;
      width: min(100%, 430px) !important;
      margin: 0 auto !important;
      justify-self: center !important;
      display: block !important;
    }

    body.woocommerce.woocommerce-page.tax-product_cat .woo-listing-top > div.pd-shop-search,
    body.archive.tax-product_cat .woo-listing-top > div.pd-shop-search,
    body.page-id-547 .woo-listing-top > div.pd-shop-search {
      display: block !important;
      visibility: visible !important;
      opacity: 1 !important;
      height: auto !important;
      overflow: visible !important;
      pointer-events: auto !important;
    }

    body.page-id-547 .pd-shop-search form,
    body.tax-product_cat .pd-shop-search form,
    body.woocommerce-shop .pd-shop-search form,
    body.post-type-archive-product .pd-shop-search form {
      width: 100% !important;
      height: 44px !important;
      display: flex !important;
      align-items: center !important;
      background: #f6f6f6 !important;
      border: 0 !important;
      border-radius: 25px !important;
      overflow: hidden !important;
      box-shadow: none !important;
    }

    body.page-id-547 .pd-shop-search input[type="search"],
    body.tax-product_cat .pd-shop-search input[type="search"],
    body.woocommerce-shop .pd-shop-search input[type="search"],
    body.post-type-archive-product .pd-shop-search input[type="search"] {
      height: 44px !important;
      flex: 1 1 auto !important;
      min-width: 0 !important;
      border: 0 !important;
      outline: 0 !important;
      box-shadow: none !important;
      background: transparent !important;
      color: #111111 !important;
      padding: 0 18px !important;
      font-family: 'Roboto Serif', serif !important;
      font-size: 13px !important;
    }

    body.page-id-547 .pd-shop-search button[type="submit"],
    body.tax-product_cat .pd-shop-search button[type="submit"],
    body.woocommerce-shop .pd-shop-search button[type="submit"],
    body.post-type-archive-product .pd-shop-search button[type="submit"] {
      width: 52px !important;
      height: 44px !important;
      min-width: 52px !important;
      padding: 0 !important;
      border: 0 !important;
      border-radius: 25px !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      background: #000000 !important;
      color: #ffffff !important;
      box-shadow: none !important;
    }

    body.page-id-547 .pd-shop-search button[type="submit"] svg,
    body.tax-product_cat .pd-shop-search button[type="submit"] svg,
    body.woocommerce-shop .pd-shop-search button[type="submit"] svg,
    body.post-type-archive-product .pd-shop-search button[type="submit"] svg {
      width: 15px !important;
      height: 15px !important;
      stroke: currentColor !important;
    }

    body.page-id-547 .woo-listing-top .woocommerce-ordering,
    body.tax-product_cat .woo-listing-top .woocommerce-ordering,
    body.woocommerce-shop .woo-listing-top .woocommerce-ordering,
    body.post-type-archive-product .woo-listing-top .woocommerce-ordering {
      grid-area: order !important;
      justify-self: end !important;
      margin: 0 !important;
      width: 240px !important;
      position: relative !important;
      display: flex !important;
      align-items: center !important;
    }

    /* Orden por defecto: seleccionado y opciones centradas */
    body.page-id-547 .woocommerce-ordering select.orderby,
    body.tax-product_cat .woocommerce-ordering select.orderby,
    body.woocommerce-shop .woocommerce-ordering select.orderby,
    body.post-type-archive-product .woocommerce-ordering select.orderby {
      width: 100% !important;
      height: 44px !important;
      border: 0 !important;
      border-radius: 25px !important;
      background-color: #000000 !important;
      color: #ffffff !important;
      font-family: 'Roboto Serif', serif !important;
      font-size: 12px !important;
      font-weight: 700 !important;
      letter-spacing: .6px !important;
      text-transform: uppercase !important;
      text-align: center !important;
      text-align-last: center !important;
      -moz-text-align-last: center !important;
      appearance: none !important;
      -webkit-appearance: none !important;
      -moz-appearance: none !important;
      padding: 0 42px !important;
      line-height: 44px !important;
      cursor: pointer !important;
      box-shadow: none !important;
    }

    body.page-id-547 .woocommerce-ordering select.orderby option,
    body.tax-product_cat .woocommerce-ordering select.orderby option,
    body.woocommerce-shop .woocommerce-ordering select.orderby option,
    body.post-type-archive-product .woocommerce-ordering select.orderby option {
      background: #ffffff !important;
      color: #000000 !important;
      font-family: 'Roboto Serif', serif !important;
      font-size: 13px !important;
      font-weight: 500 !important;
      text-align: center !important;
      text-align-last: center !important;
      padding: 10px 0 !important;
    }

    body.page-id-547 .woocommerce-ordering::after,
    body.tax-product_cat .woocommerce-ordering::after,
    body.woocommerce-shop .woocommerce-ordering::after,
    body.post-type-archive-product .woocommerce-ordering::after {
      content: "" !important;
      position: absolute !important;
      right: 18px !important;
      top: 50% !important;
      width: 6px !important;
      height: 6px !important;
      border-right: 1.5px solid #ffffff !important;
      border-bottom: 1.5px solid #ffffff !important;
      transform: translateY(-65%) rotate(45deg) !important;
      pointer-events: none !important;
      z-index: 3 !important;
    }

    body.page-id-547 .woocommerce-ordering .ct-sort-icon,
    body.tax-product_cat .woocommerce-ordering .ct-sort-icon,
    body.woocommerce-shop .woocommerce-ordering .ct-sort-icon,
    body.post-type-archive-product .woocommerce-ordering .ct-sort-icon {
      display: none !important;
    }

    @media (max-width: 768px) {
      body.page-id-547 .woo-listing-top,
      body.tax-product_cat .woo-listing-top,
      body.woocommerce-shop .woo-listing-top,
      body.post-type-archive-product .woo-listing-top {
        grid-template-columns: 1fr !important;
        grid-template-areas:
          "search"
          "count"
          "order" !important;
        gap: 14px !important;
      }

      body.page-id-547 .woo-listing-top .woocommerce-result-count,
      body.tax-product_cat .woo-listing-top .woocommerce-result-count,
      body.woocommerce-shop .woo-listing-top .woocommerce-result-count,
      body.post-type-archive-product .woo-listing-top .woocommerce-result-count,
      body.page-id-547 .woo-listing-top .woocommerce-ordering,
      body.tax-product_cat .woo-listing-top .woocommerce-ordering,
      body.woocommerce-shop .woo-listing-top .woocommerce-ordering,
      body.post-type-archive-product .woo-listing-top .woocommerce-ordering {
        justify-self: center !important;
      }
    }

    /* Carrito vacio */
    body.woocommerce-cart .entry-content > .woocommerce {
      max-width: 760px !important;
      margin: 40px auto 70px !important;
      padding: 0 18px !important;
      text-align: center !important;
    }

    body.woocommerce-cart .wc-empty-cart-message {
      margin: 0 !important;
    }

    body.woocommerce-cart .cart-empty.woocommerce-info {
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      min-height: 210px !important;
      padding: 38px 24px !important;
      margin: 0 0 22px !important;
      border: 1px solid rgba(0,0,0,.08) !important;
      border-radius: 18px !important;
      background: #ffffff !important;
      box-shadow: 0 18px 50px rgba(0,0,0,.06) !important;
      color: #111111 !important;
      font-family: 'Roboto Serif', serif !important;
      font-size: clamp(22px, 3vw, 34px) !important;
      font-weight: 700 !important;
      line-height: 1.2 !important;
    }

    body.woocommerce-cart .cart-empty.woocommerce-info::before {
      display: none !important;
    }

    body.woocommerce-cart p.return-to-shop {
      margin: 0 !important;
      text-align: center !important;
    }

    body.woocommerce-cart p.return-to-shop a.button.wc-backward {
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      min-width: 190px !important;
      height: 46px !important;
      padding: 0 28px !important;
      border: 1px solid #000000 !important;
      border-radius: 25px !important;
      background: #000000 !important;
      color: #ffffff !important;
      font-family: 'Roboto Serif', serif !important;
      font-size: 12px !important;
      font-weight: 700 !important;
      letter-spacing: 1px !important;
      text-transform: uppercase !important;
      text-decoration: none !important;
    }

    body.woocommerce-cart p.return-to-shop a.button.wc-backward:hover {
      background: #333333 !important;
      border-color: #333333 !important;
      color: #ffffff !important;
    }
    </style>
    <?php
}, 9999);
/* PRIME_DROP_CATEGORY_SEARCH_CART_EMPTY_FIXES_END */

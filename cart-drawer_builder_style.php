<?php
if (!defined('ABSPATH')) {
	exit;
}

if (!function_exists('WC') || !WC()->cart) {
	return;
}
?>
<div class="pd-cart-drawer cart-drawer" aria-hidden="true" id="cart-drawer">
  <div class="pd-cart-drawer-header cart-drawer-header">
    <h3>Carrito de compra</h3>
    <button class="pd-cart-drawer-close cart-drawer-close" type="button" aria-label="Cerrar carrito">&times;</button>
  </div>

  <div class="pd-cart-drawer-items cart-drawer-items">
    <?php if (WC()->cart->is_empty()) : ?>
      <p class="pd-cart-empty">El carrito de compras está vacío</p>
    <?php else : ?>
      <?php foreach (WC()->cart->get_cart() as $cart_item_key => $cart_item) :
        $product = isset($cart_item['data']) ? $cart_item['data'] : null;
        if (!$product || !$product->exists()) {
          continue;
        }

        $product_id = $cart_item['product_id'];
        $thumbnail = get_the_post_thumbnail_url($product_id, 'thumbnail');
        $name = $product->get_name();
        $attributes = array();

        if (!empty($cart_item['variation']) && is_array($cart_item['variation'])) {
          foreach ($cart_item['variation'] as $attribute_name => $attribute_value) {
            if (!$attribute_value) {
              continue;
            }
            $attributes[] = wc_attribute_label(str_replace('attribute_', '', $attribute_name)) . ': ' . $attribute_value;
          }
        }

        $quantity = max(1, absint($cart_item['quantity']));
        $remove_url = wc_get_cart_remove_url($cart_item_key);
        ?>
        <div class="pd-cart-item">
          <a class="pd-cart-item-thumb" href="<?php echo esc_url($product->get_permalink()); ?>">
            <img src="<?php echo esc_url($thumbnail ?: wc_placeholder_img_src()); ?>" alt="<?php echo esc_attr($name); ?>">
          </a>

          <div class="pd-cart-item-info">
            <a class="pd-cart-item-name" href="<?php echo esc_url($product->get_permalink()); ?>"><?php echo esc_html($name); ?></a>
            <?php if (!empty($attributes)) : ?>
              <p class="pd-cart-item-meta"><?php echo esc_html(implode(' / ', $attributes)); ?></p>
            <?php endif; ?>

            <div class="pd-cart-item-bottom">
              <div class="pd-cart-qty" aria-label="Cantidad">
                <button type="button" class="pd-cart-qty-btn" data-key="<?php echo esc_attr($cart_item_key); ?>" data-qty="<?php echo esc_attr(max(0, $quantity - 1)); ?>">-</button>
                <span><?php echo esc_html($quantity); ?></span>
                <button type="button" class="pd-cart-qty-btn" data-key="<?php echo esc_attr($cart_item_key); ?>" data-qty="<?php echo esc_attr($quantity + 1); ?>">+</button>
              </div>
              <div class="pd-cart-item-price"><?php echo wp_kses_post(WC()->cart->get_product_subtotal($product, $quantity)); ?></div>
            </div>
          </div>

          <a href="<?php echo esc_url($remove_url); ?>" class="pd-cart-item-remove" data-key="<?php echo esc_attr($cart_item_key); ?>" aria-label="<?php echo esc_attr('Eliminar ' . $name); ?>">
            <svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none">
              <path d="M4 7h16M10 11v6M14 11v6M6 7l1 14h10l1-14M9 7V4h6v3" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </a>
        </div>
      <?php endforeach; ?>
    <?php endif; ?>
  </div>

  <div class="pd-cart-drawer-footer cart-drawer-footer">
    <div class="pd-cart-subtotal">
      <span>Subtotal:</span>
      <span><?php echo wp_kses_post(WC()->cart->get_cart_subtotal()); ?></span>
    </div>
    <p class="pd-cart-shipping-note">El envío se calcula al finalizar la compra</p>
    <a href="<?php echo esc_url(wc_get_checkout_url()); ?>" class="pd-btn pd-btn-dark pd-cart-checkout">Comprar</a>
    <div class="pd-cart-secure">
      <svg aria-hidden="true" width="13" height="13" viewBox="0 0 24 24" fill="none">
        <path d="M7 10V7a5 5 0 0 1 10 0v3M6 10h12v10H6V10Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      <span>Pago seguro</span>
    </div>
  </div>
</div>

document.addEventListener('DOMContentLoaded', function () {
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach((toast) => {
        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 500);
        }, 4000);
    });

    const changeAddressButton = document.querySelector('[data-change-address]');
    const addressFields = document.querySelector('[data-address-fields]');
    const savedAddress = document.querySelector('[data-saved-address]');
    if (changeAddressButton && addressFields && savedAddress) {
        changeAddressButton.addEventListener('click', function () {
            savedAddress.classList.add('is-hidden');
            addressFields.classList.remove('is-hidden');
        });
    }

    const cartItems = [...document.querySelectorAll('.cart-item')];
    const updateCartTotal = function () {
        let total = 0;
        cartItems.forEach(function (item) {
            const input = item.querySelector('[data-quantity-input]');
            const subtotal = item.querySelector('[data-item-subtotal]');
            if (!input || !subtotal) return;
            const quantity = Math.max(1, Number.parseInt(input.value, 10) || 1);
            const price = Number.parseInt(subtotal.dataset.price, 10) || 0;
            subtotal.textContent = `₹${price * quantity}`;
            total += price * quantity;
        });
        const totalElement = document.querySelector('[data-cart-total]');
        if (totalElement) totalElement.textContent = `₹${total}`;
    };
    cartItems.forEach(function (item) {
        const input = item.querySelector('[data-quantity-input]');
        item.querySelectorAll('[data-quantity-step]').forEach(function (button) {
            button.addEventListener('click', function () {
                const next = Math.max(1, (Number.parseInt(input.value, 10) || 1) + Number(button.dataset.quantityStep));
                input.value = Math.min(Number(input.max) || next, next);
                updateCartTotal();
            });
        });
        if (input) input.addEventListener('input', updateCartTotal);
    });
    if (cartItems.length) updateCartTotal();
});

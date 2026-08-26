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

    const chatAssistant = document.querySelector('[data-chat-assistant]');
    if (chatAssistant) {
        const chatWindow = chatAssistant.querySelector('[data-chat-window]');
        const chatToggleButtons = chatAssistant.querySelectorAll('[data-chat-toggle]');
        const chatForm = chatAssistant.querySelector('[data-chat-form]');
        const chatInput = chatAssistant.querySelector('[data-chat-input]');
        const chatMessages = chatAssistant.querySelector('[data-chat-messages]');

        const addChatMessage = function (text, type) {
            const message = document.createElement('div');
            message.className = `chat-message chat-message-${type}`;
            message.textContent = text;
            chatMessages.appendChild(message);
            chatMessages.scrollTop = chatMessages.scrollHeight;
            return message;
        };

        chatToggleButtons.forEach(function (button) {
            button.addEventListener('click', function () {
                const isOpening = chatWindow.hidden;
                chatWindow.hidden = !isOpening;
                chatToggleButtons.forEach((toggle) => toggle.setAttribute('aria-expanded', String(isOpening)));
                if (isOpening) chatInput.focus();
            });
        });

        chatForm.addEventListener('submit', async function (event) {
            event.preventDefault();
            const message = chatInput.value.trim();
            if (!message) return;
            addChatMessage(message, 'user');
            chatInput.value = '';
            chatInput.disabled = true;
            const pending = addChatMessage('Thinking...', 'assistant');
            try {
                const response = await fetch('/api/assistant', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message }),
                });
                if (!response.ok) throw new Error('Assistant request failed');
                const data = await response.json();
                pending.textContent = data.reply || 'I could not find an answer for that yet.';
            } catch (error) {
                pending.textContent = 'I am unable to connect right now. Please try again or visit the menu.';
            } finally {
                chatInput.disabled = false;
                chatInput.focus();
            }
        });
    }
});

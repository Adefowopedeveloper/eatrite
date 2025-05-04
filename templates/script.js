{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Cart - Eatrite</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body style="background-color: rgb(238, 213, 73);">

<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
        <a class="navbar-brand" href="{% url 'home' %}">
            <img src="{% static 'eatritelogo.webp' %}" alt="Logo" height="70" width="70">
            EATRITE – Where Flavor Meets Freshness!
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto">
                <li class="nav-item"><a class="nav-link" href="{% url 'home' %}">Home</a></li>
                <li class="nav-item"><a class="nav-link" href="{% url 'menu' %}">Menu</a></li>
                <li class="nav-item"><a class="nav-link active" href="{% url 'cart' %}">Cart</a></li>
                <li class="nav-item"><a class="nav-link" href="{% url 'about' %}">About Us</a></li>
            </ul>
        </div>
    </div>
</nav>

<section id="cart" class="container mt-5">
    <h2>Your Cart</h2>
    <div id="cart-items"></div>
    <div id="cart-total" class="mt-3"></div>
    <div class="d-flex justify-content-between mt-4">
        <button class="btn btn-secondary" onclick="goBackToMenu()">Back to Menu</button>
        <button class="btn btn-danger" onclick="clearCart()">Clear Cart</button>
    </div>
</section>

<footer class="bg-dark text-white text-center py-3 mt-5">
    <p>&copy; 2024 Eatrite Restaurant. All rights reserved.</p>
</footer>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>

<script>
    let cart = [];
    const cartItemsContainer = document.getElementById("cart-items");
    const cartTotal = document.getElementById("cart-total");

    function addToCart(name, price) {
        const parsedPrice = parseFloat(price);
        if (!name || isNaN(parsedPrice)) return;
        cart.push({ name, price: parsedPrice });
        localStorage.setItem("cart", JSON.stringify(cart));
        updateCart();
    }

    function updateCart() {
        cart = JSON.parse(localStorage.getItem("cart")) || [];
        if (!cartItemsContainer || !cartTotal) return;

        cartItemsContainer.innerHTML = "";
        let total = 0;
        const grouped = {};

        cart.forEach(({ name, price }) => {
            if (grouped[name]) {
                grouped[name].quantity += 1;
            } else {
                grouped[name] = { price: parseFloat(price), quantity: 1 };
            }
        });

        for (const [name, item] of Object.entries(grouped)) {
            total += item.price * item.quantity;
            const div = document.createElement("div");
            div.className = "card mb-2";
            div.innerHTML = `
                <div class="card-body d-flex justify-content-between align-items-center">
                    <strong>${name}</strong>
                    <span>Qty: ${item.quantity}</span>
                    <span>$${(item.price * item.quantity).toFixed(2)}</span>
                </div>
            `;
            cartItemsContainer.appendChild(div);
        }

        cartTotal.innerHTML = `<h4>Total: $${total.toFixed(2)}</h4>`;
    }

    function clearCart() {
        localStorage.removeItem('cart');
        cart = [];
        updateCart();
    }

    function goBackToMenu() {
        window.location.href = "{% url 'menu' %}";
    }
    function placeOrder() {
        const name = document.getElementById('name').value.trim();
        const email = document.getElementById('email').value.trim();
        const address = document.getElementById('address').value.trim();
        const phone = document.getElementById('phone').value.trim();
        const payment = document.getElementById('payment-method').value;
        const note = document.getElementById('note').value.trim();
        const btn = document.getElementById("submit-btn");
    
        if (!name || !email || !address || !phone || !payment) {
            alert("Please fill all required fields and select a payment method.");
            return;
        }
    
        const cart = JSON.parse(localStorage.getItem("cart")) || [];
    
        // Disable button to prevent multiple clicks
        btn.disabled = true;
        btn.textContent = "Placing Order...";
    
        fetch("/submit_order/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken") // if using CSRF
            },
            body: JSON.stringify({
                name,
                email,
                address,
                phone,
                payment_method: payment,
                note,
                cart
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                localStorage.removeItem('cart');
                document.getElementById('checkout').classList.add('d-none');
                const thankYou = document.getElementById('thank-you');
                if (thankYou) thankYou.classList.remove('d-none');
                setTimeout(() => window.location.href = "{% url 'menu' %}", 3000);
            } else {
                alert("Something went wrong.");
            }
        })
        .catch(err => {
            console.error("Order error:", err);
            alert("Error placing order.");
        });
    }
    
    // CSRF helper (only if CSRF is enforced)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
</script>

</body>
</html>

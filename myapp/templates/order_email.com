Hi {{ order.full_name }},

Thank you for shopping with The BikeStore!

Your order (ID: {{ order.id }}) has been successfully placed.

Order Summary:
{% for item in order.items.all %}
- {{ item.product_name }} (x{{ item.quantity }}) - ₹{{ item.price|floatformat:2 }}
{% endfor %}

<h2>✅ Order Placed Successfully!</h2>
<p>Thank you for your purchase. A confirmation email has been sent.</p>
<p><strong>Order ID:</strong> {{ order.id }}</p>
<p><a href="{% url 'home' %}">Back to Home</a></p>


from fooddelivery.models import MenuItem
from fooddelivery.orders import CourierApp, CustomerNotifier, Order, OrderStatus, RestaurantDashboard
from fooddelivery.payments import PayPalAdapter, StripeAdapter
from fooddelivery.service import CheckoutService


def demo(processor, token, distance, express=False):
    order = Order("Aigerim", [MenuItem("Beshbarmak", 9.50), MenuItem("Kumis", 2.00)])
    customer, restaurant, courier = CustomerNotifier(), RestaurantDashboard(), CourierApp()
    for observer in (customer, restaurant, courier):
        order.attach(observer)

    CheckoutService(processor).checkout(order, token, distance, express)
    order.advance_to(OrderStatus.PREPARING)
    order.advance_to(OrderStatus.OUT_FOR_DELIVERY)
    order.advance_to(OrderStatus.DELIVERED)

    print(f"Order #{order.id}: total {order.total} + delivery {order.delivery_plan.fee} "
          f"via {order.delivery_plan.method} (ETA {order.delivery_plan.eta_minutes} min), "
          f"paid with {order.payment.provider} [{order.payment.transaction_id}]")
    print(*customer.messages, sep="\n")
    print(*courier.tasks, sep="\n")
    print("Restaurant active orders:", restaurant.active_orders or "none", "\n")


if __name__ == "__main__":
    demo(StripeAdapter(), "tok_visa_4242", distance=2.0)
    demo(PayPalAdapter(), "aigerim@example.com", distance=8.0, express=True)

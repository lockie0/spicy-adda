from app import db
from app.models import Order, OrderDetail


def create_order(user_id, total, shipping_address, status='Processing'):
    return Order(
        user_id=user_id,
        total=total,
        shipping_address=shipping_address,
        status=status,
    )


def save_order(order, items):
    db.session.add(order)
    db.session.flush()
    for item in items:
        db.session.add(OrderDetail(
            order_id=order.id,
            product_id=item.product.id,
            quantity=item.quantity,
            price=item.product.price,
        ))
        item.product.stock -= item.quantity
        db.session.delete(item)
    db.session.commit()
    return order

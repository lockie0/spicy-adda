from datetime import date

from app.models import Order
from app.utils import get_company_from_email


def get_orders():
    return Order.query.order_by(Order.created_at.desc()).all()


def get_user_orders(user_id):
    return Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()


def filter_orders_by_company(orders, company):
    return [
        order for order in orders
        if (order.user.company or get_company_from_email(order.user.email)) == company
    ]


def get_company_orders(company):
    return filter_orders_by_company(get_orders(), company)


def get_today_orders(orders):
    today = date.today()
    return [
        order for order in orders
        if order.status == 'Completed' and order.created_at.date() == today
    ]


def calculate_today_order_count(orders):
    return len(get_today_orders(orders))


def calculate_today_revenue(orders):
    return sum(order.total for order in get_today_orders(orders))

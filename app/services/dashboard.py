from datetime import date

from sqlalchemy.orm import joinedload, selectinload

from app.models import Order, OrderDetail
from app.utils import get_company_from_email


def get_orders():
    return Order.query.options(
        joinedload(Order.user),
        selectinload(Order.details).joinedload(OrderDetail.product),
    ).order_by(Order.created_at.desc()).all()


def get_user_orders(user_id):
    return Order.query.filter_by(user_id=user_id).options(
        joinedload(Order.user),
        selectinload(Order.details).joinedload(OrderDetail.product),
    ).order_by(Order.created_at.desc()).all()


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


def get_today_metrics(orders):
    today_orders = get_today_orders(orders)
    return len(today_orders), sum(order.total for order in today_orders)


def calculate_today_order_count(orders):
    return get_today_metrics(orders)[0]


def calculate_today_revenue(orders):
    return get_today_metrics(orders)[1]

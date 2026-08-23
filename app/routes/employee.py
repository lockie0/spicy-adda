from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_required

from app.services.dashboard import (
    calculate_today_order_count,
    calculate_today_revenue,
    filter_orders_by_company,
    get_user_orders,
    get_orders,
)
from app.utils import COMPANY_DOMAINS

employee_bp = Blueprint('employee', __name__, url_prefix='/employee')


@employee_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        return redirect(url_for('admin.dashboard'))

    tab = request.args.get('tab', 'home')
    companies = list(COMPANY_DOMAINS.values())
    selected_company = request.args.get('company', current_user.company or companies[0])
    if selected_company not in companies:
        selected_company = companies[0]

    all_orders = get_orders()
    company_orders = filter_orders_by_company(all_orders, selected_company)
    return render_template(
        'employee_dashboard.html',
        tab=tab,
        companies=companies,
        selected_company=selected_company,
        my_orders=get_user_orders(current_user.id),
        company_orders=company_orders,
        today_order_count=calculate_today_order_count(company_orders),
        today_revenue=calculate_today_revenue(company_orders),
    )

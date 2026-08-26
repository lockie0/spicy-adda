def has_saved_address(user):
    return all([
        user.address_full_name,
        user.address_mobile,
        user.address_house,
        user.address_street,
        user.address_city,
        user.address_state,
        user.address_pincode,
    ])


def save_user_address(user, form):
    user.address_full_name = form.full_name.data.strip()
    user.address_mobile = form.mobile.data.strip()
    user.address_house = form.house_number.data.strip()
    user.address_street = form.street.data.strip()
    user.address_city = form.city.data.strip()
    user.address_state = form.state.data.strip()
    user.address_pincode = form.pincode.data.strip()


def load_address_form(user, form):
    if has_saved_address(user):
        form.full_name.data = user.address_full_name
        form.mobile.data = user.address_mobile
        form.house_number.data = user.address_house
        form.street.data = user.address_street
        form.city.data = user.address_city
        form.state.data = user.address_state
        form.pincode.data = user.address_pincode


def format_user_address(user):
    if not has_saved_address(user):
        return ''
    return f'{user.address_full_name}, {user.address_house}, {user.address_street}, {user.address_city}, {user.address_state} - {user.address_pincode}, Mobile: {user.address_mobile}'
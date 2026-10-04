CUSTOMER_STOCK_CAP = 5


def customer_visible_stock(quantity):
    """Show leftover count only when 1–5 remain. Plenty of stock is hidden."""
    try:
        n = int(quantity or 0)
    except (TypeError, ValueError):
        return 0
    if n <= 0:
        return 0
    if n > CUSTOMER_STOCK_CAP:
        return None
    return n

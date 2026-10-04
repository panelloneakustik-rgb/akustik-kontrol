CUSTOMER_STOCK_CAP = 5


def customer_visible_stock(quantity):
    """Shoppers only see leftover scarcity, never the warehouse count."""
    try:
        n = int(quantity or 0)
    except (TypeError, ValueError):
        return 0
    if n <= 0:
        return 0
    return min(n, CUSTOMER_STOCK_CAP)

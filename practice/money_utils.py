def format_rupees(amount_paise):
    """Convert integer paise to a display string like Rs. 180.50."""
    return f"Rs. {amount_paise / 100:.2f}"


def rupees_to_paise(amount_rupees):
    """Convert rupees (int, float or str) to integer paise."""
    return round(float(amount_rupees) * 100)
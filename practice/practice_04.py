from money_utils import format_rupees, rupees_to_paise

paise = rupees_to_paise("180.50")
print(paise)
print(format_rupees(paise))
def safe_amount(text):
    """Return paise as int, or None if the input is invalid."""
    try:
        value = rupees_to_paise(text)
    except ValueError:
        return None
    if value <= 0:
        return None
    return value


print(safe_amount("250"))
print(safe_amount("abc"))
print(safe_amount("-50"))
import re

RATES = {"DOM": 3, "COM": 6}
SLAB = {"A": 1, "B": 2}

# Strict ASCII non-negative integer (rejects "", "-5", "1_0", "²", " ", "1.5")
_INT_RE = re.compile(r"[0-9]+")


def _to_int(text):
    """Return int for a string of ASCII digits (surrounding spaces allowed), else None."""
    if not isinstance(text, str):
        return None
    text = text.strip()
    if not _INT_RE.fullmatch(text):
        return None
    return int(text)


def units_consumed(reading):
    """'previous:current' -> units used, or None if the input is invalid."""
    if not isinstance(reading, str):
        return None
    parts = reading.split(':')
    if len(parts) != 2:
        return None
    previous, current = _to_int(parts[0]), _to_int(parts[1])
    if previous is None or current is None:
        return None
    if current < previous:          # meter cannot run backwards
        return None
    return current - previous


def daily_average(units_csv):
    """'5,7,6' -> average rounded to 2 dp, or None if the input is invalid."""
    if not isinstance(units_csv, str):
        return None
    units = [_to_int(u) for u in units_csv.split(',')]
    if not units or any(u is None for u in units):   # empty / bad element
        return None
    return round(sum(units) / len(units), 2)


def tariff_rate(code):
    """'DOM-A' -> rate per unit, or None if the code is invalid."""
    if not isinstance(code, str):
        return None
    parts = code.strip().split('-')
    if len(parts) != 2:
        return None
    category, slab = parts[0].strip().upper(), parts[1].strip().upper()
    if category not in RATES or slab not in SLAB:
        return None
    return RATES[category] * SLAB[slab]


def main():
    print("==== Running units_consumed ====")
    user_input = input("Enter meter readings as previous:current (e.g. 1200:1350): ")
    result = units_consumed(user_input)
    print("Units Consumed:", result if result is not None else "Invalid input")

    print("\n==== Running daily_average ====")
    user_input = input("Enter daily units as CSV (e.g. 5,7,6): ")
    result = daily_average(user_input)
    print("Daily Average:", result if result is not None else "Invalid input")

    print("\n==== Running tariff_rate ====")
    user_input = input("Enter a tariff code (e.g. DOM-A): ")
    result = tariff_rate(user_input)
    print("Rate per Unit:", result if result is not None else "Invalid input")


if __name__ == "__main__":
    main()
RATES = {"DOM": 3, "COM": 6}
SLAB = {"A": 1, "B": 2}

def units_consumed(reading):
    previous, current = reading.split(':')
    return int(current) - int(previous)

def daily_average(units_csv):
    units = [int(u) for u in units_csv.split(',')]
    return round(sum(units) / len(units), 2)

def tariff_rate(code):
    category, slab = code.split('-')
    return RATES[category.upper()] * SLAB[slab.upper()]

def main():
    print("==== Running units_consumed ====")
    user_input = input("Enter meter readings as previous:current (e.g. 1200:1350): ")
    result = units_consumed(user_input)
    print("Units Consumed:", result)

    print("\n==== Running daily_average ====")
    user_input = input("Enter daily units as CSV (e.g. 5,7,6): ")
    result = daily_average(user_input)
    print("Daily Average:", result)

    print("\n==== Running tariff_rate ====")
    user_input = input("Enter a tariff code (e.g. DOM-A): ")
    result = tariff_rate(user_input)
    print("Rate per Unit:", result)

if __name__ == "__main__":
    main()

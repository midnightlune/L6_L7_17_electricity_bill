from hypothesis import given, strategies as st
from electricity_bill import units_consumed, daily_average, tariff_rate


@given(st.text() | st.none())
def test_units_consumed_no_crash(s):
    try:
        units_consumed(s)
    except Exception as e:
        assert False, f"units_consumed crashed with: {e!r}"


@given(st.text() | st.none())
def test_daily_average_no_crash(s):
    try:
        daily_average(s)
    except Exception as e:
        assert False, f"daily_average crashed with: {e!r}"


@given(st.text() | st.none())
def test_tariff_rate_no_crash(s):
    try:
        tariff_rate(s)
    except Exception as e:
        assert False, f"tariff_rate crashed with: {e!r}"


# ---- Extra property tests: correct behaviour on valid input ----

@given(st.integers(0, 10**6), st.integers(0, 10**6))
def test_units_consumed_valid(a, b):
    lo, hi = sorted((a, b))
    assert units_consumed(f"{lo}:{hi}") == hi - lo


@given(st.lists(st.integers(0, 10**5), min_size=1))
def test_daily_average_valid(nums):
    res = daily_average(",".join(map(str, nums)))
    assert res == round(sum(nums) / len(nums), 2)


@given(st.sampled_from(["DOM", "COM"]), st.sampled_from(["A", "B"]),
       st.booleans())
def test_tariff_rate_valid(cat, slab, lower):
    code = f"{cat}-{slab}"
    expected = {"DOM": 3, "COM": 6}[cat] * {"A": 1, "B": 2}[slab]
    assert tariff_rate(code.lower() if lower else code) == expected
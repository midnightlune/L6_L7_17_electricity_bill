from hypothesis import given, strategies as st
from electricity_bill import units_consumed, daily_average, tariff_rate

@given(st.text() | st.none())
def test_units_consumed_no_crash(s):

@given(st.text() | st.none())
def test_daily_average_no_crash(s):

@given(st.text() | st.none())
def test_tariff_rate_no_crash(s):

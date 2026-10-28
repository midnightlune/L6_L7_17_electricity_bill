import pytest
from electricity_bill import energy_charge, late_fee, subsidy


#energy_charge: every branch 
def test_low_usage_domestic():
    assert energy_charge(50, "domestic") == 200            # slab 1, not commercial

def test_slab1_boundary_100():
    assert energy_charge(100, "domestic") == 350           # 300 + 50

def test_slab2_boundary_101():
    assert energy_charge(101, "domestic") == 355           # 300 + 5 + 50

def test_slab2_boundary_300():
    assert energy_charge(300, "domestic") == 1350          # 300 + 1000 + 50

def test_slab3_boundary_301():
    assert energy_charge(301, "domestic") == 1358          # 1300 + 8 + 50

def test_high_usage_domestic():
    assert energy_charge(400, "domestic") == 2150

def test_zero_units():
    assert energy_charge(0, "domestic") == 50

def test_commercial_true_branch():
    assert energy_charge(50, "commercial") == 450

def test_commercial_high_usage():
    assert energy_charge(400, "commercial") == 4350        # (1300+800)*2 + 150

def test_unknown_connection():
    with pytest.raises(ValueError, match="unknown connection"):
        energy_charge(50, "industrial")

def test_negative_units():
    with pytest.raises(ValueError, match="invalid units"):
        energy_charge(-1, "domestic")

def test_unknown_connection_checked_before_units():
    with pytest.raises(ValueError, match="unknown connection"):
        energy_charge(-1, "industrial")


#  late_fee: every branch 
def test_paid_on_time():
    assert late_fee(500, 0) == 0

def test_negative_days_late():
    assert late_fee(500, -3) == 0

def test_late_1_day():
    assert late_fee(500, 1) == 50

def test_late_boundary_15():
    assert late_fee(5000, 15) == 50

def test_late_16_small_bill():
    assert late_fee(1000, 16) == 100                       # bill <= 2000

def test_late_16_bill_exactly_2000():
    assert late_fee(2000, 16) == 100                       # boundary: not > 2000

def test_late_16_big_bill():
    assert late_fee(2001, 16) == 100 + 2001 // 20          # 200

def test_late_big_bill_large():
    assert late_fee(4000, 30) == 300


#  subsidy: every branch 
def test_no_subsidy_high_units_not_senior():
    assert subsidy(200, False, False) == 0

def test_low_units_not_senior():
    assert subsidy(50, False, False) == 0                  # units<=100 True, senior False

def test_high_units_senior():
    assert subsidy(150, True, False) == 0                  # units<=100 False (short-circuit)

def test_senior_low_units():
    assert subsidy(50, True, False) == 50

def test_senior_boundary_100():
    assert subsidy(100, True, False) == 50

def test_solar_only():
    assert subsidy(200, False, True) == 100

def test_senior_and_solar_low_units():
    assert subsidy(50, True, True) == 150

def test_solar_boundary_300():
    assert subsidy(300, False, True) == 100                # not > 300

def test_solar_over_300_cancels():
    assert subsidy(301, False, True) == 0

def test_senior_solar_high_units():
    assert subsidy(400, True, True) == 0
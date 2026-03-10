# Service charge apportionment calculator.
#
# Formula:
#   unit_share  = unit_floor_area / total_floor_area  (or lease-defined ratio)
#   unit_charge = total_expenditure * unit_share
#
# All monetary values in pence (integers). Round to 2 dp; reconcile penny
# rounding on the largest unit so the sum always equals total_expenditure.

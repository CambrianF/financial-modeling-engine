# assumptions.py

class ModelAssumptions:
    def __init__(self):
        self.revenue_growth_rate = 0.10
        self.cogs_pct_revenue = 0.40
        self.salaries_pct_revenue = 0.20
        self.rent_and_overhead = 15000
        self.tax_rate = 0.21
        self.days_in_period = 365
        self.ar_days = 45
        self.inventory_days = 65
        self.ap_days = 30
        self.capex = 20.0
        self.depreciation_rate = 0.10
        self.interest_rate = 0.06
        self.debt_issuance = 0
        self.equity_issuance = 0
        self.dividend_payout_ratio = 0.20

BASE_ASSUMPTIONS = {
    'interest_rate': 0.06,
    'tax_rate': 0.21,
    'dda': 15.0,
    'capex': 20.0,
    'dividends': 5.0
}

PRIOR_BALANCE_SHEET = {
    'cash': 50.0,
    'debt': 100.0,
    'ppe': 300.0,
    'accounts_receivable': 30.0,
    'inventory': 12.0,
    'accounts_payable': 14.4,
    'retained_earnings': 150.0,
    'common_stock': 127.6
}

INCOME_STATEMENT_INPUTS = {
    'revenue': 200.0,
    'opex': 120.0
}
# engine.py

class FinancialEngine:
    def __init__(self, income_statement, balance_sheet_current, balance_sheet_prior):
        self.is_data = income_statement
        self.bs_curr = balance_sheet_current
        self.bs_prior = balance_sheet_prior

    def calculate_operating_cash_flow(self, dda_expense, other_non_cash=0):
        net_income = self.is_data.get('net_income', 0)
        delta_ar = self.bs_prior.get('accounts_receivable', 0) - self.bs_curr.get('accounts_receivable', 0)
        delta_inventory = self.bs_prior.get('inventory', 0) - self.bs_curr.get('inventory', 0)
        delta_ap = self.bs_curr.get('accounts_payable', 0) - self.bs_prior.get('accounts_payable', 0)
        working_capital_change = delta_ar + delta_inventory + delta_ap
        cfo = net_income + dda_expense + other_non_cash + working_capital_change
        return cfo

    def calculate_investing_cash_flow(self, capex, acquisitions=0):
        cfi = -abs(capex) - abs(acquisitions)
        return cfi

    def calculate_financing_cash_flow(self, debt_issued=0, debt_repaid=0, equity_issued=0, dividends_paid=0):
        net_debt = debt_issued - debt_repaid
        net_equity = equity_issued - dividends_paid
        cff = net_debt + net_equity
        return cff

    def generate_cash_flow_statement(self, dda_expense, capex, debt_issued=0, debt_repaid=0, dividends_paid=0):
        cfo = self.calculate_operating_cash_flow(dda_expense)
        cfi = self.calculate_investing_cash_flow(capex)
        cff = self.calculate_financing_cash_flow(debt_issued, debt_repaid, 0, dividends_paid)
        net_change_in_cash = cfo + cfi + cff
        return {
            "Operating Cash Flow": cfo,
            "Investing Cash Flow": cfi,
            "Financing Cash Flow": cff,
            "Net Change in Cash": net_change_in_cash
        }


def calculate_debt_and_interest(beginning_debt, cash_before_revolver, minimum_cash=10.0, interest_rate=0.06):
    revolver_draw = 0
    revolver_paydown = 0
    ending_cash = cash_before_revolver
    if cash_before_revolver < minimum_cash:
        revolver_draw = minimum_cash - cash_before_revolver
        ending_cash = cash_before_revolver
    elif cash_before_revolver > minimum_cash:
        excess_cash = cash_before_revolver - minimum_cash
        revolver_paydown = min(excess_cash, beginning_debt)
        ending_cash = cash_before_revolver - revolver_paydown

    ending_debt = beginning_debt + revolver_draw - revolver_paydown
    average_debt = (beginning_debt + ending_debt) / 2
    interest_expense = average_debt * interest_rate
    return {
        "Ending Debt": ending_debt,
        "Interest Expense": interest_expense,
        "Revolver Draw": revolver_draw,
        "Revolver Paydown": revolver_paydown,
        "Ending Cash": ending_cash
    }


def run_forecast_period(prior_bs, is_data_inputs, assumptions):
    revenue = is_data_inputs['revenue']
    opex = is_data_inputs['opex']
    interest_rate = assumptions.get('interest_rate', 0.06)
    tax_rate = assumptions.get('tax_rate', 0.21)
    dda = assumptions.get('dda', 15.0)
    capex = assumptions.get('capex', 20.0)
    dividends = assumptions.get('dividends', 5.0)
    
    beginning_debt = prior_bs['debt']
    beginning_cash = prior_bs['cash']
    interest_expense = beginning_debt * interest_rate

    for _ in range(3):
        ebitda = revenue - opex
        ebit = ebitda - dda
        ebt = ebit - interest_expense
        taxes = ebt * tax_rate
        net_income = ebt - taxes
        
        is_dict = {'net_income': net_income}
        bs_prior = prior_bs
        bs_curr_stub = {
            'accounts_receivable': revenue * 0.15,
            'inventory': opex * 0.10,
            'accounts_payable': opex * 0.12
        }
        
        engine = FinancialEngine(is_dict, bs_curr_stub, bs_prior)
        cfo = engine.calculate_operating_cash_flow(dda)
        cfi = engine.calculate_investing_cash_flow(capex)
        
        cash_before_revolver = beginning_cash + cfo + cfi - dividends
        debt_results = calculate_debt_and_interest(beginning_debt, cash_before_revolver, minimum_cash=10.0, interest_rate=interest_rate)
        interest_expense = debt_results['Interest Expense']

    ending_cash = debt_results['Ending Cash']
    ending_debt = debt_results['Ending Debt']
    ending_ar = bs_curr_stub['accounts_receivable']
    ending_inv = bs_curr_stub['inventory']
    ending_ap = bs_curr_stub['accounts_payable']
    
    beginning_ppe = prior_bs['ppe']
    ending_ppe = beginning_ppe - dda + capex
    
    total_assets = ending_cash + ending_ar + ending_inv + ending_ppe
    ending_retained_earnings = prior_bs['retained_earnings'] + net_income - dividends
    shareholder_equity = prior_bs['common_stock'] + ending_retained_earnings
    total_liabilites_and_equity = ending_debt + ending_ap + shareholder_equity
    
    balance_discrepancy = total_assets - total_liabilites_and_equity
    is_balanced = abs(balance_discrepancy) < 0.01

    return {
        "Net Income": net_income,
        "Ending Cash": ending_cash,
        "Ending Debt": ending_debt,
        "Total Assets": total_assets,
        "Total Liab & Equity": total_liabilites_and_equity,
        "Is Balanced": is_balanced,
        "Discrepancy": balance_discrepancy
    }
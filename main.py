# main.py
from assumptions import PRIOR_BALANCE_SHEET, INCOME_STATEMENT_INPUTS, BASE_ASSUMPTIONS
from engine import run_forecast_period

def run_multi_year_forecast(initial_bs, initial_inputs, base_assumptions, years=5):
    current_bs = initial_bs.copy()
    forecast_history = []
    
    revenue = initial_inputs['revenue']
    opex = initial_inputs['opex']
    
    for year in range(1, years + 1):
        if year > 1:
            revenue *= 1.08
            opex *= 1.04
            
        is_inputs = {'revenue': revenue, 'opex': opex}
        results = run_forecast_period(current_bs, is_inputs, base_assumptions)
        results['Year'] = year
        results['Revenue'] = revenue
        forecast_history.append(results)
        
        current_bs = {
            'cash': results['Ending Cash'],
            'debt': results['Ending Debt'],
            'ppe': current_bs['ppe'] - base_assumptions['dda'] + base_assumptions['capex'],
            'retained_earnings': current_bs['retained_earnings'] + results['Net Income'] - base_assumptions['dividends'],
            'common_stock': current_bs['common_stock'],
            'accounts_payable': opex * 0.12,
            'inventory': opex * 0.10,
            'accounts_receivable': revenue * 0.15
        }
        
    return forecast_history

if __name__ == "__main__":
    forecast_results = run_multi_year_forecast(
        initial_bs=PRIOR_BALANCE_SHEET,
        initial_inputs=INCOME_STATEMENT_INPUTS,
        base_assumptions=BASE_ASSUMPTIONS,
        years=5
    )

    print("--- 5-YEAR ASSET FORECAST SCHEDULE ---")
    for res in forecast_results:
        print(f"\nYear {res['Year']}:")
        print(f"  Revenue:          ${res['Revenue']:.2f}")
        print(f"  Net Income:       ${res['Net Income']:.2f}")
        print(f"  Ending Cash:      ${res['Ending Cash']:.2f}")
        print(f"  Ending Debt:      ${res['Ending Debt']:.2f}")
        print(f"  Total Assets:     ${res['Total Assets']:.2f}")
        print(f"  Balance Check:    ${res['Is Balanced']} (Discrepancy: {res['Discrepancy']:.4f})")
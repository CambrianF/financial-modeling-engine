# Programmatic 3-Statement Financial Modeling Engine

A modular, object-oriented financial forecasting engine built in Python to automate multi-period 3-statement projections, circular debt/interest schedules, and balance sheet roll-forwards.

## Architecture & Features
* **Circularity Solver:** Implements an iterative 3-pass convergence loop to simultaneously resolve interest expense, debt balances, and cash flows.
* **Indirect Method Cash Flow Statement:** Dynamically calculates Operating, Investing, and Financing cash flows by tracking working capital deltas (AR, Inventory, AP) against multi-year balance sheet roll-forwards.
* **Modular Design:** Strictly separates parameters (`assumptions.py`), core engine logic (`engine.py`), and execution schedules (`main.py`) for plug-and-play valuation across different balance sheet baselines.
* **Invariants & Checks:** Enforces a strict balance sheet identity ($Assets = Liabilities + Equity$) across a multi-year projection horizon with zero-dollar terminal discrepancies.

## File Structure
```text
├── assumptions.py    # Baseline financial inputs, growth vectors, and tax/interest parameters
├── engine.py         # FinancialEngine class, circular debt solver, and cash flow logic
└── main.py           # Multi-year forecast loop and execution schedule
python main.py
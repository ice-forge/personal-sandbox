PRINCIPAL = 250  # current holdings
MONTHLY_MONEY_DEPOSIT = 250  # deposit
COMPOUND_FREQUENCY = 12  # monthly contributions
RATE_OF_RETURN = 0.08  # yearly rate of return
YEARS_SPENT_COMPOUNDING = 42  # years invested

DIVIDEND_YIELD = 0.00132  # annual dividend yield: automatically reinvests with REINVEST_DIVIDENDS parameter // 0.132% dividend annual rate
REINVEST_DIVIDENDS = True  # option to reinvest dividends anually

def calculate_compound_interest(principal, money_deposit, rate_of_return, year_span, compound_frequency):
    total_periods = compound_frequency * year_span
    interest_rate_per_period = rate_of_return / compound_frequency

    future_value = principal * (1 + (interest_rate_per_period)) ** total_periods
    future_value += money_deposit * (((1 + interest_rate_per_period) ** total_periods - 1) / interest_rate_per_period)

    return future_value

def reinvest_dividends(principal, money_deposit, rate_of_return, year_span, compound_frequency, dividend_yield):
    total_years = int(year_span)
    remaining_months = round((year_span - total_years) * 12)
    total_dividends = 0

    for year in range(total_years):
        principal = calculate_compound_interest(principal, money_deposit, rate_of_return, 1, compound_frequency)
        annual_dividend = principal * dividend_yield
        principal += annual_dividend  # reinvest dividend
        total_dividends += annual_dividend

    # calculate for remaining months
    interest_rate_per_period = rate_of_return / compound_frequency
    for month in range(remaining_months):
        principal *= (1 + interest_rate_per_period)
        monthly_dividend = principal * dividend_yield / 12
        principal += monthly_dividend  # reinvest dividend
        total_dividends += monthly_dividend

    return principal, total_dividends

if REINVEST_DIVIDENDS:
    future_value, total_dividends = reinvest_dividends(PRINCIPAL, MONTHLY_MONEY_DEPOSIT, RATE_OF_RETURN, YEARS_SPENT_COMPOUNDING, COMPOUND_FREQUENCY, DIVIDEND_YIELD)
else:
    future_value = calculate_compound_interest(PRINCIPAL, MONTHLY_MONEY_DEPOSIT, RATE_OF_RETURN, YEARS_SPENT_COMPOUNDING, COMPOUND_FREQUENCY)
    total_dividends = 0

print(f"Predicted Outcome: [{future_value:,.2f}].\nDividend Payouts: [{total_dividends:,.2f}].\n\tTotal: [{future_value + total_dividends:,.2f}]")
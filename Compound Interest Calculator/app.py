PRINCIPAL = 250  # current holdings
MONTHLY_MONEY_DEPOSIT = 250  # deposit
COMPOUND_FREQUENCY = 12  # monthly contributions
RATE_OF_RETURN = 0.12  # yearly rate of return
YEARS_SPENT_COMPOUNDING = 42  # years invested

DIVIDEND_YIELD = 0.00132  # annual dividend yield
REINVEST_DIVIDENDS = True  # option to reinvest dividends anually

GOAL = 28640800  # $28,640,800

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

def estimate_time_to_reach_goal(principal, money_deposit, rate_of_return, compound_frequency, goal, dividend_yield=0, parameter_reinvest_dividends=False):
    years = 0

    while principal < goal:
        if parameter_reinvest_dividends:
            principal, _ = reinvest_dividends(principal, money_deposit, rate_of_return, 1, compound_frequency, dividend_yield)
        else:
            principal = calculate_compound_interest(principal, money_deposit * compound_frequency, rate_of_return, 1, 1) # changed here
        years += 1
    return years

if REINVEST_DIVIDENDS:
    future_value, total_dividends = reinvest_dividends(PRINCIPAL, MONTHLY_MONEY_DEPOSIT, RATE_OF_RETURN, YEARS_SPENT_COMPOUNDING, COMPOUND_FREQUENCY, DIVIDEND_YIELD)
else:
    future_value = calculate_compound_interest(PRINCIPAL, MONTHLY_MONEY_DEPOSIT, RATE_OF_RETURN, YEARS_SPENT_COMPOUNDING, COMPOUND_FREQUENCY)
    total_dividends = 0

estimated_time = estimate_time_to_reach_goal(future_value, MONTHLY_MONEY_DEPOSIT, RATE_OF_RETURN, COMPOUND_FREQUENCY, GOAL, DIVIDEND_YIELD, REINVEST_DIVIDENDS)

string_future_value = f"${future_value:,.2f}"
string_total_dividends = f"${total_dividends:,.2f}"
string_total = f"${(future_value + total_dividends):,.2f}"

string_goal = f"${GOAL:,.2f}"
string_estimated_time = "" if estimated_time <= 0 else f"~ {estimated_time} Years"

# Define a width for alignment
width = 35

print(f"\n{'Predicted Outcome:':<{width}}" + string_future_value)
print(f"{'Dividend Payouts:':<{width}}" + string_total_dividends)

# Separator line matching total width
print("-" * (width + len(string_total)))

print(f"{'Total:':<{width}}" + string_total)
print(f"{'Goal:':<{width}}" + string_goal)

# Separator line matching total width
print("-" * (width + len(string_total)))

if estimated_time <= 0:
    print (f"{'Overbalance:':<{width}}" + f"${future_value - GOAL:,.2f}\n")
else:
    print(f"{'Estimated Time:':<{width}}" + string_estimated_time)

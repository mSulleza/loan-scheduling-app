import datetime
import pandas as pd

def generate_loan_schedule(release_date, term, frequency):
    schedule = []
    end_date = release_date + datetime.timedelta(days=term * 30)
    date_diff = end_date - release_date
    
    if frequency == "monthly":
        num_payments = date_diff.days // 30
        interval = datetime.timedelta(days=30)
    elif frequency == "weekly":
        num_payments = date_diff.days // 7
        interval = datetime.timedelta(days=7)
    elif frequency == "bi-weekly":
        num_payments = date_diff.days // 15
        interval = datetime.timedelta(days=15)
    elif frequency == "daily":
        num_payments = date_diff.days
        interval = datetime.timedelta(days=1)
    else:
        raise ValueError("Invalid frequency")

    # Start scheduling from the first payment date
    payment_date = release_date + interval
    for _ in range(num_payments):
        schedule.append(payment_date)
        payment_date += interval  # Increment by the interval each time
    
    return schedule

def generate_amortization_schedule(loan_amount, interest_rate, schedule, term):
    interest_amount = loan_amount * interest_rate * term
    principal_amount = loan_amount / len(schedule)
    amortization_schedule = []

    for payment_date in schedule:
        amortization_schedule.append({
            "payment_date": payment_date,
            "interest_amount": interest_amount / len(schedule),
            "principal_amount": principal_amount,
            "total_payment": principal_amount + interest_amount / len(schedule)
        })
    
    return amortization_schedule

## This is the main function to generate the amortization schedule
def generate_loan_amortization_schedule_df(loan_amount, interest_rate, release_date, term, frequency):
    schedule = generate_loan_schedule(release_date, term, frequency)
    amortization_schedule = generate_amortization_schedule(loan_amount, interest_rate, schedule, term)
    return amortization_schedule

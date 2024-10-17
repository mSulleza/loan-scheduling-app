import datetime

import pandas as pd


def generate_loan_schedule(release_date, term, frequency):
    schedule = []
    end_date = release_date + datetime.timedelta(days=term * 30)
    date_diff = end_date - release_date
    num_payments = 0
    first_payment_date = release_date
    
    if frequency == "monthly":
        num_payments = date_diff.days // 30
        first_payment_date = release_date + datetime.timedelta(days=30)
    elif frequency == "weekly":
        num_payments = date_diff.days // 7
        first_payment_date = release_date + datetime.timedelta(days=7)
    elif frequency == "bi-weekly":
        num_payments = date_diff.days // 15
        first_payment_date = release_date + datetime.timedelta(days=14)
    elif frequency == "daily":
        num_payments = date_diff.days
        first_payment_date = release_date
    else:
        raise ValueError("Invalid frequency")
    
    for i in range(num_payments):
        if frequency == "monthly":
            multiplier = 30
        elif frequency == "weekly":
            multiplier = 7
        elif frequency == "bi-weekly":
            multiplier = 15
        elif frequency == "daily":
            multiplier = 1
        else:
            raise ValueError("Invalid frequency")
        
        payment_date = first_payment_date + (datetime.timedelta(days=i * multiplier))
        schedule.append(payment_date)
        
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

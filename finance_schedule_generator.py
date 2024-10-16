import datetime


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
    interest_amount = 0
    principal_amount = 0
    total_payment = 0
    amortization_schedule = []
    
    return amortization_schedule
        

def main():
    print("Finance Schedule Generator")
    start_date = datetime.datetime(2024, 1, 1)
    frequency = "bi-weekly"
    term = 6
    schedule = generate_loan_schedule(start_date, term, frequency)
    print(len(schedule))
    amortization_schedule = generate_amortization_schedule(100000, 0.035, schedule, term)
    for amortization in amortization_schedule:
        print(amortization)

if __name__ == "__main__":
    main()
import calendar
import datetime
import pandas as pd

from finance_schedule_generator import generate_loan_amortization_schedule_df


def generate_release_strategy(recurring_investment, start_date, month_to_generate, initial_investment_pool):
    # This function generates a release strategy based on the recurring investment
    minimum_release_amount = 100000
    current_investment_pool = initial_investment_pool
    # get the current month and year
    current_month = start_date.month
    current_year = start_date.year
    interest_rate = 0.035
    term = 6
    frequency = "bi-weekly"
    clients = []
    release_strategy = []
    client_index = 1
    total_interest_paid = 0
    # queue of clients that are done paying
    done_clients = []
    
    for i in range(month_to_generate):
        max_loan_amount = 0
        current_investment_pool += recurring_investment
        new_client = []
        paying_clients = []
        if current_investment_pool >= minimum_release_amount:
            # release the loan to a client
            max_loan_amount = int(current_investment_pool // minimum_release_amount)
            for j in range (max_loan_amount):
                if (current_month + 1) % 12 == 0:
                    release_month = 12
                else:
                    release_month = (current_month + 1) % 12
                release_date = datetime.datetime(current_year, release_month, 1)
                loan_schedule = generate_loan_amortization_schedule_df(minimum_release_amount, interest_rate, release_date, term, frequency)
                loan_schedule_df = pd.DataFrame(loan_schedule)
                
                if len(done_clients) > 0:
                    old_client = done_clients.pop()
                    # change the loan schedule of the old client
                    old_client["loan_schedule"] = loan_schedule
                    old_client["release_month"] = current_month
                    old_client["release_year"] = current_year
                    clients.append(old_client)
                else:
                    clients.append({
                        "client": "Client " + str(client_index),
                        "release_month": current_month,
                        "release_year": current_year,
                        "loan_schedule": loan_schedule
                    })
                    new_client.append("Client " + str(client_index))
                    
                total_interest_paid += loan_schedule_df["interest_amount"].sum()
                
                current_investment_pool -= minimum_release_amount
                client_index += 1
            
        recurring_payment = 0
        # check as well if there is already a payment due for this month
        for client in clients:
            is_paying = False
            for payment in client["loan_schedule"]:
                if payment["payment_date"].month == current_month and payment["payment_date"].year == current_year:
                    current_investment_pool += payment["total_payment"]
                    recurring_payment += payment["total_payment"]
                    is_paying = True
            # add client to the list if the loan is paying
            if is_paying:
                paying_clients.append(client["client"])
            # remove client from the list if the loan is paid
            print("Checking client: ", client["client"])
            print("Loan schedule: ", client["loan_schedule"][-1]["payment_date"])
            if client["loan_schedule"][-1]["payment_date"].month == current_month and client["loan_schedule"][-1]["payment_date"].year < current_year:
                print("For renewal of loan: ", client["client"])
                done_clients.append(client)
                clients.remove(client)
        
        release_strategy.append({
                "month": calendar.month_name[current_month],
                "year": current_year,
                "recurring_investment": f"{recurring_investment:.2f}",
                "investment_pool": f"{current_investment_pool:.2f}",
                "number_of_clients": len(paying_clients),
                "new_client": new_client,
                "release_amount": f"{minimum_release_amount * max_loan_amount:.2f}",
                "payments_received": f"{recurring_payment:.2f}",
                "done_clients": len(done_clients),
                # "paying_clients": paying_clients
            })
                    
        # increment the month and year
        current_month += 1
        if current_month > 12:
            current_month = 1
            current_year += 1
    
    print("Total interest earned: ", f"{total_interest_paid:.2f}")
    return release_strategy

def export_to_csv(release_strategy):
    df_clients = pd.DataFrame(release_strategy)
    df_clients.to_csv("release_strategy.csv", index=False)

if __name__ == "__main__":
    clients = generate_release_strategy(10000, datetime.datetime(2025, 1, 1), 24, 70000)
    print(pd.DataFrame(clients))
    export_to_csv(clients)


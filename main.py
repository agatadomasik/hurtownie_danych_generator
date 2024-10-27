from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta

fake = Faker()
passengers = []
check_ins = []
baggages = []
employees = []
boarding_passes = []
security_checks = []

passengers_num = 100000
check_ins_num = 120000
employeesNum = 50
maxBaggage = 5


def weighted_random_baggage(max_baggage):
    weights = [0.5] * 1 + [0.25] * 2 + [0.1] * (max_baggage - 2)
    return random.choices(range(1, max_baggage + 1), weights=weights, k=1)[0]


for i in range(passengers_num):
    passengers.append({
        "PassengerID": i + 1,
        "FirstName": fake.first_name(),
        "LastName": fake.last_name(),
        "DocumentType": random.choice(["ID", "Passport"]),
        "DocumentNumber": fake.bothify(text='??######'),
        "Nationality": fake.country(),
        "FlightNumber": fake.bothify(text='FL####'),
        "Destination": fake.city()
    })

for i in range(check_ins_num):
    check_in_time = fake.date_time_this_month()
    check_ins.append({
        "CheckInID": i + 1,
        "PassengerID": random.randint(1, passengers_num),
        "EmployeeID": random.randint(1, employeesNum),
        "CheckInTime": check_in_time,
        "BoardingPassID": fake.bothify(text='BP######'),
        "CheckInDuration": round(random.uniform(5, 30), 2),
        "ServiceRating": round(random.uniform(1, 5), 2)
    })

baggage_id = 1
for check_in in check_ins:
    baggages_num = weighted_random_baggage(maxBaggage)
    for _ in range(baggages_num):
        baggages.append({
            "BaggageID": baggage_id,
            "CheckInID": check_in["CheckInID"],
            "Weight": round(random.uniform(5, 30), 2)
        })
        baggage_id += 1

for i in range(employeesNum):
    employees.append({
        "EmployeeID": i + 1,
    })

for i in range(check_ins_num):
    boarding_passes.append({
        "BoardingPassID": f"BP{i + 1:06}",
        "CheckInID": i + 1,
        "IssueTime": fake.date_time_this_month(),
        "Gate": f"{random.randint(1, 20)}A",
        "SeatNumber": f"{random.randint(1, 30)}{random.choice(['A', 'B', 'C', 'D'])}"
    })

# for boarding_pass in boarding_passes:
#     print(boarding_pass)


for i in range(check_ins_num):
    security_start = fake.date_time_this_month()
    security_checks.append({
        "SecurityCheckID": i + 1,
        "BoardingPassID": f"BP{i + 1:06}",
        "SecurityStart": security_start,
        "SecurityEnd": security_start + timedelta(minutes=random.randint(1, 10)),
        "ClearanceStatus": random.choices(["approved", "rejected"], weights=[95, 5], k=1)[0],
        "EmployeeID": random.randint(1, employeesNum),
        "ServiceRating": round(random.uniform(1, 5), 2)
    })

# for security_check in security_checks:
#     print(security_check)

df_passengers = pd.DataFrame(passengers)
df_check_ins = pd.DataFrame(check_ins)
df_baggages = pd.DataFrame(baggages)
df_employees = pd.DataFrame(employees)
df_boarding_passes = pd.DataFrame(boarding_passes)
df_security_checks = pd.DataFrame(security_checks)

df_passengers.to_csv("passengers.csv", index=False)
df_check_ins.to_csv("check_ins.csv", index=False)
df_baggages.to_csv("baggages.csv", index=False)
df_employees.to_csv("employees.csv", index=False)
df_boarding_passes.to_csv("boarding_passes.csv", index=False)
df_security_checks.to_csv("security_checks.csv", index=False)

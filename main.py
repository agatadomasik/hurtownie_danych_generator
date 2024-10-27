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
    if max_baggage == 1:
        weights = [1.0]
    elif max_baggage == 2:
        weights = [0.5, 0.5]
    else:
        weights = [0.5] + [0.25] + [0.1] * (max_baggage - 2)
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


# excel

t1_employees_num = 50
t2_incremental_employees = 30
positions = ["Manager", "Accountant", "Engineer", "Analyst", "Developer", "Technician", "Project Manager",
             "HR Specialist", "Sales Representative", "Consultant", "Administrator", "Architect", "Designer",
             "Product Owner", "Marketing Specialist", "Operations Manager"]
departments = ["HR", "Finance", "Engineering", "Sales", "IT", "Operations", "Marketing", "Support", "Logistics", "Legal"]
employment_types = ["pełny etat", "pół etatu", "na godziny", "kontrakt"]
marital_statuses = ["single", "married", "divorced", "widowed"]
currencies = ["PLN", "USD", "EUR", "GBP"]
contract_types = ["Umowa o pracę", "Umowa zlecenie", "Umowa o dzieło", "Umowa B2B"]
salary_range = (3000, 30000)


def generate_employee_data(employee_id):
    """Generates a single row of employee data"""
    gender = random.choice(["Male", "Female"])
    salary = round(random.uniform(*salary_range), 2)
    start_date = fake.date_this_decade(before_today=True, after_today=False)

    # Losujemy, czy pracownik będzie miał zakończenie umowy
    has_termination = random.random() < 0.3  # 30% szansy na zakończenie umowy

    if has_termination:
        # Generujemy EndDate i TerminationReason
        end_date = fake.date_between(start_date=start_date, end_date="today")
        termination_reason = random.choice(["Resignation", "Layoff", "Termination for cause", "Retirement"])
    else:
        end_date = None
        termination_reason = None

    return {
        "EmployeeID": employee_id,
        "FirstName": fake.first_name_male() if gender == "Male" else fake.first_name_female(),
        "LastName": fake.last_name(),
        "Gender": gender,
        "MaritalStatus": random.choice(marital_statuses),
        "BirthDate": fake.date_of_birth(minimum_age=20, maximum_age=65),
        "Position": random.choice(positions),
        "StartDate": start_date.strftime("%Y-%m-%d"),
        "Salary": salary,
        "Currency": random.choice(currencies),
        "Email": fake.email(),
        "PhoneNumber": fake.phone_number(),
        "Department": random.choice(departments),
        "EmploymentType": random.choice(employment_types),
        "EndDate": end_date.strftime("%Y-%m-%d") if end_date else None,
        "TerminationReason": termination_reason,
        "Address": fake.address(),
        "ContractType": random.choice(contract_types)
    }

# Generowanie danych dla T1
employees_T1 = [generate_employee_data(i + 1) for i in range(t1_employees_num)]
df_employees_T1 = pd.DataFrame(employees_T1)
df_employees_T1.to_csv("employees_T1.csv", index=False)

# Generowanie danych dla T2 (z nowymi pracownikami i aktualizacjami)
# Dodajemy nowych pracowników
employees_T2 = employees_T1.copy()
for i in range(t1_employees_num + 1, t1_employees_num + t2_incremental_employees + 1):
    employees_T2.append(generate_employee_data(i))

# Aktualizacja losowych pracowników (np. awans, podwyżka, zakończenie pracy)
for emp in random.sample(employees_T2, k=50):
    emp["Position"] = random.choice(positions)
    emp["Salary"] += round(random.uniform(500, 5000), 2)
    emp["EndDate"] = (datetime.strptime(emp["StartDate"], "%Y-%m-%d") + timedelta(days=random.randint(365, 3650))).strftime("%Y-%m-%d")
    emp["TerminationReason"] = random.choice(["Retirement", "Job change", "Restructuring", "End of contract", "Personal reasons"])

df_employees_T2 = pd.DataFrame(employees_T2)
df_employees_T2.to_csv("employees_T2.csv", index=False)
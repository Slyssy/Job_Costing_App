from faker import Faker
import json

#establish faker
fake = Faker()

# function to create fake project details data
def projects_data(x): 
  
    # dictionary 
    projects_data = {} 
    for i in range(0, x): 
        projects_data[i]={} 
        projects_data[i]['name'] = fake.company() 
        projects_data[i]['street'] = fake.street_address() 
        projects_data[i]['street2'] = fake.secondary_address() 
        projects_data[i]['city'] = fake.city() 
        projects_data[i]['state'] = fake.state_abbr() 
        projects_data[i]['zip'] = fake.zipcode() 
        projects_data[i]['revenue'] = fake.pyfloat(left_digits=5, right_digits=2, positive=True, min_value=15000.00, max_value=50000.00) 
        projects_data[i]['est_labor_expense'] = fake.pyfloat(left_digits=5, right_digits=2, positive=True, min_value=5000.00, max_value=10000.00) 
        projects_data[i]['est_labor_hours'] = fake.pyint(min_value=850, max_value=3000) 
        projects_data[i]['act_start_date'] = fake.date()

    return projects_data
    
projects = projects_data(10)

# print(projects)

# serialize json
json_object = json.dumps(projects, indent = 4)

# writing to file
with open("new_projects.json", "w") as outfile:
    outfile.write(json_object)

# function to create fake users data
def users_data(x): 
  
    # dictionary 
    users_data ={} 
    for i in range(0, x): 
        users_data[i] = {} 
        users_data[i]['job_title'] = fake.job() 
        users_data[i]['pay_rate'] = fake.pyfloat(left_digits=2, right_digits=2, positive=True, min_value=18.00, max_value=35.00) 
        users_data[i]['name'] = fake.name() 
        users_data[i]['email'] = fake.email()
        users_data[i]['phone'] = fake.msisdn()
        users_data[i]['log_in'] = fake.user_name()
        users_data[i]['password'] = fake.password()
    
    return users_data
    
users = users_data(10)

# print(users)

# serialize json
json_object = json.dumps(users, indent = 4)

# writing to file
with open("new_users.json", "w") as outfile:
    outfile.write(json_object)

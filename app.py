# Setup dependencies
from flask import Flask, render_template, request, json
import psycopg2
import datetime
from datetime import date, timedelta
from pprint import pprint

# Import Postgres database details from config file
from postgres_config import pg_ipaddress, pg_port, pg_username, pg_password, pg_dbname

# Setup connection with Postgres
try:
       conn = psycopg2.connect(dbname=pg_dbname, host=pg_ipaddress, user=pg_username, password=pg_password)
       print('------------------------------------')
       print('PostgreSQL database now connected')
       print('------------------------------------')
except (Exception, psycopg2.DatabaseError) as error:
       print('----------------------------------------------------')
       print ("Error while fetching data from PostgreSQL", error)
       print('----------------------------------------------------')

if conn:
    conn.autocommit = True
    cur = conn.cursor()
    cur.close()

# Create Flask app instance
app = Flask(__name__)


# Route for Index page / Dashboard -- fetches data from db and displays on dashboard
@app.route("/", methods=['GET'])
def index():
    if request.method == 'GET':
        cur = conn.cursor()
        # Fetch data from project_details table
        cur.execute('SELECT * FROM project_details');
        project_details_data = cur.fetchall()
        print('------------------------------------------')
        print('Data fetched from Project_Details table')
        print('------------------------------------------')
        print(project_details_data)
        print('------------------------------------------')

        #  Create a list of dictionaries with selected project_details table data, and output as a JSON
        project_list = []
        for db_row in project_details_data:
            project_dict = {}
            project_dict['name'] = db_row[1]
            project_dict['revenue'] = str(db_row[7])
            project_dict['est_labor_hours'] = str(db_row[9])
            project_dict['est_labor_expense'] = str(db_row[10])
            project_dict['act_start_date'] = str(db_row[11])
            project_list.append(project_dict)
        with open('static/result.json', 'w') as fp:
            json.dump(project_list, fp)
        return render_template('index.html', project_list=json.dumps(project_list))
    else:
        print('---------------------------------------')
        db_read_error = 'Oops - could not read from database!'
        print('---------------------------------------')
        return render_template('error.html', error_type=db_read_error)

      
# Route for Enter New Project page -- saves inputs to db, then redirects to Project Details page
@app.route('/new_project', methods=['GET', 'POST'])
def projdata_html_to_db():
    if request.method == 'POST':
        print('*****************')
        print('Posting form...')
        print('*****************')
        full_values_string = ''
        name = request.form['project_name']
        full_values_string += "(" + "'" + name + "'"
        street = request.form['street']
        full_values_string += ',' + "'" + street + "'"
        street2 = request.form['street2']
        full_values_string += ',' + "'" + street2 + "'"
        city = request.form['city']
        full_values_string += ',' + "'" + city + "'"
        state = request.form['state']
        full_values_string += ',' + "'" + state + "'"
        zipcode = request.form['zipcode']  
        full_values_string += ',' + "'" + zipcode + "'"
        revenue = str("{:.2f}".format(float(request.form['revenue'])))
        full_values_string += ',' + revenue
        est_labor_rate = str("{:.2f}".format(float(request.form['est_labor_rate'])))
        full_values_string += ',' + est_labor_rate
        est_labor_hours = request.form['est_labor_hours']
        full_values_string += ',' + est_labor_hours
        est_labor_expense = str("{:.2f}".format(float(est_labor_hours) * float(est_labor_rate)))
        full_values_string += ',' + est_labor_expense
        if 'act_start_date' in request.form and request.form['act_start_date'] != "":
            act_start_date = datetime.datetime.strptime(request.form['act_start_date'], '%m/%d/%Y').date()
        else:
            act_start_date = datetime.datetime.now()           
        full_values_string += ',' + "'" + str(act_start_date) + "'" + ')'
        # Print data list for database entry
        print('-------------------------------------------------------------------')
        print('Data list prepared for entry to Project_Details table in database')
        print('-------------------------------------------------------------------')
        print(full_values_string)
        print('-------------------------------------------------------------------')
        cur = conn.cursor()
        # Adding form input data to PostgreSQL database
        try:
            cur.execute('INSERT INTO project_details (name, street, street2, city, state, zip, revenue, est_labor_rate, est_labor_hours, est_labor_expense, act_start_date) VALUES ' + full_values_string + ';')
            print('-----------------------------------')
            print('Data added to database - woohoo!')
            print('-----------------------------------')
        except:
            print('---------------------------------------')
            db_write_error = 'Oops - could not write to database!'
            print('---------------------------------------')
            return render_template('error.html', error_type=db_write_error)
        return render_template('project_details.html')
    if request.method == 'GET':
        print('*****************')
        print('Getting form...')
        print('*****************')
        return render_template('new_project.html')


# Route for Enter New User page, saves inputs to db, then redirects to Project Details page
@app.route('/new_user', methods=['GET', 'POST'])
def userdata_html_to_db():
    if request.method == 'POST':
        print('*****************')
        print('Posting form...')
        print('*****************')
        full_values_string = ''
        name = request.form['user_name']
        full_values_string += "(" + "'" + name + "'"
        job_title = request.form['job_title']
        full_values_string += ',' + "'" + job_title + "'"
        pay_rate = request.form['pay_rate']
        full_values_string += ',' + "'" + pay_rate + "'"
        email = request.form['email']
        full_values_string += ',' + "'" + email + "'"
        phone = request.form['phone']
        full_values_string += ',' + "'" + phone + "'" + ")"
        # Print data list for database entry
        print('-------------------------------------------------------------------')
        print('Data list prepared for entry to Users table in database')
        print('-------------------------------------------------------------------')
        print(full_values_string)
        print('-------------------------------------------------------------------')
        cur = conn.cursor()
        # Adding form input data to PostgreSQL database
        try:
            cur.execute('INSERT INTO users (name, job_title, pay_rate, email, phone) VALUES ' + full_values_string + ';')
            print('-----------------------------------')
            print('Data added to database - woohoo!')
            print('-----------------------------------')
        except:
            print('---------------------------------------')
            db_write_error = 'Oops - could not write to database!'
            print('---------------------------------------')
            return render_template('error.html', error_type=db_write_error)
        return render_template('project_details.html')
    if request.method == 'GET':
        print('*****************')
        print('Getting form...')
        print('*****************')
        return render_template('new_user.html')


# Route for new Time entry -- saves inputs to Time_Sheets table in db, then redirects to Project Details page
@app.route('/new_time', methods=['GET', 'POST'])
def time_html_to_db():     
    if request.method == 'GET':
        # Fetch all employee names from database for dropdown menu
        cur = conn.cursor()
        cur.execute('SELECT name FROM users')
        employee_names_fetch = cur.fetchall()
        print('------------------------------------------------------------')   
        print('All employee names fetched from database for dropdown list')   
        print('------------------------------------------------------------')   
        print(employee_names_fetch)
        print('------------------------------------------------------------')   
        # Convert employee names to a JSON
        employee_list = []
        for db_row in employee_names_fetch:
            employee_dict = {}
            employee_dict['name'] = db_row[0]
            employee_list.append(employee_dict)
        
        # Fetch all project names from database for dropdown menu
        cur.execute('SELECT name FROM project_details')    
        project_names_fetch = cur.fetchall()
        print('-----------------------------------------------------------')   
        print('All project names fetched from database for dropdown list')   
        print('-----------------------------------------------------------')   
        print(project_names_fetch)
        print('-----------------------------------------------------------') 
        # Convert project names to a list
        project_list = []
        for db_row in project_names_fetch:
            project_dict = {}
            project_dict['name'] = db_row[0]
            project_list.append(project_dict)
        
        # Create a dictionary for employee and project names, and convert to a JSON for the dropdown menus
        dropdown_dict = {}
        dropdown_dict['employee_list'] = employee_list
        dropdown_dict['project_list'] = project_list
        pprint(dropdown_dict)
        return render_template('enterTime.html', dropdown_dict=json.dumps(dropdown_dict))
        
    if request.method == 'POST':
        # Required fields, and missing fields check
        required_fields_list = ['employee_name', 'project_name', 'start_time', 'finish_time']
        missing_fields = []
        for req_field in required_fields_list:
            if req_field not in request.form:
                missing_fields.append(req_field)
        if len(missing_fields):
            missing_fields_error = 'Oops - could not find these fields ' + ' '.join(missing_fields)
            return render_template('error.html', error_type=missing_fields_error)
        
        # Fetching employee and project names from form input    
        employee_name = request.form['employee_name']
        project_name = request.form['project_name']
        # Fetching user_id and project_id from Users and Project Details tables in database  
        cur = conn.cursor() 
        user_id = cur.execute('SELECT user_id FROM users WHERE name=employee_name');
        full_values_string = "(" + "'" + user_id + "'"
        project_id = cur.execute('SELECT project_id FROM project_details WHERE name=project_name');
        full_values_string += "," + "'" + project_id + "'"

        # Fetching time data from form input, and formatting it for database entry
        start_time = request.form['start_time']
        start_time = " ".join(reversed(start_time.split(" ")))
        start_time = datetime.strptime(start_time, "%m/%d/%Y %H:%M").strftime('%Y-%m-%d %H:%M:%S')
        print('Start timestamp = ' + start_time)
        start_time = str(start_time)
        full_values_string = ',' + "'" + start_time + "'"
        finish_time = request.form['finish_time']
        finish_time = " ".join(reversed(finish_time.split(" ")))
        finish_time = datetime.strptime(finish_time, "%m/%d/%Y %H:%M").strftime('%Y-%m-%d %H:%M:%S')
        print('Finish timestamp = ' + finish_time)
        finish_time=str(finish_time)
        full_values_string += ',' + "'" + finish_time + "'" + ")"
        print('------------------------------------------------------')
        print('Data list prepared for Time_Sheets table in database')
        print('------------------------------------------------------')
        print(full_values_string)
        print('------------------------------------------------------')
        
        # Adding data to Timesheet table in database  
        try:
            cur = conn.cursor() 
            cur.execute('INSERT INTO time_sheets (user_id, project_id, start_time, finish_time) VALUES ' + full_values_string + ';')
            print('-----------------------------------')
            print('Data added to database - woohoo!')
            print('-----------------------------------')
        except:
            db_write_error = 'Oops - could not write to database!'
            return render_template('error.html', error_type=db_write_error)
        return render_template('project_details.html')


# Route for Project Details page -- retrieves data from db and/or performs analysis before displaying
def get_timesheet_dict(timesheet, act_labor_hours):
    timesheet_dict = {}
    timesheet_dict['project_id'] = str(timesheet[2])
    user_id = str(timesheet[1])
    timesheet_dict['user_id'] = user_id
    # Fetch user data from Users table
    cur = conn.cursor()
    cur.execute('SELECT user_id, name, pay_rate FROM users WHERE user_id=' + str(user_id));
    user_data = cur.fetchall()
    for user in user_data:
        employee_name = user[1]
        timesheet_dict['employee_name'] = employee_name
        hourly_pay_rate = user[2]
        timesheet_dict['hourly_pay_rate'] = hourly_pay_rate
                
    # Time Calculations
    timesheet_dict['start_time'] = str(timesheet[3])
    timesheet_dict['finish_time'] = str(timesheet[4])
    # Calculate difference of two Datetime objects to find hours worked
    start_time = str(timesheet[3])
    start_time = datetime.strptime(start_time,'%Y-%m-%d %H:%M:%S')
    finish_time = str(timesheet[4])
    finish_time = datetime.strptime(finish_time,'%Y-%m-%d %H:%M:%S')     
    # Outputs a timedelta object   
    time_difference = finish_time - start_time
    # Convert time worked into hours worked
    hours_worked = float("{:.2f}".format(time_difference.total_seconds() / 3600))
    timesheet_dict['hours_worked'] = hours_worked    
    act_labor_hours += float(hours_worked)
    return (timesheet_dict, act_labor_hours)

def get_actual_labor_rate(timesheet_all, project_labor_hours):
    sum_of_hours_t_rate = 0
    for timesheet_dict in timesheet_all:
        sum_of_hours_t_rate += float(timesheet_dict['hours_worked']) * float(timesheet_dict['hourly_pay_rate'])
    return (sum_of_hours_t_rate/float(project_labor_hours))

@app.route('/project_details', methods=['GET', 'POST'])
def proj_time_data():
    if request.method == 'GET':
        cur = conn.cursor()
        # Fetch data from Project_Details table
        cur.execute('SELECT * FROM project_details');
        project_details_data = cur.fetchall()
        # print('------------------------------------------')
        # print('Data fetched from Project_Details table')
        # print('------------------------------------------')
        # Create a list of dictionaries with Project_Details table data
        project_all = {}
        for proj in project_details_data:
            project_dict = {}
            project_id = str(proj[0])
            project_dict['project_name'] = str(proj[1])
            street = str(proj[2])
            street2 = str(proj[3])
            if street2 != "":
                street2 = street2 + ", "
            city = str(proj[4])
            state = str(proj[5])
            zipcode = str(proj[6])
            project_dict['project_address'] = street + ", " + street2 + city + ", " + state + " " + zipcode
            revenue = str(proj[7])
            est_labor_rate = str(proj[8])
            est_labor_hours = str(proj[9])
            est_labor_expense = str(proj[10])
            act_start_date = str(proj[11])
            project_dict['act_start_date'] = act_start_date
            if str(proj[12]) != "":
                project_dict['act_end_date'] = str(proj[12])              
                              
            # Fetch Time_Sheets data for given project_id
            cur = conn.cursor()
            cur.execute('SELECT * FROM time_sheets WHERE project_id=' + str(project_id));
            timesheet_data = cur.fetchall()
            # print('------------------------------------------')
            # print('Data fetched from Time_Sheets table')
            # print('------------------------------------------')
            # Create a list of dictionaries with Time_Sheets table data
            timesheet_all = []
            act_labor_hours = 0
            # Get individual timesheet dict for display
            for timesheet in timesheet_data:
                (timesheet_dict, act_labor_hours) = get_timesheet_dict(timesheet, act_labor_hours)
                timesheet_all.append(timesheet_dict)
            # Now that we know total project labor hours (act_labor_hours), find project labor rate
            act_labor_rate = get_actual_labor_rate(timesheet_all, act_labor_hours)
            project_dict["timesheets"] = timesheet_all
            project_all["project_id: "+ str(project_id)] = project_dict

            # Calculations for Project Financials - Budgeted/Estimated
            fin_est_revenue = revenue
            project_dict['fin_est_revenue '] = str(revenue)
            fin_est_labor_hours = est_labor_hours
            project_dict['fin_est_labor_hours'] = str(fin_est_labor_hours)
            fin_est_labor_rate = est_labor_rate
            project_dict['fin_est_labor_rate'] = str(fin_est_labor_rate)
            fin_est_labor_expense = float(fin_est_labor_hours) * float(fin_est_labor_rate)
            project_dict['fin_est_labor_expense'] = str(fin_est_labor_expense)
            fin_est_gross_profit = float(fin_est_revenue) - fin_est_labor_expense
            project_dict['fin_est_gross_profit'] = str(fin_est_gross_profit)
            fin_est_gross_margin = float(fin_est_gross_profit) / float(fin_est_revenue) * 100
            project_dict['fin_est_gross_margin'] = "{:.2f}".format((fin_est_gross_margin)) + " %"

            # Calculations for Project Financials - Actual
            fin_act_revenue = revenue
            project_dict['fin_act_revenue'] = str(fin_act_revenue)
            fin_act_labor_hours = act_labor_hours
            project_dict['fin_act_labor_hours'] = str(fin_act_labor_hours)
            fin_act_labor_rate = act_labor_rate
            project_dict['fin_act_labor_rate'] = "{:.2f}".format((fin_act_labor_rate))
            fin_act_labor_expense = float(fin_act_labor_hours) * float(fin_act_labor_rate)
            project_dict['fin_act_labor_expense'] = str(fin_act_labor_expense)
            fin_act_gross_profit = float(fin_act_revenue) - float(fin_act_labor_expense)
            project_dict['fin_act_gross_profit'] = str(fin_act_gross_profit)
            fin_act_gross_margin = float(fin_act_gross_profit) / float(fin_act_revenue) * 100
            project_dict['fin_act_gross_margin'] = "{:.2f}".format((fin_act_gross_margin)) + " %"
        # pprint(project_all)
        
        # Create a dictionary of all project and timesheet data, and output as a JSON
        return render_template('project_details.html', project_all=json.dumps(project_all))
    else:
        db_read_error = 'Oops - could not read from database!'
        return render_template('error.html', error_type=db_read_error)   

    if request.method == 'POST':
        act_end_date = request.form['end_date']
        cur = conn.cursor()
        # Adding project end data to Project_Details table in database
        try:
            cur.execute('INSERT INTO project_details (act_comp_date) VALUES (act_end_date);') 
            print('-----------------------------------')
            print('Data added to database - woohoo!')
            print('-----------------------------------')
        except:
            db_write_error = 'Oops - could not write to database!'
            return render_template('error.html', error_type=db_write_error)
        return render_template('project_details.html')

      
# Close database connection
    if(conn):
        cur.close()
        conn.close()
        print('PostgreSQL connection is closed')

if __name__ == "__main__":
    app.run(debug=True)
# Setup dependencies
from flask import Flask, render_template, request, json
import psycopg2
from datetime import datetime, date, time, timedelta
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


# Route for Project Details page -- retrieves data from db and/or performs analysis before displaying.
@app.route('/project_details', methods=['GET', 'POST'])
def proj_time_data():
    if request.method == 'GET':
        cur = conn.cursor()
        # Fetch data from Project_Details table
        cur.execute('SELECT * FROM project_details');
        project_details_data = cur.fetchall()
        print('------------------------------------------')
        print('Data fetched from Project_Details table')
        print('------------------------------------------')
        print(project_details_data)
        print('------------------------------------------')
        #  Create a list of dictionaries with Project_Details table data
        project_all = []
        for db_row in project_details_data:
            project_dict = {}
            project_dict['project_id'] = str(db_row[0])
            project_dict['name'] = str(db_row[1])
            project_dict['street'] = str(db_row[2])
            project_dict['street2'] = str(db_row[3])
            street2 = str(db_row[3]) + ","
            project_dict['city'] = str(db_row[4])
            project_dict['state'] = str(db_row[5])
            project_dict['zip'] = str(db_row[6])
            project_dict['project_address'] = str(db_row[2]) + "," + street2 + str(db_row[4]) + "," + str(db_row[5]) + " " + str(db_row[6])
            project_dict['revenue'] = str(db_row[7])
            project_dict['est_labor_rate'] = str(db_row[8])
            project_dict['act_labor_hours'] = str(db_row[9])
            project_dict['est_labor_expense'] = str(db_row[10])
            project_dict['act_start_date'] = str(db_row[11])
            project_dict['act_comp_date'] = str(db_row[12])
            project_all.append(project_dict)

        # Fetch data from Time_Sheets table
        cur.execute('SELECT * FROM time_sheets');
        timesheet_data = cur.fetchall()
        print('------------------------------------------')
        print('Data fetched from Time_Sheets table')
        print('------------------------------------------')
        print(timesheet_data)
        print('------------------------------------------')
        #  Create a list of dictionaries with Time_Sheets table data
        timesheet_all = []
        for db_row in timesheet_data:
            timesheet_dict = {}
            timesheet_dict['time_sheet_id'] = str(db_row[0])
            timesheet_dict['user_id'] = str(db_row[1])
            timesheet_dict['project_id'] = str(db_row[2])
            timesheet_dict['start_time'] = str(db_row[3])
            timesheet_dict['finish_time'] = str(db_row[4])
            hours_worked =
            timesheet_dict['hours_worked'] = hours_worked   
            timesheet_all.append(timesheet_dict)


        # Create a dictionary of all project and timesheet data, and convert to a JSON
        project_page_dict = {}
        project_page_dict['project_data'] = project_all
        project_page_dict['timesheet_data'] = timesheet_all
        pprint(project_page_dict)
        return render_template('project_details.html', project_page_dict=json.dumps(project_page_dict))
    else:
        print('---------------------------------------')
        db_read_error = 'Oops - could not read from database!'
        print('---------------------------------------')
        return render_template('error.html', error_type=db_read_error)


# Close database connection
    if(conn):
        cur.close()
        conn.close()
        print('PostgreSQL connection is closed')

if __name__ == "__main__":
    app.run(debug=True)